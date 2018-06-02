#!/usr/bin/env python

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog


class AppUI(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master, relief=SUNKEN, bd=2)

        self.pack()

        self.master.title("PyCode - Code Editor")

        self.load_menu_bar()
        self.load_widgets()

    def about_dialog(self):
        dialog = messagebox.showinfo(
            "About", "A Simple Text Editor by Shardul Nalegave <nalegaveshardul40@gmail.com>")

    def new_doc(self):
        self.editor.destroy()
        self.options_indicator_label.destroy()
        self.save_button.destroy()
        self.quit_btn.destroy()
        self.new_btn.destroy()
        self.load_widgets()

    def load_menu_bar(self):

        self.menubar = Menu(self)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="New", command=self.new_doc)
        menu.add_command(label="Save", command=self.save_file)
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
        text_to_save = self.editor.get("1.0", "end-1c")
        loc = filedialog.asksaveasfilename()
        try:
            with open(loc, "w+") as file:
                file.write(text_to_save)
                file.close()
        except FileNotFoundError:
            pass

    def load_widgets(self):

        # Main Editor
        self.editor = Text(self)
        self.editor.pack(side="top")
        self.editor_font_size = 10
        self.editor_font_family = "Open Sans"
        self.editor.configure(
            font=(self.editor_font_family, self.editor_font_size))

        # Label
        self.options_indicator_label = ttk.Label(self, text="Options:- ")
        self.options_indicator_label.pack(side="left")

        # New Button
        self.new_btn = ttk.Button(self, text="New", command=self.new_doc)
        self.new_btn.pack(side="left")

        # Save Button
        self.save_button = ttk.Button(
            self, text="Save", command=self.save_file)
        self.save_button.pack(side="left")

        # Quit Button
        self.quit_btn = ttk.Button(
            self, text="Quit", command=self.master.destroy)
        self.quit_btn.pack(side="left")


root = Tk()

app = AppUI(root)
app.pack()

root.mainloop()
