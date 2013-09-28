Rux
===

极简静态博客生成工具

最新版本: v0.3.0

关于
----

`rux`是我另一个项目`lilac`的精简版，只有写文章的功能，没有标签，没有rss等等.. 最初用于写爱情日记设计的，
所以名字起的我女友的名字“铷”。


安装
----

推荐使用virtualenv来安装:

    mkdir myblog
    cd myblog
    virtualenv venv
    . venv/bin/activate
    pip install git+git://github.com/hit9/rux.git


站点示例
--------

url: love.hit9.org

files: github.com/hit9/v.git

快速上手
--------

1. 建立目录, 部署博客

  ```
  cd myblog
  rux deploy
  ```

2. 编辑博客配置, 指明博客名字和介绍

  ```
  vim config.toml
  ```

3. 打开服务, `rux`会自动监视文件改动并编译

  ```
  rux start
  ```

4. 新建一个文章，会返回新建文章的位置

  ```
  rux post
  ```

5. 编写刚刚新建的文章

  ```
  vim src/post/2013-03-27-10-10.md
  ```

  每次保存会自动编译, 到浏览器中`http://localhost:8888`预览博客

6. 关闭服务

  ```
  rux stop
  ```


使用说明
--------

```
Usage:
  rux [-h|-v]
  rux post
  rux (deploy|build|clean|serve)
  rux (start|stop|status)

Options:
  -h --help         show help
  -v --version      show version

Commands:
  post              begin a new post
  deploy            deploy new blog in this directory
  build             build blog
  server            start server listen at 0.0.0.0:8888
  clean             clean built htmls
  start             start builder server
  stop              stop builder server
  status            get builder server's status
```

协议
----

BSD
