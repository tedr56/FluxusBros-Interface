import wx
import SpeedMeter as SM
from math import pi, sqrt

class SpeedMeterDemo(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "SpeedMeter Demo ;-)",
                         wx.DefaultPosition,
                         size=(100,100),
                         style=wx.DEFAULT_FRAME_STYLE |
                         wx.NO_FULL_REPAINT_ON_RESIZE)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        knob = SM.SpeedMeter(   self,
                                extrastyle=
                                SM.SM_DRAW_HAND |
#                                SM.SM_DRAW_SECTORS |
#                                SM.SM_DRAW_PARTIAL_SECTORS |
#                                SM.SM_DRAW_SHADOW |
#                                SM.SM_DRAW_PARTIAL_FILLER |
#                                SM.SM_DRAW_SECONDARY_TICKS |
#                                SM.SM_ROTATE_TEXT |
                                SM.SM_DRAW_MIDDLE_TEXT
                                ,
                                mousestyle=1
                                )
#        knob.SetSpeedBackground(wx.WHITE)
        knob.SetAngleRange(-pi/6, 7*pi/6)
        intervals = range(0, 128)
        knob.SetIntervals(intervals)
        colours = [wx.BLACK]*127
        knob.SetIntervalColours(colours)
        ticks = ["" for interval in intervals]
        knob.SetTicks(ticks)
        knob.SetTicksColour(wx.BLACK)
#        knob.SetNumberOfSecondaryTicks(10)
        knob.SetMiddleTextColour(wx.BLACK)
        knob.SetMiddleTextFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        knob.SetSpeedBackground(wx.NamedColour("YELLOW"))
        knob.SetSpeedBackground(wx.NamedColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME)))
        knob.SetHandColour(wx.BLACK)
#        knob.SetArcColour(wx.BLUE)
        knob.DrawExternalArc(False)
        
        hbox.Add(knob,1,wx.EXPAND)
        self.SetSizer(hbox)
        self.Fit()

if __name__ == "__main__":
    
    app = wx.PySimpleApp()
    frame = SpeedMeterDemo()
    frame.Show()
    frame.Maximize()

    app.MainLoop()

    
