
simple_app = """

if __name__ == "__main__":
    print("Hello, World!")

"""
flask = """

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)

"""
command_line = """

from sys import argv

def greet(name):
    print("Hello, {}!".format(name))

if __name__ == "__main__":
    if len(argv) == 1:
        print("Usage: python[x[.y]] main.py")
    else:
        greet(argv[1])

"""
wx = """

import wx

app = wx.app

frm = wx.Frame(None)
frm.Show()

app.MainLoop()

"""
tkinter = """

import tkinter

app = tkinter.Tk()

label = tkinter.Label(app, text="Hello, World!")
label.pack()

app.mainloop()

"""