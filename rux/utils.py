# coding=utf8

"""
    rux.utils
    ~~~~~~~~~

    All helper functions defined here.
"""

import os
import errno


class Color(object):
    """
    utility to return colored ansi text.
    usage::

        >>> colored("text", "red")
        '\x1b[31mtext\x1b[0m']]'

    """

    colors = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
        'bgred': 41,
        'bggrey': 100
    }

    prefix = '\033['
    suffix = '\033[0m'

    def colored(self, text, color=None):

        if color not in self.colors:
            color = 'white'

        clr = self.colors[color]
        return (self.prefix + '%dm%s' + self.suffix) % (clr, text)


colored = Color().colored


def join(*p):
    """return normpath version of path.join"""
    return os.path.normpath(os.path.join(*p))


def chunks(lst, number):
    """
    A generator, split list `lst` into `number` equal size parts.
    usage::

        >>> parts = chunks(range(8),3)
        >>> parts
        <generator object chunks at 0xb73bd964>
        >>> list(parts)
        [[0, 1, 2], [3, 4, 5], [6, 7]]

    """
    lst_len = len(lst)

    for i in xrange(0, lst_len, number):
        yield lst[i: i+number]


def update_nested_dict(a, b):
    """
    update nested dict `a` with another dict b.
    usage::

        >>> a = {'x' : { 'y': 1}}
        >>> b = {'x' : {'z':2, 'y':3}, 'w': 4}
        >>> update_nested_dict(a,b)
        {'x': {'y': 3, 'z': 2}, 'w': 4}

    """
    for k, v in b.iteritems():
        if isinstance(v, dict):
            d = a.setdefault(k, {})
            update_nested_dict(d, v)
        else:
            a[k] = v
    return a


def mkdir_p(path):
    """mkdir -p
    Note: comes from stackoverflow"""
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
