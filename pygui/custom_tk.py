from tkinter import Entry, END, Text, Listbox, Spinbox
from tkinter import ttk


class Entry(Entry):
    """ Custom Entry obj with the added .val() for ease of use """
    def val(self, value=None):
        if value is None:
            return self.get()
        else:
            self.delete(0, END)
            self.insert(0, value)


class Text(Text):
    """ Custome Text obj wit the added .val() for ease of use """
    def val(self, value=None):
        if value is None:
            return self.get("1.0", END)
        else:
            self.delete("1.0", END)
            self.insert("1.0", value)


class Checkbutton(ttk.Checkbutton):
    def val(self, value=None):
        if value is True:
            self.select()
            return
        elif value is False:
            self.deselect()
            return
        state = self.state()
        if 'selected' in state:
            return True
        else:
            return False


class Listbox(Listbox):
    def val(self, values=[]):
        if len(values) == 0:
            selected_items = []
            _items = self.get(0, END)

            for num in self.curselection():
                selected_items.append(_items[num])

            return selected_items
        else:
            self.delete(0, END)
            for val in values:
                self.insert(END, val)


class Spinbox(Spinbox):
    def val(self, value=None):
        if value is not None:
            self.delete(0, END)
            self.insert(0, value)
        else:
            return self.get()
