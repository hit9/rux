from setuptools import setup
from ru import __version__


setup(
    name='ru',
    version=__version__,
    author='hit9',
    author_email='nz2324@126.com',
    description='''A simple, micro and lightweight static site generator,
    built for mini needs personal blog.''',
    license='BSD',
    keywords='static blog generator, markdown, html',
    url='http://github.com/hit9/ru',
    packages=['ru'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ru=ru.cli:main'
        ]
    },
    install_requires=open("requirements.txt").read().splitlines(),
    dependency_links=[
        'https://pypi.python.org/packages/source/b/blinker/blinker-1.2.tar.gz#md5=6b0a876f0778084e97935a951ea96ded',
        'https://github.com/hit9/toml.py/zipball/master#egg=toml.py-0.1.2',
        'https://github.com/sramana/pyatom/archive/master.zip#egg=pyatom-1.3',
    ]
)
