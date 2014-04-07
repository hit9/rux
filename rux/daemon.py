# coding=utf8

"""
    rux.daemon
    ~~~~~~~~~~

    rux's http server and wacher daemon, it runs rux in the background. This
    daemon is modified from <david@boxedice.com>'s generic daemon class.
"""


import atexit
import logging
import os
import signal
import sys
import time

from .logger import logger
from .server import server


class Daemon(object):

    def __init__(self, pidfile, stdin=os.devnull, stdout=os.devnull,
                 stderr=os.devnull, home_dir='.', umask=022):
        self.pidfile = pidfile
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.home_dir = home_dir
        self.umask = umask
        self.daemon_alive = True

    def daemonize(self, server_port):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno,
                                                            e.strerror))
            sys.exit(1)

        os.chdir(self.home_dir)
        os.setsid()
        os.umask(self.umask)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno,
                                                            e.strerror))
            sys.exit(1)

        if sys.platform != 'darwin':
            sys.stdout.flush()
            sys.stderr.flush()
            si = file(self.stdin, 'r')
            so = file(self.stdout, 'a+')
            if self.stderr:
                se = file(self.stderr, 'a+', 0)
            else:
                se = so
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

        def sigtermhandler(signum, frame):
            self.daemon_alive = False
        signal.signal(signal.SIGTERM, sigtermhandler)
        signal.signal(signal.SIGINT, sigtermhandler)

        logger.success('Started')

        # Write pidfile
        atexit.register(self.delpid)  # Make sure pid file is removed if we \
                                      # quit
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s:%s\n" % (pid, server_port))

    def delpid(self):
        os.remove(self.pidfile)

    def start(self, server_port):
        logger.info('Starting http server(0.0.0.0:%d)'
                    ' and source files watcher..' % server_port)

        try:
            pf = file(self.pidfile, 'r')
            pid, port = map(int, pf.read().strip().split(':'))
            pf.close()
        except (IOError, SystemExit) as e:
            pid, port = None, None

        if pid and port:
            message = ('pidfile %s already exists(pid: %d, port: %d). Is it already running?')
            logger.warning(message % (self.pidfile, pid, port))
            sys.exit(1)

        self.daemonize(server_port)
        self.run(server_port)

    def stop(self):
        logger.info('Stopping the daemon..')

        try:
            pf = file(self.pidfile)
            pid, port = map(int, pf.read().strip().split(':'))
            pf.close()
        except (IOError, ValueError) as e:
            pid, port = None, None

        if not (pid and port):
            message = 'pidfile %s does not exist. Not running?'
            logger.warning(message % self.pidfile)

            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)

            return  # Not an error in a restart process

        # Try killing the daemon process
        try:
            i = 0
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
                i = i + 1
                if i % 10 == 0:
                    os.kill(pid, signal.SIGHUP)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                logger.error(str(err))
                sys.exit(1)

        logger.success('Stopped.')

    def status(self):

        try:
            pf = file(self.pidfile)
            pid, port = map(int, pf.read().strip().split(':'))
            pf.close()
        except (IOError, ValueError) as e:
            pid, port = None, None

        if pid and port:
            logger.info('Running: 0.0.0.0:%d, pid: %d.' % (port, pid))
        else:
            logger.info('Stopped.')

    def run(self, port):
        logger.setLevel(logging.ERROR)
        server.run(port)
        logger.setLevel(logging.INFO)


daemon = Daemon("/tmp/rux-daemon.pid", stdout="/dev/stdout")
