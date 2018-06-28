
import wx
import json
import pyHighlight
import htmlHighlighter
import yamlHighlighter

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


def python(editor):

    styles = json.loads(open("./user_config.json",
                             "r").read())["styles"]["python"]
    pyHighlight.highlight(editor, styles, faces)


def html(editor):

    styles = json.loads(open("./user_config.json",
                             "r").read())["styles"]["html"]
    htmlHighlighter.highlight(editor, styles, faces)


def yaml(editor):

    styles = json.loads(open("./user_config.json",
                             "r").read())["styles"]["yaml"]
    yamlHighlighter.highlight(editor, styles, faces)
