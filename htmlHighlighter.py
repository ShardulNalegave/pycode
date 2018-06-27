
import wx.stc as stc


def highlight(editor, styles, faces):

    editor.SetLexer(stc.STC_LEX_HTML)

    editor.StyleSetSpec(stc.STC_HBA_DEFAULT, "fore:" +
                        styles["default"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJA_DEFAULT, "fore:" +
                        styles["default"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJ_DEFAULT, "fore:" +
                        styles["default"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_H_DEFAULT, "fore:" +
                        styles["default"] + ",face:%(helv)s,size:%(size)d" % faces)

    editor.StyleSetSpec(stc.STC_HBA_COMMENTLINE, "fore:" +
                        styles["comment"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJA_COMMENTLINE, "fore:" +
                        styles["comment"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJA_COMMENT, "fore:" +
                        styles["comment"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJA_COMMENTDOC, "fore:" +
                        styles["comment"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJ_COMMENTLINE, "fore:" +
                        styles["comment"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJ_COMMENT, "fore:" +
                        styles["comment"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJ_COMMENTDOC, "fore:" +
                        styles["comment"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_H_COMMENT, "fore:" +
                        styles["comment"] + ",face:%(helv)s,size:%(size)d" % faces)

    editor.StyleSetSpec(stc.STC_H_DOUBLESTRING, "fore:" +
                        styles["string"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_H_SINGLESTRING, "fore:" +
                        styles["string"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJ_DOUBLESTRING, "fore:" +
                        styles["string"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJ_SINGLESTRING, "fore:" +
                        styles["string"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJA_DOUBLESTRING, "fore:" +
                        styles["string"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HJA_SINGLESTRING, "fore:" +
                        styles["string"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_HBA_STRING, "fore:" +
                        styles["string"] + ",face:%(helv)s,size:%(size)d" % faces)

    editor.StyleSetSpec(stc.STC_H_TAG, "fore:" +
                        styles["tag"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_H_TAGEND, "fore:" +
                        styles["tag"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_H_TAGUNKNOWN, "fore:" +
                        styles["tag"] + ",face:%(helv)s,size:%(size)d" % faces)

    editor.StyleSetSpec(stc.STC_H_ATTRIBUTE, "fore:" +
                        styles["attribute"] + ",face:%(helv)s,size:%(size)d" % faces)
    editor.StyleSetSpec(stc.STC_H_ATTRIBUTEUNKNOWN, "fore:" +
                        styles["attribute"] + ",face:%(helv)s,size:%(size)d" % faces)
