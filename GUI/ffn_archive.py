# 2020/07/11
# GUI Implementation for FFN DB

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import os

from pages.scripts import ui_utils as ui
from pages.Search import Search

def show_frame(cont):
    shwframe = frames[cont]
    shwframe.tkraise()

# Current working directory
# current = os.path.abspath(os.getcwd())
current = os.path.dirname(os.path.realpath(__file__))

# Window Variables
maxwidth = 800
maxheight = 600

# Creating root windo
root = tk.Tk()
root.title("My FanFiction Archive")
root.geometry("800x600")
root.maxsize(maxwidth, maxheight)

# ------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- NAVIGATION BAR ----------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------

# Create navbar
navbar = tk.Frame(root, height=15, borderwidth=2, bg='grey')

# TODO - Create a function that will create the navbar/menus
#      Needs to be done by gathering SQL data

# Load image for menu
right_arr = tk.PhotoImage(file= current+'/img/caret-down.png').subsample(8)

# Home Button
home_btn = tk.Button(navbar, text = 'Home', relief = 'flat', command=None)

# Folders
fld_m = tk.Menubutton(navbar, text='Folders', compound = tk.RIGHT, image = right_arr)
fld_m.menu = tk.Menu(fld_m, tearoff = 0)
fld_m['menu'] = fld_m.menu
fld_m.menu.add_command(label = 'Dummy Fld 1', command = None)
fld_m.menu.add_command(label = 'Dummy Fld 2', command = None)
fld_m.menu.add_command(label = 'Dummy Fld 3', command = None)
fld_m.menu.add_separator()
fld_m.menu.add_command(label = 'New Folder', command = None)

# Browse Menu
browse_m = tk.Menubutton(navbar, text='Browse', compound=tk.RIGHT, image=right_arr)
browse_m.menu = tk.Menu(browse_m, tearoff=0)
browse_m['menu'] = browse_m.menu
# Label 1 - Stories
browse_m.menu.add_command(label = 'Stories', command = None, activeforeground='black', activebackground='white smoke')

# Browse Menu - Cascades
books = tk.Menu(browse_m.menu, tearoff = 0)
books.add_command(label='Harry Potter', command=None)
books.add_command(label='Percy Jackson', command=None)
# Attach books to browse menu
browse_m.menu.add_cascade(label = 'Books', menu = books)

# Separator
browse_m.menu.add_separator()

# Crossovers
browse_m.menu.add_command(label = 'Crossovers', activeforeground='black', activebackground='whitesmoke')


# Search button
search_btn = tk.Button(navbar, text='Search', relief="flat", command=None)

# Dummy space
dummy = tk.Frame(navbar)

# Add New Story button
add_btn = tk.Button(navbar, text = '+', relief="flat", font = tkFont.Font(size = 18), command = None)

# Pack Menus
fld_m.pack(side = tk.LEFT, expand = True, fill = tk.Y)
browse_m.pack(side = tk.LEFT, expand = True, fill = tk.Y)
search_btn.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
dummy.pack(side= tk.LEFT, expand= True, fill = tk.BOTH)
add_btn.pack(side = tk.RIGHT, expand = True, fill = tk.BOTH)

# Adjust placeholder
ui.resize_holder(root, dummy, navbar, maxwidth)

# Grid the navbar
navbar.pack(side = tk.TOP)

container = tk.Frame(root)
container.pack(expand = True, fill = tk.BOTH)

#print(container.winfo_geometry())

frames = {}

frame = Search(container, root)

#frames[Search] = frame

frame.pack(expand = True, fill = tk.BOTH)

#show_frame(Search)

root.mainloop()
