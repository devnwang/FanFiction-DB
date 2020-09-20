# 2020/07/16
# Add new story page

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from widgets.autocomplete import AutoEntry
from scripts.sql_utils import db

class NewStory():
    def __init__(self, parent):
        #tk.Toplevel.__init__(parent)
        self.window = tk.Toplevel(parent)

        # Window information
        self.maxsize = "700x500"
        self.window.geometry(self.maxsize)
        self.mainTitle = "My FanFiction Archive - Add New Story - "
        self.subTitle = ""

        # Stage Layout
        self.stageLbls = ('Basic Info', 'Detailed Info', 'Characters & Pairings', 'Notes', 'Confirmation')
        self.stageLayouts = (BasicInfo, DetailedInfo, CharacterPairings, Notes, Confirmation)
        self.currStage = 0
        self.finalStage = 4

        # Story info variables
        self.isCrossover = tk.IntVar()
        self.srcId = []
        self.cat1 = ''
        self.cat2 = ''
        self.title = ''
        self.author = ''
        self.rating = 0
        self.srcBool = {}
        self.storyIds = {}
        # self.hasFFN = False
        # self.ffn_storyId = ''
        # self.hasWP = False
        # self.wp_storyId = ''
        # self.hasWN = False
        # self.wn_storyId = ''

        self.btnFont = ('Roboto', 16)

        # Initialize connection to db
        self.db = db()
        # Get the sources
        self.sources = self.db.getSource()
        # Populate source dictionaries
        for source in self.sources:
            self.srcBool[source] = tk.IntVar()
            self.storyIds[source] = ''

        # Progress Bar
        frame_progress = tk.Frame(self.window)
        self.progressBar = ttk.Progressbar(frame_progress, orient = tk.HORIZONTAL, value = 20, length = 100, mode = 'determinate')
        self.progressLbl = tk.Label(frame_progress, text = self.stageLbls[self.currStage], font=('Roboto'))

        self.progressBar.pack(pady=5, ipadx = 250)
        self.progressLbl.pack()
        frame_progress.pack(expand = True, fill = tk.BOTH)

        # Content Container
        frame_stageContainer = tk.Frame(self.window)
        frame_stageContainer.pack(expand = True, fill = tk.BOTH)
        # Initalize frames to an empty array
        self.stageFrames = {}
        # Iterate through page layouts
        for f in self.stageLayouts:
            # frame = f(container, self)
            frame = f(frame_stageContainer, self)
            self.stageFrames[f] = frame
            frame.pack(expand = True, fill = tk.BOTH)

        # Display the current page
        self.showPage(self.currStage)


        # Stage navigation buttons
        frame_stageNav = tk.Frame(self.window)
        #frame_stageNav = tk.Frame(self.window)
        frame_stageNav.pack(side = tk.TOP, expand = True, fill = tk.BOTH)
        # Cancel button
        cncl_btn = tk.Button(frame_stageNav, text = "Cancel", font=self.btnFont, command = self.quit)
        cncl_btn.pack(side = tk.LEFT, expand = True)
        # Next/Done button
        self.nxtdone_btn = tk.Button(frame_stageNav, text = "Next", font=self.btnFont, command = self.goToNextStage)
        self.nxtdone_btn.pack(side = tk.LEFT, expand = True)

    # Raise the selected frame to the top
    def showPage(self, page):
        # Obtain the indicated page
        stage = self.stageFrames[self.stageLayouts[page]]
        
        # Obtain and update the page name
        self.subTitle = self.stageLbls[page]
        self.window.wm_title(self.mainTitle + self.subTitle)
        
        stage.tkraise()

    # Update the UI for the Progress Bar
    def goToNextStage(self):
        # Update the progress bar value
        self.progressBar['value'] = self.progressBar['value'] + 20

        # Update the current stage
        self.currStage = self.currStage + 1
        self.progressLbl.configure(text = self.stageLbls[self.currStage])

        # Check if final stage
        if self.currStage == self.finalStage:
            self.nxtdone_btn.configure(text = "Done", command = self.complete)

        self.window.update_idletasks()

    # Cancel process
    def quit(self):
        # Ask for confirmation
        isCancel = messagebox.askyesno(message = "Are you sure you want to cancel?", title = "Cancel", icon="question", default = "no")

        # Only cancel operation if there is confirmation
        if isCancel:
            self.window.destroy()

    # Finalize new story entry
    def complete(self):
        # ask for confirmation
        # if confirmed, display success message
        # after closing success message, destroy the window
        pass

# Stage 1 - Basic Info
class BasicInfo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.itemFonts = ('Roboto', 12)

        # Init connection to db
        self.db = db()
        self.autoLabels = [['Source', 'Category'], 'Title', 'Author']
        self.crossovers = 0
        self.autoentries = []

        # Inputs for autoLabels
        for items in self.autoLabels:
            self.createAutoCompleteInputs(items)

        # Rating input
        rateFrame = tk.Frame(self)
        ratingLbl = tk.Label(rateFrame, text="Rating", font=self.itemFonts)
        ratingLbl.pack(side = tk.LEFT, expand=True)
        # Retrieve rating information from database
        ratingSqlRes = self.db.getRatings()
        self.rating = {}
        for row in ratingSqlRes:
            self.rating[row['Rating']+' - '+row['Description']] = row['Rating_Id']

        ratingList = list(self.rating.keys())
        self.ratingCbox = ttk.Combobox(rateFrame, width=len(max(ratingList, key=len)), values=ratingList, state="readonly", postcommand=self.updateRating, font = self.itemFonts)
        self.ratingCbox.pack(side = tk.LEFT, padx=5)

        rateFrame.pack(side = tk.TOP, expand = True, pady=5)

        # Story Ids
        for source in self.controller.sources:
            self.createIdInputs(source, len(max(self.controller.sources.keys(), key=len)))

        # Raise all the autocomplete suggestion boxes
        for entry in self.autoentries:
            entry.tkraise()
        


    def createAutoCompleteInputs(self, item):
        tmpFrame = tk.Frame(self)

        # current autocomplete item is a list (i.e. Source & Category)
        if isinstance(item, list):
            catSrc = self.db.getCategorySource()

            frame1 = tk.Frame(tmpFrame)
            src1Lbl = tk.Label(frame1, text=item[0], font=self.itemFonts)
            src1Auto = AutoEntry(frame1, self, catSrc, numShowItems=3, lbfont=self.itemFonts, font=self.itemFonts, cbFunc=lambda: self.toggle_state(cat1Auto))
            self.autoentries.append(src1Auto.lbox)
            cat1Lbl = tk.Label(frame1, text=item[1], font=self.itemFonts)
            # TODO: Add callback function to AutoEntry
            cat1Auto = AutoEntry(frame1, self, numShowItems=3, lbfont=self.itemFonts, font=self.itemFonts)
            self.autoentries.append(cat1Auto.lbox)
            cat1Auto.configure(state=tk.DISABLED)
            self.crossChk = tk.Checkbutton(frame1, text="Crossover", variable=self.controller.isCrossover, font=self.itemFonts, command=self.toggle_crossover)

            # Pack items
            src1Lbl.pack(side = tk.LEFT, expand = True, padx=5)
            src1Auto.pack(side = tk.LEFT, expand = True, padx=5)
            cat1Lbl.pack(side = tk.LEFT, expand = True, padx=5)
            cat1Auto.pack(side = tk.LEFT, expand = True, padx=5)
            self.crossChk.pack(side = tk.LEFT, expand = True, padx=5)

            frame1.pack()

            frame2 = tk.Frame(tmpFrame)
            frame2.pack()
            self.src2Lbl = tk.Label(frame2, text=item[0], font=self.itemFonts)
            self.src2Auto = AutoEntry(frame2, self, catSrc, 3, lbfont=self.itemFonts, font=self.itemFonts)
            self.autoentries.append(self.src2Auto.lbox)
            self.cat2Lbl = tk.Label(frame2, text=item[1], font=self.itemFonts)
            self.cat2Auto = AutoEntry(frame2, self, numShowItems=3, lbfont=self.itemFonts, font=self.itemFonts)
            self.autoentries.append(self.cat2Auto.lbox)
            self.cat2Auto.configure(state=tk.DISABLED)

        # 'Title' or 'Author'
        else:
            dummyFrameLeft = tk.Frame(tmpFrame, width=100)
            dummyFrameLeft.pack(side=tk.LEFT, fill=tk.BOTH)

            lblFrame = tk.Frame(tmpFrame)
            tmpLbl = tk.Label(lblFrame, text=item, font=self.itemFonts, width=10, anchor=tk.W)
            tmpLbl.pack(side = tk.LEFT, expand=True)

            entFrame = tk.Frame(tmpFrame)
            tmpAuto = AutoEntry(entFrame, self, numShowItems=3, lbfont=self.itemFonts, font=self.itemFonts)
            self.autoentries.append(tmpAuto.lbox)
            tmpAuto.configure(state=tk.DISABLED)
            tmpAuto.pack(side = tk.LEFT, expand=True, fill=tk.X)

            # Pack Frames
            lblFrame.pack(side=tk.LEFT)
            entFrame.pack(side=tk.LEFT, expand = True, fill=tk.X)

            dummyFrameRight = tk.Frame(tmpFrame, width=100)
            dummyFrameRight.pack(side=tk.RIGHT, fill=tk.BOTH)

        tmpFrame.pack(side = tk.TOP, pady = 5, expand = True, fill=tk.BOTH)

    # TODO: Write a better callback function for the autoentries that will also update the query used for the autocomplete
    def toggle_state(self, item):
        item.config(stat=tk.NORMAL)
        
    def toggle_crossover(self):
        # If boolean is true
        if self.controller.isCrossover.get():
            self.src2Lbl.pack(side = tk.LEFT, expand = True, padx=5)
            self.src2Auto.pack(side = tk.LEFT, expand = True, padx=5)
            self.cat2Lbl.pack(side = tk.LEFT, expand = True, padx=5)
            self.cat2Auto.pack(side = tk.LEFT, expand = True, padx=5)
        else:
            self.src2Lbl.pack_forget()
            self.src2Auto.pack_forget()
            self.cat2Lbl.pack_forget()
            self.cat2Auto.pack_forget()


    def updateRating(self):
        if self.ratingCbox.get() != '':
            self.controller.rating = self.rating[self.ratingCbox.get()]

    def createIdInputs(self, src, maxlen):
        tmpFrame = tk.Frame(self)

        dummyFrameTop = tk.Frame(tmpFrame, width=100)
        dummyFrameTop.pack(side=tk.LEFT)

        # Create checkbox
        chkFrame = tk.Frame(tmpFrame)
        srcCheck = tk.Checkbutton(chkFrame, text=src, variable=self.controller.srcBool[src], font=self.itemFonts, width=maxlen, anchor=tk.W, command="")
        srcCheck.pack(side=tk.LEFT)
        chkFrame.pack(side=tk.LEFT, fill=tk.BOTH)

        # Label frame for story id input
        idFrame = tk.LabelFrame(tmpFrame, text="Story Id", font=('Roboto', 8))
        idFrame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        idEntry = tk.Entry(idFrame, font=self.itemFonts)
        idEntry.pack(fill=tk.X)

        dummyFrameBtm = tk.Frame(tmpFrame, width=100)
        dummyFrameBtm.pack(side=tk.RIGHT)

        tmpFrame.pack(side=tk.TOP, expand = True, fill=tk.BOTH, pady=5)




# stage 2 - Detailed Info
class DetailedInfo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

# Stage 3 - Characters & Pairings
class CharacterPairings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

# Stage 4 - Story Notes
class Notes(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

# Stage 5 - Confirmation of all information
class Confirmation(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        

if __name__ == '__main__':
    root = tk.Tk()
    test_button = tk.Button(root, text = "Test New Story Btn", pady = 10, padx = 10, command=lambda: NewStory(root))
    test_button.pack()

    root.mainloop()