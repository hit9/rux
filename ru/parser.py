# coding=utf8

"""post parser"""


from . import charset
from .exceptions import *

import houdini
import misaka
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


class ColorRender(HtmlRenderer, SmartyPants):
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

    separator = '---'  # separator between toml header and markdown body

    def __init__(self):
        """Initialize the parser, set markdown render handler as
        an attribute `markdown` of the parser"""
        render = ColorRender()  # initialize the color render
        extensions = (
            misaka.EXT_FENCED_CODE |
            misaka.EXT_NO_INTRA_EMPHASIS |
            misaka.EXT_AUTOLINK
        )

        self.markdown = misaka.Markdown(render, extensions=extensions)

    def parse(self, source):
        """Parse unicode post source, return dict"""
        lines = source.splitlines()
        l = None  # flag: if there is separator

        for line_no, line in enumerate(lines):
            if self.separator in line:
                l = line_no  # got the separator's line number
                break

        if not l:
            raise PostTitleNotFound

        title, body = "\n".join(lines[:l]), "\n".join(lines[l+1:])
        title = title.strip()
        return {'title': title, 'body': body}


parser = Parser()  # build a runtime parser
