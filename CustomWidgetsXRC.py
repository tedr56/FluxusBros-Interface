import wx
from wx import xrc
from CustomWidgets import wxFader
from CustomWidgets import wxKnob
from CustomWidgets import wxPiano
from CustomWidgets import wxMediaVisual

class wxFaderCtrlXmlHandler(xrc.XmlResourceHandler):
    def __init__(self):
        xrc.XmlResourceHandler.__init__(self)
        # Standard styles
        self.AddWindowStyles()
        
    def CanHandle(self,node):
        return self.IsOfClass(node, 'wxFader')
 
    # Process XML parameters and create the object
    def DoCreateResource(self):
        assert self.GetInstance() is None
        #~ f = wxFader(self.GetParentAsWindow(),
                                 #~ self.GetID(),
                                 #~ self.GetPosition(),
                                 #~ self.GetSize(),
                                 #~ self.GetStyle())
        f = wxFader()
        f.Create(self.GetParentAsWindow(), self.GetID(), self.GetPosition(), self.GetSize(), self.GetStyle())
        self.SetupWindow(f)
        f.SetInput(self.GetText('input_type'), eval(self.GetText('address')))
        return f

class wxKnobCtrlXmlHandler(xrc.XmlResourceHandler):
    def __init__(self):
        xrc.XmlResourceHandler.__init__(self)
        # Standard styles
        self.AddWindowStyles()
    def CanHandle(self,node):
        return self.IsOfClass(node, 'wxKnob')
 
    # Process XML parameters and create the object
    def DoCreateResource(self):
        assert self.GetInstance() is None
        f = wxKnob()
        f.Create(self.GetParentAsWindow(), self.GetID(), self.GetPosition(), self.GetSize(), self.GetStyle())
        self.SetupWindow(f)
        f.SetInput(self.GetText('input_type'), eval(self.GetText('address')))
        return f

class wxPianoCtrlXmlHandler(xrc.XmlResourceHandler):
    def __init__(self):
        xrc.XmlResourceHandler.__init__(self)
        # Standard styles
        self.AddWindowStyles()
        
    def CanHandle(self,node):
        return self.IsOfClass(node, 'wxPiano')
 
    # Process XML parameters and create the object
    def DoCreateResource(self):
        assert self.GetInstance() is None
        f = wxPiano(self.GetParentAsWindow(),
                                 self.GetID(),
                                 self.GetPosition(),
                                 self.GetSize(),
                                 self.GetStyle())
        self.SetupWindow(f)
        return f

class wxMediaVisualCtrlXmlHandler(xrc.XmlResourceHandler):
    def __init__(self):
        xrc.XmlResourceHandler.__init__(self)
        # Standard styles
        self.AddWindowStyles()
        
    def CanHandle(self,node):
        return self.IsOfClass(node, 'wxMediaVisual')
 
    # Process XML parameters and create the object
    def DoCreateResource(self):
        assert self.GetInstance() is None
        f = wxMediaVisual()
        f.Create(self.GetParentAsWindow(), self.GetID())
        self.SetupWindow(f)
        f.SetInput(self.GetText('input_type'), eval(self.GetText('address')))
        return f
