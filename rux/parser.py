# coding=utf8

"""
    rux.parser
    ~~~~~~~~~~

    Parser from post source to html.
"""

from datetime import datetime
import os

from . import charset, src_ext
from .exceptions import *
import libparser

import houdini
import misaka
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

src_ext_len = len(src_ext)  # cache this, call only once

to_unicode = lambda string: string.decode(charset)


class RuxHtmlRenderer(HtmlRenderer, SmartyPants):
    """misaka render with color codes feature"""

    def _code_no_lexer(self, text):
        # encode to utf8 string
        text = text.encode(charset).strip()
        return(
            """
            <div class="highlight">
              <pre><code>%s</code></pre>
            </div>
            """ % houdini.escape_html(text)
        )

    def block_code(self, text, lang):
        """text: unicode text to render"""

        if not lang:
            return self._code_no_lexer(text)

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:  # lexer not found, use plain text
            return self._code_no_lexer(text)

        formatter = HtmlFormatter()

        return highlight(text, lexer, formatter)


class Parser(object):
    """Usage::

        parser = Parser()
        parser.parse(str)   # return dict
        parser.markdown.render(markdown_str)  # render markdown to html

    """

    def __init__(self):
        """Initialize the parser, set markdown render handler as
        an attribute `markdown` of the parser"""
        render = RuxHtmlRenderer()  # initialize the color render
        extensions = (
            misaka.EXT_FENCED_CODE |
            misaka.EXT_NO_INTRA_EMPHASIS |
            misaka.EXT_AUTOLINK
        )

        self.markdown = misaka.Markdown(render, extensions=extensions)

    def parse_markdown(self, markdown):
        return self.markdown.render(markdown)

    def parse(self, source):
        """Parse ascii post source, return dict"""

        rt, title, title_pic, markdown = libparser.parse(source)

        if rt == -1:
            raise SeparatorNotFound
        elif rt == -2:
            raise PostTitleNotFound

        # change to unicode
        title, title_pic, markdown = map(to_unicode, (title, title_pic,
                                                      markdown))

        # render to html
        html = self.markdown.render(markdown)
        summary = self.markdown.render(markdown[:200])

        return {
            'title': title,
            'markdown': markdown,
            'html': html,
            'summary': summary,
            'title_pic': title_pic
        }

    def parse_filename(self, filepath):
        """parse post source files name to datetime object"""
        name = os.path.basename(filepath)[:-src_ext_len]
        try:
            dt = datetime.strptime(name, "%Y-%m-%d-%H-%M")
        except ValueError:
            raise PostNameInvalid
        return {'name': name, 'datetime': dt, 'filepath': filepath}


parser = Parser()  # build a runtime parser
