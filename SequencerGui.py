import math
import wx
import rtmidi
from MessageDispatch import *
from wx.lib.scrolledpanel import ScrolledPanel
from wx.lib.buttons import ThemedGenBitmapToggleButton

class SequencerPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.InitUI()
        wx.PostEvent(self, SequencerRecord(self))
        EVT_WIDGET_SEQUENCER_MESSAGE_RECORD(self, self.InitSequence)
    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SequencesWindow = SequencerWindow(self, wx.NewId())
        vbox.Add(self.SequencesWindow, proportion=1, flag=wx.EXPAND|wx.ALL)
        self.SetSizer(vbox)
    def InitSequence(self, event):
        self.SequencesWindow.InitSequence(event)
    def DelSequence(self, event):
        print("Sequencer DelSequence from Widget")
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
        self.Layout()
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
        self.Sequence = SequenceGraph(self, ID_SEQ_PANEL, event.GetValue())
        self.Sequence.SetBackgroundColour('YELLOW')
        hbox.Add(self.Sequence, proportion = 1,flag=wx.EXPAND)
        vbox_tempo = wx.BoxSizer(wx.VERTICAL)
        self.TempoBars = wx.StaticText(self, -1, str(self.Sequence.GetBarsSeq()))
        vbox_tempo.Add(self.TempoBars)
        ID_BUTTON_PLUS = wx.NewId()
        ID_BUTTON_MINUS = wx.NewId()
        ID_BUTTON_FIT = wx.NewId()
        button_plus = wx.Button(self, id=ID_BUTTON_PLUS, label=">", size=wx.Size(25,25))
        button_minus = wx.Button(self, id=ID_BUTTON_MINUS, label="<", size=wx.Size(25,25))
        button_fit = wx.Button(self, id=ID_BUTTON_FIT, label="|", size=wx.Size(25,25))
        button_plus.SetToolTipString("Plus")
        button_minus.SetToolTipString("Minus")
        button_fit.SetToolTipString("Fit")
        self.Bind(wx.EVT_BUTTON, self.TempoPlus , id=ID_BUTTON_PLUS)
        self.Bind(wx.EVT_BUTTON, self.TempoMinus, id=ID_BUTTON_MINUS)
        self.Bind(wx.EVT_BUTTON, self.TempoFit, id=ID_BUTTON_FIT)
        vbox_tempo.Add(button_plus)
        vbox_tempo.Add(button_minus)
        vbox_tempo.Add(button_fit)
        hbox.Add(vbox_tempo, proportion = 0,flag=wx.EXPAND)
        self.SetSizer(hbox)
        wx.PostEvent(self, MessageGet(event.GetEventObject(), Source=self))
        EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(self, self.Sequence.DelSequence)
    def GetValue(self):
        return self.Sequence.GetValue()
    def GetRecording(self):
        return self.Sequence.GetRecording()
    def GetNumSequence(self):
        return self.NumSequence
    def SetNumSequence(self, num):
        self.NumSequence = num
    def TempoPlus(self, event):
        SeqRec = self.Sequence.GetBarsSeq()
        self.Sequence.SetBarsReq(SeqRec * 2.0)
        self.TempoBars.SetLabel(str(self.Sequence.GetBarsSeq()))
    def TempoMinus(self, event):
        SeqRec = self.Sequence.GetBarsSeq()
        self.Sequence.SetBarsReq(SeqRec / 2.0)
        self.TempoBars.SetLabel(str(self.Sequence.GetBarsSeq()))
    def TempoFit(self, event):
        self.Sequence.SetBarsReqFit()
    def Lock(self, evnt):
        if self.Sequence.isLocked():
            self.Sequence.UnLock()
        else:
            self.Sequence.Lock()
    def Pause(self, event):
        #~ print("Pause")
        #~ if self.Paused:
            #~ self.Paused = False
        #~ else:
            #~ self.Paused = True
        #~ print self.Paused
        if self.Sequence.isPaused():
            self.Sequence.UnPause()
        else:
            self.Sequence.Pause()
    def Clean(self, event):
        self.Sequence.Clean()
    def DelSequence(self, e):
        #~ print("SeqPanel Del")
        for event in self.SeqEvent:
            wx.PostEvent(self.parent, MessageUnRecord(self, self.GetId(), event.GetType(), event.GetAddress(), event.GetOption()))
        
        wx.CallAfter(self.DestroyChildren)
        wx.CallAfter(self.Destroy)
        #~ wx.CallAfter(self.parent.DelSequence,self)
        self.parent.DelSequence(self)
        #wx.CallAfter(self.DestroyChildren)
        
    def UnRecordMessage(self):
        wx.PostEvent(self.parent, MessageSequencerUnRecord(self))
    def AddControl(self, event):
        wx.PostEvent(self.parent, MessageRecord(self, self.GetId(), event.GetType(), event.GetAddress(), event.GetOption()))
        self.SeqEvent.append(event)
    def Update(self, event):
        self.Sequence.Update(event)
            
class SequenceGraph(wx.Panel):
    def __init__(self, parent, Id, Value):
        wx.Panel.__init__(self, parent, Id)
        self.parent = parent
        self.pDC = wx.PseudoDC()
        ## Events
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        EVT_WIDGET_UPDATE(self, self.ClockUpdate)
        EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(self, self.DelSequence)
        self.Bind(wx.EVT_SIZE , self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        ## Sequences Stocking Variables
        first_seq = {'Time': 0 , 'Value': Value, 'Id' : wx.NewId(), 'Color' : 'BLUE'}
        self.first_seq = first_seq
        second_seq= {'Time': 69 , 'Value': 69, 'Id' : wx.NewId(), 'Color' : 'BLUE'}
        self.Seq = []               #Store Sequence Messages + Time + ID + Color
        self.SeqN = 1               #Store Sequence Cursor
        self.SeqTime = None         #Store Time ID
        ## Time Parsing Variables
        self.Time = 0               #Store Current Time Tick
        self.TimeLock = False       #Store Lock if Seq already recorded on Tick Time
        self.TimeSum = 0            #Store the Time past in dTime
        self.TimeSumDx = 0          #Store the Time past to restore on reset clock
        self.Bars = 1.0             #Store Showed Bars Number
        self.BarsSeq = self.Bars    #Store Sequenced Bars Number
        self.BeatPerBar = 4
        ## Sequencer Config Variables
        self.ClockEvts = True       #Store START CONTINUE STOP Clock Events
        self.ExtFirstUpdate = True  #Store if First Update set the First Seq
        self.Locked = False
        self.SubLocked = False
        self.Record = False
        self.Paused = False
        ## Display Variables
        self.dTime = None
        self.SizeX = None
        self.SizeY = None
        self.OnSize(None)
        ## Init Sequencer
        self.Seq.append(first_seq)
        #self.Seq.append(second_seq)
        self.FakeSeq = {'Time': (self.Bars * self.BeatPerBar * 25) , 'Value': Value, 'Id' : wx.NewId(), 'Color' : 'BLUE'}
        self.NextSeq = self.FakeSeq
        ## Record Sequencer Inputs Events
        self.SetInput()
        if self.ClockEvts:
            self.SetInput(address=252)
            self.SetInput(address=251)
            self.SetInput(address=250)
        ## Store the Value for Player change recovery
        self.Value = Value
        wx.CallAfter(self.InitDraw)
    def InitDraw(self):
        self.pDC.BeginDrawing()
        self.InitClockDraw()
        self.pDC.EndDrawing()
    def InitClockDraw(self):
        self.SeqTime = wx.NewId()
        self.pDC.SetId(self.SeqTime)
        pen = wx.Pen('GREEN')
        self.pDC.SetPen(pen)
        TimeX = (self.Time * self.BeatPerBar * self.dTime)
        self.pDC.DrawLine(TimeX, 0, TimeX, self.SizeY)
        TimeBound = wx.Rect(TimeX , 1 , 1 , self.SizeY)
        TimeBound.Inflate(pen.GetWidth(),pen.GetWidth())
        self.pDC.SetIdBounds(self.SeqTime, TimeBound)
    def OnSize(self, event):
        w,h = self.GetSize()
        #~ print("OnSize : %i %i" % (w,h))
        self.dTime = w / (self.Bars * self.BeatPerBar * 24.0)
        #~ print("debug OnSize")
        #~ print w
        #~ print (self.Bars * self.BeatPerBar * 24.0)
        #~ print self.dTime
        self.SizeX = w
        self.SizeY = h
    def SetInput(self, input_type='Clock', address=248, option = None):
        wx.PostEvent(self, MessageRecord(self, self.Id, input_type, address, option))
    def UnSetInput(self, input_type='Clock', address=248, option = None):
        wx.PostEvent(self, MessageUnRecord(self, self.Id, input_type, address, option))    
    def OnMiddleDown(self, event):
        self.parent.UnRecordMessage()
        self.DelSequence(event)
    def DelSequence(self, event):
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
        if not self.Locked and not self.SubLocked and not self.TimeLock:
            #~ print("Seq Widget Update")
            #~ print self.Time
            #~ self.printSeq()
            #~ print self.SeqN
            Value = event.GetValue()
            Type = event.GetType()
            if not Type == "note" and not Value == 0:
                self.Record = True
            self.TimeLock = True
            UpdatedSeq = {'Time' : self.Time, 'Value' : Value, 'Id' : wx.NewId(), 'Color' : 'BLUE'}
            self.Seq.insert(self.SeqN, UpdatedSeq)
            if self.SeqN == 1:
                if self.ExtFirstUpdate:
                    self.Seq[0]['Value'] = Value
            if self.Time == self.Seq[self.SeqN - 1]['Time']:
                print("pop")
                self.Seq.pop(self.SeqN - 1)
            else:
                self.SeqN += 1
        #~ else:
            #~ print("Debug Sequencer Control Update")
            #~ print self.Locked
            #~ print self.SubLocked
            #~ print self.TimeLock
    def ClockUpdate(self, event):
        if event.GetAddress() == 248:
            self.Time += 1
            self.TimeLock = False
            if not self.SubLocked:
                if self.Time > (self.BarsSeq * self.BeatPerBar * 24):
                    self.SubLocked = True
            if self.Time > (self.Bars * self.BeatPerBar * 24):
                self.ClockReset()
            else:
                if (self.Time * self.dTime) >= math.floor(self.TimeSum) + 1:
                    Dx = (self.Time * self.dTime) - self.TimeSum
                    Dxi = math.floor(Dx) 
                    self.TimeSum = (self.Time * self.dTime)
                    self.ClockDraw(math.floor(self.TimeSum) - self.TimeSumDx)
                    self.TimeSumDx = math.floor(self.TimeSum)

            if self.Time == self.NextSeq['Time']:
                if self.Record:
                    self.Seq.pop(self.SeqN)
                    if self.SeqN >= len(self.Seq):
                        self.NextSeq = self.FakeSeq
                    else:
                        self.NextSeq = self.Seq[self.SeqN]
                    #~ print("pop record")
                    #~ self.Seq[self.SeqN]
                else:
                    self.Value = self.NextSeq['Value']
                    wx.PostEvent(self, InternalMessage(self.parent, self.NextSeq['Value']))
                    self.SeqN += 1
                    if self.SeqN >= len(self.Seq):
                        self.NextSeq = self.FakeSeq
                    else:
                        self.NextSeq = self.Seq[self.SeqN]
                #~ print self.SeqN
                #~ print self.NextSeq
            
        elif event.GetAddress() == 252:
            self.UnSetInput()
        elif event.GetAddress() == 250:
            self.ClockReset()
            self.SetInput()
        elif event.GetAddress() == 251:
            self.SetInput()
    def printSeq(self):
        print("")
        for i in self.Seq:
            print i
    def ClockReset(self):
        self.NextSeq = self.Seq[0]
        self.Record = False
        self.SubLocked = False
        self.TimeLock = False
        self.Time = 0
        self.SeqN = 0
        self.ClockDraw(math.floor(self.TimeSumDx) * -1)
        self.TimeSum = 0
        self.TimeSumDx = 0
    def ClockDraw(self, dTime):
        #~ w,h = self.GetSize()
        self.pDC.TranslateId(self.SeqTime, dTime, 0)
        self.Refresh()
    def isPaused(self):
        return self.Paused
    def isLocked(self):
        return self.Locked
    def Pause(self):
        self.Paused = True
        self.UnSetInput()
    def UnPause(self):
        self.Paused = False
        self.SetInput()
    def Lock(self):
        self.Locked = True
    def UnLock(self):
        self.Locked = False
    def Clean(self):
        self.Seq = []
        self.SeqN = 1
        self.Seq.append(self.first_seq)
    def GetBarsSeq(self):
        if self.BarsSeq == math.floor(self.BarsSeq):
            return int(self.BarsSeq)
        else:
            return self.BarsSeq
    def SetBarsReq(self, bars):
        #~ print bars
        #~ print self.Bars
        #~ print self.BarsSeq
        if bars >= 0.25:
            if bars > self.Bars:
                #~ print("SupBar")
                self.ClockDraw(self.TimeSumDx * -1)
                self.BarsSeq = bars
                self.Bars = bars
                self.FakeSeq['Time'] = (self.Bars * self.BeatPerBar * 25)
                self.OnSize(None)
                Dx = (self.Time * self.dTime)
                Dxi = math.floor(Dx)
                self.TimeSum = Dx
                self.TimeSumDx = Dxi
                self.ClockDraw(self.TimeSumDx)
            else:
                self.ClockDraw(self.TimeSumDx * -1)
                self.BarsSeq = bars
                self.OnSize(None)
                self.ClockDraw(self.TimeSumDx)
    def SetBarsReqFit(self):
        self.ClockDraw(self.TimeSumDx * -1)
        
        self.Bars = self.BarsSeq
        self.FakeSeq['Time'] = (self.Bars * self.BeatPerBar * 25)
        self.OnSize(None)
        if self.Time >= (self.Bars * self.BeatPerBar * 24):
            #~ print("SupTicks")
            #~ print self.Time
            #~ print self.Time % (self.Bars * self.BeatPerBar * 24)
            self.Time = self.Time % (self.Bars * self.BeatPerBar * 24)
            Dx = (self.Time * self.dTime)
            Dxi = math.floor(Dx)
            self.TimeSum = Dx
            self.TimeSumDx = Dxi
        self.ClockDraw(self.TimeSumDx)
        #~ self.SetClockReq()
        #~ self.InitDraw()
    def SetClockReq(self):
        self.ClockDraw(self.Time * 24.0)
        self.OnSize(None)
        self.ClockDraw(self.dTime)
    def GetValue(self):
        return self.Value
    def GetRecording(self):
        return True
