# coding=utf8

"""
    rux.generator
    ~~~~~~~~~~~~~

    The core builder processor.
"""

from datetime import datetime
import gc
from os import listdir as ls
from os.path import exists
import sys
import time

from . import src_ext
from .config import config
from .exceptions import *
from .logger import logger
from .models import blog, author, Post, Page
from .parser import parser
from .renderer import renderer
from .utils import chunks, update_nested_dict, mkdir_p, join


def render_to(path, template, **data):
    """shortcut to render data with `template` and then write to `path`.
    Just add exception catch to `renderer.render_to`"""
    try:
        renderer.render_to(path, template, **data)
    except JinjaTemplateNotFound as e:
        logger.error(e.__doc__ + ', Template: %r' % template)
        sys.exit(e.exit_code)


class Generator(object):

    POSTS_COUNT_EACH_PAGE = 15

    def __init__(self):
        self.reset()

    def reset(self):
        self.config = config.default
        self.author = author
        self.blog = blog
        self.posts = []
        self.pages = []
        self.root = ''

        gc.collect()

    def initialize(self):
        """Initialize configuration and renderer environment"""

        # read configuration
        try:
            conf = config.parse()
        except ConfigSyntaxError as e:
            logger.error(e.__doc__)
            sys.exit(e.exit_code)

        # update default configuration with user defined
        update_nested_dict(self.config, conf)
        self.blog.__dict__.update(self.config['blog'])
        self.author.__dict__.update(self.config['author'])
        self.root = self.config['root']

        # initialize jinja2
        templates = join(self.blog.theme, 'templates')  # templates directory path
        # set a renderer
        jinja2_global_data = {
            'blog': self.blog,
            'author': self.author,
            'config': self.config,
            'root': self.root
        }
        renderer.initialize(templates, jinja2_global_data)
        logger.success('Initialized')

    def get_posts(self):

        if not exists(Post.src_dir):
            logger.error(SourceDirectoryNotFound.__doc__)
            sys.exit(SourceDirectoryNotFound.exit_code)

        source_files = [join(Post.src_dir, fn)
                        for fn in ls(Post.src_dir) if fn.endswith(src_ext)]

        for filepath in source_files:
            try:
                data = parser.parse_filename(filepath)
            except ParseException as e:  # skip single post parse exception
                logger.warn(e.__doc__ + ', filepath: %r' % filepath)
            else:
                self.posts.append(Post(**data))


        # sort posts by its created time, from new to old
        self.posts.sort(key=lambda post: post.datetime.timetuple(), reverse=True)

        count = len(self.posts)

        for idx, post in enumerate(self.posts):

            if idx == 0:
                _next = None
            else:
                _next = self.posts[idx-1]

            if idx == count - 1:
                _prev = None
            else:
                _prev = self.posts[idx+1]

            setattr(post, 'next', _next)
            setattr(post, 'prev', _prev)

    def parse_posts(self):

        for post in self.posts:

            with open(post.filepath, 'r') as file:
                content = file.read()

            try:
                data = parser.parse(content)
            except ParseException, e:
                logger.warn(e.__doc__ + ', filepath %r' % post.filepath)
                pass
            else:
                post.__dict__.update(data)

    def get_pages(self):

        groups = chunks(self.posts, self.POSTS_COUNT_EACH_PAGE)
        self.pages = [Page(number=idx, posts=list(group))
                      for idx, group in enumerate(groups, 1)]

        if self.pages:
            self.pages[0].first = True
            self.pages[-1].last = True

    def render(self):

        mkdir_p(Post.out_dir)
        mkdir_p(Page.out_dir)

        for page in self.pages:
            for post in page.posts:
                render_to(post.out, Post.template, post=post)
            render_to(page.out, Page.template, page=page)

    def generate(self):
        start_time = time.time()
        self.initialize()
        self.get_posts()
        self.get_pages()
        self.parse_posts()
        self.render()

        logger.success("Build done in %.3f seconds" % (time.time() - start_time))

    def re_generate(self):
        self.reset()
        self.generate()


generator = Generator()
