import wx
import rtmidi

class SequencerPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        event_type_static = wx.StaticText(self, label='Event Type')
        hbox1.Add(event_type_static , proportion=1)
        self.event_type = wx.TextCtrl(self)
        hbox1.Add(self.event_type , proportion=1)
        vbox.Add(hbox1)
        self.inputlist = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        vbox.Add(self.inputlist, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)

    def UpdateMidi(self, data):
        self.inputlist.AppendText(data)

