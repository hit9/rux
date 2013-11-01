# coding=utf8

"""
    rux.libparser
    ~~~~~~~~~~~~~

    Parse post source, return title, title-picture, body(markdown).
"""

import os
from ctypes import *
from distutils.sysconfig import get_python_lib


dll_path = os.path.join(get_python_lib(), 'ruxlibparser.so')

libparser = CDLL(dll_path)


class Post(Structure):
    _fields_ =  (
        ('title', c_void_p),
        ('tpic', c_void_p),
        ('body', c_char_p),
        ('tsz', c_int),
        ('tpsz', c_int)
    )


post = Post()


def parse(src):
    """Note: src should be ascii string"""
    rt = libparser.parse(byref(post), src)
    return (
        rt,
        string_at(post.title, post.tsz),
        string_at(post.tpic, post.tpsz),
        post.body
    )
