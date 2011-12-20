# -*- coding: utf-8 -*-

import wx
import wx.lib.buttons

import SpeedMeter as SM
from math import pi, sqrt

# This Is For Latin/Greek Symbols I Used In The Demo Only
wx.SetDefaultPyEncoding('iso8859-1')

#----------------------------------------------------------------------
# Get Some Icon/Data
#----------------------------------------------------------------------

def GetMondrianData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82' 

def GetMondrianBitmap():
    return wx.BitmapFromImage(GetMondrianImage())

def GetMondrianImage():
    import cStringIO
    stream = cStringIO.StringIO(GetMondrianData())
    return wx.ImageFromStream(stream)

def GetMondrianIcon():
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon


#----------------------------------------------------------------------
# Beginning Of SPEEDMETER Demo wxPython Code
#----------------------------------------------------------------------

class SpeedMeterDemo(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "SpeedMeter Demo ;-)",
                         wx.DefaultPosition,
                         size=(400,400),
                         style=wx.DEFAULT_FRAME_STYLE |
                         wx.NO_FULL_REPAINT_ON_RESIZE)


        self.SetIcon(GetMondrianIcon())
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)

        self.statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("wxPython SpeedControl Demo, Andrea Gavana @ 25 Sep 2005"),
                            ("Welcome To wxPython!")]
        
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        
        self.SetMenuBar(self.CreateMenuBar())
        
        panel = wx.Panel(self, -1)
        sizer = wx.FlexGridSizer(2, 3, 2, 5)

        # 6 Panels To Hold The SpeedMeters ;-)
        
        panel1 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        panel2 = wx.Panel(panel, -1, style=wx.RAISED_BORDER)
        panel3 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        panel4 = wx.Panel(panel, -1, style=wx.RAISED_BORDER)
        panel5 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        panel6 = wx.Panel(panel, -1, style=wx.RAISED_BORDER)
        
        # First SpeedMeter: We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_SECTORS: Full Sectors Will Be Drawn, To Indicate Different Intervals
        # SM_DRAW_MIDDLE_TEXT: We Draw Some Text In The Center Of SpeedMeter
        # SM_DRAW_SECONDARY_TICKS: We Draw Secondary (Intermediate) Ticks Between
        #                          The Main Ticks (Intervals)

        self.SpeedWindow1 = SM.SpeedMeter(panel1,
                                          extrastyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS |
                                          SM.SM_DRAW_MIDDLE_TEXT |
                                          SM.SM_DRAW_SECONDARY_TICKS
                                          )

        # Set The Region Of Existence Of SpeedMeter (Always In Radians!!!!)
        self.SpeedWindow1.SetAngleRange(-pi/6, 7*pi/6)

        # Create The Intervals That Will Divide Our SpeedMeter In Sectors        
        intervals = range(0, 201, 20)
        self.SpeedWindow1.SetIntervals(intervals)

        # Assign The Same Colours To All Sectors (We Simulate A Car Control For Speed)
        # Usually This Is Black
        colours = [wx.BLACK]*10
        self.SpeedWindow1.SetIntervalColours(colours)

        # Assign The Ticks: Here They Are Simply The String Equivalent Of The Intervals
        ticks = [str(interval) for interval in intervals]
        self.SpeedWindow1.SetTicks(ticks)
        # Set The Ticks/Tick Markers Colour
        self.SpeedWindow1.SetTicksColour(wx.WHITE)
        # We Want To Draw 5 Secondary Ticks Between The Principal Ticks
        self.SpeedWindow1.SetNumberOfSecondaryTicks(5)

        # Set The Font For The Ticks Markers
        self.SpeedWindow1.SetTicksFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL))
                                       
        # Set The Text In The Center Of SpeedMeter
        self.SpeedWindow1.SetMiddleText("Km/h")
        # Assign The Colour To The Center Text
        self.SpeedWindow1.SetMiddleTextColour(wx.WHITE)
        # Assign A Font To The Center Text
        self.SpeedWindow1.SetMiddleTextFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        # Set The Colour For The Hand Indicator
        self.SpeedWindow1.SetHandColour(wx.Colour(255, 50, 0))

        # Do Not Draw The External (Container) Arc. Drawing The External Arc May
        # Sometimes Create Uglier Controls. Try To Comment This Line And See It
        # For Yourself!
        self.SpeedWindow1.DrawExternalArc(False)        

        # Set The Current Value For The SpeedMeter
        self.SpeedWindow1.SetSpeedValue(44)

        
        # Second SpeedMeter: We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_SECTORS: Full Sectors Will Be Drawn, To Indicate Different Intervals
        # SM_DRAW_MIDDLE_TEXT: We Draw Some Text In The Center Of SpeedMeter
        # SM_DRAW_SECONDARY_TICKS: We Draw Secondary (Intermediate) Ticks Between
        #                          The Main Ticks (Intervals)
        # SM_DRAW_PARTIAL_FILLER: The Region Passed By The Hand Indicator Is Highlighted
        #                         With A Different Filling Colour
        # SM_DRAW_SHADOW: A Shadow For The Hand Indicator Is Drawn
        
        self.SpeedWindow2 = SM.SpeedMeter(panel2,
                                          extrastyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS |
                                          SM.SM_DRAW_MIDDLE_TEXT |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          SM.SM_DRAW_PARTIAL_FILLER |
                                          SM.SM_DRAW_SHADOW
                                          )

        # We Want To Simulate A Clock. Somewhat Tricky, But Did The Job
        self.SpeedWindow2.SetAngleRange(pi/2, 5*pi/2)

        intervals = range(0, 13)
        self.SpeedWindow2.SetIntervals(intervals)

        colours = [wx.SystemSettings_GetColour(0)]*12
        self.SpeedWindow2.SetIntervalColours(colours)

        ticks = [str(interval) for interval in intervals]
        ticks[-1] = ""
        ticks[0] = "12"
        self.SpeedWindow2.SetTicks(ticks)
        self.SpeedWindow2.SetTicksColour(wx.BLUE)
        self.SpeedWindow2.SetTicksFont(wx.Font(11, wx.SCRIPT, wx.NORMAL, wx.BOLD, True))
        self.SpeedWindow2.SetNumberOfSecondaryTicks(4)

        # Set The Colour For The External Arc        
        self.SpeedWindow2.SetArcColour(wx.BLUE)

        self.SpeedWindow2.SetHandColour(wx.BLACK)

        self.SpeedWindow2.SetMiddleText("0 s")
        self.SpeedWindow2.SetMiddleTextColour(wx.RED)

        # We Set The Background Colour Of The SpeedMeter OutSide The Control
        self.SpeedWindow2.SetSpeedBackground(wx.WHITE)

        # Set The Colour For The Shadow
        self.SpeedWindow2.SetShadowColour(wx.Colour(128, 128, 128))        

        self.SpeedWindow2.SetSpeedValue(0.0)


        # Third SpeedMeter: We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_PARTIAL_SECTORS: Partial Sectors Will Be Drawn, To Indicate Different Intervals
        # SM_DRAW_MIDDLE_ICON: We Draw An Icon In The Center Of SpeedMeter
        
        self.SpeedWindow3 = SM.SpeedMeter(panel3,
                                          extrastyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_PARTIAL_SECTORS |
                                          SM.SM_DRAW_MIDDLE_ICON
                                          )

        # We Want To Simulate A Car Gas-Control
        self.SpeedWindow3.SetAngleRange(-pi/3, pi/3)

        intervals = range(0, 5)
        self.SpeedWindow3.SetIntervals(intervals)

        colours = [wx.BLACK]*3
        colours.append(wx.RED)
        self.SpeedWindow3.SetIntervalColours(colours)

        ticks = ["F", "", "", "", "E"]
        self.SpeedWindow3.SetTicks(ticks)
        self.SpeedWindow3.SetTicksColour(wx.WHITE)
        
        self.SpeedWindow3.SetHandColour(wx.Colour(255, 255, 0))

        # Define The Icon We Want
        icon = wx.Icon("fuel.ico", wx.BITMAP_TYPE_ICO)
        icon.SetWidth(24)
        icon.SetHeight(24)

        # Draw The Icon In The Center Of SpeedMeter        
        self.SpeedWindow3.SetMiddleIcon(icon)        

        self.SpeedWindow3.SetSpeedBackground(wx.BLACK)        

        self.SpeedWindow3.SetArcColour(wx.WHITE)
        
        self.SpeedWindow3.SetSpeedValue(0.7)

                
        # Fourth SpeedMeter: We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_SECTORS: Full Sectors Will Be Drawn, To Indicate Different Intervals
        # SM_DRAW_SHADOW: A Shadow For The Hand Indicator Is Drawn
        # SM_DRAW_MIDDLE_ICON: We Draw An Icon In The Center Of SpeedMeter
        #
        # NOTE: We Use The Mouse Style mousestyle=SM_MOUSE_TRACK. In This Way, Mouse
        # Events Are Catched (Mainly Left Clicks/Drags) And You Can Change The Speed
        # Value Using The Mouse
        
        self.SpeedWindow4 = SM.SpeedMeter(panel4,
                                          extrastyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS |
                                          SM.SM_DRAW_SHADOW |
                                          SM.SM_DRAW_MIDDLE_ICON,
                                          mousestyle=SM.SM_MOUSE_TRACK
                                          )

        # We Want To Simulate Some Kind Of Thermometer (In Celsius Degrees!!!)
        self.SpeedWindow4.SetAngleRange(pi, 2*pi)

        intervals = range(35, 44)
        self.SpeedWindow4.SetIntervals(intervals)

        colours = [wx.BLUE]*5
        colours.extend([wx.Colour(255, 255, 0)]*2)
        colours.append(wx.RED)
        self.SpeedWindow4.SetIntervalColours(colours)

        ticks = [str(interval) + "°" for interval in intervals]
        self.SpeedWindow4.SetTicks(ticks)
        self.SpeedWindow4.SetTicksColour(wx.BLACK)
        self.SpeedWindow4.SetTicksFont(wx.Font(7, wx.TELETYPE, wx.NORMAL, wx.BOLD))
        
        self.SpeedWindow4.SetHandColour(wx.Colour(0, 0, 255))

        self.SpeedWindow4.SetSpeedBackground(wx.SystemSettings_GetColour(0))        

        self.SpeedWindow4.DrawExternalArc(False)

        self.SpeedWindow4.SetHandColour(wx.GREEN)
        self.SpeedWindow4.SetShadowColour(wx.Colour(50, 50, 50))  

        # We Want A Simple Arrow As Indicator, Not The More Scenic Hand ;-)
        self.SpeedWindow4.SetHandStyle("Arrow")

        # Define The Icon We Want
        icon = wx.Icon("temp.ico", wx.BITMAP_TYPE_ICO)
        icon.SetWidth(16)
        icon.SetHeight(16)

        # Draw The Icon In The Center Of SpeedMeter        
        self.SpeedWindow4.SetMiddleIcon(icon)        

        # Quite An High Fever!!!        
        self.SpeedWindow4.SetSpeedValue(41.4)


        # Fifth SpeedMeter: We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_PARTIAL_SECTORS: Partial Sectors Will Be Drawn, To Indicate Different Intervals
        # SM_DRAW_SECONDARY_TICKS: We Draw Secondary (Intermediate) Ticks Between
        #                          The Main Ticks (Intervals)
        # SM_DRAW_MIDDLE_TEXT: We Draw Some Text In The Center Of SpeedMeter
        # SM_ROTATE_TEXT: The Ticks Texts Are Rotated Accordingly To Their Angle
        
        self.SpeedWindow5 = SM.SpeedMeter(panel5,
                                          extrastyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_PARTIAL_SECTORS |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          SM.SM_DRAW_MIDDLE_TEXT |
                                          SM.SM_ROTATE_TEXT
                                          )

        # We Want To Simulate The Round Per Meter Control In A Car
        self.SpeedWindow5.SetAngleRange(-pi/6, 7*pi/6)

        intervals = range(0, 9)
        self.SpeedWindow5.SetIntervals(intervals)

        colours = [wx.BLACK]*6
        colours.append(wx.Colour(255, 255, 0))
        colours.append(wx.RED)
        self.SpeedWindow5.SetIntervalColours(colours)

        ticks = [str(interval) for interval in intervals]
        self.SpeedWindow5.SetTicks(ticks)
        self.SpeedWindow5.SetTicksColour(wx.WHITE)
        self.SpeedWindow5.SetTicksFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.SpeedWindow5.SetHandColour(wx.Colour(255, 50, 0))

        self.SpeedWindow5.SetSpeedBackground(wx.SystemSettings_GetColour(0))        

        self.SpeedWindow5.DrawExternalArc(False)

        self.SpeedWindow5.SetShadowColour(wx.Colour(50, 50, 50))

        self.SpeedWindow5.SetMiddleText("rpm")
        self.SpeedWindow5.SetMiddleTextColour(wx.WHITE)
        self.SpeedWindow5.SetMiddleTextFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.SpeedWindow5.SetSpeedBackground(wx.Colour(160, 160, 160)) 
        
        self.SpeedWindow5.SetSpeedValue(5.6)
        

        # Sixth SpeedMeter: That Is Complete And Complex Example.
        #                   We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_PARTIAL_FILLER: The Region Passed By The Hand Indicator Is Highlighted
        #                         With A Different Filling Colour
        # SM_DRAW_MIDDLE_ICON: We Draw An Icon In The Center Of SpeedMeter
        # SM_DRAW_GRADIENT: A Circular Colour Gradient Is Drawn Inside The SpeedMeter, To
        #                   Give Some Kind Of Scenic Effect
        # SM_DRAW_FANCY_TICKS: We Use wx.lib.
        # SM_DRAW_SHADOW: A Shadow For The Hand Indicator Is Drawn
        
        self.SpeedWindow6 = SM.SpeedMeter(panel6,
                                          extrastyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_PARTIAL_FILLER  |
                                          SM.SM_DRAW_MIDDLE_ICON |
                                          SM.SM_DRAW_GRADIENT |
                                          SM.SM_DRAW_FANCY_TICKS |
                                          SM.SM_DRAW_SHADOW
                                          )

        self.SpeedWindow6.SetAngleRange(0, 4*pi/3)

        intervals = [0, pi/6, sqrt(pi), 2./3.*pi, pi**2/4, pi, 7./6.*pi, 4*pi/3]
        self.SpeedWindow6.SetIntervals(intervals)

        # If You Use The Style SM_DRAW_FANCY_TICKS, Refer To wx.lib.fancytext To Create
        # Correct XML Strings To Put Here
        ticks = ["0", "<pi/>/6", "sq(<pi/>)", "2<pi/>/3", "<pi/><sup>2</sup>/4", "<pi/>", "7<pi/>/6", "4<pi/>/3"]
        self.SpeedWindow6.SetTicks(ticks)
        self.SpeedWindow6.SetTicksColour(wx.Colour(0, 90, 0))
        self.SpeedWindow6.SetTicksFont(wx.Font(6, wx.ROMAN, wx.NORMAL, wx.BOLD))

        self.SpeedWindow6.SetHandColour(wx.Colour(60, 60, 60))

        self.SpeedWindow6.DrawExternalArc(False)

        self.SpeedWindow6.SetFillerColour(wx.Colour(145, 220, 200))        

        self.SpeedWindow6.SetShadowColour(wx.BLACK)

        self.SpeedWindow6.SetDirection("Reverse")        

        self.SpeedWindow6.SetSpeedBackground(wx.SystemSettings_GetColour(0))

        # Set The First Gradient Colour, Which Is The Colour Near The External Arc
        self.SpeedWindow6.SetFirstGradientColour(wx.RED)
        # Set The Second Gradient Colour, Which Is The Colour Near The Center Of The SpeedMeter
        self.SpeedWindow6.SetSecondGradientColour(wx.WHITE)

        icon = wx.Icon("pi.ico", wx.BITMAP_TYPE_ICO)
        icon.SetHeight(12)
        icon.SetWidth(12)
        self.SpeedWindow6.SetMiddleIcon(icon)            
        
        self.SpeedWindow6.SetSpeedValue(pi/3)


        # End Of SpeedMeter Controls Construction. Add Some Functionality

        self.helpbuttons = []
        self.isalive = 0
        
        icononselected = wx.Icon("help.ico", wx.BITMAP_TYPE_ICO, 16, 16)
        icoselected = wx.Icon("pressed.ico", wx.BITMAP_TYPE_ICO, 16, 16)

        bmp1 = wx.EmptyBitmap(16,16)
        bmp1.CopyFromIcon(icononselected)
        bmp2 = wx.EmptyBitmap(16,16)
        bmp2.CopyFromIcon(icoselected)

        for ind in range(6):
            helpbtn = wx.lib.buttons.GenBitmapToggleButton(eval("panel" + str(ind+1)), -1, None,
                                                     size=(20,20), style=wx.NO_BORDER)

            helpbtn.SetBitmapLabel(bmp1)
            helpbtn.SetBitmapSelected(bmp2)
            helpbtn.SetUseFocusIndicator(False)
            helpbtn.Bind(wx.EVT_ENTER_WINDOW, self.EnterWindow)
            helpbtn.Bind(wx.EVT_LEAVE_WINDOW, self.ExitWindow)
            self.helpbuttons.append(helpbtn)

        

        # These Are Cosmetics For The First SpeedMeter Control
        bsizer1 = wx.BoxSizer(wx.VERTICAL)

        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)        
        slider = wx.Slider(panel1, -1, 44, 0, 200, size=(-1, 40), 
                           style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS )
        slider.SetTickFreq(5, 1)
        slider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
        slider.SetToolTip(wx.ToolTip("Drag The Slider To Change The Speed!"))

        hsizer1.Add(slider, 1, wx.EXPAND)
        hsizer1.Add(self.helpbuttons[0], 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)

        bsizer1.Add(self.SpeedWindow1, 1, wx.EXPAND)
        bsizer1.Add(hsizer1, 0, wx.EXPAND)
        panel1.SetSizer(bsizer1)


        # These Are Cosmetics For The Second SpeedMeter Control
        
        # Create The Timer For The Clock
        self.timer = wx.PyTimer(self.ClockTimer)
        self.currvalue = 0

        bsizer2 = wx.BoxSizer(wx.VERTICAL)

        hsizer2 = wx.BoxSizer(wx.HORIZONTAL) 
        stattext2 = wx.StaticText(panel2, -1, "A Simple Clock", style=wx.ALIGN_CENTER)

        button2 = wx.Button(panel2, -1, "Stop")
        self.stopped = 0
        button2.Bind(wx.EVT_BUTTON, self.OnStopClock)
        button2.SetToolTip(wx.ToolTip("Click To Stop/Resume The Clock"))

        hsizer2.Add(button2, 0, wx.LEFT, 5)
        hsizer2.Add(stattext2, 1, wx.EXPAND)
        hsizer2.Add(self.helpbuttons[1], 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)
        
        bsizer2.Add(self.SpeedWindow2, 1, wx.EXPAND)        
        bsizer2.Add(hsizer2, 0, wx.EXPAND)        
        panel2.SetSizer(bsizer2)

        
        # These Are Cosmetics For The Third SpeedMeter Control
        self.timer3 = wx.PyTimer(self.OilTimer)

        bsizer3 = wx.BoxSizer(wx.VERTICAL)
        
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sc = wx.SpinCtrl(panel3, -1, size=(60,20))
        sc.SetRange(1, 250)
        sc.SetValue(50)

        self.spinctrl = sc
        
        strs = "Change The Speed And See How Much Fuel You Loose"
        self.spinctrl.SetToolTip(wx.ToolTip(strs))
        
        button3 = wx.Button(panel3, -1, "Refill!", size=(60,20))
        button3.SetToolTip(wx.ToolTip("Click Here To Refill!"))
        button3.Bind(wx.EVT_BUTTON, self.OnRefill)

        hsizer3.Add(self.spinctrl, 0, wx.EXPAND | wx.LEFT, 5)
        hsizer3.Add(button3, 0, wx.EXPAND | wx.LEFT, 5)
        hsizer3.Add((1,0), 2, wx.EXPAND)
        hsizer3.Add(self.helpbuttons[2], 0, wx.ALIGN_CENTER | wx.RIGHT, 5)

        bsizer3.Add(self.SpeedWindow3, 1, wx.EXPAND)
        bsizer3.Add(hsizer3, 0, wx.EXPAND)
        panel3.SetSizer(bsizer3)


        # These Are Cosmetics For The Fourth SpeedMeter Control
        bsizer4 = wx.BoxSizer(wx.VERTICAL)

        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        stattext4 = wx.StaticText(panel4, -1, "Use The Mouse ;-)")

        hsizer4.Add(stattext4, 1, wx.EXPAND | wx.LEFT, 5)
        hsizer4.Add(self.helpbuttons[3], 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)
        
        bsizer4.Add(self.SpeedWindow4, 1, wx.EXPAND)
        bsizer4.Add(hsizer4, 0, wx.EXPAND)
        panel4.SetSizer(bsizer4)


        # These Are Cosmetics For The Fifth SpeedMeter Control
        bsizer5 = wx.BoxSizer(wx.VERTICAL)

        hsizer5 = wx.BoxSizer(wx.HORIZONTAL)
        
        button5 = wx.Button(panel5, -1, "Simulate")
        button5.SetToolTip(wx.ToolTip("Start A Car Acceleration Simulation"))
        button5.Bind(wx.EVT_BUTTON, self.OnSimulate)

        hsizer5.Add(button5, 0, wx.EXPAND | wx.LEFT, 5)
        hsizer5.Add((1,0), 1, wx.EXPAND)
        hsizer5.Add(self.helpbuttons[4], 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        
        bsizer5.Add(self.SpeedWindow5, 1, wx.EXPAND)
        bsizer5.Add(hsizer5, 0, wx.EXPAND)
        panel5.SetSizer(bsizer5)


        # These Are Cosmetics For The Sixth SpeedMeter Control
        bsizer6 = wx.BoxSizer(wx.VERTICAL)
        hsizer6 = wx.BoxSizer(wx.HORIZONTAL)
        
        txtctrl6 = wx.TextCtrl(panel6, -1, "60", size=(60, 20))
        txtctrl6.SetToolTip(wx.ToolTip("Insert An Angle In DEGREES"))

        self.txtctrl = txtctrl6        
        
        button6 = wx.Button(panel6, -1, "Go!")
        button6.SetToolTip(wx.ToolTip("Calculate The Equivalent In Radians And Display It"))

        hsizer6.Add(txtctrl6, 0, wx.EXPAND | wx.LEFT, 5)
        hsizer6.Add(button6, 0, wx.EXPAND | wx.LEFT, 5)
        hsizer6.Add((1,0), 1, wx.EXPAND)
        hsizer6.Add(self.helpbuttons[5], 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        
        button6.Bind(wx.EVT_BUTTON, self.OnCalculate)
        bsizer6.Add(self.SpeedWindow6, 1, wx.EXPAND)
        bsizer6.Add(hsizer6, 0, wx.EXPAND)
        panel6.SetSizer(bsizer6)
        
        bsizer1.Layout()
        bsizer2.Layout()
        bsizer3.Layout()
        bsizer4.Layout()
        bsizer5.Layout()
        bsizer6.Layout()
        
        sizer.Add(panel1, 1, wx.EXPAND)
        sizer.Add(panel2, 1, wx.EXPAND)
        sizer.Add(panel3, 1, wx.EXPAND)
        
        sizer.Add(panel4, 1, wx.EXPAND)
        sizer.Add(panel5, 1, wx.EXPAND)
        sizer.Add(panel6, 1, wx.EXPAND)

        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)
        
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(2)
        
        panel.SetSizer(sizer)
        sizer.Layout()

        self.timer.Start(1000)
        self.timer3.Start(500)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)


    def EnterWindow(self, event):

        if self.isalive == 1:
            return

        btn = event.GetEventObject()
        btn.SetToggle(True)
        self.isalive = 1
        self.selectedbutton = btn

        indx = self.helpbuttons.index(btn)

        win = MyTransientPopup(self, wx.SIMPLE_BORDER, helpid=indx)
        pos = btn.ClientToScreen((0,0))
        sz =  btn.GetSize()
        self.popup = win

        win.Position(pos, (0, sz[1]))
        win.Show()
        

    def ExitWindow(self, event):

        if hasattr(self, "popup"):
            self.popup.Destroy()
            del self.popup
            self.selectedbutton.SetToggle(False)

        self.isalive = 0
        

    def OnSliderScroll(self, event):

        slider = event.GetEventObject()
        self.SpeedWindow1.SetSpeedValue(slider.GetValue())

        event.Skip()


    def ClockTimer(self):
        if self.currvalue >= 59:
            self.currvalue = 0
        else:
            self.currvalue = self.currvalue + 1

        self.SpeedWindow2.SetMiddleText(str(self.currvalue) + " s")            
        self.SpeedWindow2.SetSpeedValue(self.currvalue/5.0)


    def OnStopClock(self, event):

        btn = event.GetEventObject()
        
        if self.stopped == 0:
            self.stopped = 1
            self.timer.Stop()
            btn.SetLabel("Resume")
        else:
            self.stopped = 0
            self.timer.Start()
            btn.SetLabel("Stop")
            
        
    def OilTimer(self):

        val = self.spinctrl.GetValue()
        
        if val > 250:
            return

        current = self.SpeedWindow3.GetSpeedValue()
        new = current + val*0.0005

        if new > 4.0:
            return
        
        self.SpeedWindow3.SetSpeedValue(new)


    def OnRefill(self, event):

        self.SpeedWindow3.SetSpeedValue(0)


    def OnSimulate(self, event):
        
        for ii in range(50):
            self.SpeedWindow5.SetSpeedValue(ii/10.0)
            wx.MilliSleep(10)

        current = self.SpeedWindow5.GetSpeedValue()
        for ii in range(40):
            current = current - 1.0/10.0
            self.SpeedWindow5.SetSpeedValue(current)
            wx.MilliSleep(40)

        wx.MilliSleep(50)
        current = self.SpeedWindow5.GetSpeedValue()
        
        for ii in range(59):
            current = current + 1.0/10.0
            self.SpeedWindow5.SetSpeedValue(current)
            wx.MilliSleep(10)        
        
        event.Skip()


    def OnCalculate(self, event):

        try:
            myval = self.txtctrl.GetValue()
            val = float(myval)
        except:
            msg = "ERROR: Value Entered In The TextCtrl:\n\n" + myval + "\n\n"
            msg = msg + "Is Not A Valid Integer/Float Number."
            dlg = wx.MessageDialog(self, msg, "SpeedMeter Demo Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False, "Verdana"))
            dlg.ShowModal()
            dlg.Destroy()
            return

        newval = val*pi/180.0
        anglerange = self.SpeedWindow6.GetAngleRange()
        start = anglerange[0]
        end = anglerange[1]

        error = 0
        
        if newval < start:
            msg = "ERROR: Value Entered In The TextCtrl:\n\n" + myval + "\n\n"
            msg = msg + "Is Smaller Than Minimum Value."
            error = 1
        elif newval > end:
            msg = "ERROR: Value Entered In The TextCtrl:\n\n" + myval + "\n\n"
            msg = msg + "Is Greater Than Maximum Value."
            error = 1

        if error:
            dlg = wx.MessageDialog(self, msg, "SpeedMeter Demo Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False, "Verdana"))
            dlg.ShowModal()
            dlg.Destroy()
            return

        self.SpeedWindow6.SetSpeedValue(newval)
        

    def OnClose(self, event):

        try:
            self.timer.Stop()
            self.timer3.Stop()
            del self.timer
            del self.timer3
        except:
            pass        
        
        self.Destroy()


    def OnAbout(self, event):

        msg = "This Is The About Dialog Of The SpeedMeter Demo.\n\n" + \
              "Author: Andrea Gavana @ 25 Sep 2005\n\n" + \
              "Please Report Any Bug/Requests Of Improvements\n" + \
              "To Me At The Following Adresses:\n\n" + \
              "andrea.gavana@agip.it\n" + "andrea_gavana@tin.it\n\n" + \
              "Welcome To wxPython " + wx.VERSION_STRING + "!!"
              
        dlg = wx.MessageDialog(self, msg, "SpeedMeter Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False, "Verdana"))
        dlg.ShowModal()
        dlg.Destroy()
        

    def CreateMenuBar(self):

        file_menu = wx.Menu()
        
        SM_EXIT = wx.NewId()        
        file_menu.Append(SM_EXIT, "&Exit")
        self.Bind(wx.EVT_MENU, self.OnClose, id=SM_EXIT)

        help_menu = wx.Menu()

        SM_ABOUT = wx.NewId()        
        help_menu.Append(SM_ABOUT, "&About...")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=SM_ABOUT)

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")        

        return menu_bar        
        

# Auxiliary Help Class. Just To Displkay Some Help Functionalities
# About SpeedMeter Control Using TransientPopups When The User
# Enter With The Mouse The Help Button

class MyTransientPopup(wx.PopupWindow):
    
    def __init__(self, parent, style, helpid=None):
        
        wx.PopupWindow.__init__(self, parent, style)
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour(wx.Colour(255,255,190))

        self.parent = parent
        
        icon = wx.Icon("OK.ico", wx.BITMAP_TYPE_ICO, 16, 16)
        bmp = wx.EmptyBitmap(16,16)
        bmp.CopyFromIcon(icon)
        
        ontext, thehelp = self.GetStatic(helpid)

        sx = 0
        sy = 0
        
        txt = wx.StaticText(panel, -1, thehelp, pos=(5,5))
        txt.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, "tahoma"))

        sz = txt.GetBestSize()
        sx = sx + sz[0]
        sy = sy + sz[1] + 5

        maxlen = 0

        for strs in ontext:
            txt = wx.StaticText(panel, -1, strs, pos=(30,20+sy))
            txt.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, "tahoma"))
            sz = txt.GetBestSize()
            stbmp = wx.StaticBitmap(panel, -1, bmp, pos=(10, 5+sy+sz[1]))
            sy = sy + sz[1] + 5
            maxlen = max(maxlen, sz[0])


        oldsz = sz
        
        if helpid == 1:  # Show Some Warning...
            strs = "Combination Of Styles 'SM_DRAW_SECTORS'\nAnd 'SM_DRAW_PARTIAL_FILLERS' "
            strs = strs + "Does Not\nWork Very Well If The Sectors Colours Are\nDifferent."
            txt = wx.StaticText(panel, -1, strs, pos=(30,30+sy))
            txt.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, "tahoma"))
            sz = txt.GetBestSize()

            icon = wx.Icon("warn.ico", wx.BITMAP_TYPE_ICO, 16, 16)
            bmp2 = wx.EmptyBitmap(16,16)
            bmp2.CopyFromIcon(icon)
        
            stbmp = wx.StaticBitmap(panel, -1, bmp2, pos=(10, 15+sy+oldsz[1]))
            sy = sy + sz[1] + 15
            maxlen = max(maxlen, sz[0])

        elif helpid == 3:   # Show The Fact That We Catch Mouse Events
            strs = "This Example Use The SM_MOUSE_TRACK\nmousestyle To Catch Click/Drag Events\n"
            strs = strs + "Use The Mouse To Move The Arrow!"
            txt = wx.StaticText(panel, -1, strs, pos=(30,30+sy))
            txt.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, "tahoma"))
            sz = txt.GetBestSize()

            icon = wx.Icon("info.ico", wx.BITMAP_TYPE_ICO, 16, 16)
            bmp2 = wx.EmptyBitmap(16,16)
            bmp2.CopyFromIcon(icon)
        
            stbmp = wx.StaticBitmap(panel, -1, bmp2, pos=(10, 15+sy+oldsz[1]))
            sy = sy + sz[1] + 15
            maxlen = max(maxlen, sz[0])
            
            
        panel.SetSize((maxlen+50, 25+sy))
        self.SetSize(panel.GetSize())
            

    def GetStatic(self, helpid):

        if helpid == 0: 
            ontext = self.parent.SpeedWindow1.GetSpeedStyle()[0]
            thehelp = "Speed Control"
        elif helpid == 1:
            ontext = self.parent.SpeedWindow2.GetSpeedStyle()[0]
            thehelp = "Simple Clock"
        elif helpid == 2:
            ontext = self.parent.SpeedWindow3.GetSpeedStyle()[0]
            thehelp = "Fuel Control"
        elif helpid == 3:
            ontext = self.parent.SpeedWindow4.GetSpeedStyle()[0]
            thehelp = "Temperature Control"
        elif helpid == 4:
            ontext = self.parent.SpeedWindow5.GetSpeedStyle()[0]
            thehelp = "RPM Control"
        elif helpid == 5:
            ontext = self.parent.SpeedWindow6.GetSpeedStyle()[0]
            thehelp = "Complex Sample"

        return ontext, thehelp


    def ProcessLeftDown(self, evt):
        return False

    def OnDismiss(self):
        return False

        
if __name__ == "__main__":
    
    app = wx.PySimpleApp()
    frame = SpeedMeterDemo()
    frame.Show()
    frame.Maximize()

    app.MainLoop()

    