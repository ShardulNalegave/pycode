
import os.path as path
import os
import wx
import wx.stc as stc


class App(wx.Frame):

    def __init__(self, parent, title):

        self.title = title
        self.filename = ""
        self.dirname = os.getcwd()

        wx.Frame.__init__(self, parent, title=self.title, size=(800, 600))

        self.create_status_and_menu_bar()
        self.load_widgets()

        self.Show()
        self.Maximize()

    def create_status_and_menu_bar(self):

        filemenu = wx.Menu()
        file_new = filemenu.Append(
            wx.ID_NEW, "&New\tCtrl+N", "Create A New Document")
        file_open = filemenu.Append(
            wx.ID_OPEN, "&Open\tCtrl+O", "Open An Existing Document")
        file_save = filemenu.Append(
            wx.ID_SAVE, "&Save\tCtrl+S", "Save Document")
        file_saveas = filemenu.Append(
            wx.ID_SAVEAS, "Save &As\tCtrl+Shift+S", "Save As Document")
        filemenu.AppendSeparator()
        quit_menuitem = filemenu.Append(
            wx.ID_EXIT, "&Quit\tCtrl+Q", "Quits The Application")

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.new_file, file_new)
        self.Bind(wx.EVT_MENU, self.open_file, file_open)
        self.Bind(wx.EVT_MENU, self.save_file, file_save)
        self.Bind(wx.EVT_MENU, self.saveas_file, file_saveas)
        self.Bind(wx.EVT_MENU, self.exit_app, quit_menuitem)

        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour((220, 220, 220))

    def load_widgets(self):

        self.editor = stc.StyledTextCtrl(
            self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        self.editor.CmdKeyAssign(
            ord("+"), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.editor.CmdKeyAssign(
            ord("-"), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        self.editor.SetViewWhiteSpace(False)
        self.editor.SetMargins(10, 0)
        self.editor.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.editor.SetMarginWidth(1, 25)
        self.editor.SetValue("""

from sys import argv

def greet(name):
    print("Hello, {}".format(name))

if __name__ == "__main__":
    greet(argv[1])

""")

    def new_file(self, event):
        projectTypeList = [
            "Simple App", "Command Line App", "Tkinter App", "WxPython App", "Flask Web App"]
        dlg = wx.SingleChoiceDialog(
            self, "Pick The Type Of Project You Want To Create:", "New Project", projectTypeList)
        if dlg.ShowModal() == wx.ID_OK:
            filename = ""
            selection = dlg.GetSelection()
            selection = projectTypeList[selection]
            if selection == "Simple App":
                self.editor.SetValue("print(Hello, World!'')")
            elif selection == "Command Line App":
                self.editor.SetValue("""

from sys import argv

def greet(name):
    print("Hello, {}".format(name))

if __name__ == "__main__":
    greet(argv[1])

""")
            elif selection == "Tkinter App":
                self.editor.SetValue("""

import tkinter

root = tkinter.Tk()
root.title("Hello World App")

label = tkinter.Label(root, text="Hello, World!")
label.pack(pady=20)

root.mainloop()

""")

            elif selection == "WxPython App":
                self.editor.SetValue("""

import wx

app = wx.App()

frm = wx.Frame(None, title="Hello World")
frm.Show()

app.MainLoop()

""")

            elif selection == "Flask Web App":
                self.editor.SetValue("""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)

""")
        dlg.Destroy()

    def exit_app(self, event):
        self.Close()

    def open_file(self, event):
        dlg = wx.FileDialog(
            self,
            message="Open File",
            defaultDir=self.dirname,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            self.editor.SetValue(open(paths[0], "r").read())
            self.filename = path.basename(paths[0])
            self.dirname = path.dirname(paths[0])
        dlg.Destroy()

    def save_file(self, event):
        try:
            fp = path.join(self.dirname, self.filename)
            with open(fp, "w+") as file:
                file.write(self.editor.GetValue())
        except:
            dlg = wx.FileDialog(
                self,
                message="Save As",
                defaultDir=self.dirname,
                style=wx.FD_SAVE
            )
            if dlg.ShowModal() == wx.ID_OK:
                loc = dlg.GetPath()
                self.dirname = path.dirname(loc)
                self.filename = path.basename(loc)
                fp = path.join(self.dirname, self.filename)
                with open(fp, "w+") as file:
                    file.write(self.editor.GetValue())
                dlg.Destroy()

    def saveas_file(self, event):
        dlg = wx.FileDialog(
            self,
            message="Save As",
            defaultDir=self.dirname,
            style=wx.FD_SAVE
        )
        if dlg.ShowModal() == wx.ID_OK:
            loc = dlg.GetPath()
            self.dirname = path.dirname(loc)
            self.filename = path.basename(loc)
            fp = path.join(self.dirname, self.filename)
            with open(fp, "w+") as file:
                file.write(self.editor.GetValue())
            dlg.Destroy()


root = wx.App()
App(None, title="PyCode - Code Editor")
root.MainLoop()
