import wx
from wx import xrc
import rtmidi
from CustomWidgets import wxFader
from CustomWidgets import wxKnob
from CustomWidgets import wxPiano
from CustomWidgetsXRC import wxFaderCtrlXmlHandler
from wx.lib.agw.knobctrl import *

class TablePanel(wx.Panel):
    def __init__(self, parent, player):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        self.player = player
        print("debug")
        print player
        xrc_path = player + '.xrc'
        xrc_path = 'test.xrc'
        
        self.res = xrc.XmlResource(xrc_path)
        self.res.InsertHandler(wxFaderCtrlXmlHandler())
        self.res.LoadPanel(self, 'TablePanel')
