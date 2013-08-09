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
      html      unicode     post's html, parsed from markdown
      summary   unicode     post's summary"""

    def __init__(self, title=None, datetime=None, markdown=None, html=None,
                 summary=None):
        self.title = title
        self.datetime = datetime
        self.markdown = markdown
        self.html = html
        self.summary = summary


class Page(object):
    """The 1st, 2nd, 3rd page..
    attributes
      number    int         the page's order
      posts     list        lists of post objects
      first     bool        is the first page?
      last      bool        is the last page?"""

    def __init__(self, number=1, posts=None, first=False, last=False):
        self.number = number
        self.first = first
        self.last = last

        if posts is None:
            self.posts = []
        else:
            self.posts = posts


class About(object):
    """The blog's about page
    attributes
      markdown  unicode     the about page's source content
      html      unicode     the about page's html"""

    def __init__(self, markdown=None, html=None):
        self.markdown = markdown
        self.html = html
