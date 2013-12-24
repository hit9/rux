# coding=utf8

"""
    rux.cli
    ~~~~~~~

    rux's commandline interface.
"""
import datetime
import logging
from os.path import dirname, exists
from subprocess import call
import sys

from . import __version__
from . import src_ext
from .daemon import rux_daemon
from .exceptions import SourceDirectoryNotFound
from .generator import generator
from .pdf import pdf_generator
from .logger import logger
from .models import Post
from .server import server
from .utils import join

from docopt import docopt


usage = """Usage:
  rux [-h|-v]
  rux post
  rux (deploy|build|clean|serve)
  rux (start|stop|status|restart)
  rux pdf

Options:
  -h --help         show help
  -v --version      show version

Commands:
  post              create an empty new post
  deploy            deploy new blog in current directory
  build             build source files to html
  serve             start rux server
  clean             clean built htmls
  start             start builder daemon
  stop              stop builder daemon
  status            report builder daemon status
  restart           restart builder daemon
  pdf               generate pdf from posts"""


def deploy_blog():
    """deploy blog to current directory"""
    logger.info(deploy_blog.__doc__)
    # `rsync -aqu path/to/res/* .`
    call('rsync -aqu ' + join(dirname(__file__), 'res', '*') + ' .', shell=True)
    logger.success('deploy done')
    logger.info('Please edit config.toml to meet your needs')


def new_post():
    """touch an empty new post to src/"""
    logger.info(new_post.__doc__)
    # make the new post's filename
    now = datetime.datetime.now()
    now_s = now.strftime('%Y-%m-%d-%H-%M')
    filepath = join(Post.src_dir, now_s + src_ext)
    # check if `src/` exists
    if not exists(Post.src_dir):
        logger.error(SourceDirectoryNotFound.__doc__)
        sys.exit(SourceDirectoryNotFound.exit_code)
    # write sample content to new post
    content = (
        'Title\n'
        'Title Picture URL\n'
        '---\n'
        'Markdown content ..'
    )
    f = open(filepath, 'w')
    f.write(content)
    f.close()
    logger.success('new post created: %s' % filepath)


def clean():
    """clean: rm -rf post page index.html"""
    logger.info(clean.__doc__)
    paths = ['post', 'page', 'index.html']
    call(['rm', '-rf'] + paths)
    logger.success('clean done')


def main():
    arguments = docopt(usage, version=__version__)
    logger.setLevel(logging.INFO)  # !important

    if arguments['post']:
        new_post()
    elif arguments['deploy']:
        deploy_blog()
    elif arguments['build']:
        generator.generate()
    elif arguments["serve"]:
        server.run()
    elif arguments['clean']:
        clean()
    elif arguments['start']:
        rux_daemon.start()
    elif arguments['stop']:
        rux_daemon.stop()
    elif arguments['status']:
        rux_daemon.status()
    elif arguments['restart']:
        rux_daemon.restart()
    elif arguments['pdf']:
        pdf_generator.generate()
    else:
        exit(usage)


if __name__ == '__main__':
    main()
