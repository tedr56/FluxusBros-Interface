import wx
from threading import Thread

#Create Internal and External OUT Events
EVT_INTERNAL_OUT_MSG_ID = wx.NewId()
EVT_EXTERNAL_OUT_MSG_ID = wx.NewId()

def EVT_INTERNAL_OUT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_INTERNAL_OUT_MSG_ID, func)

class InternalOutEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_INTERNAL_OUT_MSG_ID)
        self.data = data
        
def EVT_EXTERNAL_OUT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_EXTERNAL_OUT_MSG_ID, func)

class ExternalOutEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_EXTERNAL_OUT_MSG_ID)
        self.data = data

#Create Internal and External IN Events
EVT_INTERNAL_IN_MSG_ID = wx.NewId()
EVT_EXTERNAL_IN_MSG_ID = wx.NewId()

def EVT_INTERNAL_IN(win, func):
    win.Connect(-1, -1, EVT_INTERNAL_IN_MSG_ID, func)

class InternalOutEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_INTERNAL_IN_MSG_ID)
        self.data = data
        
def EVT_EXTERNAL_IN(win, func):
    win.Connect(-1, -1, EVT_EXTERNAL_IN_MSG_ID, func)

class ExternalOutEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_EXTERNAL_IN_MSG_ID)
        self.data = data

class MessageDispatch(Thread):
    def __init__(self, wxObject,Message,MessageList):
        Thread.__init__(self)
        self.wxObject = wxObject
        self.MessageList = MessageList
        self.Message = Message
        self.start()
    #def run(self):
        

#Event based Message Dispactch Rules Hanlder
EVT_WIDGET_MESSAGE_RECORD_ID = wx.NewId()

def EVT_WIDGET_MESSAGE_RECORD(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MESSAGE_RECORD_ID, func)

class MessageRecord(wx.PyCommandEvent):
    def __init__(self, Object, Id, Type, Address, Option):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_WIDGET_MESSAGE_RECORD_ID)
        self.SetEventObject(Object)
        self.SetId(Id)
        self.Type = Type
        self.Address = Address
        self.Option = Option
    def GetType(self):
        return self.Type
    def GetAddress(self):
        return self.Address
    def GetOption(self):
        return self.Option

EVT_WIDGET_MESSAGE_UNRECORD_ID = wx.NewId()

def EVT_WIDGET_MESSAGE_UNRECORD(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MESSAGE_UNRECORD_ID, func)

class MessageUnRecord(wx.PyCommandEvent):
    def __init__(self, Object, Id, Type, Address, Option):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_WIDGET_MESSAGE_UNRECORD_ID)
        self.SetEventObject(Object)
        self.SetId(Id)
        self.Type = Type
        self.Address = Address
        self.Option = Option
    def GetType(self):
        return self.Type
    def GetAddress(self):
        return self.Address
    def GetOption(self):
        return self.Option

EVT_WIDGET_MESSAGE_GET_ID = wx.NewId()

def EVT_WIDGET_MESSAGE_GET(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MESSAGE_GET_ID, func)

class MessageGet(wx.PyCommandEvent):
    def __init__(self, Object):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_WIDGET_MESSAGE_GET_ID)
        self.SetEventObject(Object)

class MessageDispatchRules(wx.PyEvtHandler):
    def __init__(self):
        wx.PyEvtHandler.__init__(self)
        self.OutMessages = []
        self.OutObjectMessages = dict()
        self.OutTypeMessages = dict()
    def AddInMessage(self, event):
        Object = event.GetEventObject()
        Id = event.GetId()
        Type = event.GetType()
        Address = event.GetAddress()
        Option  = event.GetOption()
        
        MessagePos  = len(self.OutMessages)
        OutMessages = event
        self.OutMessages.append(OutMessages)
        print("debug")
        if Id in self.OutObjectMessages:
            self.OutObjectMessages[Id].append(MessagePos)
        else:
            
            self.OutObjectMessages[Id] = [MessagePos]
        if Type in self.OutTypeMessages:
            self.OutTypeMessages[Type].append(MessagePos)
        else:
            self.OutTypeMessages[Type] = [MessagePos]
        print Type
        print Id
        print Address
        print self.OutObjectMessages
        print self.OutTypeMessages

    def DelInMessage(self, event):
        Object = event.GetEventObject()
        Id = event.GetId()
        Type = event.GetType()
        Address = event.GetAddress()
        if Id in self.OutObjectMessages:
            MessageIndex = self.OutObjectMessages[Id]
            for MsgPos in MessageIndex:
                Msg = self.OutMessages[MsgPos]
                MsgType = Msg.GetType()
                MsgAddress = Msg.GetAddress()
                if MsgType == Type and MsgAddress == Address:
                    self.OutMessages.pop(MsgPos)
                    index = self.SearchIndex(MsgPos, self.OutObjectMessages[Id])
                    if not index == None:
                        self.OutObjectMessages[Id].pop(index)
                        if len(self.OutObjectMessages[Id]) == 0:
                            del self.OutObjectMessages[Id]
                    index = self.SearchIndex(MsgPos, self.OutTypeMessages[Type])
                    if not index == None:
                        self.OutTypeMessages[Type].pop(index)
                        if len(self.OutTypeMessages[Type]) == 0:
                            del self.OutTypeMessages[Type]
                    for elmt in range(MsgPos, len(self.OutMessages)): #Shift all the next elements references -1
                        Elmt = self.OutMessages[elmt]
                        ElmtType = Elmt.GetType()
                        ElmtId = Elmt.GetId()
                        print Elmt.GetAddress()
                        index = SearchIndex(elmt, self.OutObjectMessages[ElmtId])
                        ElmtIndex = self.OutObjectMessages[ElmtId][index]
                        self.self.OutObjectMessages[ElmtId].pop(index)
                        self.self.OutObjectMessages[ElmtId].insert(ElmtIndex - 1, index)
                        index = SearchIndex(elmt, self.OutTypeMessages[ElmtType])
                        ElmtIndex = self.OutTypeMessages[ElmtType][index]
                        self.self.OutTypeMessages[ElmtType].pop(index)
                        self.self.OutTypeMessages[ElmtType].insert(ElmtIndex - 1, index)
                        
                        
    def SearchIndex(self, index, Table):
        result = None
        print("search")
        for i in range(len(Table)):
            print i
            if Table[i] == index:
                print("index found")
                result = i
                return result
