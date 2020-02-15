#! python3

import tkinter as tk
from tkinter import ttk
import Styles
import FileInfo
import os


class NoteBookCatdv(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)

        self.config(padding='10 10 10 10', style='catdv.TNotebook')
        self.grid(column=0, row=0, ipady=5)
        self.t_flow = ttk.Frame(style='TFrame')
        self.t_speechmatics = ttk.Frame(style='TFrame')

        self.imagepath = os.path.join(FileInfo.currentDir(), "images")
        self.ok_png = tk.PhotoImage(
            file=os.path.join(self.imagepath, "checkmark-12.png"))
        self.warn_png = tk.PhotoImage(
            file=os.path.join(self.imagepath, "warning-16.png"))

        self.add(self.t_flow, text='Flow')
        self.add(self.t_speechmatics, text='Speechmatics')

    # add an image to a notebook tab
    def tab_image(self, tab, *image):
        # if image is not provided, the current image turns off
        self.tab(tab, image=image, compound=tk.RIGHT)


root = tk.Tk()
root.title('Flow Transcribe Control Panel')
Styles.defineStyles(root)

mainframe = ttk.Frame(root, padding='0 0 0 0', style='catdv.TFrame')
mainframe.pack(expand=tk.YES, fill=tk.BOTH)

notebook = NoteBookCatdv(mainframe)

notebook.tab_image(notebook.t_flow, notebook.warn_png)
notebook.tab_image(notebook.t_speechmatics, notebook.ok_png)
# notebook.tab_image(notebook.t_flow, '')

print(notebook.tab(1))

root.mainloop()
