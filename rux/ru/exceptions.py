# coding=utf8

"""
    rux.exceptions
    ~~~~~~~~~~~~~~

    All possible exceptions.
"""


class RuxException(Exception):
    """There was an ambiguous exception that occurred while handling
    rux's process"""
    pass


class SourceDirectoryNotFound(RuxException):
    """Source directory was not found"""
    pass


class ParseException(RuxException):
    """There was an exception while parsing the source"""
    pass


class RenderException(RuxException):
    """There was an exception while rendering to html"""
    pass


class PostTitleNotFound(ParseException):
    """There was no title found in post's source"""
    pass


class PostNameInvalid(ParseException):
    """Invalid post name, should be datetime, like '1992-04-05-10-10'"""
    # 1992-04-05 is my birthday! :)
    pass


class ConfigSyntaxError(RuxException):
    """Toml syntax error occurred in config.toml"""
    pass


class JinjaTemplateNotFound(RuxException):
    """Jinja2 template was not found"""
    pass
