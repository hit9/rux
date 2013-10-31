# coding=utf8

'''
Setup script for rux with the ugly setuptools.
'''


import os
from setuptools import setup, Extension
from rux import __version__


setup(
    name='rux',
    version=__version__,
    author='hit9',
    author_email='nz2324@126.com',
    description='''Micro and fast static blog generator designed only for writing''',
    license='BSD',
    keywords='static blog generator, markdown, html',
    url='http://github.com/hit9/rux',
    packages=['rux'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'rux=rux.cli:main'
        ]
    },
    install_requires=open("requirements.txt").read().splitlines(),
    dependency_links=[
        # 'https://pypi.python.org/packages/source/b/blinker/blinker-1.2.tar.gz#md5=6b0a876f0778084e97935a951ea96ded',
        'https://github.com/hit9/toml.py/zipball/master#egg=toml.py-0.1.2',
        # 'https://github.com/sramana/pyatom/archive/master.zip#egg=pyatom-1.3',
    ],
    ext_modules=[Extension('ruxlibparser', ['rux/csrc/libparser.c'])],
)
