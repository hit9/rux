# coding=utf8

"""all possible exceptions"""


class RuException(Exception):
    """There was an ambiguous exception that occurred while handling
    ru's process"""
    pass


class SourceDirectoryNotFound(RuException):
    """Source directory was not found"""
    pass


class ParseException(RuException):
    """There was an exception while parsing the source"""
    pass


class RenderException(RuException):
    """There was an exception while rendering to html"""
    pass


class PostTitleNotFound(ParseException):
    """There was no title found in post's source"""
    pass


class PostTitleEmpty(ParseException):
    """The post's title was found empty"""
    pass


class PostNameInvalid(ParseException):
    """Invalid post name, should be datetime, like '1992-04-05-10-10'"""  # my birth
    pass


class ConfigSyntaxError(RuException):
    """Toml syntax error occurred in config.toml"""
    pass


class JinjaTemplateNotFound(RuException):
    """Jinja2 template was not found"""
    pass
