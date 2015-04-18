![Rux](https://raw.githubusercontent.com/hit9/artworks/master/png/Rux.png)
=======================================================================

Micro & Fast static blog generator (markdown => html).

latest version: v0.6.6-Beta

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

Install troubles: https://github.com/hit9/rux#common-issues

Demo
----

- http://hit9.github.io  (https://github.com/hit9/hit9.github.io.git)


QuickStart
-----------

1. Create a new directory and install rux:

   ```bash
   mkdir myblog && cd myblog
   virtualenv venv
   . venv/bin/activate
   pip install rux
   ```

   Deploy blog inside it:

   ```bash
   mkdir blog && cd blog
   rux deploy
   ```

2. Edit generated configuration:

   ```bash
   vi config.toml
   ```

3. Start rux daemon:

   ```bash
   rux start
   ```

4. New a post:

   ```bash
   rux post
   ```

5. Preview site in browser, default url: `0.0.0.0:8888`.

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

To run rux's server and rebuilder in the background(so we can write blog with at most one shell session.):

```bash
rux start
```

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

- default: https://github.com/hit9/rux-theme-default by @hit9

- clr: https://github.com/hit9/rux-theme-clr by @hit9

Common Issues
--------------

1. Installation troubles on Ubuntu: `cann't find Python.h`, solution:

  ```
  sudo apt-get install python-dev
  ```

2. How to generate PDF from my blog? You need to install [wkhtmltopdf](http://wkhtmltopdf.org/downloads.html) first:

License
-------

BSD. `Rux` can be used, modified for any purpose.
