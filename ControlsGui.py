import wx
from CustomWidgets import wxCrossFader

class ControlsPanel(wx.Panel):
    def __init__(self, parent, Id=wx.NewId()):
        wx.Panel.__init__(self, parent, Id)
        self.vbox = wx.RowColSizer()
        self.vbox.Add(wx.StaticText(self, wx.NewId(), "Controls List"))
        self.SetSizer(self.vbox)
    def AddControl(self, Control):
        self.vbox.Add(ControlWidget(Control))

class ControlWidget(wx.Panel):
    def __init__(self, parent, Id, Control):
        wx.Panel.__init__(self, parent, Id)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(Control.GetName()))
        hbox.Add(wxCrossfader)
