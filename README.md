Rux
===

```
     _/_/_/
    _/    _/  _/    _/  _/    _/
   _/_/_/    _/    _/    _/_/
  _/    _/  _/    _/  _/    _/
 _/    _/    _/_/_/  _/    _/
```


A simple, micro and lightweight static site generator, built for mini needs personal blog.

latest version: v0.3.0

Sample site
-----------

- site: [love.hit9.org](http://love.hit9.org)

- files: [github.com/hit9/v.git](https://github.com/hit9/v.git)

Features
--------

- Source in markdown 
- No tags, No categories
- No comment system(disqus, duoshuo..)
- Minimal configuration
- Running in the background as a daemon

`rux` is designed **only for writing**.

Installation
------------

- Install rux using [virtualenv](http://www.virtualenv.org/):

  ```
  mkdir myblog && cd myblog
  virtualenv venv
  . venv/bin/activate
  pip install git+git://github.com/hit9/rux.git
  ```

- System-Wide Installation

  ```
  sudo pip install git+git://github.com/hit9/rux.git
  ```

Quick start
-----------

1. deploy a new blog

  ```
  cd myblog
  rux deploy
  ```

2. edit the configuration, the config file is simple.

  ```
  vim config.toml
  ```

3. start rux's server(include a web server and a file watcher)

  ```
  rux start
  ```

4. new a post

  ```
  rux post
  ```

5. write this post in markdown

  ```
  vim src/post/2013-03-27-10-10.md
  ```

  `rux` will automatically build blog each time you save.

6. stop the server

  ```
  rux stop
  ```

Sample Post
-----------

A post is make up of title and body, split by `===`:

```
Title
=====

Markdown body..
```

Common Issues
--------------

1. Installation troubles on Ubuntu: cann't find Python.h, solution:

  ```
  sudo apt-get install python-dev
  ```

License
-------

BSD
