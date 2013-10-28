# coding=utf8

"""
    rux.generator
    ~~~~~~~~~~~~~

    The core builder processor.
"""

from datetime import datetime
import gc
from itertools import groupby
import multiprocessing
from os import listdir as ls
from os.path import exists
import sys
import time

from . import src_ext, charset
from .config import config
from .exceptions import *
from .logger import logger
from .models import blog, author, Post, Page
from .parser import parser
from .renderer import renderer
from .utils import chunks, update_nested_dict, mkdir_p, join


def render_to(path, template, **data):
    """shortcut to render data with template and then write to path.
    Just add exception catch to renderer.render_to"""
    try:
        renderer.render_to(path, template, **data)
    except JinjaTemplateNotFound as e:
        logger.error(e.__doc__ + ": Template: '%s'" % template)
        sys.exit(e.exit_code)


class Generator(object):
    """
    This is the core builder, parse markdown source and render html
    with jinja2 templates.

    We use at most 4 processes to build posts.

        1. sort source files by its created time
        2. chunk posts to pages
        3. group all pages into 4 processes
        4. lunch each process to build
        5. each process will build one page by one page(to save memory usage)

    Build objects at first, and fill in them with data(file contents) one
    by one.
    """
    POSTS_COUNT_EACH_PAGE = 9  # each page has 9 posts at most
    BUILDER_PROCESS_COUNT = 4  # at most 4 processes to build posts

    def __init__(self):
        self.reset()

    def reset(self):
        self.config = config.default
        self.author = author
        self.blog = blog

    def initialize(self):
        """Initialize configuration and renderer environment"""

        # read config
        try:
            conf = config.parse()
        except ConfigSyntaxError as e:
            logger.error(e.__doc__)
            sys.exit(e.exit_code)

        # update default configuration with use defined
        update_nested_dict(self.config, conf)
        self.blog.__dict__.update(self.config['blog'])
        self.author.__dict__.update(self.config['author'])

        # initialize jinja2
        templates = join(self.blog.theme, 'templates')  # templates directory
        # set a renderer
        jinja2_global_data = {
            'blog': self.blog, 'author': self.author, 'config': self.config
        }
        renderer.initialize(templates, jinja2_global_data)
        logger.success('Initialized')

    def get_pages(self):
        """Sort source files by its created time, and then chunk all posts into
        9 pages"""

        if not exists(Post.src_dir):
            logger.error(SourceDirectoryNotFound.__doc__)
            sys.exit(SourceDirectoryNotFound.exit_code)

        source_files = [join(Post.src_dir, fn)
                        for fn in ls(Post.src_dir) if fn.endswith(src_ext)]

        posts = []  # all posts objects

        for filepath in source_files:
            try:
                data = parser.parse_filename(filepath)
            except ParseException as e:  # skip single post parse exceptions
                logger.warn(e.__doc__ + ", filepath '%s'" % filepath)
            else:
                posts.append(Post(**data))

        # sort posts by its created time, from new to old
        posts.sort(key=lambda post: post.datetime.timetuple(),
                        reverse=True)

        # each page has 9 posts
        groups = chunks(posts, self.POSTS_COUNT_EACH_PAGE)
        pages = [Page(number=idx, posts=list(group))
                 for idx, group in enumerate(groups, 1)]
        # mark the first page and the last page
        if pages:  # !important: Not empty list
            pages[0].first = True
            pages[-1].last = True

        return pages

    def build_pages(self, pages):
        """Build pages, and its posts the same time"""
        # check output directory
        mkdir_p(Post.out_dir)
        mkdir_p(Page.out_dir)

        for page in pages:
            for post in page.posts:
                # read and parse file content
                with open(post.filepath) as f:
                    content = f.read().decode(charset)
                try:
                    data = parser.parse(content)
                except ParseException, e:
                    logger.warn(e.__doc__+", filepath '%s'" % post.filepath)
                    pass  # skip the trouble posts
                else:
                    post.__dict__.update(data)  # set attributes: html, markdown..
                    # render to html
                    render_to(post.out, Post.template, post=post)
            # render pages to html
            render_to(page.out, Page.template, page=page)
            # now this page is over, free its posts
            del page.posts[:]
            del page.posts

        # free all pages
        del pages[:]
        del pages

    def generate(self):
        start_time = time.time()
        self.initialize()
        pages = self.get_pages()

        # group all pages into 4 processes
        processes = []
        n = self.BUILDER_PROCESS_COUNT
        # group pages into 4 parts, thanks to itertools
        # I have to sort this list before I groupby it

        groups = []

        for k, g in groupby(sorted(pages, key=lambda x: x.number % n),
                            lambda x: x.number % n):
            groups.append(list(g))

        for group in groups:
            process = multiprocessing.Process(target=self.build_pages,
                                        args=(group,))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        logger.success("Build done with %d process in %.3f seconds" % (
            len(processes), time.time() - start_time))

    def re_generate(self):
        self.reset()
        self.generate()
        gc.collect()  # gc each time rebuild done

generator = Generator()
