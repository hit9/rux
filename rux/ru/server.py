# coding=utf8

"""
    rux.server
    ~~~~~~~~~~

    rux's server, include a web server and a watcher.
"""

import sys
import logging
import socket
from os import listdir as ls
from os import stat
from os.path import exists
from time import sleep
from threading import Thread
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler

from . import src_ext
from .config import config
from .exceptions import SourceDirectoryNotFound
from .generator import generator
from .logger import logger
from .models import Post
from .utils import join


class Handler(SimpleHTTPRequestHandler):
    """Our own http handler"""

    def log_message(self, format, *args):
        logger.info("%s - %s" % (self.address_string(), format % args))


class MultiThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Multiple threaded http server"""
    pass


class Server(object):
    """To build source to html, optional, can watch files for
    changes to auto rebuild , or start a web server here the same time"""

    def __init__(self):
        # filepath to file's updated time dict
        self.files_stat = {}
        # the server instance initialized from MultiThreadedHTTPServer
        self.server = None
        # the thread to watch files for changes
        self.watcher = Thread(target=self.watch_files)
        # this tell thread to terminate when the main process ends
        self.watcher.daemon = True

    def run_server(self, port=8888):
        """run a server binding to port(default 8888)"""

        try:
            self.server = MultiThreadedHTTPServer(('0.0.0.0', port), Handler)
        except socket.error, e:  # failed to bind port
            logger.error(str(e))
            sys.exit(1)

        logger.info("Serve at http://0.0.0.0:%d (ctrl-c to stop) ..." % port)

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("^C received, shutting down server")
            self.shutdown_server()

    def get_files_stat(self):
        """Get current filepath to file updated time dict"""

        if not exists(Post.src_dir):
            logger.error(SourceDirectoryNotFound.__doc__)
            sys.exit(1)

        paths = []

        for fn in ls(Post.src_dir):
            if fn.endswith(src_ext):
                paths.append(join(Post.src_dir, fn))

        # config.toml
        if exists(config.filepath):
            paths.append(config.filepath)

        # files - a <filepath to updated time> dict
        files = dict((p, stat(p).st_mtime) for p in paths)
        return files

    def watch_files(self):
        """watch files for changes, if changed, rebuild blog. this thread
        will quit if the main process ends"""

        try:
            while 1:
                sleep(1.5)  # check every 1.5s

                try:
                    files_stat = self.get_files_stat()
                except SystemExit:
                    logger.error("Error occurred, server shut down")
                    self.shutdown_server()

                if self.files_stat != files_stat:
                    logger.info("Changes detected, start rebuilding..")

                    try:
                        generator.re_generate()
                        logger.success("Rebuild success")
                    except SystemExit:  # catch sys.exit, it means fatal error
                        logger.error("Error occurred, server shut down")
                        self.shutdown_server()

                    self.files_stat = files_stat  # update files' stat
        except KeyboardInterrupt:
            # I dont know why, but this exception won't be catched
            # because absolutly each KeyboardInterrupt is catched by
            # the server thread, which will terminate this thread the same time
            logger.info("^C received, shutting down watcher")
            self.shutdown_watcher()

    def run(self, port=8888):
        self.watcher.start()
        self.run_server(port)

    def shutdown_server(self):
        """shut down the web server"""
        self.server.shutdown()
        self.server.socket.close()

    def shutdown_watcher(self):
        """shut down the watcher thread"""
        self.watcher.join()


server = Server()
