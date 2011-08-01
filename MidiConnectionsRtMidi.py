from os import popen, getpid
import rtmidi
import re
import numpy as np
#import threading
#import wx

FluxusInClient = "FluxusMidi Input Client"
FluxusInPort = "FluxusMidi Input Client:0"
MicroKontrol_Out_Client = "microKontrol"
MicroKontrol_Out_Port = "microKONTROL:1"
VirtualKeyboard_Port = "Virtual Keyboard:0"


#Class to manage MIDI Connections
class Connections:
    def __init__(self, callback):
        self.midi_client_name = "FluxusBros-Interface"
        self.midi_in_port_name = "fluxusbros-in"
        self.midi_out_port_name = "fluxusbros-out"
        self.MidiIn = rtmidi.RtMidiIn(self.midi_client_name)
        self.MidiOut = rtmidi.RtMidiOut(self.midi_client_name)
        self.MidiIn.ignoreTypes(0,0,0)
        #self.MidiIn.closePort()
        #self.MidiOut.closePort()
        
        self.callback = callback
        self.MidiIn.setCallback(self.CallBack)
        self.in_ports_connexions =dict()
        self.out_ports_connexions =dict()
        
        self.port_in_wishes = []
        self.port_out_wishes = []
        
        self.add_in_port_wish(VirtualKeyboard_Port)
        self.add_in_port_wish(MicroKontrol_Out_Port)
        self.add_out_port_wish(FluxusInPort)
        self.refresh_connections()

    def sendMessage(self, message):
        self.MidiOut.sendMessage(message)
    def CallBack(self, data):
        message = self.MidiFormat(data)
        #print message
        self.callback(message)
        
    def MidiFormat(self, data):
#        if data.isController():
#            return str("CC %i %i %i\n" % (data.getChannel(), data.getControllerNumber(), data.getControllerValue()))
#        if data.isSysEx():
#            SysExRaw = data.getSysExData()
#            decoded_SysExRaw = list(hex(ord (i)) for i in SysExRaw)
#            return str("%s\n" % decoded_SysExRaw)
#        else:
#            DataRaw = data.getRawData()
#            print("\n")
#            decoded_DataRaw = list(hex(ord (i)) for i in data.getRawData())
#            return str("%s\n" % decoded_DataRaw)
        print list(hex(ord (i)) for i in data.getRawData())
        return data
            
    def refresh_connections(self):
        #connect to input port wishes
        for input_port in range(self.MidiIn.getPortCount()):
            input_port_name = self.MidiIn.getPortName(input_port)
            #print input_port_name
            if input_port_name in self.port_in_wishes and input_port_name not in self.in_ports_connexions:
                print("%s found" % input_port_name)
                self.connect_input_port(input_port_name, input_port)
        #disconnect connected ports no longer in input port wish list
        input_unwishes = dict()
        for input_connected_port_name, input_connected_port  in self.in_ports_connexions.iteritems():
            if input_connected_port_name not in self.port_in_wishes:
                input_unwishes[input_connected_port_name] = input_connected_port
        for input_connected_port_name, input_connected_port  in input_unwishes:
            self.disconnect_input_port(input_connected_port_name, input_connected_port)

        #connect to output port wishes
        for output_port in range(self.MidiOut.getPortCount()):
            output_port_name = self.MidiOut.getPortName(output_port)
            if output_port_name in self.port_out_wishes and output_port_name not in self.out_ports_connexions:
                print("%s found" % output_port_name)
                self.connect_output_port(output_port_name, output_port)
        #disconnect connected ports no longer in output port wish list
        output_unwishes = dict()
        for output_connected_port_name, output_connected_port  in self.out_ports_connexions.iteritems():
            if output_connected_port_name not in self.port_out_wishes:
                output_unwishes[input_connected_port_name] = output_connected_port
        for output_connected_port_name, output_connected_port  in output_unwishes:
                self.disconnect_output_port(output_connected_port_name, output_connected_port)
        

    def connect_input_port(self, port_name, port):
        self.MidiIn.openPort(port,self.midi_in_port_name)
        self.in_ports_connexions[port_name] = port

    def connect_output_port(self, port_name, port):
        self.MidiOut.openPort(port, self.midi_out_port_name)
        self.out_ports_connexions[port_name] = port

    def disconnect_input_port(self, port_name, port):
        self.MidiIn.closePort()
        del self.in_ports_connexions [port_name]
#        self.refresh_connections()

    def disconnect_output_port(self, port_name, port):
        self.MidiOut.closePort()
        del self.out_ports_connexions [port_name]
#        self.refresh_connections()

    def add_in_port_wish(self, in_wish_port):
        if in_wish_port not in self.port_in_wishes:
            self.port_in_wishes.append(in_wish_port)
            self.refresh_connections()
        
    def add_out_port_wish(self, out_wish_port):
        if out_wish_port not in self.port_in_wishes:
            self.port_out_wishes.append(out_wish_port)
            self.refresh_connections()

    def del_in_port_wish(self, in_wish_port):
        if in_wish_port in self.port_in_wishes:
            self.port_in_wishes.remove(in_wish_port)
            self.refresh_connections()
        
    def del_out_port_wish(self, out_wish_port):
        if out_wish_port in self.port_out_wishes:
            self.port_out_wishes.remove(out_wish_port)
            self.refresh_connections()
