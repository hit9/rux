from setuptools import setup
from ru import version


setup(
    name='ru',
    version=version,
    author='hit9',
    author_email='nz2324@126.com',
    description='Minimal static blog generator.',
    license='BSD',
    keywords='static blog generator, markdown, toml, posts',
    url='http://github.com/hit9/ru',
    packages=['ru'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ru = ru.cli:main'
        ]
    },
    install_requires=open("requirements.txt").read().splitlines(),
    dependency_links=[
        # 'https://github.com/mitsuhiko/jinja2/zipball/master#egg=jinja2-2.6',
        # 'https://pypi.python.org/packages/source/P/Pygments/Pygments-1.6.tar.gz',
        # 'https://pypi.python.org/packages/source/b/blinker/blinker-1.2.tar.gz',
        # 'https://github.com/docopt/docopt/zipball/master#egg=docopt-0.6.1',
        # 'https://github.com/FSX/houdini.py/zipball/master#egg=houdini.py-0.1.0',
        # 'https://github.com/FSX/misaka/zipball/master#egg=misaka-1.0.2',
        'https://pypi.python.org/packages/source/b/blinker/blinker-1.2.tar.gz#md5=6b0a876f0778084e97935a951ea96ded',
        'https://github.com/hit9/toml.py/zipball/master#egg=toml.py-0.1.2',
        'https://github.com/sramana/pyatom/archive/master.zip#egg=pyatom-1.3',
    ]
)
