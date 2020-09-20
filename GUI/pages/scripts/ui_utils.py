# 2020/07/11
# UI Functions

import tkinter as tk
import tkinter.ttk as ttk
import os

# Resizes the space holder in the navbar
def resize_holder(root, frame, parent, maxwidth):
    # update the root to get accurate info
    root.update()

    # get the current width of the navbar
    par_width = parent.winfo_reqwidth()

    # calculate the new width of the frame
    new_width = maxwidth - par_width

    # configure the frame with the new width
    frame.configure(width = new_width)

# Creates the navigation bar
def create_navbar(root, h = 15, bw = 2, bg = 'grey'):
    mdrop_img_path = os.path.abspath(os.getcwd()) + '/img/caret-down.png'
    mdrop_img = tk.PhotoImage(file = mdrop_img_path).subsample(8)

    navbar = tk.Frame(root, height = h, borderwidth = bw, bg = bg)

    dropdowns = ['Folders', 'Browse']

    folders = ['d1', 'd2', 'd3']

    for items in dropwdowns:
        mitem = tk.Menubutton(navbar, text = item, compound = tk.RIGHT, image = mdrop_img)
        mitem.menu = tk.Menu(mitem, tearoff = 0)
        mitem['menu'] = mitem.menu
    

# Creates a menu
def create_menu(parent, name, img):
    mitem = tk.Menubutton(parent, text = name, compound = tk.RIGHT, image = img)
    mitem.menu = tk.Menu(mitem, tearoff = 0)
    mitem['menu'] = mitem.menu


def populate_menu(mtype):
    if mtype == 'Folders':
        # Query for folders
        pass
    elif mtype == 'Browse':
        # Query for Category Source
        pass

if __name__ == '__main__':
    pass
