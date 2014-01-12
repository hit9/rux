.. _theme:

Theme
=====

Rux uses ``Jinja2`` to render templates.

.. Contents::

.. _use_a_theme:

Use A Theme
-----------

To use a theme, clone it down, for example::

    $ cd myblog
    $ git clone git://github.com/hit9/rux-theme-default.git default

and then set ``blog.theme`` to ``"default"`` in ``config.toml``::

    [blog]
    theme = "default"

You really should manage blog's theme in a standalone git repository, and use it
as a submodule of your blog if your blog is under git versioning too.

But it’s 100% ok to use themes not in the submodule way.

To add a theme as a submodule of blog's repo::

    $ git submodule add git://github.com/hit9/rux-theme-default.git default

Available Themes
----------------

- default https://github.com/hit9/rux-theme-default.git
