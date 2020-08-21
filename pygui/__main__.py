from tkinter import Tk, Frame, Label, Button, Image
from xmlparser import XMLParser
from .exceptions import WindowNotFound, ComponentNotFound
import os

class PyGui:
    def __init__(self):
        self.parser = XMLParser.XMLParser()
        self.vars = {}
        self.vars['variable'] = 'test123'  # DEBUG

    def show(self, window):
        """ Show a specific window """
        try:
            xml_str = open(f'templates/windows/{window}.xml', 'r').read()
        except FileNotFoundError:
            raise WindowNotFound(f"The specified window '{window}' was not found at templates/windows/{window}.xml")

        window_xml = self.set_variables(xml_str)
        print(window_xml)

    def set_variables(self, xml_str, **kwargs):
        """ searches for places with {{ a tag }} like that to replace that with the variable as named inside """

        for var in self.vars:
            findable_ways = [
                "{{" + f" {var} " + "}}",
                "{{" + f"{var}" + "}}",
                "{{" + f"{var} " + "}}",
                "{{" + f" {var}" + "}}"
            ]

            for possible in findable_ways:
                xml_str = xml_str.replace(possible, self.vars[var])

        return xml_str
