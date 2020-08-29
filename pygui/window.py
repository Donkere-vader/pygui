from tkinter import Tk, Frame, Label, Button, Menu
from PIL import Image, ImageTk
from .custom_tk import Entry, Text, Checkbutton, Listbox, Spinbox

class Window(Tk):
    def __init__(self, parent, xml, showing_window_vars):
        """ Initialize the window """
        super().__init__()
        self.parent = parent
        self.xml = xml
        self.working_masters = []
        self.showing_window_vars = showing_window_vars
        self.items = {}

    def get_item(self, id):
        """ Get the TK widget if it has the id="" attribute in the XML """
        if id in self.items:
            return self.items[id]
        return None

    def show(self):
        """ Show the current window """
        self.mainloop()

    def construct(self):
        """ Construct the current window """
        self._loop_tag(self.xml)

    def _loop_tag(self, tag):
        """ Loop over the XML tags and let the tags be generated and place them on their masters grid """
        new_obj = None
        loop_children = True

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

        new_obj = self.construct_tag(tag)

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

    def construct_tag(self, tag):
        """ Construct a tag into a tkinter object """
        if 'command' in tag.attrs:
            tag.attrs['command'] = lambda cmd=tag.attrs['command']: exec(cmd, {**self.showing_window_vars, **self.parent.globals})

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
            new_obj = Frame(master=self.working_masters[-1], **tag.attrs)
        elif tag.name == 'label':
            new_obj = Label(master=self.working_masters[-1], text=tag.content, **tag.attrs)
        elif tag.name == 'button':
            new_obj = Button(master=self.working_masters[-1], text=tag.content, **tag.attrs)
        elif tag.name in ['entry', 'text']:
            if tag.name == 'entry':
                new_obj = Entry(master=self.working_masters[-1], **tag.attrs)
            else:
                new_obj = Text(master=self.working_masters[-1], **tag.attrs)

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
            new_obj = Label(self.working_masters[-1], image=render)
            new_obj.image = render
        elif tag.name == 'checkbutton':
            new_obj = Checkbutton(master=self.working_masters[-1], text=tag.content, **tag.attrs)
        elif tag.name == 'listbox':
            new_obj = Listbox(master=self.working_masters[-1], **tag.attrs)

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
                            new_sub_menu.add_command(label=_t.content, command=lambda cmd=_t.attrs['command']: exec(cmd))
                        if _t.name == 'seperator':
                            new_sub_menu.add_separator()
                    menubar.add_cascade(label=t.content, menu=new_sub_menu)

            self.config(menu=menubar)
            loop_children = False
        elif tag.name == 'spinbox':
            new_obj = Spinbox(self.working_masters[-1], **tag.attrs)

        return new_obj
