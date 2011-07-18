import wx

class wxFader(wx.Slider):
    def __init__(self, *args, **kwargs):
        wx.Slider.__init__(self, *args, style = wx.SL_AUTOTICKS |  wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)
        self.SetRange(0, 127)
        
class wxCrossFader(wx.Slider):
    def __init__(self, *args, **kwargs):
        wx.Slider.__init__(self, *args, style = wx.SL_AUTOTICKS |  wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)
        self.SetRange(0, 127)

