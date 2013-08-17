# coding=utf8

import datetime
import logging
from os.path import dirname, exists
from subprocess import call

from . import version
from .daemon import ru_daemon
from .exceptions import SourceDirectoryNotFound
from .generator import generator
from .logger import logger
from models import Post, src_ext
from .server import server
from .utils import join
from docopt import docopt

"""command line interface"""

usage = """Usage:
  ru [-h|-v]
  ru post
  ru (deploy|build|clean|serve)
  ru (start|stop|status)

Options:
  -h --help         show help
  -v --version      show version

Commands:
  post              begin a new post
  deploy            deploy new blog in this directory
  build             build blog
  server            start server listen at 0.0.0.0:8888
  clean             clean built htmls
  start             start builder server
  stop              stop builder server
  status            get builder server's status"""


def deploy_blog():
    """deploy blog to current directory"""
    logger.info(deploy_blog.__doc__)
    lib_dir = dirname(__file__)  # this library's directory
    res = join(lib_dir, "res")
    call("rsync -aqu " + join(res, "*") + " .", shell=True)
    logger.success("deploy done")
    logger.info("Please edit config.toml to meet tour needs")


def new_post():
    """touch new post to src/post"""
    logger.info(deploy_blog.__doc__)
    now = datetime.datetime.now()
    now_s = now.strftime("%Y-%m-%d-%H-%M")
    filepath = join(Post.src_dir, now_s + src_ext)

    if not exists(Post.src_dir):
        logger.error(SourceDirectoryNotFound.__doc__)
        sys.exit(1)

    content = """Title\n=====\nMarkdown content..."""
    f = open(filepath, "w")
    f.write(content)
    f.close()

    logger.success("new post created: %s" % filepath)


def clean():
    """clean: rm post/ page/ about.html index.html"""
    logger.info(clean.__doc__)
    paths = [
        "post",
        "page",
        "about.html",
        "index.html",
    ]

    cmd = ["rm", "-rf"] + paths
    call(cmd)
    logger.success("clean done")

def main():
    arguments = docopt(usage, version=version)

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
        ru_daemon.start()
    elif arguments["stop"]:
        ru_daemon.stop()
    elif arguments["status"]:
        ru_daemon.status()
    else:
        exit(usage)


if __name__ == '__main__':
    main()
