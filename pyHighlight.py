
import wx.stc as stc
import keyword


def highlight(editor, python_styles, faces):

    editor.SetLexer(stc.STC_LEX_PYTHON)
    editor.SetKeyWords(0, " ".join(keyword.kwlist))

    # Python styles
    # Default
    editor.StyleSetSpec(stc.STC_P_DEFAULT,
                        "fore:" + python_styles["default"] + ",face:%(helv)s,size:%(size)d" % faces)
    # Comments
    editor.StyleSetSpec(stc.STC_P_COMMENTLINE,
                        "fore:" + python_styles["comment-line"] + ",face:%(helv)s,size:%(size)d" % faces)
    # Number
    editor.StyleSetSpec(stc.STC_P_NUMBER,
                        "fore:" + python_styles["number"] + ",face:%(helv)s,size:%(size)d" % faces)
    # String
    editor.StyleSetSpec(stc.STC_P_STRING,
                        "fore:" + python_styles["string"] + ",face:%(helv)s,size:%(size)d" % faces)
    # Single quoted string
    editor.StyleSetSpec(stc.STC_P_CHARACTER,
                        "fore:" + python_styles["string"] + ",face:%(helv)s,size:%(size)d" % faces)
    # Keyword
    editor.StyleSetSpec(
        stc.STC_P_WORD, "fore:" + python_styles["keyword"] + ",face:%(helv)s,size:%(size)d" % faces)

    # Decorators
    editor.StyleSetSpec(
        stc.STC_P_DECORATOR, "fore:" + python_styles["decorator"] + ",face:%(helv)s,size:%(size)d" % faces)

    # Triple quotes
    editor.StyleSetSpec(stc.STC_P_TRIPLE,
                        "fore:" + python_styles["block_string"] + ",face:%(helv)s,size:%(size)d" % faces)
    # Triple double quotes
    editor.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE,
                        "fore:" + python_styles["block_string"] + ",face:%(helv)s,size:%(size)d" % faces)
    # Class name definition
    editor.StyleSetSpec(stc.STC_P_CLASSNAME,
                        "fore:" + python_styles["class_and_function_names"] + ",face:%(helv)s,size:%(size)d" % faces)
    # Function or method name definition
    editor.StyleSetSpec(stc.STC_P_DEFNAME,
                        "fore:" + python_styles["class_and_function_names"] + ",face:%(helv)s,size:%(size)d" % faces)
    # Operators
    editor.StyleSetSpec(
        stc.STC_P_OPERATOR, "fore:" + python_styles["operators"] + ",face:%(helv)s,size:%(size)d" % faces)
    # Identifiers
    editor.StyleSetSpec(stc.STC_P_IDENTIFIER,
                        "fore:" + python_styles["identifiers"] + ",face:%(helv)s,size:%(size)d" % faces)
    # Comment-blocks
    editor.StyleSetSpec(stc.STC_P_COMMENTBLOCK,
                        "fore:" + python_styles["block_comment"] + ",face:%(helv)s,size:%(size)d" % faces)
    # End of line where string is not closed
    editor.StyleSetSpec(
        stc.STC_P_STRINGEOL, "fore:" + python_styles["EOL_when_string_not_closed"] + ",face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)
