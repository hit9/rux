# coding=utf8

"""the core builder"""

import sys
from os import listdir as ls
from os.path import exists
from datetime import datetime

from . import src_ext
from .config import config
from .exceptions import *
from .logger import logger
from .models import blog, author, Post, Page, about
from .parser import parser
from .renderer import renderer
import signals
from .utils import chunks, update_nested_dict, mkdir_p, join


class Generator(object):

    def __init__(self):
        self.reset()
        self.register_signals()

    def reset(self):
        self.posts = []
        self.pages = []
        self.about = about
        self.config = config.default
        self.blog = blog
        self.author = author

    def register_signals(self):
        """register all blinker signals"""
        signals.initialized.connect(self.parse_posts)
        # signals.initialized.connect(self.render_about_page)
        # signals.posts_parsed.connect(self.compose_pages)
        # signals.posts_parsed.connect(self.render_posts)
        # signals.page_composed.connect(self.render_pages)

    def step(step_method):
        """decorator to wrap each step method"""
        def wrapper(self, *args, **kwargs):
            logger.info(step_method.__doc__)
            return step_method(self, *args, **kwargs)
        return wrapper

    @step
    def initialize(self):
        """Initialize config, blog, author and jinja2 environment"""

        # read config to update the default
        try:
            conf = config.parse()
        except ConfigSyntaxError as e:
            logger.error(e.__doc__)
            sys.exit(1)

        update_nested_dict(self.config, conf)

        # update blog and author according to configuration
        self.blog.__dict__.update(self.config['blog'])
        self.author.__dict__.update(self.config['author'])

        #
        # -------- initialize jinja2 --
        #

        # get templates directory
        templates = join(self.blog.theme, "templates")
        # set a render
        jinja_global_data = dict(
            blog=self.blog,
            author=self.author,
            config=self.config,
        )
        renderer.initialize(templates, jinja_global_data)
        logger.success("Generator initialized")
        # send signal that generator was already initialized
        signals.initialized.send(self)

    # make alias to initialize
    generate = initialize

    def re_generate(self):
        self.reset()
        self.generate()

    @step
    def parse_posts(self, sender):
        """Parse posts and sort them by create time"""

        if not exists(Post.src_dir):
            logger.error(SourceDirectoryNotFound.__doc__)
            sys.exit(1)

        files = []

        for fn in ls(Post.src_dir):
            if fn.endswith(src_ext):
                files.append(join(Post.src_dir, fn))

        for filepath in files:
            try:
                data = parser.parse_file(filepath)
            except ParseException, e:
                logger.warn(e.__doc__ + ": filepath '%s'" % filepath)
                pass
            else:
                self.posts.append(Post(**data))

        # sort posts by its create time
        self.posts.sort(
            key=lambda post: post.datetime.timetuple(),  # from now to past
            reverse=True
        )
        logger.success("Posts parsed")
        signals.posts_parsed.send(self)


generator = Generator()
