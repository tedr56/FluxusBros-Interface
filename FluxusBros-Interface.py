#!/usr/bin/python

from os import popen
import wx
import re
from MidiConnectionsRtMidi import Connections
from TableGui import TablePanel

APP_SIZE_X = 300
APP_SIZE_Y = 200

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, wx.Size(APP_SIZE_X, APP_SIZE_Y))
        self.InitPanels()
        self.InitMidi()
    def InitPanels(self):
        self.Table = TablePanel(self)
    def InitMidi(self):
        self.MidiConnect = Connections(self.MidiRefresh)
    def MidiRefresh(self, data):
        wx.CallAfter(self.MidiDispatch, data)
    def MidiDispatch(self, data):
        self.Table.UpdateMidi(data)
         
class MyApp(wx.App):
    def OnInit(self, *args, **kwargs):
        self.MainFrame = MyFrame(None, -1, "Midi Router/Sequencer")
        self.MainFrame.Show(True)
        self.SetTopWindow(self.MainFrame)
        return True

app = MyApp(0)
app.MainLoop()
