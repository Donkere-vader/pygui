from .window import Window
from XMLParser import XMLParser
from jinja2 import Environment, PackageLoader, select_autoescape
from tkinter import messagebox, filedialog


class PyGui:
    message = messagebox

    def __init__(self, app_name):
        """ Construct the PyGui class """
        self.parser = XMLParser()
        self.showing_window_vars = None

        # Jinja2 enviroment
        self.env = Environment(
            loader=PackageLoader(app_name, "/templates/"),
            autoescape=select_autoescape(['xml'])
        )

    def set_globals(self, **kwargs):
        self.env.globals.update(**kwargs)

    def render_xml(self, xml_file):
        template = self.env.get_template(xml_file)
        xml_str = template.render(self.showing_window_vars)
        return self.parser.loads(xml_str)

    def construct(self, _window, **kwargs):
        """ Show a specific window """
        self.showing_window_vars = kwargs

        window_xml = self.render_xml(f'windows/{_window}.xml')
        self._construct(window_xml)

        window = Window(self, window_xml, self.showing_window_vars)
        window.construct()
        return window

    def _construct(self, xml_obj):
        """ Construct the window """
        self._loop_tag(xml_obj)

    def _loop_tag(self, tag):
        """ Check if there are any components """
        if tag.name.startswith('_'):
            # it is a component
            new_tag = self._construct_component(tag)
            tag.replace(new_tag)

        for child in tag.children:
            self._loop_tag(child)

    def _construct_component(self, tag):
        """ Returns a Tag object resulting from the component """
        attrs = self.showing_window_vars
        for attr in tag.attrs:
            attrs[attr] = tag.attrs[attr]

        template = self.env.get_template(f'components/{tag.name[1:]}.xml')
        xml_str = template.render(**attrs)
        new_tag = self.parser.loads(xml_str)

        for grid_str in ['row', 'column', 'columnspan', 'rowspan']:
            if grid_str in tag.attrs:
                new_tag.attrs[grid_str] = tag.attrs[grid_str]

        return new_tag

    def getfile(self, **kwargs):
        return filedialog.askopenfilename(**kwargs)
