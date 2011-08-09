import wx
import rtmidi
from MessageDispatch import *
from wx.lib.scrolledpanel import ScrolledPanel
from wx.lib.buttons import ThemedGenBitmapToggleButton

class SequencerPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.InitUI()
    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SequencesWindow = SequencerWindow(self, wx.NewId())
        vbox.Add(self.SequencesWindow, proportion=1, flag=wx.EXPAND|wx.ALL)
        self.SetSizer(vbox)
    def InitSequence(self, event):
        self.SequencesWindow.InitSequence(event)

class SequencerWindow(ScrolledPanel):
    def __init__(self, *args, **kwargs):
        ScrolledPanel.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.SetupScrolling(scroll_x=False, scroll_y=True)
        self.SequenceSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.SequenceSizer)
    def InitSequence(self, event):
        NewSequence = SequencePanel(self, wx.NewId(), event)
        self.SequenceSizer.Add(NewSequence, proportion=0, flag=wx.EXPAND|wx.BOTTOM, border=2)
        self.FitInside()
    def DelSequence(self, item):
        self.SequenceSizer.Remove(item)
        self.Layout()

class SequencePanel(wx.Panel):
    def __init__(self, parent, Id, event):
        wx.Panel.__init__(self, parent, Id)
        self.parent = parent
        self.SeqEvent = []
        self.Paused = False
        EVT_WIDGET_MESSAGE(self, self.AddControl)
        EVT_WIDGET_UPDATE(self, self.Update)
        self.InitSequencer(event)
    def InitSequencer(self, event):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        pause_bmp = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_OTHER, (16, 16))
        clean_bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_OTHER, (16, 16))
        del_bmp   = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, (16, 16))
        ID_BUTTON_QUIT  = wx.NewId()
        ID_BUTTON_PAUSE = wx.NewId()
        ID_BUTTON_CLEAN = wx.NewId()
        button_pause = ThemedGenBitmapToggleButton(self, ID_BUTTON_PAUSE, pause_bmp)
        button_clean = wx.BitmapButton(self, ID_BUTTON_CLEAN, clean_bmp)
        button_del   = wx.BitmapButton(self, ID_BUTTON_QUIT, del_bmp)
        self.Bind(wx.EVT_BUTTON, self.Pause, id=ID_BUTTON_PAUSE)
        self.Bind(wx.EVT_BUTTON, self.Clean, id=ID_BUTTON_CLEAN)
        self.Bind(wx.EVT_BUTTON, self.DelSequence, id=ID_BUTTON_QUIT)
        vbox.Add(button_pause, proportion = 0, flag=wx.EXPAND)
        vbox.Add(button_clean, proportion = 0, flag=wx.EXPAND)
        vbox.Add(button_del, proportion = 0, flag=wx.EXPAND)
        hbox.Add(vbox, proportion = 0,flag=wx.EXPAND)
        ID_SEQ_PANEL = wx.NewId()
        self.Sequence = SequenceGraph(self, ID_SEQ_PANEL)
        self.Sequence.SetBackgroundColour('YELLOW')
        hbox.Add(self.Sequence, proportion = 1,flag=wx.EXPAND)
        self.SetSizer(hbox)
        wx.PostEvent(self, MessageGet(event.GetEventObject(), Source=self))
        
    def GetNumSequence(self):
        return self.NumSequence
    def SetNumSequence(self, num):
        self.NumSequence = num
    def Pause(self, event):
        print("Pause")
        if self.Paused:
            self.Paused = False
        else:
            self.Paused = True
        print self.Paused
    def Clean(self, event):
        print("Clean")
    def DelSequence(self, event):
        for event in self.SeqEvent:
            wx.PostEvent(self.parent, MessageUnRecord(self, self.GetId(), event.GetType(), event.GetAddress(), event.GetOption()))
        wx.CallAfter(self.DestroyChildren)
        self.parent.DelSequence(self)
        wx.CallAfter(self.Destroy)
    def AddControl(self, event):
        wx.PostEvent(self.parent, MessageRecord(self, self.GetId(), event.GetType(), event.GetAddress(), event.GetOption()))
        self.SeqEvent.append(event)
    def Update(self, event):
        if not self.Paused:
            self.Sequence.Update(event)
class SequenceGraph(wx.Panel):
    def __init__(self, parent, Id):
        wx.Panel.__init__(self, parent, Id)
        self.parent = parent
        self.pDC = wx.PseudoDC()
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        
    def OnMiddleDown(self, event):
        self.parent.DelSequence(event)
    def OnPaint(self, event):
        w, h = self.GetSize()
        dc = wx.BufferedPaintDC(self)
        self.PrepareDC(dc)
        bg = wx.Brush(self.GetBackgroundColour())
        dc.SetBackground(bg)
        dc.Clear()
        self.pDC.DrawToDC(dc)
    def DrawGraph(self):
        print("DrawGraph")
        
    def Update(self, event):
        GraphSize = self.GetSize()
        print("Graph Update")
