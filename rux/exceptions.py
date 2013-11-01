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


# !Fatal

class RuxFatalError(RuxException):
    """There was a fatal error exception that occurred in rux process"""
    exit_code = 1  # must terminate its process with a non-zero exit code
    pass


class SourceDirectoryNotFound(RuxFatalError):
    """Source directory was not found"""

    exit_code = 2
    pass


class ConfigSyntaxError(RuxFatalError):
    """Toml syntax error occurred in config.toml"""
    exit_code = 3
    pass


class JinjaTemplateNotFound(RuxFatalError):
    """Jinja2 template was not found"""
    exit_code = 4
    pass


# Warning

class RuxWarnException(RuxException):  # warning exception
    """There was a warning exception that occurred in rux process"""
    pass


class ParseException(RuxWarnException):
    """There was an exception while parsing the source"""
    pass


class RenderException(RuxWarnException):
    """There was an exception while rendering to html"""
    pass


class PostNameInvalid(ParseException):
    """Invalid post name, should be datetime, like '1992-04-05-10-10'"""
    # 1992-04-05 is my birthday! :)
    pass


class SeparatorNotFound(ParseException):
    """Separator '---' not found in post source"""
    pass


class PostTitleNotFound(ParseException):
    """There was no title found in post's source"""
    pass
