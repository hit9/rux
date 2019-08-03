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

Simple static site generator for my blog.

:copyright: (c) 2014-2019 Chao Wang <hit9@icloud.com>
:license: BSD.

"""

from typing import Callable, Any, Dict
import os
import yaml
from enum import Enum
import logging
import datetime
from dataclasses import dataclass
import hashlib

import mistune
import pygments

__version__ = "0.7.0"


###
# Utils
###


class cached_property:
    """cached_property is a decorator to decorate given function ``func`` to be a property
    and cache its result in the memory at the first call.

    Usage::

        >>> class Foo:
            @cached_property
            def attr(self) -> int:
                print("Called!")
                return sum(range(10))
        >>> foo = Foo()
        >>> foo.attr
        Called!
        45
        >>> foo.attr
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


class Color(Enum):
    """Color is an enum collection of console color codes. """

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


def colored_text(text: str, color: Color) -> str:
    """Returns a colored version of given ``text``.
    """
    return "\033[%dm%s\033[0m".format(text, color.value)


###
# Logging
###


class ColoredFormatter(logging.Formatter):
    """ColoredFormatter inherits from :class:`logging.Formatter` and implements a custom
    logging formatter for colored logging.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Overrides upper :meth:`Formatter.format()`."""
        message: str = record.getMessage()
        #: mapping is a map from logging levelname to color enums.
        mapping: Dict[str, Color] = {
            "CRITICAL": Color.BGRED,
            "ERROR": Color.RED,
            "WARNING": Color.YELLOW,
            "INFO": Color.GREEN,
            "DEBUG": Color.BGGREY,
        }
        color: Color = mapping.get(record.levelname, Color.WHITE)
        level_str: str = colored_text("%-8s" % record.levelname, color)
        time_str: str = colored_text(
            datetime.datetime.now().strftime("(%H:%M:%S)"), Color.MAGENTA
        )
        return " ".join([level_str, time_str, message])


#: ``logger`` is the global logger.
logger: logging.Logger = logging.getLogger("rux")
logger_console_handler: logging.Handler = logging.StreamHandler()
logger_console_handler.setLevel(logging.INFO)
logger_console_handler.setFormatter(ColoredFormatter())
logger.addHandler(logger_console_handler)


###
# Configs
###


class Configs:
    """Configs is the abstraction of rux's configuration file ``config.yaml``.
    """

    #: `configs_filename` is the file name of the configuration file.
    configs_filename: str = "config.yaml"
    #: `configs_filepath` is the absolute path of the configuration file.
    configs_filepath: str = os.path.join(os.getcwd(), configs_filename)

    def __init__(self) -> None:
        #: Attribute `configs` holds the original parsed yaml dict from the configuration
        #: file.
        self.configs: Dict[str, Any] = {}

    def load(self) -> None:
        """Load configurations from the file `configs_filepath`.
        Raises :exec:`IOError` or :exec:`yaml.error.YAMLError` any io errors or yaml
        syntax errors occurr.
        """
        try:
            self.configs = yaml.load(open(self.configs_filepath))
        except (IOError, yaml.error.YAMLError) as exc:
            logger.critical("Failed to load {0}".format(self.configs_filepath))
            raise exc

    @cached_property
    def site(self) -> Dict[str, Any]:
        """Returns the configuration section `site`."""
        return self.configs.get("site", {})

    @cached_property
    def site_name(self) -> str:
        """Returns the configured `site.name`."""
        return self.site.get("name", "")

    @cached_property
    def site_description(self) -> str:
        """Returns the configured `site.description`."""
        return self.site.get("description", "")

    @cached_property
    def site_theme(self) -> str:
        """Returns the configured `site.theme`."""
        return self.site.get("theme", "default")

    @cached_property
    def author(self) -> Dict[str, Any]:
        """Returns the configured `author`."""
        return self.configs.get("author", {})

    @cached_property
    def author_name(self) -> str:
        """Returns the configured `author.name`."""
        return self.author.get("name", "")

    @cached_property
    def author_email(self) -> str:
        """Returns the configured `author.email`."""
        return self.author.get("email", "")

    @cached_property
    def author_description(self) -> str:
        """Returns the configured `author.description`."""
        return self.author.get("description", "")

    @cached_property
    def disqus(self) -> str:
        """Returns the configured section `disqus`."""
        return self.configs.get("disqus", {})

    @cached_property
    def disqus_enable(self) -> bool:
        """Returns the configured `disqus.enable`."""
        return self.disqus.get("enable", False)

    @cached_property
    def disqus_shortname(self) -> str:
        """Returns the configured `disqus.shortname`."""
        return self.disqus.get("shortname", "")


###
# Models
###


@dataclass
class Site:
    """Site is an abstraction of model site."""

    #: `name` is the name of this site which is read from configuration.
    name: str
    #: `description` is the description of this site which is read from configuration.
    description: str
    #: `theme` is the theme path  of this site which is read from configuration.
    theme: str = "default"

    @classmethod
    def from_cofnigs(cls, configs: Configs) -> "Site":
        """Constructs a :class:`Site` instance from given `configs`."""
        return cls(
            name=configs.site_name,
            description=configs.site_description,
            theme=configs.site_theme,
        )


@dataclass
class Author:
    """Author is an abstraction of model author."""

    #: `name` is the name of this author which is read from configuration.
    name: str
    #: `email` is the email of this author which is read from configuration.
    email: str

    @classmethod
    def from_cofnigs(cls, configs: Configs) -> "Author":
        """Constructs a :class:`Author` instance from given `configs`."""
        return cls(name=configs.author_name, email=configs.author_email)

    @cached_property
    def gravatar_id(self) -> str:
        """Returns the gravatar id of this author by email."""
        return hashlib.md5(self.email.encode("utf8")).hexdigest()


@dataclass
class Post:
    """Post is an abstraction of model post."""

    name: str
    title: str
    datetime: datetime.datetime
    markdown: str
    html: str
    summary: str
    filepath: str
    title_pic: str


###
# Parser
###


class MarkdownRenderer(mistune.Renderer):
    """MarkdownRenderer inherits the :class:`mistune.Renderer` and implements a custom
    markdown renderer for rux.
    """

    def _code_no_lexer(self, code: str) -> str:
        """Parts of :meth:`block_code()` for the no language condition."""
        return """<div class="highlight"><pre><code>{0}</code></pre></div>""".format(
            mistune.escape(code.strip())
        )

    def block_code(self, code: str, lang: str) -> str:
        """Overrides upper :meth:`mistune.Renderer.block_code()`."""
        if not lang:
            return self._code_no_lexer(code)
        try:
            lexer: pygments.lexer.Lexer = pygments.lexers.get_lexer_by_name(
                lang, stripall=True
            )
        except pygments.util.ClassNotFound:
            logger.warning("pygments lexer not found for {0}, ignored", lang)
            return self._code_no_lexer(code)
        formatter: pygments.formatter.Formatter = pygments.formatters.HtmlFormatter()
        return pygments.highlight(code, lexer, formatter)


class Parser:
    pass
