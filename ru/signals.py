# coding=utf8

"""All blinker signals in building process, actually this
enable as to make our plugins. And `ru` use it in build-in
building process"""


from blinker import signal

initialized = signal('initialized')
posts_parsed = signal('posts_parsed')
page_composed = signal('page_composed')
