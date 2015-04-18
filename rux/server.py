# coding=utf8

"""
    rux.server
    ~~~~~~~~~~

    rux's server, include a web server and a watcher, running in two threads,
    the file watcher will watch source files updates and start building process
    automatically, the http server host the static site at 0.0.0.0:port
"""

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import logging
from os import listdir as ls
from os import stat, getcwd
from os.path import exists, relpath
import posixpath
from SimpleHTTPServer import SimpleHTTPRequestHandler
import socket
from SocketServer import ThreadingMixIn
import sys
from threading import Thread
from time import sleep

from . import src_ext
from .config import config
from .exceptions import SourceDirectoryNotFound
from .generator import generator
from .logger import logger
from .models import Post
from .utils import join

_root = ''

class Handler(SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        # http server's output message formatter
        logger.info("%s - %s" % (self.address_string(), format % args))

    def translate_path(self, path):
        if not path.startswith(_root):
            path = _root
        path_ = join(getcwd(), relpath(path, _root or '/'))
        path_ = path_.split('?')[0]
        path_ = path_.split('#')[0]
        return posixpath.normpath(path_)


class MultiThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Multiple threaded http server"""
    pass


class Server(object):
    """rux's server, include a web server to host this static blog at localhost
    , and a files watcher to automatically once source files updated"""

    def __init__(self):
        self.files_stat = {}  # dict, {filepath: file updated time}
        self.server = None  # instance of `MultiThreadedHTTPServer`
        self.watcher = Thread(target=self.watch_files)  # the thread of watcher
        self.watcher.daemon = True  # terminate watcher once main process ends

    def run_server(self, port):
        """run a server binding to port"""

        try:
            self.server = MultiThreadedHTTPServer(('0.0.0.0', port), Handler)
        except socket.error, e:  # failed to bind port
            logger.error(str(e))
            sys.exit(1)

        logger.info("HTTP serve at http://0.0.0.0:%d (ctrl-c to stop) ..."
                    % port)

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("^C received, shutting down server")
            self.shutdown_server()

    def get_files_stat(self):
        """get source files' update time"""

        if not exists(Post.src_dir):
            logger.error(SourceDirectoryNotFound.__doc__)
            sys.exit(SourceDirectoryNotFound.exit_code)

        paths = []

        for fn in ls(Post.src_dir):
            if fn.endswith(src_ext):
                paths.append(join(Post.src_dir, fn))

        # config.toml
        if exists(config.filepath):
            paths.append(config.filepath)

        # files: a <filepath to updated time> dict
        files = dict((p, stat(p).st_mtime) for p in paths)
        return files

    def watch_files(self):
        """watch files for changes, if changed, rebuild blog. this thread
        will quit if the main process ends"""

        try:
            while 1:
                sleep(1)  # check every 1s

                try:
                    files_stat = self.get_files_stat()
                except SystemExit:
                    logger.error("Error occurred, server shut down")
                    self.shutdown_server()

                if self.files_stat != files_stat:
                    logger.info("Changes detected, start rebuilding..")

                    try:
                        generator.re_generate()
                        global _root
                        _root = generator.root
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

    def run(self, port):
        """start web server and watcher"""
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
