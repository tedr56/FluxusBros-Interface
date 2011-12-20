#!/usr/bin/python

from os import popen
import os.path
import wx
from wx import xrc
import re
import rtmidi
from MidiConnectionsRtMidi import Connections
from MessageDispatch import *
from ClockGui import ClockControl
from MediaGui import MediaPanel
from ControlsGui import ControlsPanel
from TableGui import TablePanel
from SequencerGui import SequencerPanel
from configobj import ConfigObj
from CustomWidgets import wxFader
from CustomWidgets import wxKnob
from CustomWidgets import wxPiano
from CustomWidgetsXRC import wxFaderCtrlXmlHandler
from CustomWidgetsXRC import wxKnobCtrlXmlHandler
from CustomWidgetsXRC import wxPianoCtrlXmlHandler
from CustomWidgetsXRC import wxMediaVisualCtrlXmlHandler
APP_SIZE_X = 900
APP_SIZE_Y = 400

FluxusInClient = "FluxusMidi Input Client"
FluxusInPort = "FluxusMidi Input Client:0"
MicroKontrol_Out_Client = "microKontrol"
MicroKontrol_Out_Port = "microKONTROL:1"
Bitstream_Out_Port = "Bitstream 3X:0"
VirtualKeyboard_Port = "Virtual Keyboard:0"
Kmidimon_Port = "KMidimon:0"
NanoKontrolPort = "nanoKONTROL:0"
LMMSPort = "LMMS:1"

INMIDIPORT = [MicroKontrol_Out_Port , Bitstream_Out_Port , VirtualKeyboard_Port , NanoKontrolPort]
OUTMIDIPORT = [FluxusInPort , Kmidimon_Port, LMMSPort]

DEFAULT_PLAYERS = ["Korg" , "VMXVJ" , "BitStream"]
DEFAULT_PROFILE = ["Layer 1"]

global FLUXUSBROS_DIRECTORY
FLUXUSBROS_DIRECTORY = "~/Sources/git/FluxusBros"
global FLUXUSBROS_INTERFACE_DIRECTORY
FLUXUSBROS_INTERFACE_DIRECTORY = "~/Sources/git/FluxusBros-Interface"

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        self.cfg = ConfigObj("./config.cfg")
        
        self.InitFrame(parent, ID, title)
        
        self.Dispatch = MessageDispatchRules(self)
        #~ self.Dispatch = MessageDispatch(self)
        
        EVT_WIDGET_MESSAGE_RECORD(self, self.Dispatch.AddInMessage)
        EVT_WIDGET_MESSAGE_UNRECORD(self, self.Dispatch.DelInMessage)
        EVT_WIDGET_MESSAGE_GET(self, self.Dispatch.GetInMessage)
        EVT_WIDGET_MESSAGE_UPDATE(self, self.Dispatch.InternalMessage)
        EVT_EXTERNAL_MIDI_IN_MESSAGE(self, self.Dispatch.ExternalMidiInMessage)
        EVT_EXTERNAL_MIDI_OUT_MESSAGE(self, self.MidiOutputRefresh)
        
        EVT_WIDGET_SEQUENCER_RECORD(self, self.Dispatch.AddSequencer)
        EVT_WIDGET_SEQUENCER_MESSAGE_RECORD(self, self.Dispatch.AddSequence)
        EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(self, self.Dispatch.DelSequence)
        
        self.InitConfig(parent, ID, title)
    def InitFrame(self, parent, ID, title):
        global FLUXUSBROS_DIRECTORY
        global FLUXUSBROS_INTERFACE_DIRECTORY
        try:
            print("Config File")
            w , h = self.cfg['App'].as_int('width'), self.cfg['App'].as_int('height')
            FLUXUSBROS_DIRECTORY = self.cfg['App']['FluxusBros_Directory']
            FLUXUSBROS_INTERFACE_DIRECTORY = self.cfg['App']['FluxusBros_Interface_Directory']
        except:
            print("Defaults")
            w, h = (APP_SIZE_X, APP_SIZE_Y)
            self.cfg['App'] = {}
            self.cfg['App']['width'] = w
            self.cfg['App']['height'] = h
            self.cfg['App']['FluxusBros_Directory'] = FLUXUSBROS_DIRECTORY
            self.cfg['App']['FluxusBros_Interface_Directory'] = FLUXUSBROS_INTERFACE_DIRECTORY
            self.cfg.write()
            FLUXUSBROS_DIRECTORY = self.cfg['App']['FluxusBros_Directory']
            FLUXUSBROS_INTERFACE_DIRECTORY = self.cfg['App']['FluxusBros_Interface_Directory']
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, wx.Size(w, h))
    def InitConfig(self, parent, ID, title):
        try:
            inmidiport = self.cfg['MidiPort'].as_list('InPort')
            outmidiport = self.cfg['MidiPort'].as_list('OutPort')
        except:
            inmidiport = INMIDIPORT
            outmidiport = OUTMIDIPORT
            self.cfg['MidiPort']={}
            self.cfg['MidiPort']['InPort'] = inmidiport
            self.cfg['MidiPort']['OutPort'] = outmidiport
            self.cfg.write()
        self.InitMidi(inmidiport, outmidiport)
        try:
            self.Players = self.cfg.as_list('Players')
        except:
            self.Players = DEFAULT_PLAYERS
            self.cfg['Players'] = self.Players
            self.cfg.write()
        try:
            self.DefaultPlayer = self.cfg['DefaultPlayer']
        except:
            self.DefaultPlayer = self.cfg.as_list('Players')[1]
            self.cfg['DefaultPlayer'] = self.DefaultPlayer
            self.cfg.write()
        try:
            self.Player = self.cfg[self.DefaultPlayer]
        except:
            self.cfg[self.DefaultPlayer] = {}
            self.cfg.write()
            self.Player = self.cfg[self.DefaultPlayer]
        self.SetPlayerName(self.DefaultPlayer)
        try:
            self.Layers = self.cfg[self.DefaultPlayer]['Layers'].keys()
            self.DefaultLayer = self.cfg[self.DefaultPlayer]['DefaultLayer']
            self.Layer = self.cfg[self.DefaultPlayer]['Layers'][self.DefaultLayer]
        except:
            self.cfg[self.DefaultPlayer]['Layers'] = {}
            self.cfg[self.DefaultPlayer]['Layers']['Layer 1'] = {}
            self.cfg[self.DefaultPlayer]['DefaultLayer'] = self.cfg[self.DefaultPlayer]['Layers'].keys()[0]
            self.cfg.write()
            self.Layers = self.cfg[self.DefaultPlayer]['Layers'].keys()
            self.DefaultLayer = self.cfg[self.DefaultPlayer]['DefaultLayer']
            self.Layer = self.cfg[self.DefaultPlayer]['Layers'][self.DefaultLayer]
        self.SetLayerName(self.DefaultLayer)
        try:
            Medias = self.Layer['Media']
        except:
            self.Layer['Media'] = {}
            self.cfg.write()
            Medias = self.Layer['Media']
        self.InitPanels()
    def InitMidi(self, inmidi=[], outmidi=[]):
        self.MidiConnect = Connections(self.MidiInputRefresh, inmidi, outmidi)
    def MidiInputRefresh(self, midi_data):
        wx.PostEvent(self, ExternalMidiInMessage(midi_data))
    def MidiOutputRefresh(self, event):
        self.MidiConnect.sendMessage(event.GetMidiMessage())
    def InitPanels(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        toolbar = self.InitToolBar()
        vbox.Add(toolbar, 0, wx.EXPAND)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        #~ self.Media = MediaPanel(self)
        self.Table = self.LoadTable(self.GetPlayerName(), self.GetLayerName())
        #~ print("debug")
        #~ print self.Layers
        #~ print self.Layer
        #~ print self.GetLayerName()
        #~ print self.GetPlayerName() + '-' + self.GetLayerName()
        self.Sequencer = SequencerPanel(self)
        #~ hbox.Add(self.Media, proportion = 0)
        self.TableBox = wx.BoxSizer(wx.VERTICAL)
        #~ TableBox.Add(self.Controls, proportion = 1, flag=wx.EXPAND)
        self.TableBox.Add(self.Table, proportion = 2, flag=wx.EXPAND)
        hbox.Add(self.TableBox, 2, wx.EXPAND)
        hbox.Add(self.Sequencer, proportion = 1, flag=wx.EXPAND)
        vbox.Add(hbox, proportion=-1, flag=wx.EXPAND)
        self.SetSizer(vbox)
        #~ EVT_WIDGET_SEQUENCER_MESSAGE_RECORD(self, self.Sequencer.InitSequence)
        #~ EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(self, self.Sequencer.DelSequence)
    def LoadTable(self, player, layer):
        xrc_path = player + '-' + layer + '.xrc'
        if os.path.exists(xrc_path):
            res = xrc.XmlResource(xrc_path)
            res.InsertHandler(wxKnobCtrlXmlHandler())
            res.InsertHandler(wxFaderCtrlXmlHandler())
            res.InsertHandler(wxPianoCtrlXmlHandler())
            res.InsertHandler(wxMediaVisualCtrlXmlHandler())
            Table = res.LoadPanel(self, 'TablePanel')
            return Table
        else:
            DefaultPanel = wx.Panel(self)
            hbox = wx.BoxSizer(wx.VERTICAL)
            DefaultPanelMsg1 = wx.StaticText(DefaultPanel, -1, "Missing XRC Xml Ressource File : ")
            DefaultPanelMsg2 = wx.TextCtrl(DefaultPanel, -1, xrc_path, style=wx.TE_READONLY)
            hbox.Add(DefaultPanelMsg1,proportion=0)
            hbox.Add(DefaultPanelMsg2, 0, wx.EXPAND)
            DefaultPanel.SetSizer(hbox)
            return DefaultPanel
    def InitToolBar(self):
        toolbar = wx.ToolBar(self, -1)
        TOOL_ID = wx.NewId()
        TOOL_ID_PLAYER_COMBO = wx.NewId()
        self.PlayerCombo = wx.ComboBox(toolbar, TOOL_ID_PLAYER_COMBO, choices = self.Players)
        self.PlayerCombo.SetStringSelection(self.GetPlayerName())
        toolbar.AddControl(self.PlayerCombo)
        wx.EVT_COMBOBOX(self, TOOL_ID_PLAYER_COMBO, self.SetPlayer)
        
        TOOL_ID_COMBO_LAYERS = wx.NewId()
        self.LayerCombo = wx.ComboBox(toolbar, TOOL_ID_COMBO_LAYERS, choices = self.Layers)
        self.LayerCombo.SetStringSelection(self.DefaultLayer)
        toolbar.AddControl(self.LayerCombo)
        wx.EVT_COMBOBOX(self, TOOL_ID_COMBO_LAYERS, self.SetLayer)
        
        Clock = ClockControl(toolbar, wx.NewId())
        toolbar.AddControl(Clock)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_OTHER, (16, 16))
        toolbar.AddSeparator()
        ToolbarPreferences = toolbar.AddLabelTool(-1, 'Preferences', bmp, shortHelp='Preferences')
        #~ self.Bind(wx.EVT_MENU, self.onPrint, printTool)
        toolbar.Realize()
        return toolbar
    def SetComboLayers(self):
        self.LayerCombo.Clear()
        self.SetLayers()
        self.LayerCombo.Append(self.Layer)
        self.LayerCombo.SetSelection(0)
        self.SetLayer(0)
    def SetLayers(self):
        try:
            self.Layers = self.cfg[self.GetPlayerName()]['Layers'].keys()
            self.DefaultLayer = self.cfg[self.GetPlayerName()]['DefaultLayer']
            self.Layer = self.DefaultLayer
        except:
            self.cfg[self.GetPlayerName()]['Layers'] = {}
            self.cfg[self.GetPlayerName()]['Layers']['Layer 1'] = {}
            self.cfg[self.GetPlayerName()]['DefaultLayer'] = self.cfg[self.GetPlayerName()]['Layers'].keys()[0]
            self.cfg.write()
            self.Layers = self.cfg[self.GetPlayerName()]['Layers'].keys()
            self.DefaultLayer = self.cfg[self.GetPlayerName()]['DefaultLayer']
            print self.DefaultLayer
            self.Layer = self.DefaultLayer
    def SetPlayer(self, event):
        print("New Player : %s" % event.GetEventObject().GetValue())
        self.SetPlayerName(event.GetEventObject().GetValue())
        try:
            self.Player = self.cfg[self.GetPlayerName()]
        except:
            self.cfg[self.GetPlayerName()] = {}
            self.cfg.write()
            self.Player = self.cfg[self.GetPlayerName()]
        
        self.SetComboLayers()
        #~ self.SetLayer(0)
    def GetPlayer(self):
        return self.Player
    def SetPlayerName(self, name):
        self.PlayerName = name
    def GetPlayerName(self):
        return self.PlayerName
    def SetLayer(self, event):
        self.SetLayerName(self.LayerCombo.GetValue())
        NewTable = self.LoadTable(self.GetPlayerName(), self.GetLayerName())
        self.TableBox.Replace(self.Table, NewTable)
        self.TableBox.Layout()
        self.Table.DestroyChildren()
        self.Table.Destroy()
        self.Table = NewTable
    def SetLayerName(self, name):
        self.LayerName = name
    def GetLayerName(self):
        return self.LayerName
class MyApp(wx.App):
    def OnInit(self, *args, **kwargs):
        self.MainFrame = MyFrame(None, -1, "FluxusBros Interface")
        self.MainFrame.Show(True)
        self.SetTopWindow(self.MainFrame)
        return True

app = MyApp(0)
app.MainLoop()
