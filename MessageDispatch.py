import wx
#from threading import Thread
from rtmidi import MidiMessage
import  thread
#Event based Message Dispactch Rules Hanlder

#Basic Message Event handles Type,Address,Option
EVT_WIDGET_MESSAGE_ID = wx.NewId()
def EVT_WIDGET_MESSAGE(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MESSAGE_ID, func)

class Message(wx.PyCommandEvent):
    def __init__(self, Object, Id, Type, Address, Option=None):
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
    def __init__(self, Object, Id, Type, Address, Option=None):
        Message.__init__(self, Object, Id, Type, Address, Option)
        self.SetEventType(EVT_WIDGET_MESSAGE_RECORD_ID)

#Event send by Widgets to UNrecord them to the MessageDispatch
EVT_WIDGET_MESSAGE_UNRECORD_ID = wx.NewId()
def EVT_WIDGET_MESSAGE_UNRECORD(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MESSAGE_UNRECORD_ID, func)

class MessageUnRecord(Message):
    def __init__(self, Object, Id, Type=None, Address=None, Option=None):
        Message.__init__(self, Object, Id, Type, Address, Option)
        #~ print("Unrecord Message")
        self.SetEventType(EVT_WIDGET_MESSAGE_UNRECORD_ID)

#Event from Widget to ask their recorded messages
EVT_WIDGET_MESSAGE_GET_ID = wx.NewId()
def EVT_WIDGET_MESSAGE_GET(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MESSAGE_GET_ID, func)

class MessageGet(wx.PyCommandEvent):
    def __init__(self, Object, Source=None):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_WIDGET_MESSAGE_GET_ID)
        self.SetEventObject(Object)
        self.SetId(Object.GetId())
        if Source:
            self.Source = Source
        else:
            self.Source = Object
    def GetId(self):
        return self.Id
    def GetSource(self):
        return self.Source

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

#Media Panel Visu Loading
EVT_WIDGET_MEDIA_MESSAGE_ID = wx.NewId()
def EVT_WIDGET_MEDIA_MESSAGE(win, func):
    win.Connect(-1, -1, EVT_WIDGET_MEDIA_MESSAGE_ID, func)

class MediaMessage(wx.PyCommandEvent):
    def __init__(self, Object, Id, Controls):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_WIDGET_MEDIA_MESSAGE_ID)
        self.SetEventObject(Object)
        self.SetId(Id)
        self.Controls = Controls
    def GetControls(self):
        return self.Controls

#~ TODO : CLEAR Media Message Event

#Threading Midi Messages Class
class MessageDispatch(wx.PyEvtHandler):
    def __init__(self, parent, clock_signature=4):
        #~ thread.__init__()
        wx.PyEvtHandler.__init__(self)
        self.Dispatch = MessageDispatchRules(self)
    def AddInMessage(self, event):
        thread.start_new_thread(self.Dispatch.AddInMessage, (event,))
    def DelInMessage(self, event):
        #~ print("debug MessageDispatch")
        #~ print event
        thread.start_new_thread(self.Dispatch.DelInMessage, (event,))
    def GetInMessage(self,event):
        thread.start_new_thread(self.Dispatch.GetInMessage, (event,))
    def InternalMessage(self, event):
        thread.start_new_thread(self.Dispatch.InternalMessage, (event,))
        #~ thread.start_new_thread(self.Dispatch.InternalMessage, (1,2))
    def ExternalMidiInMessage(self, event):
        thread.start_new_thread(self.Dispatch.ExternalMidiInMessage, (event,))
    #~ def ExternalMidiMessageInDispatch(self, Type, Address, Value):
    #~ def SendExternalMessage(self, Type, Address, Option, Value):
    
#Main Messages Dispatch Class
class MessageDispatchRules(wx.PyEvtHandler):
    def __init__(self, parent, clock_signature=4):
        wx.PyEvtHandler.__init__(self)
        self.parent = parent
        self.Id = wx.NewId()
        self.OutMessages = []
        self.OutObjectMessages = dict()
        self.OutTypeMessages = dict()
        self.Sequences = []
    def GetId(self):
        return self.Id
    def AddSequencer(self, event):
        self.Sequences.append(event)
    def AddSequence(self, event):
        #~ print("Add Sequence Dispatch")
        Object = event.GetEventObject()
        ObjectId = event.GetId()
        #~ print("Dispatch")
        #~ print self.Id
        #~ print("Emitter")
        #~ print ObjectId
        #~ print self.OutObjectMessages
        for Seq in self.Sequences:
            wx.PostEvent(Seq.GetEventObject(), MessageSequencerRecord(Object, event.GetValue()))
        if ObjectId in self.OutObjectMessages:
            for obj in self.OutObjectMessages[ObjectId]:
                EmitterObject = self.OutMessages[obj]
                for type_object in self.OutTypeMessages[self.OutMessages[obj].GetType()]:
                    InternalObject = self.OutMessages[type_object]
                    if not InternalObject.GetId() == ObjectId:
                        if InternalObject.GetAddress() == EmitterObject.GetAddress():
                            #~ print("Send RecordSequence to")
                            #~ print InternalObject.GetId()
                            #~ print InternalObject.GetType()
                            #~ print InternalObject.GetAddress()
                            wx.PostEvent(InternalObject.GetEventObject(), MessageSequencerRecord(EmitterObject.GetEventObject(), event.GetValue()))
    def DelSequence(self, event):
        Object = event.GetEventObject()
        ObjectId = event.GetId()
        #~ print("Dispatch")
        #~ print self.Id
        #~ print("Emitter")
        #~ print ObjectId
        #~ print self.OutObjectMessages
        if ObjectId in self.OutObjectMessages:
            for obj in self.OutObjectMessages[ObjectId]:
                EmitterObject = self.OutMessages[obj]
                for type_object in self.OutTypeMessages[self.OutMessages[obj].GetType()]:
                    InternalObject = self.OutMessages[type_object]
                    if not InternalObject.GetId() == ObjectId:
                        if InternalObject.GetAddress() == EmitterObject.GetAddress():
                            #~ print("Send UnRecordSequence to")
                            #~ print InternalObject.GetId()
                            #~ print InternalObject.GetType()
                            #~ print InternalObject.GetAddress()
                            wx.PostEvent(InternalObject.GetEventObject(), MessageSequencerUnRecord(EmitterObject.GetEventObject()))
    def SearchIndex(self, val, Table):
        #~ TODO - Switch this function with list.index(x) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~&
        #~ Result = None
        try:
            Result = Table.index(val)
        except:
            Result = None
        #~ Result = None
        #~ for i in range(len(Table)):
            #~ if Table[i] == val:
                #~ Result = i
                #~ break
        return Result
    def AddInMessage(self, event):
        Object = event.GetEventObject()
        Id = event.GetId()
        Type = event.GetType()
        Address = event.GetAddress()
        Option  = event.GetOption()
        MessageAlreadyRecorded = False
        #~ print("AddInMessage debug")
        #~ print Id
        #~ print Type
        #~ print Address
        if Id in self.OutObjectMessages:
            for e in self.OutObjectMessages[Id]:
                evt = self.OutMessages[e]
                if evt.GetType() == Type and evt.GetAddress() == Address and evt.GetOption() == Option:
                    print("Message Already Registered")
                    MessageAlreadyRecorded = True
                    break
        if not MessageAlreadyRecorded:
            MessagePos  = len(self.OutMessages)
            self.OutMessages.append(event)
            if Id in self.OutObjectMessages:
                self.OutObjectMessages[Id].append(MessagePos)
            else:
                self.OutObjectMessages[Id] = [MessagePos]
            if Type in self.OutTypeMessages:
                self.OutTypeMessages[Type].append(MessagePos)
            else:
                self.OutTypeMessages[Type] = [MessagePos]
            if not Object.GetRecording():
                for o in self.OutTypeMessages[Type]:
                    InternalObject = self.OutMessages[o]
                    if not InternalObject.GetId() == Id:
                        if InternalObject.GetAddress() == Address:
                            if InternalObject.GetEventObject().GetRecording():
                                wx.PostEvent(Object, MessageSequencerRecord(InternalObject.GetEventObject(), InternalObject.GetEventObject().GetValue()))
                                break
            #~ print self.OutObjectMessages
    def GetTypeInMessages(self):
        return self.OutTypeMessages
    def GetInMessages(self):
        return self.OutObjectMessages
    def DelInMessage(self, event):
        #~ print("DelInMessage")
        #~ print self.OutObjectMessages
        #~ print self.OutTypeMessages
        Id = event.GetId()
        Type = event.GetType()
        Address = event.GetAddress()
        if Id in self.OutObjectMessages:
            MessageIndex = self.OutObjectMessages[Id]
            #~ if not Type and not Address and len(MessageIndex) == 1:
                #~ Index = MessageIndex[0]
                #~ DefaultMsg = self.OutMessages[Index]
                #~ Type = DefaultMsg.GetType()
                #~ Address = DefaultMsg.GetAddress()
                #~ print("MonoSub")
                #~ print Type
                #~ print Address
            for MsgPos in MessageIndex:
                Msg = self.OutMessages[MsgPos]
                MsgType = Msg.GetType()
                MsgAddress = Msg.GetAddress()
                if (MsgType == Type and MsgAddress == Address) or (Type == None and Address == None):
                    self.OutMessages.pop(MsgPos)
                    index = self.SearchIndex(MsgPos, self.OutObjectMessages[Id])
                    if not index == None:
                        self.OutObjectMessages[Id].pop(index)
                        if len(self.OutObjectMessages[Id]) == 0:
                            del self.OutObjectMessages[Id]
                    index = self.SearchIndex(MsgPos, self.OutTypeMessages[MsgType])
                    if not index == None:
                        self.OutTypeMessages[MsgType].pop(index)
#~ TODO : Remplacer la recherche par Type par Objet/Id dans self.OutMessages (cf ligne 256)    
                        if len(self.OutTypeMessages[MsgType]) == 0:
                            del self.OutTypeMessages[MsgType]
                    #~ print self.OutObjectMessages
                    #~ print self.OutTypeMessages
                    #~ print range(MsgPos+1, len(self.OutMessages)+1)
                    for elmt in range(MsgPos, len(self.OutMessages)): #Shift all the next elements references -1
                        #~ print("Num : %i" % elmt)
                        Elmt = self.OutMessages[elmt]
                        ElmtType = Elmt.GetType()
                        ElmtId = Elmt.GetId()
                        #~ print("ElmtId : %i" % ElmtId)
                        index2 = self.SearchIndex(elmt+1, self.OutObjectMessages[ElmtId])
                        if not index2 == None:
                            ElmtIndex = self.OutObjectMessages[ElmtId][index2]
                            #~ print("ElmtObjectIndex: %i" % ElmtIndex)
                            #~ print("ElmtObjectIndex-: %i" % (ElmtIndex-1))
                            self.OutObjectMessages[ElmtId].pop(index2)
                            self.OutObjectMessages[ElmtId].insert(index2, (ElmtIndex-1))
                            index3 = self.SearchIndex(elmt+1, self.OutTypeMessages[ElmtType])
                            if not index3 == None:
                                ElmtIndex = self.OutTypeMessages[ElmtType][index3]
                                #~ print("ElmtTypeIndex: %i" % ElmtIndex)
                                self.OutTypeMessages[ElmtType].pop(index3)
                                self.OutTypeMessages[ElmtType].insert(index3, (ElmtIndex-1))
    def GetInMessage(self,event):
        Id = event.GetId()
        if Id in self.OutObjectMessages:
            for elmt in self.OutObjectMessages[Id]:
                message = self.OutMessages[elmt]
                wx.PostEvent(event.GetSource(), Message(message.GetEventObject(), message.GetId(), message.GetType(), message.GetAddress(), message.GetOption()))
        else:
                wx.PostEvent(event.GetSource(), Message(event.GetEventObject(), event.GetId(), None, None, None))
    def InternalMessage(self, event):
        #~ print("Internal Message")
        #~ Object = event.GetEventObject()
        Id = event.GetId()
        Value = event.GetValue()
        #~ print Object
        #~ print Id 
        #~ print Value
        if Id in self.OutObjectMessages:
            #~ print self.OutObjectMessages
            for elmt in self.OutObjectMessages[Id]:
                Elmt = self.OutMessages[elmt]
                ElmtType = Elmt.GetType()
                ElmtAdd  = Elmt.GetAddress()
                ElmtOpt  = Elmt.GetOption()
                self.SendExternalMessage(ElmtType, ElmtAdd, ElmtOpt, Value)
                for subelmt in self.OutTypeMessages[ElmtType]:
                    subElmt = self.OutMessages[subelmt]
                    if subElmt.GetAddress() == ElmtAdd and not subElmt.GetId() == Id:
                        #~ print("SubElmt")
                        #~ print subElmt.GetId()
                        
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
                #~ print Address[0]
                #~ print Address[1]
                #~ print Value
                midi_message = MidiMessage().noteOn(Address[0] , Address[1], Value)
                wx.PostEvent(self.parent , ExternalMidiOutMessage(midi_message))
            else:
                midi_message = MidiMessage().noteOff(Address[0] , Address[1])
                wx.PostEvent(self.parent , ExternalMidiOutMessage(midi_message))
        elif Type == 'Clock':
            if Address == 248:
                midi_message = MidiMessage().midiClock()
                wx.PostEvent(self.parent , ExternalMidiOutMessage(midi_message))
#        elif Type == 
#        print("SendExternalMessage")
#        print Type
#        print Address
#        print Value


EVT_WIDGET_SEQUENCER_MESSAGE_RECORD_ID = wx.NewId()
def EVT_WIDGET_SEQUENCER_MESSAGE_RECORD(win, func):
    win.Connect(-1, -1, EVT_WIDGET_SEQUENCER_MESSAGE_RECORD_ID, func)

class MessageSequencerRecord(wx.PyCommandEvent):
    def __init__(self, Object, value):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_WIDGET_SEQUENCER_MESSAGE_RECORD_ID)
        self.SetEventObject(Object)
        self.SetId(Object.GetId())
        self.Value = value
    def GetValue(self):
        return self.Value

EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD_ID = wx.NewId()
def EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(win, func):
    win.Connect(-1, -1, EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD_ID, func)

class MessageSequencerUnRecord(wx.PyCommandEvent):
    def __init__(self, Object):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD_ID)
        self.SetEventObject(Object)
        self.SetId(Object.GetId())

EVT_WIDGET_SEQUENCER_RECORD_ID = wx.NewId()
def EVT_WIDGET_SEQUENCER_RECORD(win, func):
    win.Connect(-1, -1, EVT_WIDGET_SEQUENCER_RECORD_ID, func)

class SequencerRecord(wx.PyCommandEvent):
    def __init__(self, Object):
        wx.PyCommandEvent.__init__(self)
        self.SetEventType(EVT_WIDGET_SEQUENCER_RECORD_ID)
        self.SetEventObject(Object)
        self.SetId(Object.GetId())
