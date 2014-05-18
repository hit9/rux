.. _quickstart:

Quick Start
===========

.. Contents::

This section assumes that you have ``rux`` installed.

New Blog
--------

Create a new directory::

    $ mkdir myblog && cd myblog

If you installed ``rux`` via virtualenv, activate the environment::

    $ . path/to/venv/bin/activate

Run ``rux deploy`` inside the empty directory::

    $ rux deploy


Let's see what was created::

    $ ls
    config.toml default/ src/


- ``config.toml`` - the configuration file

- ``default`` - the built-in theme

-  ``src/`` - the directory of source.

We can now run ``rux serve`` to serve this site up, and preview it at ``http://localhost:8888`` in
web browser.

Configuration
-------------

Configuration in ``config.toml`` is simple and obvious::

    root = ""

    [blog]
    name = "Sunshine Every Day"
    description = "Never give up, my determination is to chase for success"
    theme = "default"  # path to theme
    
    [author]
    name = "Hit9"
    email = "nz2324@126.com"
    description = "I am a happy boy."
    url = "http://hit9.org"  # author's index url
    
    [disqus]
    enable = true  # enable comment? true or false
    shortname = "rux"  # shortname from disqus.com

Build Site
----------

To build site::

    $ rux build

To start server(including a http server and a file monitor)::

    $ rux serve

To serve in the background(no logging output)::

    $ rux start


New Post
--------

To new a post::

    $ rux post

rux will feedback new-created file's path, edit it::

    Title
    Title Picture URL
    ---
    Markdown content ..


The header includes ``title`` and an optional ``title_pic``, the body is in
markdown.

Writing Steps
-------------

Writing with rux is easy::

1. activate the environment if you install rux via virtualenv

2. start rux daemon: ``rux start``

3. create a new post: ``rux post``

4. edit the post and save.

5. preview site in browser.


What's Next
-----------

See also:

- :ref:`post`

- :ref:`use_a_theme`

- :ref:`commands`

- :ref:`pdf`
