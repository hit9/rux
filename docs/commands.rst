.. _commands:

Command Usage
==============

All available commands are here::

    Usage:
      rux [-h|-v]
      rux post
      rux (deploy|build|clean)
      rux (serve|start) [<port>]
      rux (stop|status)
      rux pdf
    
    Options:
      -h --help         show help
      -v --version      show version
    
    Commands:
      post              create a new post
      deploy            create new blog in current directory
      build             build source files to htmls
      serve             start a HTTP server and watch source changes
      clean             remove all htmls rux built
      start             start http server and rebuilder in the background
      stop              stop http server and rebuilder daemon
      status            report the daemon's status
      restart           restart the daemon
      pdf               generate all posts to PDF
