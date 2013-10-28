.. _theme:

Theme
=====

.. Contents::

Use Theme
---------

Set this item in `config.toml`::

    [blog]
    theme = "the-theme-path"

As an example, to install a theme::

    $ git submodule add git://github.com/hit9/rux-theme-default.git  default
    $ vim config.toml
    $ rux build



You really should manage your theme in a standalone git repository, and use it
as a submodule of your blog if your blog is under git versioning too.
But it’s 100% ok to use themes not in the submodule way.

Available Themes
----------------

- default https://github.com/hit9/rux-theme-default.git


Theme Development
-----------------

I have no time introducing this part.

Checking out theme ``default`` may be helpful: https://github.com/hit9/rux-theme-default

PS: Rux uses Jinja2 to render templates.
