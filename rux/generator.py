# coding=utf8

"""
    rux.generator
    ~~~~~~~~~~~~~

    The core builder processor.
"""

from datetime import datetime
import gc
import multiprocessing
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
        logger.error(e.__doc__ + 'Template: %r' % template)
        sys.exit(e.exit_code)


def parse_post(post):
    """woker function for pool. to parse single post"""

    with open(post.filepath, 'r') as f:
        content = f.read()

    try:
        data = parser.parse(content)
    except ParseException, e:
        logger.warn(e.__doc__ + ', filepath %r' % post.filepath)
        pass  # skip
    else:
        post.__dict__.update(data)  # set attributes: html, markdown

    return post


def render_page(page):
    """woker function for pool. to render single page and posts inside it"""

    for post in page.posts:
        render_to(post.out, Post.template, post=post)
    render_to(page.out, Page.template, page=page)


class Generator(object):
    """
    This is the core builder, parse markdown source and render html with
    jinja2 templates.

    We use at most 4(cpu numbers) to build posts

        1. sort source fils by its created time
        2. parse all posts with 4 processes
        3. chunk posts to pages, group all pages into 4 groups
        4. render posts & pages with the same 4 processes
    """

    POSTS_COUNT_EACH_PAGE = 15  # each page has 15 posts at most
    BUILDER_PROCESS_COUNT = multiprocessing.cpu_count()

    def __init__(self):
        self.reset()

    def reset(self):
        self.config = config.default
        self.author = author
        self.blog = blog

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

        # initialize jinja2
        templates = join(self.blog.theme, 'templates')  # templates directory path
        # set a renderer
        jinja2_global_data = {
            'blog': self.blog,
            'author': self.author,
            'config': self.config
        }
        renderer.initialize(templates, jinja2_global_data)
        logger.success('Initialized')

    def get_posts(self):

        if not exists(Post.src_dir):
            logger.error(SourceDirectoryNotFound.__doc__)
            sys.exit(SourceDirectoryNotFound.exit_code)

        source_files = [join(Post.src_dir, fn)
                        for fn in ls(Post.src_dir) if fn.endswith(src_ext)]

        posts = []

        for filepath in source_files:
            try:
                data = parser.parse_filename(filepath)
            except ParseException as e:  # skip single post parse exception
                logger.warn(e.__doc__ + ', filepath: %r' % filepath)
            else:
                posts.append(Post(**data))

        return posts

    def deal_posts(self, posts):

        # sort posts by its created time, from new to old
        posts.sort(key=lambda post: post.datetime.timetuple(), reverse=True)

        # set attributes `next` and `prev` for each post
        length = len(posts)

        for idx, post in enumerate(posts):

            if idx == 0 :
                setattr(post, 'next', None)
            else:
                setattr(post, 'next', posts[idx-1])

            if idx == length - 1:
                setattr(post, 'prev', None)
            else:
                setattr(post, 'prev', posts[idx+1])

        return posts

    def get_pages(self, posts):
        groups = chunks(posts, self.POSTS_COUNT_EACH_PAGE)
        pages = [Page(number=idx, posts=list(group)) for idx, group in enumerate(groups, 1)]

        if pages:
            pages[0].first = True
            pages[-1].last = True

        return pages


    def generate(self):
        start_time = time.time()

        # -----------------  {{initialization
        self.initialize()
        n = self.BUILDER_PROCESS_COUNT
        # ---------------}}

        # -----------------  {{ parsing
        posts = self.get_posts()
        pool = multiprocessing.Pool(n)
        pool.apply(parse_post, args=posts)  # parse posts

        # ----------------------------- }}

        # deal with posts
        self.deal_posts(posts)

        # -----------------  {{ rendering
        pages = self.get_pages(posts)
        # if `post/` or `page/` not exist, mkdir
        mkdir_p(Post.out_dir)
        mkdir_p(Page.out_dir)

        pool.map(render_page, pages)

        # ----------------------------- }}

        pool.close()
        pool.join()

        # cleanup memory
        del posts[:]
        del posts
        del pages[:]
        del pages

        logger.success("Build done with %d process in %.3f seconds" % (
            n, time.time() - start_time))

    def re_generate(self):
        self.reset()
        self.generate()
        # gc
        gc.collect()


generator = Generator()
