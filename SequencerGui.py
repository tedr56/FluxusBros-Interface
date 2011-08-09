import wx
import rtmidi
from MessageDispatch import *
from wx.lib.scrolledpanel import ScrolledPanel

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
        self.Sequences = []
    def InitSequence(self, event):
        NewSequence = SequencePanel(self, len(self.Sequences), event)
        self.SequenceSizer.Add(NewSequence, proportion=0, flag=wx.EXPAND|wx.BOTTOM, border=2)
        #~ self.Sequences.append(NewSequence)
        self.FitInside()
    def DelSequence(self, item):
        #~ self.Sequences.pop(sequence)
        #~ for s in range(sequence, len(self.Sequences)):
            #~ self.Sequences[s].SetNumSequence(s.GetNumSequence() - 1)
        print("ScrolledPanel DelSequence")
        print item
        self.SequenceSizer.Remove(item)
        print item
        self.Layout()
        print("DelSequence End")
        #~ wx.CallAfter(self.SequenceSizer.Remove,item)
        #~ wx.CallAfter(self.Layout)
        #~ self.Sequence[sequence].Destroy()
        #~ -1 () a chaque sequences apres sequence

class SequencePanel(wx.Panel):
    def __init__(self, parent, num, event):
        wx.Panel.__init__(self, parent, wx.NewId())
        self.parent = parent
        self.NumSeq = num
        self.SeqEvent = []
        self.Paused = False
        EVT_WIDGET_MESSAGE(self, self.AddControl)
        EVT_WIDGET_UPDATE(self, self.Update)
        self.InitSequencer(event)
    def InitSequencer(self, event):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        pause_bmp = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_OTHER, (16, 16))
        del_bmp   = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, (16, 16))
        ID_BUTTON_QUIT = wx.NewId()
        ID_BUTTON_PAUSE = wx.NewId()
        button_pause = wx.BitmapButton(self, ID_BUTTON_PAUSE, pause_bmp)
        button_del   = wx.BitmapButton(self, ID_BUTTON_QUIT, del_bmp)
        self.Bind(wx.EVT_BUTTON, self.Pause, id=ID_BUTTON_PAUSE)
        self.Bind(wx.EVT_BUTTON, self.DelSequence, id=ID_BUTTON_QUIT)
        vbox.Add(button_pause, proportion = 0, flag=wx.EXPAND)
        vbox.Add(button_del, proportion = 0, flag=wx.EXPAND)
        hbox.Add(vbox, proportion = 0,flag=wx.EXPAND)
        self.Sequence = wx.Panel(self, -1)
        self.Sequence.SetBackgroundColour('YELLOW')
        hbox.Add(self.Sequence, proportion = 1,flag=wx.EXPAND)
        self.SetSizer(hbox)
        wx.PostEvent(self, MessageGet(event.GetEventObject(), Source=self))
    def GetNumSequence(self):
        return self.NumSequence
    def SetNumSequence(self, num):
        self.NumSequence = num
    def Pause(self, event):
        if self.Pause:
            self.Pause = False
        else:
            self.Pause = True
    def DelSequence(self, event):
        for event in self.SeqEvent:
            wx.PostEvent(self.parent, MessageUnRecord(self, self.GetId(), event.GetType(), event.GetAddress(), event.GetOption()))
        self.DestroyChildren()
        self.parent.DelSequence(self)
        wx.CallAfter(self.Destroy)
        
    def AddControl(self, event):
        wx.PostEvent(self.parent, MessageRecord(self, self.GetId(), event.GetType(), event.GetAddress(), event.GetOption()))
        self.SeqEvent.append(event)
    def Update(self, event):
        if not self.Paused:
            print("Sequencer Widget Update")
            print event.GetType()
            print event.GetAddress()
            print event.GetValue()
            
