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
import temps_for_project
import wx.lib.agw.flatnotebook as Notebook_Widget
import wx.py
import yaml

from yapf.yapflib.yapf_api import FormatCode

import highlighter as Highlighter

try:
    config = yaml.load(open("./user_config.yml").read())
except FileNotFoundError:
    with open("./user_config.yml", "w+") as file:
        file.write("""
styles:
    python:
        default: "#000000"
        keyword: "#EF5350"
        comment-line: "#BDBDBD"
        block_comment: "#BDBDBD"
        string: "#43A047"
        block_string: "#43A047"
        operators: "#EF5350"
        number: "#29B6F6"
        EOL_when_string_not_closed: "#E53935"
        class_and_function_names: "#7E57C2"
        identifiers: "#000000"
        decorator: "#E53935"
    global:
        linenum_back: "#F5F5F5"
        cursor: "#000000"
    html:
        default: "#000000"
        comment: "#9E9E9E"
        string: "#66BB6A"
        attribute: "#EF5350"
        tag: "#7986CB"
    yaml:
        default: "#000000"
        comment: "#66BB6A"
        identifier: "#7E57C2"
        error: "#E53935"
        number: "#2196F3"
""")


class App(wx.Frame):
    def __init__(self, parent, title, dir_or_file_path):

        self.title = title
        self.dirname = os.getcwd()
        self.filename = ""
        self.file_ext = ".py"

        wx.Frame.__init__(self, parent, title=self.title, size=(800, 600))

        self.create_status_and_menu_bar()
        self.load_widgets()
        self.load_settings_widgets()
        self.editor_keyup()

        print(dir_or_file_path)

        if dir_or_file_path != "":
            path_to_open = path.abspath(
                path.join(path.abspath(os.getcwd()), dir_or_file_path))
            if path.isdir(path_to_open):
                self.dirname = path.abspath(path_to_open)
                items_in_project = os.listdir(path.abspath(self.dirname))
                self.dirTree.DeleteAllItems()
                self.updateDirTree()
                for item in items_in_project:
                    if (item == "main.py"
                            or item == "index.py") and not path.isdir(item):
                        self.editor.SetValue(
                            open(path.join(self.dirname, item), "r").read())
                        self.filename = item
                        self.file_ext = path.splitext(self.filename)
            elif path.isfile(path.join(os.getcwd(), dir_or_file_path)):
                self.dirname = path.dirname(path.abspath(path_to_open))
                self.dirTree.DeleteAllItems()
                self.updateDirTree()
                self.filename = path.basename(path.abspath(path_to_open))
                self.file_ext = path.splitext(self.filename)
                self.editor.SetValue(
                    open(path.join(self.dirname, self.filename), "r").read())
            # print(path.abspath(path.join(path.abspath(os.getcwd()), dir_or_file_path)))
        elif dir_or_file_path == "":
            self.dirname = os.getcwd()
            self.filename = ""
            self.file_ext = ".py"
            self.open_project()

        self.Show()
        self.Maximize()

    def create_status_and_menu_bar(self):

        self.CreateStatusBar(2)
        self.StatusBar.SetBackgroundColour((220, 220, 220))
        self.StatusBar.SetStatusWidths([-4, -1])
        self.StatusBar.SetStatusText("Line 1")
        self.StatusBar.SetStatusText("Python", 1)

        filemenu = wx.Menu()
        file_new_menu = wx.Menu()
        file_new_menu_python_project = file_new_menu.Append(
            wx.ID_ANY, "&Python Project\tCtrl+N", "Create A Python Project")
        file_new_menu_file_menu = wx.Menu()
        file_new_menu_file_menu_python = file_new_menu_file_menu.Append(
            wx.ID_ANY, "&Python File", "Create A Python File")
        file_new_menu_file_menu_html = file_new_menu_file_menu.Append(
            wx.ID_ANY, "&HTML File", "Create A HTML File")
        file_new_menu_file_menu_yaml = file_new_menu_file_menu.Append(
            wx.ID_ANY, "&YAML File", "Create A YAML File")
        file_new_menu_file_menu.AppendSeparator()
        file_new_menu_file_menu_file = file_new_menu_file_menu.Append(
            wx.ID_ANY, "&File", "Create A File")
        file_new_menu.AppendMenu(wx.ID_ANY, "&File", file_new_menu_file_menu)
        file_new_menu.AppendSeparator()
        file_new_menu_directory = file_new_menu.Append(
            wx.ID_ANY, "&Directory", "Create A New Directory")
        # file_new = filemenu.Append(
        #     wx.ID_NEW, "&New\tCtrl+N", "Create A New Document")
        filemenu.AppendMenu(wx.ID_NEW, "&New", file_new_menu)
        file_open = filemenu.Append(wx.ID_OPEN, "&Open\tCtrl+O",
                                    "Open An Existing Document")
        file_save = filemenu.Append(wx.ID_SAVE, "&Save\tCtrl+S",
                                    "Save Document")
        file_saveas = filemenu.Append(wx.ID_SAVEAS, "Save &As\tCtrl+Shift+S",
                                      "Save As Document")
        filemenu.AppendSeparator()
        quit_menuitem = filemenu.Append(wx.ID_EXIT, "&Quit\tCtrl+Q",
                                        "Quits The Application")

        projectmenu = wx.Menu()
        projectmenu_runcurrfile = projectmenu.Append(
            wx.ID_ANY, "&Run Current File\tCtrl+R", "Run Current File In Python Shell")

        viewmenu = wx.Menu()
        viewmenu_shell = viewmenu.Append(
            wx.ID_ANY, "&Shell\tCtrl+`", "Start Python Shell")
        viewmenu.AppendSeparator()
        viewmenu_settings = viewmenu.Append(
            wx.ID_ANY, "S&ettings\tCtrl+,", "Edit Settings")

        # editmenu = wx.Menu()
        # editmenu_togglecomment = editmenu.Append(wx.ID_ANY, "&Toggle Line Comment\tCtrl+.")

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        # menubar.Append(editmenu, "&Edit")
        menubar.Append(viewmenu, "&View")
        menubar.Append(projectmenu, "&Project")
        self.SetMenuBar(menubar)

        # self.Bind(wx.EVT_MENU, self.new_project, file_new)
        self.Bind(wx.EVT_MENU, self.new_directory, file_new_menu_directory)
        self.Bind(wx.EVT_MENU, self.new_python_project,
                  file_new_menu_python_project)
        self.Bind(wx.EVT_MENU, self.new_file, file_new_menu_file_menu_file)
        self.Bind(wx.EVT_MENU, self.new_python_file,
                  file_new_menu_file_menu_python)
        self.Bind(wx.EVT_MENU, self.new_html_file,
                  file_new_menu_file_menu_html)
        self.Bind(wx.EVT_MENU, self.new_yaml_file,
                  file_new_menu_file_menu_yaml)
        self.Bind(wx.EVT_MENU, self.open_project, file_open)
        self.Bind(wx.EVT_MENU, self.save_file, file_save)
        self.Bind(wx.EVT_MENU, self.saveas_file, file_saveas)
        self.Bind(wx.EVT_MENU, self.exit_app, quit_menuitem)
        self.Bind(wx.EVT_MENU, self.view_python_shell, viewmenu_shell)
        self.Bind(wx.EVT_MENU, self.open_settings, viewmenu_settings)
        self.Bind(wx.EVT_MENU, self.run_curr_file, projectmenu_runcurrfile)

    def open_settings(self, event):
        self.settings_win.Show()
        self.load_settings_widgets()

    def view_python_shell(self, event):
        shellWin = wx.Frame(self, title="Python Shell", size=(800, 600))
        shell = wx.py.shell.Shell(
            shellWin, wx.ID_ANY)
        shellWin.Show()

    def run_curr_file(self, event):
        if self.file_ext == ".py":
            shellWin = wx.Frame(
                self, title="Run Current File", size=(800, 600))
            shell = wx.py.shell.Shell(
                shellWin, wx.ID_ANY)
            shellWin.Show()
            shell.run("import os")
            shell.run("os.system('python3.6 {}')".format(
                path.join(self.dirname, self.filename)))
            shellWin.Close()
        elif self.file_ext in [".html", ".htm"]:
            import webbrowser
            webbrowser.open("file://{}".format(self.dirname, self.filename))

    def new_directory(self, event):
        dlg = wx.TextEntryDialog(
            self, "New Directory", "Enter The Name Of Directory")
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetValue()
            os.mkdir(path.join(self.dirname, dirname))
            self.dirTree.DeleteAllItems()
            self.updateDirTree()
        dlg.Destroy()

    def new_python_file(self, event):
        dlg = wx.TextEntryDialog(self, "New File", "Enter The Name Of File")
        if dlg.ShowModal() == wx.ID_OK:
            path_of_file = dlg.GetValue()
            open(path.join(self.dirname, "{}.py".format(path_of_file)),
                 "w+").write("import __hello__")
            self.dirTree.DeleteAllItems()
            self.updateDirTree()
        dlg.Destroy()

    def new_html_file(self, event):
        dlg = wx.TextEntryDialog(self, "New File", "Enter The Name Of File")
        if dlg.ShowModal() == wx.ID_OK:
            path_of_file = dlg.GetValue()
            open(
                path.join(self.dirname, "{}.html".format(path_of_file)),
                "w+").write(temps_for_project.html)
            self.dirTree.DeleteAllItems()
            self.updateDirTree()
        dlg.Destroy()

    def new_yaml_file(self, event):
        dlg = wx.TextEntryDialog(self, "New File", "Enter The Name Of File")
        if dlg.ShowModal() == wx.ID_OK:
            path_of_file = dlg.GetValue()
            open(path.join(self.dirname, "{}.yml".format(path_of_file)),
                 "w+").write(temps_for_project.yml)
            self.dirTree.DeleteAllItems()
            self.updateDirTree()
        dlg.Destroy()

    def new_file(self, event):
        dlg = wx.TextEntryDialog(self, "New File", "Enter The Name Of File")
        if dlg.ShowModal() == wx.ID_OK:
            path_of_file = dlg.GetValue()
            open(path.join(self.dirname, path_of_file), "w+").write("")
            self.dirTree.DeleteAllItems()
            self.updateDirTree()
        dlg.Destroy()

    def install_package(self, event):
        pass

    def updateDirTree(self):
        def recursion(items, parent=None, folName=""):
            for item in items:
                if path.isdir(path.join(self.dirname, item)):
                    folder_for_dir = self.dirTree.AppendItem(parent, item)
                    self.dirTree.SetItemData(folder_for_dir, ("key", "value"))
                    recursion(
                        os.listdir(path.join(self.dirname, item)),
                        folder_for_dir, item)
                else:
                    file = self.dirTree.AppendItem(parent, item)
                    self.dirTree.SetItemData(
                        file, {"Path": path.join(self.dirname, folName, item)})

        root = self.dirTree.AddRoot(path.basename(self.dirname))
        self.dirTree.SetItemData(root, ("key", "value"))
        recursion(os.listdir(self.dirname), root)

    def updateEditorContent(self, event):
        self.filename = self.dirTree.GetItemData(
            self.dirTree.GetSelection())["Path"]
        self.editor.SetValue(open(self.filename, "r").read())
        _, self.file_ext = path.splitext(self.filename)
        del _
        if self.file_ext == ".py":
            Highlighter.python(editor=self.editor)
            self.StatusBar.SetStatusText("Python", 1)
        elif self.file_ext == ".htm" or self.file_ext == ".html":
            self.StatusBar.SetStatusText("HTML", 1)
            Highlighter.html(editor=self.editor)
        elif self.file_ext in [".yml", ".yaml"]:
            self.StatusBar.SetStatusText("YAML", 1)
            Highlighter.yaml(editor=self.editor)
        elif self.file_ext in [".css"]:
            self.StatusBar.SetStatusText("CSS", 1)
            Highlighter.css(editor=editor)
        self.notebook.SetSelection(1)

    def load_widgets(self):

        self.notebook = Notebook_Widget.FlatNotebook(self, wx.ID_ANY)

        self.notebook.SetAGWWindowStyleFlag(Notebook_Widget.FNB_NO_X_BUTTON)
        self.notebook.SetAGWWindowStyleFlag(Notebook_Widget.FNB_NO_NAV_BUTTONS)
        self.notebook.SetAGWWindowStyleFlag(Notebook_Widget.FNB_NODRAG)

        self.dirTree = wx.TreeCtrl(self.notebook, wx.ID_ANY,
                                   wx.DefaultPosition, wx.DefaultSize,
                                   wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)
        self.dirTree.Bind(wx.EVT_TREE_SEL_CHANGED, self.updateEditorContent)
        self.updateDirTree()

        self.notebook.AddPage(self.dirTree, "Project")

        self.editor = stc.StyledTextCtrl(
            self.notebook, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        self.editor.CmdKeyAssign(
            ord("+"), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.editor.CmdKeyAssign(
            ord("-"), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        self.editor.SetViewWhiteSpace(False)
        self.editor.SetMargins(50, 50)
        self.editor.SetMarginType(2, stc.STC_MARGIN_NUMBER)
        self.editor.SetMarginWidth(2, 35)
        self.editor.SetMarginLeft(10)
        # self.editor.SetMarginType(
        #     2, stc.STC_MARGIN_SYMBOL | stc.STC_MARGIN_NUMBER)
        # self.editor.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        # self.editor.SetMarginSensitive(2, True)
        # self.editor.SetMarginWidth(2, 35)
        self.editor.SetProperty("fold", "1")
        self.editor.SetProperty("tab.timmy.whinge.level", "1")
        self.editor.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        self.editor.SetEdgeColumn(78)
        self.editor.Bind(wx.EVT_KEY_UP, self.editor_keyup)
        self.editor.SetValue("import __hello__")
        self.editor.SetIndent(4)
        self.editor.SetUseHorizontalScrollBar(False)

        Highlighter.python(editor=self.editor)
        self.file_ext = ".py"

        self.notebook.AddPage(self.editor, "Editor")
        self.notebook.SetSelection(1)

    def load_settings_widgets(self, event=None):
        global config
        self.settings_win = wx.Frame(self, title="Settings")
        self.settings_editor = stc.StyledTextCtrl(
            self.settings_win, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        Highlighter.yaml(editor=self.settings_editor)
        config = yaml.load(open("./user_config.yml"))
        self.settings_editor.SetValue(open("./user_config.yml").read())
        self.settings_editor.SetViewWhiteSpace(False)
        self.settings_editor.SetMargins(50, 50)
        self.settings_editor.SetMarginType(2, stc.STC_MARGIN_NUMBER)
        self.settings_editor.SetMarginWidth(2, 35)
        self.settings_editor.SetMarginLeft(10)

    def editor_keyup(self, event=None):
        lineno = int(self.editor.GetCurrentLine()) + 1
        colno = int(self.editor.GetColumn(self.editor.GetCurrentPos()))
        self.StatusBar.SetStatusText(
            "Line {}, Column {}".format(str(lineno), str(colno)))
        if event != None:
            if event.GetKeyCode() == ord("("):
                pos = self.editor.GetCurrentPos()
                self.editor.AddText(")")
                self.editor.CharLeft()
            event.Skip()

    def new_python_project(self, event):
        projectTypeList = [
            "Simple App", "Command Line App", "Tkinter App", "WxPython App",
            "Flask Web App"
        ]
        dlg = wx.SingleChoiceDialog(
            self, "Pick The Type Of Project You Want To Create:",
            "New Project", projectTypeList)
        if dlg.ShowModal() == wx.ID_OK:
            filename = ""
            selection = dlg.GetSelection()
            selection = projectTypeList[selection]
            dlg = wx.DirDialog(
                self,
                "Select Directory For Your Project",
                self.dirname,
                style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                self.editor.SetValue("")
                self.dirname = dlg.GetPath()
                os.chdir(self.dirname)
                with open(path.join(os.getcwd(), "main.py"), "w+") as file:
                    if selection == "Simple App":
                        self.editor.SetValue(temps_for_project.simple_app)
                        file.write(self.editor.GetValue)
                    elif selection == "Command Line App":
                        self.editor.SetValue(temps_for_project.command_line)
                        file.write(self.editor.GetValue())
                    elif selection == "Tkinter App":
                        self.editor.SetValue(temps_for_project.tkinter)
                        file.write(self.editor.GetValue())
                    elif selection == "WxPython App":
                        self.editor.SetValue(temps_for_project.wx)
                        file.write(self.editor.GetValue())
                    elif selection == "Flask Web App":
                        self.editor.SetValue(temps_for_project.flask)
                        file.write(self.editor.GetValue())
                self.dirTree.DeleteAllItems()
                self.updateDirTree()
                self.notebook.SetSelection(1)
        dlg.Destroy()

    def exit_app(self, event):
        self.Close()

    def open_project(self, event=None):
        dlg = wx.DirDialog(self, "Open Project", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetPath()
            self.dirTree.DeleteAllItems()
            self.updateDirTree()
            items_in_project = os.listdir(self.dirname)
            for item in items_in_project:
                if (item == "main.py"
                        or item == "index.py") and not path.isdir(item):
                    self.editor.SetValue(
                        open(path.join(self.dirname, item), "r").read())
                    self.filename = item
                    self.file_ext = ".py"
        dlg.Destroy()

    def save_file(self, event):
        self.editor.SetValue(FormatCode(self.editor.GetValue())[0])
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
        self.editor.SetValue(FormatCode(self.editor.GetValue())[0])
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


import click


@click.command()
@click.argument("dir_or_file_path")
@click.version_option("0.0.1")
def pycode(dir_or_file_path=""):
    print(path.abspath(dir_or_file_path))
    root = wx.App()
    App(None, title="PyCode - Code Editor", dir_or_file_path=dir_or_file_path)
    root.MainLoop()


if __name__ == "__main__":
    pycode()
