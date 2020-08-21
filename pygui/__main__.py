from tkinter import Tk, Frame, Label, Button, Image
from xmlparser import XMLParser
from .exceptions import WindowNotFound, ComponentNotFound
import os

class PyGui:
    def __init__(self):
        self.parser = XMLParser.XMLParser()
        self.showing_window_vars = None

    def show(self, _window, **kwargs):
        self.showing_window_vars = kwargs
        """ Show a specific window """
        try:
            xml_str = open(f'templates/windows/{_window}.xml', 'r').read()
        except FileNotFoundError:
            raise WindowNotFound(f"The specified window '{_window}' was not found at templates/windows/{_window}.xml")

        window_xml_str = self.set_variables(xml_str, **kwargs)
        window_xml = self.parser.loads(window_xml_str)
        self.construct(window_xml)

        window_xml.print_out()

    def construct(self, xml_obj):
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
        try:
            xml_str = open(f'templates/components/{tag.name[1:]}.xml').read()
        except FileNotFoundError:
            raise ComponentNotFound(f"No component {tag.name[1:]} found at /templates/components/{tag.name[1:]}.xml")

        attrs = self.showing_window_vars
        for attr in tag.attrs:
            attrs[attr] = tag.attrs[attr]

        xml_str = self.set_variables(xml_str, **attrs)
        new_tag = self.parser.loads(xml_str)
        return new_tag

    def set_variables(self, xml_str, **kwargs):
        """ searches for places with {{ a tag }} like that to replace that with the variable as named inside """

        for var in kwargs:
            findable_ways = [
                "{{" + f" {var} " + "}}",
                "{{" + f"{var}" + "}}",
                "{{" + f"{var} " + "}}",
                "{{" + f" {var}" + "}}"
            ]

            for possible in findable_ways:
                xml_str = xml_str.replace(possible, kwargs[var])

        return xml_str
