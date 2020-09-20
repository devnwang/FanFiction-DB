# 2020/07/19
# Auto-complete Entry Widget

import tkinter as tk

class AutoEntry(tk.Entry):
    def __init__(self, parent, top=None, items=None, numShowItems = 5, cbFunc=None, lbfont=None, *args, **kwargs):
        tk.Entry.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.callback = cbFunc
            
        # root of the listbox is the parent of the entry widget
        self.lboxParent = top if top is not None else parent
        print(self.lboxParent)
        self.isMain = True if self.lboxParent is parent else False

        self.lbox = tk.Listbox(self.lboxParent, selectmode = tk.SINGLE, height=numShowItems, font=lbfont)
        self.lbox.bind('<<ListboxSelect>>', self.onSelectItem)

        # If list items given upon instantiation
        if items is not None:
            self.updateAutoEntry(items)

        # bind function to event
        self.bind('<KeyRelease>', self.checkKey)

    # Check the input to filter the list
    def checkKey(self, event):
        value = event.widget.get()
        print(value)

        if value == '':
            data = self.items
            self.lbox.place_forget()
        else:
            print("winfo_x: " + str(self.winfo_x()))
            print("winfo_parent: " + str(self.lbox.winfo_parent()))
            print("winfo_parent.winfo_x: " + str(self.parent.winfo_x()))
            self.x = self.winfo_x() if self.isMain else self.parent.winfo_x() + self.winfo_x()
            height = self.winfo_height() if self.isMain else self.parent.winfo_y() + self.winfo_height()
            self.ty = self.winfo_y() + height
            self.lbox.place(x = self.x, y = self.ty)
            data = []
            for item in self.items:
                if value.lower() in item.lower():
                    data.append(item)

        self.updateData(data)

    def updateData(self, data):
        self.lbox.delete(0, tk.END)
        for item in data:
            self.lbox.insert(tk.END, item)

    # Function to change the list being used for auto complete
    def updateAutoEntry(self, dataList):
        self.items = dataList
        self.updateData(self.items)

    # Callback function after item is selected from listbox
    def onSelectItem(self, event):
        # Retrieve the selected item
        selected = event.widget
        index = int(selected.curselection()[0])
        value = selected.get(index)

        # Update the entry box to display selected item
        self.delete(0, tk.END)
        self.insert(tk.END, value)

        # Remove the listbox from view
        self.lbox.place_forget()

        # If callback function exists, call it
        if self.callback:
            self.callback()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("700x500")

    l = ('Harry Potter', 'Harry Wells', 'League of Shadows', 'League of Warriors', 'League of Legends', 'League', 'Legend of Zelda')

    e = AutoEntry(parent = root, items = l, numShowItems = 7)
    e.pack()

    root.mainloop()