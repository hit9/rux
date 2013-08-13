# coding=utf8

import logging
from subprocess import call

from . import version
from .daemon import ru_daemon
from .logger import logger
from docopt import docopt

"""command line interface"""

usage = """Usage:
  ru [-h|-v]
  ru new (post|blog)
  ru server (start|stop|status)

Options:
  -h --help         show help
  -v --version      show version

Commands:
  new post          new post
  new blog          new blog in this directory
  server start      start builder server
  server stop       stop builder server
  server status     get builder server's status"""


def main():
    arguments = docopt(usage, version=version)

    logger.setLevel(logging.INFO)

    if arguments["new"]:
        if arguments["post"]:
            logger.info("deploy post")
        elif arguments["blog"]:
            logger.info("deploy blog")
    elif arguments["server"]:
        if arguments["start"]:
            ru_daemon.start()
        elif arguments["stop"]:
            ru_daemon.stop()
        elif arguments["status"]:
            ru_daemon.status()
    else:
        exit(usage)


if __name__ == '__main__':
    main()
