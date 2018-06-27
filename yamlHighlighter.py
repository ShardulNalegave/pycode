
import wx.stc as stc


def highlight(editor, styles, faces):

    editor.SetLexer(stc.STC_LEX_YAML)

    editor.StyleSetSpec(stc.STC_YAML_DEFAULT, "fore:" +
                        styles["default"] + ",face:%(helv)s,size:%(size)d" % faces)

    editor.StyleSetSpec(stc.STC_YAML_COMMENT, "fore:" +
                        styles["comment"] + ",face:%(helv)s,size:%(size)d" % faces)

    editor.StyleSetSpec(stc.STC_YAML_ERROR, "fore:" +
                        styles["error"] + ",face:%(helv)s,size:%(size)d" % faces)

    editor.StyleSetSpec(stc.STC_YAML_IDENTIFIER, "fore:" +
                        styles["identifier"] + ",face:%(helv)s,size:%(size)d" % faces)

    editor.StyleSetSpec(stc.STC_YAML_NUMBER, "fore:" +
                        styles["number"] + ",face:%(helv)s,size:%(size)d" % faces)
