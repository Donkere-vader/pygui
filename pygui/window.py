from tkinter import Tk, Frame, Label, Button, Menu
from PIL import Image, ImageTk
from .custom_tk import Entry, Text, Checkbutton, Listbox, Spinbox
import json


class Window(Tk):
    def __init__(self, parent, xml, showing_window_vars):
        """ Initialize the window """
        super().__init__()
        self.parent = parent
        self.xml = xml
        self.working_masters = []
        self.showing_window_vars = showing_window_vars
        self.items = {}

        self.style_sheet = self.get_style_sheet()

    def get_item(self, id):
        """ Get the TK widget if it has the id="" attribute in the XML """
        if id in self.items:
            return self.items[id]
        return None

    def show(self):
        """ Show the current window """
        self.mainloop()

    def replace(self, new_window):
        new_window.geometry(f"+{self.winfo_x()}+{self.winfo_y()}")
        self.destroy()
        new_window.show()

    def get_style_sheet(self):
        if 'style' in self.xml.attrs:
            file_name = self.xml.attrs["style"]
            del self.xml.attrs['style']
            return json.load(open(f'static/{file_name}.json'))

    def construct(self, tag=None, master=None):
        """ Construct the current window """
        if master is not None:
            self.working_masters = [master]

        self._loop_tag(self.xml if tag is None else tag)

    def _loop_tag(self, tag):
        """ Loop over the XML tags and let the tags be generated and place
        them on their masters grid """
        # set style sheet attrs
        if 'class' in tag.attrs and self.style_sheet is not None:
            class_name = tag.attrs['class']
            del tag.attrs['class']
            tag.attrs = {**tag.attrs, **self.style_sheet[f".{class_name}"]}

        if 'id' in tag.attrs and self.style_sheet is not None:
            if f"#{tag.attrs['id']}" in self.style_sheet:
                tag.attrs = {
                    **tag.attrs,
                    **self.style_sheet[f"#{tag.attrs['id']}"]
                }

        # get grid attrs
        grid = {
            "row": 0,
            "column": 0,
            "columnspan": 1,
            "rowspan": 1
        }

        to_remove = []
        for item in tag.attrs:
            if item in grid:
                grid[item] = tag.attrs[item]
                to_remove.append(item)

        for item in to_remove:
            del tag.attrs[item]

        item_id = None
        if 'id' in tag.attrs:
            item_id = tag.attrs['id']
            del tag.attrs['id']

        new_obj, loop_children = self.construct_tag(
            tag,
            self.working_masters[-1] if len(self.working_masters) > 0 else None
        )

        if new_obj is not None and tag.name != 'root':
            new_obj.grid(**grid)

        if item_id is not None:
            self.items[item_id] = new_obj

        if not tag.self_closing:
            self.working_masters.append(new_obj)

            if loop_children:
                for child in tag.children:
                    self._loop_tag(child)

            self.working_masters.remove(new_obj)

    def construct_command(self, command_text):
        return lambda cmd=command_text: exec(
            cmd,
            {
                **self.showing_window_vars,
                **self.parent.env.globals
            }
        )

    def construct_tag(self, tag, master):
        """ Construct a tag into a tkinter object """
        new_obj = None
        loop_children = True

        if 'command' in tag.attrs:
            tag.attrs['command'] = self.construct_command(tag.attrs['command'])
        if 'image' in tag.attrs:
            tag.attrs['image'] = ImageTk.PhotoImage(
                Image.open(tag.attrs['image'])
            )

        if tag.name == 'root':
            if 'title' in tag.attrs:
                self.title(tag.attrs['title'])
                del tag.attrs['title']
            if 'geometry' in tag.attrs:
                self.geometry(tag.attrs['geometry'])
                del tag.attrs['geometry']
            new_obj = self
            self.configure(**tag.attrs)

        elif tag.name == 'frame':
            new_obj = Frame(master=master, **tag.attrs)

        elif tag.name == 'label':
            new_obj = Label(master=master, text=tag.content, **tag.attrs)

        elif tag.name == 'button':
            new_obj = Button(master=master, text=tag.content, **tag.attrs)

        elif tag.name in ['entry', 'text']:
            if tag.name == 'entry':
                new_obj = Entry(master=master, **tag.attrs)
            else:
                new_obj = Text(master=master, **tag.attrs)
            if tag.content is not None:
                new_obj.val(tag.content)

        elif tag.name in ['image', 'img']:
            src = None
            for possible_attr in ['image', 'img', 'src']:
                if possible_attr in tag.attrs:
                    src = tag.attrs[possible_attr]
                    break
            load = Image.open(src)
            cur_width, cur_height = load.size
            width = height = None

            if 'size' in tag.attrs:
                width = tag.attrs['size'].split('x')[0]
                height = tag.attrs['size'].split('x')[1]
            if 'width' in tag.attrs:
                width = tag.attrs['width']
                if 'height' not in tag.attrs:
                    height = cur_height * (width / cur_width)
            if 'height' in tag.attrs:
                height = tag.attrs['height']
                if 'width' not in tag.attrs:
                    width = cur_width * (height / cur_height)

            load = load.resize((int(width), int(height)), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(load)
            new_obj = Label(master, image=render)
            new_obj.image = render

        elif tag.name == 'checkbutton':
            new_obj = Checkbutton(master=master, text=tag.content, **tag.attrs)

        elif tag.name == 'listbox':
            new_obj = Listbox(master=master, **tag.attrs)

            for t in tag.children:
                if t.name == 'li':
                    new_obj.insert('end', t.content)
            loop_children = False

        elif tag.name == 'menu':
            menubar = Menu(self)
            for t in tag.children:
                if t.name == 'menu':
                    new_sub_menu = Menu(menubar, tearoff=0)
                    for _t in t.children:
                        if _t.name == 'command':
                            if 'command' in _t.attrs:
                                _t.attrs['command'] = self.construct_command(
                                    _t.attrs['command']
                                )
                            new_sub_menu.add_command(
                                label=_t.content,
                                **_t.attrs
                            )
                        if _t.name == 'seperator':
                            new_sub_menu.add_separator()
                    menubar.add_cascade(label=t.content, menu=new_sub_menu)

            self.config(menu=menubar)
            loop_children = False

        elif tag.name == 'spinbox':
            new_obj = Spinbox(master, **tag.attrs)

        return new_obj, loop_children

    def reload(self, id):
        item = self.get_item(id)
        if item is None:
            return

        master = item.master
        item.grid_forget()
        item.destroy()
        del self.items[id]

        self.construct(
            self.parent.render_xml(f"components/{id}.xml"),
            master=master
        )
