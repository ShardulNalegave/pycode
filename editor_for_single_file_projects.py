
"""

    author: Shardul Nalegave
    license:-

        MIT License

        Copyright (c) 2018 Shardul Nalegave

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.

"""

import os.path as path
import os
import wx
import wx.stc as stc
import keyword

if wx.Platform == '__WXMSW__':
    faces = {'times': 'Times New Roman',
             'mono': 'Courier New',
             'helv': 'Arial',
             'other': 'Comic Sans MS',
             'size': 10,
             'size2': 8,
             }
elif wx.Platform == '__WXMAC__':
    faces = {'times': 'Times New Roman',
             'mono': 'Monaco',
             'helv': 'Arial',
             'other': 'Comic Sans MS',
             'size': 12,
             'size2': 10,
             }
else:
    faces = {'times': 'Times',
             'mono': 'Courier',
             'helv': 'Helvetica',
             'other': 'new century schoolbook',
             'size': 12,
             'size2': 10,
             }


class App(wx.Frame):

    def __init__(self, parent, title):

        self.title = title
        self.filename = ""
        self.dirname = os.getcwd()

        wx.Frame.__init__(self, parent, title=self.title, size=(800, 600))

        self.create_status_and_menu_bar()
        self.load_widgets()
        self.updateCaretPosInStatusBar()

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

        projectmenu = wx.Menu()
        project_install_package = projectmenu.Append(
            wx.ID_ANY, "&Install A Package\tCtrl+Shift+I", "Install A Python Package")

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        menubar.Append(projectmenu, "&Project")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.new_file, file_new)
        self.Bind(wx.EVT_MENU, self.open_file, file_open)
        self.Bind(wx.EVT_MENU, self.save_file, file_save)
        self.Bind(wx.EVT_MENU, self.saveas_file, file_saveas)
        self.Bind(wx.EVT_MENU, self.exit_app, quit_menuitem)

        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour((220, 220, 220))

    def install_package(self, event):
        pass

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
        self.editor.SetMarginWidth(2, 35)
        # self.editor.SetMarginType(
        #     2, stc.STC_MARGIN_SYMBOL | stc.STC_MARGIN_NUMBER)
        # self.editor.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        # self.editor.SetMarginSensitive(2, True)
        # self.editor.SetMarginWidth(2, 35)
        self.editor.SetLexer(stc.STC_LEX_PYTHON)
        self.editor.SetKeyWords(
            0, " ".join(keyword.kwlist))
        self.editor.SetProperty("fold", "1")
        self.editor.SetProperty("tab.timmy.whinge.level", "1")
        self.editor.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        self.editor.SetEdgeColumn(78)
        self.editor.Bind(wx.EVT_KEY_DOWN, self.updateCaretPosInStatusBar)
        self.editor.SetValue("""

from sys import argv

def greet(name):
        print("Hello, {}".format(name))

if __name__ == "__main__":
        greet(argv[1])

""")

        self.syntax_highlight_styles_python = {
            "default": "#000000",
            "keyword": "#EF5350",
            "comment-line": "#BDBDBD",
            "block_comment": "#BDBDBD",
            "string": "#43A047",
            "block_string": "#43A047",
            "operators": "#EF5350",
            "number": "#29B6F6",
            "EOL_when_string_not_closed": "#E53935",
            "class_and_function_names": "#7E57C2",
            "identifiers": "#000000"
        }

        self.global_styles = {
            "linenum_back": "#F5F5F5",
            "cursor": "#000000"
        }

        self.update_syntax_highlight(
            self.syntax_highlight_styles_python, self.global_styles)

    def updateCaretPosInStatusBar(self, event=None):
        lineno = int(self.editor.GetCurrentLine()) + 1
        self.StatusBar.SetStatusText("Line {}".format(str(lineno)))
        if event != None:
            event.Skip()

    def update_syntax_highlight(self, python_styles, global_styles):

        if not isinstance(python_styles, dict):
            print("Styles Passed Should Be Dictionaries")
            return False

        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted from
        # Scintilla sample property files.

        # Global default styles for all languages
        self.editor.StyleSetSpec(stc.STC_STYLE_DEFAULT,
                                 "face:%(helv)s,size:%(size)d" % faces)
        self.editor.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.editor.StyleSetSpec(stc.STC_STYLE_DEFAULT,
                                 "face:%(helv)s,size:%(size)d" % faces)
        self.editor.StyleSetSpec(stc.STC_STYLE_LINENUMBER,
                                 "back:" + global_styles["linenum_back"] + ",face:%(helv)s,size:%(size2)d" % faces)
        self.editor.StyleSetSpec(
            stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.editor.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,
                                 "fore:#FFFFFF,back:#0000FF,bold")
        self.editor.StyleSetSpec(stc.STC_STYLE_BRACEBAD,
                                 "fore:#000000,back:#FF0000,bold")

        # Python styles
        # Default
        self.editor.StyleSetSpec(stc.STC_P_DEFAULT,
                                 "fore:" + python_styles["default"] + ",face:%(helv)s,size:%(size)d" % faces)
        # Comments
        self.editor.StyleSetSpec(stc.STC_P_COMMENTLINE,
                                 "fore:" + python_styles["comment-line"] + ",face:%(other)s,size:%(size)d" % faces)
        # Number
        self.editor.StyleSetSpec(stc.STC_P_NUMBER,
                                 "fore:" + python_styles["number"] + ",size:%(size)d" % faces)
        # String
        self.editor.StyleSetSpec(stc.STC_P_STRING,
                                 "fore:" + python_styles["string"] + ",face:%(helv)s,size:%(size)d" % faces)
        # Single quoted string
        self.editor.StyleSetSpec(stc.STC_P_CHARACTER,
                                 "fore:" + python_styles["string"] + ",face:%(helv)s,size:%(size)d" % faces)
        # Keyword
        self.editor.StyleSetSpec(
            stc.STC_P_WORD, "fore:" + python_styles["keyword"] + ",size:%(size)d" % faces)
        # Triple quotes
        self.editor.StyleSetSpec(stc.STC_P_TRIPLE,
                                 "fore:" + python_styles["block_string"] + ",size:%(size)d" % faces)
        # Triple double quotes
        self.editor.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE,
                                 "fore:" + python_styles["block_string"] + ",size:%(size)d" % faces)
        # Class name definition
        self.editor.StyleSetSpec(stc.STC_P_CLASSNAME,
                                 "fore:" + python_styles["class_and_function_names"] + ",size:%(size)d" % faces)
        # Function or method name definition
        self.editor.StyleSetSpec(stc.STC_P_DEFNAME,
                                 "fore:" + python_styles["class_and_function_names"] + ",size:%(size)d" % faces)
        # Operators
        self.editor.StyleSetSpec(
            stc.STC_P_OPERATOR, "fore:" + python_styles["operators"] + ",size:%(size)d" % faces)
        # Identifiers
        self.editor.StyleSetSpec(stc.STC_P_IDENTIFIER,
                                 "fore:" + python_styles["identifiers"] + ",face:%(helv)s,size:%(size)d" % faces)
        # Comment-blocks
        self.editor.StyleSetSpec(stc.STC_P_COMMENTBLOCK,
                                 "fore:" + python_styles["block_comment"] + ",size:%(size)d" % faces)
        # End of line where string is not closed
        self.editor.StyleSetSpec(
            stc.STC_P_STRINGEOL, "fore:" + python_styles["EOL_when_string_not_closed"] + ",face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

        self.editor.SetCaretForeground(global_styles["cursor"])

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
