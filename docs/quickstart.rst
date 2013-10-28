.. _quickstart:

Quick Start
===========

.. Contents::

Deploy
------

Once you have Rux installed, deploy a new blog::

    $ cd myblog
    $ rux deploy

You can run ``ls`` to see what has happened.


Configure 
---------

Edit the configuration that rux generated::

    $ vim config.toml

Configuration is simple::

    [blog]
    name = "Sunshine Every Day"
    description = "Never give up, my determination is to chase for success"
    theme = "default"
    
    [author]
    name = "Hit9"
    email = "nz2324@126.com"
    description = "I am a happy boy."
    
    [disqus]
    enable = true  # enable comment? true or false
    shortname = "rux"

Start blogging
--------------

First, start Rux's server(include a http server and a files watcher)::

    $ rux start

You can now see your site at ``http://localhost:8888`` in your web browser.

Now new a post::

    $ rux post

Rux will feedback you the filepath of the new post, edit it.

A post is made up of head and body, head include ``title`` and ``title_pic``
(optional), body is in markdown::

    I am the title
    I am the url of title picture 
    ---
    
    Markdown content...

And, Rux will automatically buil blog each time you save.

To stop Rux's server::

    $ rux stop
