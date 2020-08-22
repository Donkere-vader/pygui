from tkinter import Entry, END

class Entry(Entry):
    def val(self, value=None):
        if value is None:
            return self.get()
        else:
            self.delete(0, END)
            self.insert(0, value)
