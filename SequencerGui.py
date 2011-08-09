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
        lock_bmp  = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, (16, 16))
        pause_bmp = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_OTHER, (16, 16))
        clean_bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_OTHER, (16, 16))
        ID_BUTTON_LOCK = wx.NewId()
        ID_BUTTON_PAUSE = wx.NewId()
        ID_BUTTON_CLEAN = wx.NewId()
        button_lock  = ThemedGenBitmapToggleButton(self, ID_BUTTON_LOCK, lock_bmp)
        button_pause = ThemedGenBitmapToggleButton(self, ID_BUTTON_PAUSE, pause_bmp)
        button_clean = wx.BitmapButton(self, ID_BUTTON_CLEAN, clean_bmp)
        button_lock.SetToolTipString("Lock")
        button_pause.SetToolTipString("Pause")
        button_clean.SetToolTipString("Clean")
        self.Bind(wx.EVT_BUTTON, self.Lock , id=ID_BUTTON_LOCK)
        self.Bind(wx.EVT_BUTTON, self.Pause, id=ID_BUTTON_PAUSE)
        self.Bind(wx.EVT_BUTTON, self.Clean, id=ID_BUTTON_CLEAN)
        vbox.Add(button_lock , proportion = 0, flag=wx.EXPAND)
        vbox.Add(button_pause, proportion = 0, flag=wx.EXPAND)
        vbox.Add(button_clean, proportion = 0, flag=wx.EXPAND)
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
    def Lock(self, evnt):
        print("Lock")
    def Pause(self, event):
        print("Pause")
        if self.Paused:
            self.Paused = False
        else:
            self.Paused = True
        print self.Paused
    def Clean(self, event):
        print("Clean")
    def DelSequence(self, e):
        print("SeqPanel Del")
        for event in self.SeqEvent:
            wx.PostEvent(self.parent, MessageUnRecord(self, self.GetId(), event.GetType(), event.GetAddress(), event.GetOption()))
        wx.CallAfter(self.DestroyChildren)
        wx.CallAfter(self.Destroy)
        #~ wx.CallAfter(self.parent.DelSequence,self)
        self.parent.DelSequence(self)
        #wx.CallAfter(self.DestroyChildren)
        
        
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
        EVT_WIDGET_UPDATE(self, self.ClockUpdate)
        self.Bind(wx.EVT_SIZE , self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Seq = []           #Store Sequence Messages + Time + ID + Color
        self.SeqTime = None     #Store Time ID
        self.Time = 0           #Store Current Time Tick    
        self.Bars = 4           #Store Showed Bars Number
        self.BarsSeq = 2        #Store Sequenced Bars Number
        self.ClockEvts = True    #Store START CONTINUE STOP Clock Events
        self.dTime = None
        self.SizeX = None
        self.SizeY = None
        self.OnSize(None)
        self.SetInput()
        if self.ClockEvts:
            self.SetInput(address=252)
            self.SetInput(address=250)
        wx.CallAfter(self.InitDraw)
    def InitDraw(self):
        self.pDC.BeginDrawing()
        self.InitClockDraw()
        self.pDC.EndDrawing()
        print("pDC len")
        print self.pDC.GetLen()
    def InitClockDraw(self):
        self.SeqTime = wx.NewId()
        self.pDC.SetId(self.SeqTime)
        pen = wx.Pen('GREEN')
        self.pDC.SetPen(pen)
        TimeX = (self.Time * self.dTime)
        self.pDC.DrawLine(TimeX, 0, TimeX, self.SizeY)
        TimeBound = wx.Rect(TimeX , 1 , 1 , self.SizeY)
        TimeBound.Inflate(pen.GetWidth(),pen.GetWidth())
        self.pDC.SetIdBounds(self.SeqTime, TimeBound)
    def OnSize(self, event):
        w,h = self.GetSize()
        print("OnSize : %i %i" % (w,h))
        self.dTime = w / (self.Bars * 24)
        self.SizeX = w
        self.SizeY = h
    def SetInput(self, input_type='Clock', address=248, option = None):
        wx.PostEvent(self, MessageRecord(self, self.Id, input_type, address, option))
    def UnSetInput(self, input_type='Clock', address=248, option = None):
        wx.PostEvent(self, MessageUnRecord(self, self.Id, input_type, address, option))    
    def OnMiddleDown(self, event):
        self.UnSetInput()
        if self.ClockEvts:
            self.UnSetInput(address=252)
            self.UnSetInput(address=250)
        self.DestroyChildren()
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
    def ClockUpdate(self, event):
        if event.GetAddress() == 248:
            self.Time += 1
            if self.Time > (self.Bars * 24):
                self.Time = 0
                self.ClockDraw(self.dTime * self.Bars * 24 * -1)
            else:
                self.ClockDraw(self.dTime)
            #~ print self.Time
        elif event.GetAddress() == 252:
            print("Clock Stop")
            self.UnSetInput()
        elif event.GetAddress() == 250:
            print("Clock Start")
            self.ClockDraw(self.Time * self.dTime * -1)
            self.Time = 0
            self.SetInput()
    def ClockDraw(self, dTime):
        w,h = self.GetSize()
        #~ print("")
        #~ print w
        #~ print w / (self.Bars * 24)
        #~ print (self.Bars * 24)
        #~ print dTime * (self.Bars * 24)
        #~ print dTime
        self.pDC.TranslateId(self.SeqTime, dTime, 0)
        self.Refresh()
        
