Ru
==

Dirty, Dirty, Dirty site generator.

About
------

个人使用的简陋博客生成器, 我用来写日记, 心事的. 项目名字取自我的女朋友.

88.88888888%代码的代码取自[lilac](github.com/hit9/lilac), 不过没有了标签,评论等等.
只剩下简单的写文章功能.

文档暂无, 试用即懂.

Installation
-------------

    pip install git+git://github.com/hit9/ru.git

Usage
-----

1. 建立目录, 部署博客

  ```
  mkdir myblog
  cd myblog
  ru new blog
  ```

2. 配置博客

  ```
  vim config.toml
  ```

3. 打开服务

  ```
  ru server start
  ```

4. 新建文章

  ```
  ru new post
  ```

5. 编写文章

  ```
  vim src/post/2013-03-27-10-10.md
  ```

  每次保存会自动编译, 到浏览器中`http://localhost:8888`预览博客

6. 关闭服务

  ```
  ru server stop
  ```

License
--------

BSD
