# 2020/07/12
# Search Page

import tkinter as tk
import tkinter.ttk as ttk
import sys
import os

from PIL import ImageTk, Image

# Add to root dir to system path to access 'scripts'
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(1, root_dir)

try:
    from scripts import sql_utils as sql
except:
    from pages.scripts import sql_utils as sql

class Search(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.tl_img = self.getCornerImg(1)
        self.tr_img = self.getCornerImg(2)
        self.bl_img = self.getCornerImg(3)
        self.br_img = self.getCornerImg(4)
        
        dframe1 = self.createTBFrame('top')
        
        srch_frame = tk.Frame(self)
        # Search Label
        lblSrch = tk.Label(srch_frame, text = "Search", font = ('Roboto', 16, 'bold'))
        lblSrch.pack(side = tk.LEFT, expand = True, anchor = tk.E)
        
        # Search Box
        entSrch = tk.Entry(srch_frame, font = ('Roboto', 16))
        entSrch.pack(side = tk.LEFT, expand = True, anchor = tk.W)
        
        num_bdframes = 3
        bdframes = []
        for i in range(num_bdframes):
            if i < num_bdframes - 1:
                bdframes.append(tk.Frame(self))
            else:
                bdframes.append(self.createTBFrame('bottom'))
        
        
        dframe1.pack(side = tk.TOP, expand = True, fill = tk.BOTH)
        srch_frame.pack(side = tk.TOP, expand = True)
        for dframe in bdframes:
            dframe.pack(side = tk.TOP, expand = True, fill = tk.BOTH)
            
    def getCornerImg(self, corner = 2):
        img = Image.open(root_dir + '/img/red-corner.png')
        
        # Reduce the img by a factor of 5
        img = img.reduce(5)
        
        if corner == 1 or corner == 3:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if corner == 3 or corner == 4:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            
        return ImageTk.PhotoImage(img)
        
    def createTBFrame(self, pos):
        frame = tk.Frame(self)
        lframe = tk.Frame(frame)
        #mframe = tk.Frame(frame, background="red")
        rframe = tk.Frame(frame)
        
        if pos == 'top':
            limg = self.tl_img
            rimg = self.tr_img
        elif pos == 'bottom':
            limg = self.bl_img
            rimg = self.br_img
        else:
            raise Exception("{0} is not a valid argument".format(pos))
        
        lpnl = tk.Label(frame, image = limg)
        rpnl = tk.Label(frame, image = rimg)
        
        lpnl.pack(side = tk.LEFT)
        lframe.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
        #mframe.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
        rpnl.pack(side = tk.RIGHT)
        rframe.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
        
        return frame


# TODO_1: Implement autocomplete combobox --> gfg tutorial, but only display listbox upon entry
# TODO_2: Look into ttk.Entry and see if the style can change based on results of autocomplete

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("800x585")
    root.maxsize(800, 585)
    controller = tk.Frame(root)
    srchpg = Search(root, controller)
    srchpg.pack(expand = True, fill = tk.BOTH)
    #sql.getFolders()
    print("got folders")
    
