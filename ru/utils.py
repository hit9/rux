# coding=utf8

"""helper functions defined here"""


class Color(object):
    """
    utility to return colored ansi text.
    usage::

        >>> colored("text", "red")
        '\x1b[31mtext\x1b[0m']]'

    """

    colors = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "bgred": 41,
        "bggrey": 100
    }

    prefix = "\033["
    suffix = "\033[0m"

    def colored(self, text, color=None):

        if color not in self.colors:
            color = "while"

        clr = self.colors[color]
        return (self.prefix + "%dm%s" + self.suffix) % (clr, text)


colored = Color().colored
