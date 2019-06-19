# coding=utf8
#
#  /(__M__)\
# /, ,   , ,\
# /' ' 'V' ' '\
#    ~ ~ ~
#     rux
#

"""
Rux
~~~

Minimal static blog generator (markdown => html).

## Features

* Not tags, No categories, No feed generation, ...
* Simple configurations.
* Ability to run in the background as a daemon.
* Ability to save posts in PDF for offline reading.
* Ability to build automatically once source updated

## Howtos

1. Creates a blog:

    $ mkdir blog && cd blog
    $ rux init


2. Starts a rux daemon:

    $ rux stop

3. Writes a blog post:

    $ rux post
    $ vim src/...md

4. Preview webpages at https://0.0.0.0:8888
5. Stop the daemon:

    $ rux stop


## Sample Post

Head and body, splits by `---`:

    The title
    An optional banner picture
    ---
    Markdown content..

## Other Commands

1. `rux pdf` generates a pdf of all posts.
2. `rux serve` starts a simple http server (not daemon).
3. `rux clean` removes all generated html files.

## Themes

Uses git submodule to manage themes:

    $ git submodule add git://github.com/hit9/rux-theme-default.git default

Available themes:

    * https://github.com/hit9/rux-theme-default
    * https://github.com/hit9/rux-theme-clr

## Requirements

Python3.4+

## License

BSD, Chao Wang <hit9@icloud.com>

"""

__version__: str = "0.7.0"


from typing import Dict, Any, MutableMapping, Callable
from enum import Enum
import logging
import datetime
import toml


####
# Utils
###


class Color(Enum):
    """Color is an enum collection of colors.
    The value of color enum item is the ansi escape code for the color.
    References: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors.
    """

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    BGRED = 41
    BGGREY = 100


def colored_string(color: Color, text: str) -> str:
    """Returns a colored version of given `text` by given `color`.

        >>> from rux import Color, colored_string
        >>> print(colored_string(Color.RED, "hello world"))

    """
    return "\033[{0}m{1}\033[0m".format(color.value, text)


class cached_property:
    """Decorates the given function ``func`` to cache its result at the first call.

    :param func: The target function to decorate.

    Usage::

        >>> class Foo:
              @cached_property
              def some_attribute(self):
                print("Called!")
                return sum(range(10))
        >>> foo = Foo()
        >>> foo.some_attribute
        Called!
        45
        >>> foo.some_attribute
        45

    """

    def __init__(self, func: Callable) -> None:
        self.func = func
        self.__doc__ = func.__doc__

    def __get__(self, inst: Any, cls: Any) -> Any:
        if inst is None:
            return self
        val = inst.__dict__[self.func.__name__] = self.func(inst)
        return val


###
# Logging
###


class ColoredFormatter(logging.Formatter):
    """ColoredFormatter is an implementation of colored logging formatter."""

    #: color_mappings is the mappings from logging levels to color names.
    COLOR_MAPPINGS: Dict[str, Color] = {
        "CRITICAL": Color.BGRED,
        "ERROR": Color.RED,
        "WARNING": Color.YELLOW,
        "SUCCESS": Color.GREEN,
        "INFO": Color.CYAN,
        "DEBUG": Color.BGGREY,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Overrides `logging.Formatter` to implement a custom colored formatter.
        """
        message: str = record.getMessage()
        # Gets properly color for this record by its level, defaults to `Color.WHITE`.
        color: Color = self.COLOR_MAPPINGS.get(record.levelname, Color.WHITE)
        # Formats level string with paddings.
        level: str = colored_string(color, "%-8s" % record.levelname)
        # Formats time now.
        now: str = colored_string(
            Color.MAGENTA, datetime.datetime.now().strftime("%H:%M:%S")
        )
        # Upper format of logger's name.
        name_upper: str = record.name.upper()
        return " :: ".join([name_upper, level, now, message])


#: `logger` is the global logger.
logger: logging.Logger = logging.getLogger(__name__)
#: `logger_console_handler` is the logging handler that logs to current console.
logger_console_handler: logging.Handler = logging.StreamHandler()
logger_console_handler.setFormatter(ColoredFormatter())
logger.addHandler(logger_console_handler)
# Using level `INFO`.
logger.setLevel(logging.INFO)


###
# Configs
###


class Configs:
    """Configs is the abstraction of rux blog's `config.toml`.
    """

    #: configs_filename is the file's name of target configuration file.
    CONFIGS_FILENAME: str = "config.toml"

    def __init__(self) -> None:
        #: ``configs`` is the internal configuration holder for the data loaded
        #: from configuration file.
        self.configs: MutableMapping[str, Any] = {}

    def load(self) -> None:
        """Loads `config.toml` to this instance.
        Raises `IOError` if any io errors occurr during the load.
        Raises `toml.DecodeError` if target file's syntax is checked invalid by toml.
        """
        try:
            self.configs = toml.load(open(self.CONFIGS_FILENAME))
        except (IOError, toml.TomlDecodeError) as err:
            logger.critical(
                "Failed to loads {0}: {1}".format(self.CONFIGS_FILENAME, err)
            )
            raise err

    @cached_property
    def root(self) -> str:
        """Returns the configured `root` in `config.toml`.
        Which is the root path of this blog.
        """
        return self.configs.get("root", "")

    @cached_property
    def blog(self) -> MutableMapping[str, Any]:
        """Returns the section `[blog]` in `configs.toml`, defaults to `{}`."""
        return self.configs.get("blog", {})

    @cached_property
    def blog_name(self) -> str:
        """Returns the configured `blog.name` in `config.toml`.
        Which is the name of this blog, defaults to `"Untitled"`.
        """
        return self.blog.get("name", "Untitled")

    @cached_property
    def blog_description(self) -> str:
        """Returns the configured `blog.description`, defaults to `""`."""
        return self.blog.get("description", "")

    @cached_property
    def blog_theme(self) -> str:
        """Returns the configured `blog.theme`, defaults to `"default"`.
        Which configures the path of the theme directory relative to the root.'"""
        return self.blog.get("theme", "default")
