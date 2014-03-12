.. _pdf:

Generate PDF
------------

Rux can generate all posts to a PDF file.

This feature requires ``wkhtmltopdf`` installed, on Ubuntu, we can 
install it via ``apt-get``::

    $ sudo apt-get install wkhtmltopdf

os OSX::

    $ brew tap homebrew/boneyard
    $ brew install wkhtmltopdf

To generate all posts to PDF::

    ~/myblog $ rux pdf
