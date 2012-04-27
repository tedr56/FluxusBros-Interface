#!/usr/bin/env python

import numpy as N
import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas
from MessageDispatch import *

ShiftStatus = False

class PolygonCustom(FloatCanvas.Polygon):
    def __init__(self, parent, Canvas, Points, LineColor = "Yellow", LineStyle="Solid", LineWidth = 2, FillColor = "Green", FillStyle = 'Transparent', InForeground=True):
        FloatCanvas.Polygon.__init__(self, Points, LineColor, LineStyle, LineWidth, FillColor, FillStyle, InForeground)
        self.parent = parent
        Canvas.AddObject(self)
        #Canvas.ZoomToBB()
        Canvas.Draw()

class PolygonMultiCustom(wx.PyEvtHandler):
#~ class PolygonMultiCustom(wx.Object):
    def __init__(self, parent, Canvas=None, id=wx.NewId(), Name=None, Points=[[1,1,0], [50,1,0], [50,50,0], [1,50,0]], LineColor = "Yellow", LineStyle="Solid", LineWidth = 2, FillColor = "Green", FillStyle = 'Transparent', InForeground=True, Selectable=True, Offset=None):
        self.parent = parent
        self.Id = id
        self.Name = Name
        wx.PyEvtHandler.__init__(self)
        #~ wx.Object.__init__(self)
        if Canvas:
            self.Canvas = Canvas
        else :
            self.Canvas = self.parent
        self.Points = Points
        if Offset is not None:
            AxisOffset = self.SetAxisPoint(self.Canvas.GetAxis(), Offset)
            self.Points = map(lambda T: [T[0] + AxisOffset[0], T[1] + AxisOffset[1], T[2] + AxisOffset[2]], self.Points)
        self.Selectable = Selectable
        self.LineColor = LineColor
        self.LineStyle = LineStyle
        self.LineWidth = LineWidth
        self.FillColor = FillColor
        self.FillStyle = FillStyle
        InForeground
        self.InitSelections()
        self.Create()
    def InitSelections(self):
        self.Selected = None
        self.PointSelected = None
        self.SelectedPointNeighbors = None
    def Create(self):
        self.CanvasList = self.Canvas.GetOtherCanvas()
        self.CanvasList.append(self.Canvas)
        self.CreatePolygons()
        return self
    def CreatePolygons(self):
        self.PolygonsList = {}
        for C in self.CanvasList:
            Poly = PolygonCustom(self, C, self.GetAxisPoints(C.GetAxis(), self.Points), self.LineColor, self.LineStyle, self.LineWidth, self.FillColor, self.FillStyle)
            self.PolygonsList[C] = Poly
            if self.Selectable:
                Poly.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.SelectPoly)
            print self.GetPoints()
    def GetId(self):
        return self.Id
    def GetParent(self):
        return self.parent
    def GetName(self):
        return self.Name
    def SetName(self, Name):
        self.Name = Name
        self.Selected.SetName(Name)
    def SetAxisPoint(self, Axis, Points, Origin=[0,0,0]):
        if len(Points) == 2 and len(Origin) == 3:
            if   Axis == "XY":
                return [Points[0], Points[1], Origin[2]]
            elif Axis == "XZ":
                return [Points[0], Origin[1], Points[1]]
            elif Axis == "YZ":
                return [Origin[0], Points[0], Points[1]]
    def GetAxisPoints(self, Axis, Points=None):
        if Points is None:
            Points = self.GetPoints()
        Vectors = self.GetAxisVector(Axis)
        VPoints = map(lambda v: (v[Vectors[0]], v[Vectors[1]]) , Points)
        return VPoints
    def GetAxisVector(self, Axis):
        if   Axis == "XY":
            return [0,1]
        elif Axis == "XZ":
            return [0,2]
        elif Axis == "YZ":
            return [1,2]
        else :
            return [0,1]
    def GetPoints(self):
        return self.Points
    def SetPoints(self, Points):
        self.Points = Points
        for C, P in self.PolygonsList.iteritems():
            P.SetPoints(self.GetAxisPoints(C.GetAxis(), self.Points), copy = False)
            C.Draw()
    def SelectPoly(self, object):
        if self.Selected:
            self.UnSelectPoly(Apply=False)
        else :
            if not ShiftStatus:
                self.Canvas.DeSelectOther(self)
            #~ self.Selected = PolygonSelectMultiCustom(self, Canvas = self.Canvas, Points = self.GetPoints())
            self.Selected = PolygonSelectMultiCustomMessage(self, Canvas = self.Canvas, Points = self.GetPoints())
            PolygonSelectMultiCustomMessage
    def GetSelected(self):
        if self.Selected:
            return True
        else :
            False
    def UnSelectPoly(self, Apply=True):
        if self.Selected is not None:
            if Apply:
                Points = self.Selected.GetPoints()
                self.Selected.Destroy()
                self.SetPoints(Points)
                self.Selected = None
            else:
                print("Debug UnSelectPoly No Apply")
                print self.GetPoints()
                self.Selected.SetPoints(self.GetPoints())
                self.Selected.Destroy()
                self.Selected = None
    def AddPoint(self, Canvas):
        if self.Selected:
            self.Selected.AddPoint(Canvas)
    def UnSelectPoint(self, event, Canvas):
        if self.Selected:
            self.Selected.ReleasePoint(event, Canvas)
    def OnMove(self, event, Canvas):
        if self.Selected:
            self.Selected.Update(event, Canvas)
    def Destroy(self):
        if self.Selected:
            if self.Selected.GetPointSelected():
                self.Points.remove(self.Selected.GetPointSelected())
                self.UnSelectPoly(Apply=False)
                for C in self.CanvasList:
                    C.RemoveObject(self.PolygonsList[C])
                    C.Draw()
                self.CreatePolygons()
            else :
                self.UnSelectPoly(Apply=False)
                for C in self.CanvasList:
                    C.RemoveObject(self.PolygonsList[C])
                    C.Draw()
class PolygonSelectMultiCustom(PolygonMultiCustom):
    def __init__(self, parent, **kwargs):
        KPoints = kwargs.pop('Points', [[1,1,0], [50,1,0], [50,50,0], [1,50,0]])
        KCanvas = kwargs.pop('Canvas', parent.GetParent())
        Kid = kwargs.pop('id', wx.NewId())
        KLineWidth = kwargs.pop('LineWidth', 2)
        KLineColor = kwargs.pop('LineColor', "Red")
        KFillColor = kwargs.pop('FillColor', "Red")
        KFillStyle = kwargs.pop('FillStyle', "CrossHatch")
        KInForeground = kwargs.pop('InForeground', True)
        KOffset = kwargs.pop('Offset', None)
        PolygonMultiCustom.__init__(self, parent, Points=KPoints, Canvas=KCanvas, id = Kid, LineWidth = KLineWidth, LineColor = KLineColor, FillColor = KFillColor, FillStyle = KFillStyle, InForeground = KInForeground, Selectable=True, Offset=None)
        self.SelectDrag  = None
        self.Draggable = False
        self.AddPointMode = None
        self.AddPointCoords = None
        self.AddPointNeighbhors = None
        self.TempPoints = []
        for I in self.Points:
            self.TempPoints.append(I)
        self.InitPoints()
        
    def InitPoints(self):
        self.SelectPoints = {}
        for C in self.CanvasList:
            self.SelectPoints[C] = C.AddPointSet(self.GetAxisPoints(C.GetAxis(), self.GetPoints()),
                                                 Diameter = 6,
                                                 Color = "Red",
                                                 InForeground = True)
            self.SelectPoints[C].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.SelectPointHit)
            C.Draw()
    def SelectPoly(self, object):
        self.Draggable = True
    def SetPoints(self, Points):
        for C, PS in self.SelectPoints.iteritems():
                PS.SetPoints(self.GetAxisPoints(C.GetAxis(), Points), copy=False)
        PolygonMultiCustom.SetPoints(self, Points)
        self.SetTempPoints(self.Points)
    def SelectPointHit(self, PointSet):
        Canvas = [C for C, PS in self.SelectPoints.iteritems() if PS == PointSet][0]
        Axis = Canvas.GetAxis()
        AxisPoints = self.SetAxisPoint(Canvas.GetAxis(), PointSet.HitCoords)
        for C, PS in self.SelectPoints.iteritems():
            PS.Index = PS.FindClosestPoint(self.GetAxisPoints(C.GetAxis(), [AxisPoints])[0])
        self.PointSelected = True
    def GetPointSelected(self):
        if self.PointSelected:
            return self.GetPoints()[self.SelectPoints[self.Canvas].Index]
        else :
            return False
    def PointsMiddle(self, P1, P2):
        print P1
        print P2
        return ((P1[0] + P2[0]) / 2 , (P1[1] + P2[1]) / 2 , (P1[2] + P2[2]) / 2)
    def Update(self, event, Canvas):
        PolyPoints = []
        for I in self.GetPoints():
            PolyPoints.append(I)
        
        if self.PointSelected:
            #PolyPoints = self.GetPoints()
            C = Canvas
            Index = self.SelectPoints[C].Index
            PixelCoords = self.SetAxisPoint(Canvas.GetAxis(), event.GetPosition(), PolyPoints[Index])
            PolyAxisPoints = self.GetAxisPoints(C.GetAxis(), PolyPoints)
            
            if self.AddPointMode is not None:
                print("OnMove AddPoints")
                print self.AddPointMode
                if self.AddPointNeighbhors is None:
                    print self.GetPoints()
                    PolyPoints.extend(PolyPoints)
                    PolyPoints.insert(0, PolyPoints[len(PolyPoints)-1])
                    print self.GetPoints()
                    Neighbhors = PolyPoints[Index:Index+3]
                    self.PointNeighbhors = [self.PointsMiddle(Neighbhors[0],Neighbhors[1]) , self.PointsMiddle(Neighbhors[1],Neighbhors[2])]
                    self.AddPointNeighbhors = {FloatCanvas.Point(self.GetAxisPoints(C.GetAxis(), [self.PointNeighbhors[0]])[0], Diameter = 6, Color = "White", InForeground = True) : self.PointNeighbhors[0], FloatCanvas.Point(self.GetAxisPoints(C.GetAxis(), [self.PointNeighbhors[1]])[0], Diameter = 6, Color = "White", InForeground = True) : self.PointNeighbhors[1]}
                    for FloatPoint, Coords in self.AddPointNeighbhors.iteritems():
                        C.AddObject(FloatPoint)
                        FloatPoint.Bind(FloatCanvas.EVT_FC_ENTER_OBJECT, self.SelectAddPoints )
                        FloatPoint.Bind(FloatCanvas.EVT_FC_LEAVE_OBJECT, self.UnSelectAddPoints )
                    C.Draw()
                     
            else :
                dc = wx.ClientDC(C)
                dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
                dc.SetLogicalFunction(wx.XOR)
                if self.SelectedPointNeighbors is None:
                    PolyAxisPoints.extend(PolyAxisPoints)
                    PolyAxisPoints.insert(0, PolyAxisPoints[len(PolyAxisPoints) - 1])
                    self.SelectedPointNeighbors = PolyAxisPoints[Index:Index+3]
                    self.SelectedPointNeighbors = C.WorldToPixel(self.SelectedPointNeighbors)
                else:
                    dc.DrawLines(self.SelectedPointNeighbors)
                self.SelectedPointNeighbors[1] = self.GetAxisPoints(C.GetAxis(), [PixelCoords])[0]
                dc.DrawLines(self.SelectedPointNeighbors)
                
                self.SetTempPoints(PointIndex = Index , Value = PixelCoords)
        else :
            if self.SelectDrag is not None:
                EventCoords = event.GetCoords()
                EventOffset = (EventCoords[0]-self.SelectDrag[0] , EventCoords[1]-self.SelectDrag[1])
                AxisEventOffset = self.SetAxisPoint(Canvas.GetAxis(), EventOffset)
                Points = map(lambda T: [T[0] + AxisEventOffset[0], T[1] + AxisEventOffset[1], T[2] + AxisEventOffset[2]], PolyPoints)
                self.SetPoints(Points)
                self.SelectDrag = event.GetCoords()
            elif self.Draggable:
                self.SelectDrag = event.GetCoords()
    def SetTempPoints(self, Points=None, PointIndex = None, Value = None):
        if Points is not None:
            self.TempPoints = Points
        elif PointIndex is not None and Value is not None:
            self.TempPoints[PointIndex] = Value
    def SelectAddPoints(self, obj):
        obj.SetDiameter(12)
        obj.SetFillColor('Yellow')
        self.Canvas.Draw()
        self.AddPointCoords = self.AddPointNeighbhors[obj]
    def UnSelectAddPoints(self, obj):
        obj.SetDiameter(6)
        obj.SetFillColor('White')
        self.Canvas.Draw()
        self.AddPointCoords = None
    def ReleasePoint(self, event, Canvas):
        if self.PointSelected:
            Points = []
            for I in self.GetPoints():
                Points.append(I)
            if self.AddPointMode is not None:
                if self.AddPointCoords == self.PointNeighbhors[0]:
                    InsertIndex = self.AddPointMode
                else :
                    InsertIndex = self.AddPointMode + 1
                for FP , Coords in self.AddPointNeighbhors.iteritems():
                    self.Canvas.RemoveObject(FP)
                self.Canvas.Draw()
                Points.insert(InsertIndex, self.AddPointCoords)
                self.SetPoints(Points)
                self.AddPointMode = None
                self.AddPointCoords = None
                self.SelectedPointNeighbors = None
                self.AddPointNeighbhors = None
                self.PointSelected = False
            else :
                PointSelect = self.SelectPoints[Canvas]
                PixelCoords = self.SetAxisPoint(Canvas.GetAxis(), event.GetCoords(), Points[PointSelect.Index])
                Points[PointSelect.Index] = PixelCoords
                self.SetPoints(Points)
                self.PointSelected = False
                self.SelectedPointNeighbors = None
        if ShiftStatus:
            self.SelectDrag = event.GetCoords()
            self.Draggable = True
        else :
            self.SelectDrag = None
            self.Draggable = False
    def AddPoint(self, Canvas):
        if len(self.SelectPoints) is not 0:
            self.AddPointMode = self.SelectPoints[Canvas].Index
    def Destroy(self):
        for C, PS in self.SelectPoints.iteritems():
            self.SetPoints(self.parent.GetPoints())
            C.RemoveObject(PS)
            C.RemoveObject(self.PolygonsList[C])
            C.Draw()

class PolygonSelectMultiCustomMessage(PolygonSelectMultiCustom):
    def __init__(self, parent, *args, **kwargs):
        PolygonSelectMultiCustom.__init__(self, parent, *args, **kwargs)
        wx.PostEvent(self, MessageRecord(self, self.Id, 'osc', self.GetAddress(), None))
    def GetAddress(self):
        address = "/Mapping"
        address += "/"
        address += str(self.GetId())
        address += "/"
        address += str(self.GetName())
        address += "/"
    def SetTempPoints(self, Points=None, PointIndex = None, Value = None):
        PolygonSelectMultiCustom.SetTempPoints(self, Points, PointIndex, Value)
        if Points is not None:
            for i in range(len(self.TempPoints)):
                value = [i , self.TempPoints[i]]
                wx.PostEvent(self, InternalMessage(self, value))
        elif  PointIndex is not None and Value is not None:
            value = [PointIndex , self.TempPoints[PointIndex]]
            print("SetTempPoints")
            Handler = self.parent.GetParent().GetEventHandler()
            print Handler
            wx.PostEvent(Handler, InternalMessage(self, value))
    def SetName(self, Name):
        PolygonSelectMultiCustom.SetName(Name)
    def Destroy(self):
        PolygonSelectMultiCustom.Destroy()
        wx.PostEvent(self, MessageUnRecord(self, self.GetId(), 'osc', self.GetAddress(), None))
class CanvasCustom(FloatCanvas.FloatCanvas):
    def __init__(self, parent, id = wx.NewId(), Axis="XY", Toolbar=True, **kwargs):
        FloatCanvas.FloatCanvas.__init__(self,parent, id, **kwargs)
        self.parent=parent
        self.Axis = Axis
        self.ClearAll()
        self.PolygonsList = []
        FloatCanvas.EVT_MIDDLE_DOWN(self, self.OnMiddleClick )
        FloatCanvas.EVT_LEFT_DOWN(self, self.OnLeftClick )
        FloatCanvas.EVT_LEFT_UP(self, self.OnLeftUp )
        FloatCanvas.EVT_RIGHT_DOWN(self, self.OnRightDown )
        FloatCanvas.EVT_MOTION(self, self.OnMove )
    def KeyDownEvent(self, event):
        global ShiftStatus
        if event.GetKeyCode() == wx.WXK_SHIFT and not ShiftStatus:
            ShiftStatus = True
        elif event.GetKeyCode() == wx.WXK_DELETE:
            self.DeletePolygon()
        elif event.GetKeyCode() == wx.WXK_ADD or event.GetKeyCode() == wx.WXK_NUMPAD_ADD:
            self.AddPoint()
        event.Skip()
    def KeyUpEvent(self,event):
        global ShiftStatus
        if event.GetKeyCode() == wx.WXK_SHIFT and ShiftStatus:
            ShiftStatus = False
        event.Skip()
    def DeletePolygon(self):
        PolygonListToPoP = False
        for i in range(len(self.PolygonsList)):
            if self.PolygonsList[i].GetSelected():
                self.PolygonsList[i].Destroy()
                PolygonListToPoP = i
                break
        if PolygonListToPoP:
            self.DeletePolygonList(i)
            for C in self.GetOtherCanvas():
                C.DeletePolygonList(i)
            self.DeletePolygon()
        self.Draw()
        for C in self.GetOtherCanvas():
            C.Draw()
    def DeletePolygonList(self, PolyN):
        self.PolygonsList.pop(PolyN)
    def GetAxis(self):
        return self.Axis
    def OnRightDown(self, event):
        SelectPolys = []
        for P in self.PolygonsList:
            if P.GetSelected():
                SelectPolys.append(P)
        if len(SelectPolys) == 1:
            PolyNameDial = PolyNameDialog(self, SelectPolys[0].GetName())
            PolyNameDial.ShowModal()
            SelectPolys[0].SetName(PolyNameDial.GetValue())
            PolyNameDial.Destroy()
    def OnMiddleClick(self, event):
        self.AddPolygon(event.GetCoords())
    def OnLeftClick(self, event):
        self.DeSelectOther(None)
    def OnLeftUp(self, event):
        for P in self.PolygonsList:
            P.UnSelectPoint(event, self)
    def OnMove(self, event):
        for P in self.PolygonsList:
            P.OnMove(event, self)
    def GetOtherCanvas(self):
        return self.parent.GetOtherCanvas(self)
    def AddPolygon(self, EvtCoord):
        Poly = PolygonMultiCustom(self,Offset=EvtCoord)
        self.AddPolygonInList(Poly)
        for C in self.GetOtherCanvas():
            C.AddPolygonInList(Poly)
    def AddPolygonInList(self, Poly):
        self.PolygonsList.append(Poly)
    def AddPoint(self):
        for P in self.PolygonsList:
            P.AddPoint(self)
    def DeSelectOther(self, exception):
        for P in filter(lambda p: p is not exception, self.PolygonsList):
            P.UnSelectPoly()
class SplitterWindowCanvasCustom(wx.SplitterWindow):
    def __init__(self, *args, **kwargs):
        wx.SplitterWindow.__init__(self, *args, **kwargs)
    def GetOtherCanvas(self, origin):
        return self.GetParent().GetOtherCanvas(origin)

class PolyNameDialog(wx.TextEntryDialog):
    def __init__(self, parent, Value):
        if Value is None:
            DefValue = ""
        else :
            DefValue = Value
        wx.TextEntryDialog.__init__(self, parent, "Polygon Name", defaultValue = DefValue)
class MappingPanel(wx.Panel):
    def __init__(self, parent, ):
        wx.Panel.__init__(self, parent)
        HBox = wx.BoxSizer(wx.HORIZONTAL)
        splitter = SplitterWindowCanvasCustom(self, style=wx.SP_LIVE_UPDATE|wx.SP_3D)
        CanvasFront =  CanvasCustom(splitter, Axis="XY", ProjectionFun = None, Debug = 0, BackgroundColor = "DARK SLATE BLUE")
        CanvasTop = CanvasCustom(splitter, Axis="XZ", ProjectionFun = None, Debug = 0, BackgroundColor = "DARK BLUE")
        HBox.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(HBox)
        
        sash_Position = 300
        splitter.SplitHorizontally(CanvasFront, CanvasTop, sash_Position)
        splitter.SetSashSize(10)
        min_Pan_size = 0
        splitter.SetMinimumPaneSize(min_Pan_size)
        self.Fit()
        
        self.CanvasList = [CanvasFront, CanvasTop]
    def GetOtherCanvas(self, origin):
        return filter(lambda x: x != origin, self.CanvasList)

class MappingFrame(wx.Frame):
    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id, title, position, size)
        mappanel = MappingPanel(self)
