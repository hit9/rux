.. _commands:

Command Usage
==============

All available commands are here::

    Usage:
      rux [-h|-v]
      rux post
      rux (deploy|build|clean|serve)
      rux (start|stop|status|restart)
    
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
      pdf               generate pdf from posts
