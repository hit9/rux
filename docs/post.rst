.. _post:

Post Syntax
===========

.. Contents::

- All posts are in directory ``src/``
  
- Post filename is datetime in formatter ``%Y-%m-%d-%H-%M``, i.e. ``2013-10-06-15-25.md``

- Post's filename extension must be ``.md``

Just run ``rux post`` to touch a new post.

Post Syntax
-----------

Sample post::

    Hello World
    https://dl.dropboxusercontent.com/u/68191343/2013-09-28-21-15_0.jpg
    ---
    
    **Markdown content..**


A post is separated into head and body by ``---``.

Head includes title (required) and title picture (optional), body is in markdown.
