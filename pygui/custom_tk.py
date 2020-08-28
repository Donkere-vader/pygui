from tkinter import Entry, END, Text

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
