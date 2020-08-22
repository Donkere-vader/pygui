from tkinter import Tk, Frame, Label, Button

class Window(Tk):
    def __init__(self, xml, showing_window_vars):
        super().__init__()
        self.xml = xml
        self.working_masters = []
        self.showing_window_vars = showing_window_vars

    def construct(self):
        self._loop_tag(self.xml)

    def _loop_tag(self, tag):
        new_obj = None

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
            if 'command' in tag.attrs:
                tag.attrs['command'] = lambda cmd=tag.attrs['command']: exec(cmd, self.showing_window_vars)
            new_obj = Button(master=self.working_masters[-1], text=tag.content, **tag.attrs)

        if new_obj is not None and tag.name != 'root':
            new_obj.grid(**grid)

        self.working_masters.append(new_obj)

        for child in tag.children:
            self._loop_tag(child)

        self.working_masters.remove(new_obj)
