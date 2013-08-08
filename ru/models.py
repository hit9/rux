# coding=utf8

"""ru's models"""


class Blog(object):
    """The blog
    attributes
      name          unicode     blog's name
      description   unicode     blog's description
      theme         str         blog's theme"""

    def __init__(self, name=None, description=None, theme=None):
        self.name = name
        self.description = description
        self.theme = theme


blog = Blog()


class Author(object):
    """The blog's owner, only one
    attributes
      name      unicode     author's name
      email     unicode     author's email
      gravatar  str         author's gravatar id
    the gravatar is a property decorated method. gravatar id
    got from email."""

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    @property
    def gravatar(self):
        from hashlib import md5
        return md5(self.email).hexdigest()


author = Author()


class Post(object):
    """The blog's post object.
    attributes
      title     unicode     post's title
      datetime  datetime    post's created time
      markdown  unicode     post's body source, it's in markdown
      html      unicode     post's html, parsed from markdown"""
    pass
