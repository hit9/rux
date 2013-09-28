# coding=utf8
"""
    rux.cli
    ~~~~~~~

    rux's commandline interface and simple tasks.
"""

import datetime
import logging
from os.path import dirname, exists
from subprocess import call

from . import __version__
from .daemon import rux_daemon
from .exceptions import SourceDirectoryNotFound
from .generator import generator
from .logger import logger
from .models import Post, src_ext
from .server import server
from .utils import join

from docopt import docopt


usage = """Usage:
  rux [-h|-v]
  rux post
  rux (deploy|build|clean|serve)
  rux (start|stop|status)

Options:
  -h --help         show help
  -v --version      show version

Commands:
  post              create an empty new post
  deploy            deploy new blog in current directory
  build             build source files to html
  server            start http server at 0.0.0.0:8888
  clean             clean built htmls
  start             start builder server
  stop              stop builder server
  status            report builder server's status"""


def deploy_blog():
    """deploy blog to current directory"""
    logger.info(deploy_blog.__doc__)
    # rsync -aqu path/to/res/* .
    call('rsync -aqu ' + join(dirname(__file__), 'res', '*') + ' .', shell=True)
    logger.success('deploy done')
    logger.info('Please edit config.toml to meet your needs')


def new_post():
    """touch an empty new post to src/"""
    logger.info(new_post.__doc__)

    # file is named as formatted time
    now = datetime.datetime.now()
    now_s = now.strftime("%Y-%m-%d-%H-%M")
    filepath = join(Post.src_dir, now_s + src_ext)

    if not exists(Post.src_dir):
        logger.error(SourceDirectoryNotFound.__doc__)
        sys.exit(1)

    # write sample content to new file
    content = """Title\n=====\nMarkdown content..."""
    f = open(filepath, "w")
    f.write(content)
    f.close()

    logger.success("new post created: %s" % filepath)


def clean():
    """clean: rm -rf post page index.html"""
    logger.info(clean.__doc__)

    paths = [
        "post",
        "page",
        "index.html",
    ]

    cmd = ["rm", "-rf"] + paths
    call(cmd)
    logger.success("clean done")


def main():
    arguments = docopt(usage, version=__version__)

    logger.setLevel(logging.INFO)

    if arguments["post"]:
        new_post()
    elif arguments["deploy"]:
        deploy_blog()
    elif arguments["build"]:
        generator.generate()
    elif arguments["serve"]:
        server.run()
    elif arguments["clean"]:
        clean()
    elif arguments["start"]:
        rux_daemon.start()
    elif arguments["stop"]:
        rux_daemon.stop()
    elif arguments["status"]:
        rux_daemon.status()
    else:
        exit(usage)


if __name__ == '__main__':
    main()
