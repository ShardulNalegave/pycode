#!/usr/bin/env python3.6

import os
import os.path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter.scrolledtext import ScrolledText


class AppUI(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master, relief=FLAT, bd=0)

        self.pack(fill=BOTH, expand=True)

        self.master.title("PyCode - Code Editor")

        self.load_menu_bar()
        self.load_widgets()

    def about_dialog(self):
        dialog = messagebox.showinfo(
            "About", "A Simple Text Editor by Shardul Nalegave <nalegaveshardul40@gmail.com>")

    def new_doc(self):
        self.editor.delete("1.0", "end-1c")
        self.master.title("PyCode - Code Editor")

    def open_file(self):
        try:
            self.status_bar["text"] = "Opening File..."
            loc = filedialog.askopenfilename()
            self.file = os.path.basename(loc)
            self.filePath = loc
            self.master.title(self.file + " - PyCode - Code Editor")
            with open(self.filePath, "r") as file:
                self.new_doc()
                self.editor.insert("1.0", file.read())
            self.status_bar["text"] = "PyCode - Code Editor"
        except TclError:
            self.master.title("PyCode - Code Editor")
        except FileNotFoundError:
            self.master.title("PyCode - Code Editor")

    def load_menu_bar(self):

        self.menubar = Menu(self)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="Open", command=self.open_file)
        menu.add_command(label="New", command=self.new_doc)
        menu.add_command(label="Save", command=self.save_file)
        menu.add_command(label="Save As", command=self.saveas_file)
        menu.add_separator()
        menu.add_command(label="Quit", command=self.master.destroy)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menu)
        menu.add_command(label="Font Size", command=self.edit_font_size)
        menu.add_command(label="Font Family", command=self.edit_font_family)

        self.menubar.add_cascade(label="About", command=self.about_dialog)

        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(master, "config", "-menu", self.menubar)

    def edit_font_size(self):
        try:
            new_size = simpledialog.askinteger("Font Size", "New Font Size")
            self.editor_font_size = new_size
            self.editor.configure(
                font=(self.editor_font_family, self.editor_font_size))
        except TclError:
            pass

    def edit_font_family(self):
        try:
            new_family = simpledialog.askstring(
                "Font Family", "New Font Family")
            self.editor_font_family = new_family
            self.editor.configure(
                font=(self.editor_font_family, self.editor_font_size))
        except TclError:
            pass

    def save_file(self):
        try:
            self.status_bar["text"] = "Saving File..."
            text_to_save = self.editor.get("1.0", "end-1c")
            loc = self.filePath
            try:
                with open(loc, "w+") as file:
                    file.write(text_to_save)
                    file.close()
            except FileNotFoundError:
                pass
            self.status_bar["text"] = "PyCode - Code Editor"
            self.master.title(os.path.basename(
                loc) + " - PyCode - Code Editor ")
            self.file = os.path.basename(loc)
            self.filePath = loc
        except TclError:
            self.master.title("PyCode - Code Editor")
        except FileNotFoundError:
            self.master.title("PyCode - Code Editor")

    def saveas_file(self):
        try:
            self.status_bar["text"] = "Saving File..."
            text_to_save = self.editor.get("1.0", "end-1c")
            loc = filedialog.asksaveasfilename()
            try:
                with open(loc, "w+") as file:
                    file.write(text_to_save)
                    file.close()
            except FileNotFoundError:
                pass
            self.status_bar["text"] = "PyCode - Code Editor"
            self.master.title(os.path.basename(
                loc) + " - PyCode - Code Editor ")
            self.file = os.path.basename(loc)
            self.filePath = loc
        except TclError:
            self.master.title("PyCode - Code Editor")
        except FileNotFoundError:
            self.master.title("PyCode - Code Editor")

    def load_widgets(self):

        # Main Editor
        self.editor_font_size = 10
        self.editor_font_family = "Open Sans"
        self.editor = ScrolledText(self, bd=0, relief=FLAT)
        self.editor.config(wrap=WORD)
        self.editor.configure(
            font=(self.editor_font_family, self.editor_font_size))
        self.editor.pack(expand=True, side=TOP, fill=BOTH)
        # self.editor.bind("<KeyPress>", self.syntaxHighlight)

        # Status Bar
        self.status_bar = Label(self, text="PyCode - Code Editor",
                                bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)


root = Tk()

app = AppUI(root)
app.pack()

root.mainloop()