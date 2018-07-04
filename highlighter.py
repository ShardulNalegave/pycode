
import wx
import json
import pyHighlight
import htmlHighlighter
import yamlHighlighter
import yaml

style_config = yaml.load(open("./user_config.yml"))["styles"]

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
    pyHighlight.highlight(editor, style_config["python"], faces)


def html(editor):
    htmlHighlighter.highlight(editor, style_config["html"], faces)


def yaml(editor):
    yamlHighlighter.highlight(editor, style_config["yaml"], faces)
