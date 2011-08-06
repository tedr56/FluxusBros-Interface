import wx
from threading import Thread
from rtmidi import MidiMessage

#Event based Message Dispactch Rules Hanlder

#Basic Message Event handles Type,Address,Option
EVT_WIDGET_MESSAGE_ID = wx.NewId()
def EVT_WIDGET_MESSAGE(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MESSAGE_ID, func)

class Message(wx.PyCommandEvent):
    def __init__(self, Object, Id, Type, Address, Option):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_WIDGET_MESSAGE_ID)
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

#Event send by Widgets to record them to the MessageDispatch
EVT_WIDGET_MESSAGE_RECORD_ID = wx.NewId()
def EVT_WIDGET_MESSAGE_RECORD(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MESSAGE_RECORD_ID, func)

class MessageRecord(Message):
    def __init__(self, Object, Id, Type, Address, Option):
        Message.__init__(self, Object, Id, Type, Address, Option)
        self.SetEventType(EVT_WIDGET_MESSAGE_RECORD_ID)

#Event send by Widgets to UNrecord them to the MessageDispatch
EVT_WIDGET_MESSAGE_UNRECORD_ID = wx.NewId()
def EVT_WIDGET_MESSAGE_UNRECORD(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MESSAGE_UNRECORD_ID, func)

class MessageUnRecord(Message):
    def __init__(self, Object, Id, Type, Address, Option):
        Message.__init__(self, Object, Id, Type, Address, Option)
        self.SetEventType(EVT_WIDGET_MESSAGE_UNRECORD_ID)

#Event from Widget to ask their recorded messages
EVT_WIDGET_MESSAGE_GET_ID = wx.NewId()
def EVT_WIDGET_MESSAGE_GET(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MESSAGE_GET_ID, func)

class MessageGet(wx.PyCommandEvent):
    def __init__(self, Object):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_WIDGET_MESSAGE_GET_ID)
        self.SetEventObject(Object)
        self.SetId(Object.GetId())
    def GetId(self):
        return self.Id

#Event from Widget signaling it have been updated
EVT_WIDGET_MESSAGE_UPDATE_ID = wx.NewId()
def EVT_WIDGET_MESSAGE_UPDATE(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MESSAGE_UPDATE_ID, func)

class InternalMessage(wx.PyCommandEvent):
    def __init__(self, Object, Value):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_WIDGET_MESSAGE_UPDATE_ID)
        self.SetEventObject(Object)
        self.SetId(Object.GetId())
        self.Value = Value
    def GetId(self):
        return self.Id
    def GetValue(self):
        return self.Value

#Event send to update Widget value
EVT_WIDGET_UPDATE_ID = wx.NewId()
def EVT_WIDGET_UPDATE(win, func):
    win.Connect(-1, -1, EVT_WIDGET_UPDATE_ID, func)

class WidgetUpdate(Message):
    def __init__(self, Object, Id, Type, Address, Value):
        Message.__init__(self, Object, Id, Type, Address, Value)
        self.SetEventType(EVT_WIDGET_UPDATE_ID)
        self.Value = Value
    def GetId(self):
        return self.Id
    def GetValue(self):
        return self.Value

#External In Midi Event
EVT_EXTERNAL_MIDI_IN_MESSAGE_ID = wx.NewId()
def EVT_EXTERNAL_MIDI_IN_MESSAGE(win, func):
    win.Connect(-1, -1, EVT_EXTERNAL_MIDI_IN_MESSAGE_ID, func)

class ExternalMidiInMessage(wx.PyCommandEvent):
    def __init__(self, midi_message):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_EXTERNAL_MIDI_IN_MESSAGE_ID)
        self.midi_message = midi_message
    def GetMidiMessage(self):
        return self.midi_message

#External Out Midi Event
EVT_EXTERNAL_MIDI_OUT_MESSAGE_ID = wx.NewId()
def EVT_EXTERNAL_MIDI_OUT_MESSAGE(win, func):
    win.Connect(-1, -1, EVT_EXTERNAL_MIDI_OUT_MESSAGE_ID, func)
    
class ExternalMidiOutMessage(wx.PyCommandEvent):
    def __init__(self, midi_message):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_EXTERNAL_MIDI_OUT_MESSAGE_ID)
        self.midi_message = midi_message
    def GetMidiMessage(self):
        return self.midi_message

#Main Messages Dispatch Class
class MessageDispatchRules(wx.PyEvtHandler):
    def __init__(self, parent):
        wx.PyEvtHandler.__init__(self)
        self.parent = parent
        self.OutMessages = []
        self.OutObjectMessages = dict()
        self.OutTypeMessages = dict()
    def SearchIndex(self, index, Table):
        result = None
        for i in range(len(Table)):
            if Table[i] == index:
                result = i
                return result
    def AddInMessage(self, event):
        Object = event.GetEventObject()
        Id = event.GetId()
        Type = event.GetType()
        Address = event.GetAddress()
        Option  = event.GetOption()
        
        MessagePos  = len(self.OutMessages)
        OutMessages = event
        self.OutMessages.append(OutMessages)
        if Id in self.OutObjectMessages:
            self.OutObjectMessages[Id].append(MessagePos)
        else:
            self.OutObjectMessages[Id] = [MessagePos]
        if Type in self.OutTypeMessages:
            self.OutTypeMessages[Type].append(MessagePos)
        else:
            self.OutTypeMessages[Type] = [MessagePos]
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
                        index = SearchIndex(elmt, self.OutObjectMessages[ElmtId])
                        ElmtIndex = self.OutObjectMessages[ElmtId][index]
                        self.self.OutObjectMessages[ElmtId].pop(index)
                        self.self.OutObjectMessages[ElmtId].insert(ElmtIndex - 1, index)
                        index = SearchIndex(elmt, self.OutTypeMessages[ElmtType])
                        ElmtIndex = self.OutTypeMessages[ElmtType][index]
                        self.self.OutTypeMessages[ElmtType].pop(index)
                        self.self.OutTypeMessages[ElmtType].insert(ElmtIndex - 1, index)
    def GetInMessage(self,event):
        Id = event.GetId()
        if Id in self.OutObjectMessages:
            for elmt in self.OutObjectMessages[Id]:
                message = self.OutMessages[elmt]
                wx.PostEvent(message.GetEventObject(), Message(message.GetEventObject(), message.GetId(), message.GetType(), message.GetAddress(), message.GetOption()))
        else:
                wx.PostEvent(event.GetEventObject(), Message(event.GetEventObject(), event.GetId(), None, None, None))
    def InternalMessage(self, event):
        Object = event.GetEventObject()
        Id = event.GetId()
        Value = event.GetValue()
        if Id in self.OutObjectMessages:
            for elmt in self.OutObjectMessages[Id]:
                Elmt = self.OutMessages[elmt]
                ElmtType = Elmt.GetType()
                ElmtAdd  = Elmt.GetAddress()
                ElmtOpt  = Elmt.GetOption()
                self.SendExternalMessage(ElmtType, ElmtAdd, ElmtOpt, Value)
                for subelmt in self.OutTypeMessages[ElmtType]:
                    subElmt = self.OutMessages[subelmt]
                    if subElmt.GetAddress() == ElmtAdd:
                        subElmtObject = subElmt.GetEventObject()
                        wx.PostEvent(subElmtObject, WidgetUpdate(subElmtObject , subElmt.GetId(), subElmt.GetType(), subElmt.GetAddress() ,Value))
    def ExternalMidiInMessage(self, event):
        MidiData = event.GetMidiMessage()
        if MidiData.isController():
            self.ExternalMidiMessageInDispatch('CC', [MidiData.getChannel(), MidiData.getControllerNumber()], MidiData.getControllerValue())
        elif MidiData.isNoteOnOrOff():
            if MidiData.isNoteOn():
                self.ExternalMidiMessageInDispatch('Note', [MidiData.getChannel(), MidiData.getNoteNumber()], MidiData.getVelocity())
            else:
                self.ExternalMidiMessageInDispatch('Note', [MidiData.getChannel(), MidiData.getNoteNumber()], 0)
        elif MidiData.isSysEx():
            self.ExternalMidiMessageInDispatch('SysEx', [0,0], MidiData.getSysExData())
        elif self.IsClockEvent(MidiData):
            self.ExternalMidiMessageInDispatch('Clock', ord(MidiData.getRawData()[0]), 1)
    def ExternalMidiMessageInDispatch(self, Type, Address, Value):
        if Type in self.OutTypeMessages:
            for elmt in self.OutTypeMessages[Type]:
                Elmt = self.OutMessages[elmt]
                if Elmt.GetAddress() == Address:
                    ElmtObject = Elmt.GetEventObject()
                    wx.PostEvent(ElmtObject, WidgetUpdate(ElmtObject , Elmt.GetId(), Type, Address, Value))
    def IsClockEvent(self, data):
        #Clock Raw Data
        #clock tick     = 248(10) F8(16)
        #clock stop     = 252(10) FC(16)
        #clock start    = 250(10) FA(16)
        #clock continue = 251(10) FB(16)
        decoded_data = ord(data.getRawData()[0])
        if decoded_data in [248,250,251,252]:
            return decoded_data
        else:
            return False
    def SendExternalMessage(self, Type, Address, Option, Value):
        if Type == 'CC':
            midi_message = MidiMessage().controllerEvent(Address[0] , Address[1], Value)
            wx.PostEvent(self.parent , ExternalMidiOutMessage(midi_message))
        elif Type == 'Note':
            if Value:
                midi_message = MidiMessage().noteOn(Address[0] , Address[1], Value)
                wx.PostEvent(self.parent , ExternalMidiOutMessage(midi_message))
            else:
                midi_message = MidiMessage().noteOff(Address[0] , Address[1])
                wx.PostEvent(self.parent , ExternalMidiOutMessage(midi_message))
#        elif Type == 
#        print("SendExternalMessage")
#        print Type
#        print Address
#        print Value

