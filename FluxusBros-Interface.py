#!/usr/bin/python

from os import popen
import wx
import re
import rtmidi
from MidiConnectionsRtMidi import Connections
from MediaGui import MediaPanel
from TableGui import TablePanel
from SequencerGui import SequencerPanel

APP_SIZE_X = 900
APP_SIZE_Y = 400

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, wx.Size(APP_SIZE_X, APP_SIZE_Y))
        self.InputCC    = []
        self.InputNote  = []
        self.InputOSC   = []
        self.InputSysEx = []
        self.InputClock = []
        self.InitMidi()
        self.InitPanels()

    def InitPanels(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.Media = MediaPanel(self)
        self.Table = TablePanel(self)
        self.Sequencer = SequencerPanel(self)
        hbox.Add(self.Media, proportion = 0, flag=wx.EXPAND)
        hbox.Add(self.Table, proportion = 1, flag=wx.EXPAND)
        hbox.Add(self.Sequencer, proportion = 1, flag=wx.EXPAND)
        vbox.Add(hbox, proportion=-1, flag=wx.EXPAND)
        self.SetSizer(vbox)
    def InitMidi(self):
        self.MidiConnect = Connections(self.MidiInputRefresh)
    def MidiInputRefresh(self, data):
        wx.CallAfter(self.MidiInDispatch, data)
    def MidiOutputRefresh(self, data):
        wx.CallAfter(self.MidiOutDispatch, data)
    def MidiOutDispatch(self, data):
        print data
        for m in data:
            self.MidiConnect.sendMessage(m)
    def MidiInDispatch(self, MidiData):
        if MidiData.isController():
            for C in self.InputCC:
                if MidiData.isForChannel(C[0][0]):
                    if MidiData.getControllerNumber() == C[0][1]:
                        C[1](input_type='cc', address=C[0], value=MidiData.getControllerValue())
        elif MidiData.isNoteOnOrOff():
            for N in self.InputNote:
                if MidiData.isForChannel(N[0][0]):
                    if MidiData.getNoteNumber() == N[0][1]:
                        #print
                        if MidiData.isNoteOn():
                            N[1](input_type='note', address=N[0], value=MidiData.getControllerValue())
                        else:
                            N[1](input_type='note', address=N[0], value=0)
        elif MidiData.isSysEx():
            for S in self.InputSysEx:
                print("SysEx")
                print S
                S[1](MidiData.getSysExData())
        elif self.IsClockEvent(MidiData):
            for C in self.InputClock:
                C[1](ord(MidiData.getRawData()[0]))
    def IsClockEvent(self, data):
        #Clock Raw Data
        #clock tick     = 248(10) F8(16)
        #clock stop     = 252(10) FC(16)
        #clock start    = 250(10) FA(16)
        #clock continue = 251(10) FB(16)
        decoded_data = ord(data.getRawData()[0])
        if decoded_data in [248,250,251,252]:
            return decoded_data
        else:
            return False
    def SetControls(self, Callback, Inputs):
        for CCin in Inputs['CC']:
            self.InputCC.append([CCin, Callback])
        for Notein in Inputs['Note']:
            self.InputNote.append([Notein, Callback])
        for OSCin in Inputs['OSC']:
            self.InputOSC.append([OSCin, Callback])
        for SysExin in Inputs['SysEx']:
            self.InputSysEx.append([SysExin, Callback])
        for Clockin in Inputs['Clock']:
            self.InputClock.append([Clockin, Callback])

    def SetPlayer(self, event):
        print("New Player : %s" % event.GetEventObject().GetValue())
         
class MyApp(wx.App):
    def OnInit(self, *args, **kwargs):
        self.MainFrame = MyFrame(None, -1, "FluxusBros Interface")
        self.MainFrame.Show(True)
        self.SetTopWindow(self.MainFrame)
        return True

app = MyApp(0)
app.MainLoop()
