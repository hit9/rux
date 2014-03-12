Rux
===

Micro & Fast static blog generator (markdown => html).

latest version: v0.5.8

**Note**: rux may not be stable before v1.0 release.

![](docs/screen-shots/rux-in-shell.png)


Features
--------

- Static: Markdown => HTML

- Not tags, No categories, No feed generation, No ...

- Minimal & Simple configuration

- Ability to run in the background as a daemon

- Ability to save posts in PDF for offline reading

- Ability to build automatically once source updated

Installation
------------

```bash
$ mkdir MyBlog
$ cd MyBlog
$ virtualenv venv
New python executable in venv/bin/python
Installing setuptools............done.
Installing pip...............done.
$ . venv/bin/activate
$ pip install rux
```

Demo
----

- Site: http://love.hit9.org
- Code: https://github.com/hit9/v.git

Sample Post
------------

Sample post:

```markdown
Hello World
http://titlepic.jpg
---
**Hello World**
```

A post is separated into head and body by ``---``.

Head includes title (required) and title picture (optional), body is in markdown.


Commands
--------

To deploy a new blog in new-created directory:

```bash
rux deploy
```

To build site from source to htmls:

```bash
rux build
```

To create a new post:

```bash
rux post
```

To remove all htmls rux built:

```bash
rux clean
```

To start a HTTP server and watch source changes:

```bash
rux serve
```

When you save your writings, rux can detect the changes and start rebuilding.

To run rux's server and rebuilder in the background:

```bash
rux start
```

We can write blog with at most one shell session.

To generate all posts to pdf:

```bash
rux pdf
```


Themes
------

You really should manage your theme in a standalone git repository, and use it as a submodule of your blog's submodule if your blog is under git versioning too.

For instance, add theme `default` a submodule of your blog's repo:

```
$ git submodule add git://github.com/hit9/rux-theme-default.git default
```
If you want to modify a theme created by someone else, just fork his(or her) repo, and then modify it.

But it's 100% ok to use themes not in the submodule way.

Theme list:

- default: https://github.com/hit9/rux-theme-default.git by @hit9

Documentation
-------------

http://rux.readthedocs.org/


Common Issues
--------------

1. Installation troubles on Ubuntu: `cann't find Python.h`, solution:

  ```
  sudo apt-get install python-dev
  ```

2. How to generate PDF from my blog? You need to install `wkhtmltopdf` first:

  ```
  # Ubuntu
  sudo apt-get install wkhtmltopdf

  # on OSX
  brew tap homebrew/boneyard
  brew install wkhtmltopdf
  ```

License
-------

BSD. `Rux` can be used, modified for any purpose.
