# coding=utf8

"""
    rux.renderer
    ~~~~~~~~~~~~

    Render data to html with jinja2 templates.
"""

from . import charset
from .exceptions import JinjaTemplateNotFound

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound


class Renderer(object):

    def initialize(self, templates_path, global_data):
        """initialize with templates' path
        parameters
          templates_path    str    the position of templates directory
          global_data       dict   globa data can be got in any templates"""
        self.env = Environment(loader=FileSystemLoader(templates_path))
        self.env.trim_blocks = True
        self.global_data = global_data

    def render(self, template, **data):
        """Render data with template, return html unicodes.
        parameters
          template   str  the template's filename
          data       dict the data to render
        """
        # make a copy and update the copy
        dct = self.global_data.copy()
        dct.update(data)

        try:
            html = self.env.get_template(template).render(**dct)
        except TemplateNotFound:
            raise JinjaTemplateNotFound
        return html

    def render_to(self, path, template, **data):
        """Render data with template and then write to path"""
        html = self.render(template, **data)
        with open(path, 'w') as f:
            f.write(html.encode(charset))


renderer = Renderer()  # initialized a renderer, and use it each time
