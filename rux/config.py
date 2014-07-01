# coding=utf8

"""
    rux.config
    ~~~~~~~~~~

    Configuration manager, rux's configuration is in toml.
"""

from os.path import exists

from . import charset
from .exceptions import ConfigSyntaxError
from .utils import join

import toml


class Config(object):

    filename = 'config.toml'
    filepath = join('.', filename)

    # default configuration
    default = {
        'root': '',
        'blog': {
            'name': '',
            'description': '',
            'theme': 'clr',
        },
        'author': {
            'name': 'hit9',
            'email': 'nz2324@126.com',
            'description': 'Who are you?'
        },
        'disqus': {
            'enable': True,
            'shortname': 'rux'
        },
    }

    def parse(self):
        """parse config, return a dict"""

        if exists(self.filepath):
            content = open(self.filepath).read().decode(charset)
        else:
            content = ""

        try:
            config = toml.loads(content)
        except toml.TomlSyntaxError:
            raise ConfigSyntaxError

        return config


config = Config()
