from os import popen, getpid
import rtmidi
import re
#import numpy as np
#import threading
#import wx



#Class to manage MIDI Connections
class Connections:
    def __init__(self, callback, in_midi_wishes=[], out_midi_wishes=[]):
        self.midi_client_name = "FluxusBros-Interface"
        self.midi_in_port_name = "fluxusbros-in"
        self.midi_out_port_name = "fluxusbros-out"
        self.MidiIn = rtmidi.RtMidiIn(self.midi_client_name)
        self.MidiOut = rtmidi.RtMidiOut(self.midi_client_name)
        self.MidiIn.ignoreTypes(0,0,0)
        
        self.callback = callback
        self.MidiIn.setCallback(self.CallBack)
        self.in_ports_connexions =dict()
        self.out_ports_connexions =dict()
        
        self.port_in_wishes = []
        self.port_out_wishes = []
        
        for in_wish in in_midi_wishes:
            self.add_in_port_wish(in_wish)
        for out_wish in out_midi_wishes:
            self.add_out_port_wish(out_wish)
        self.refresh_connections()

    def sendMessage(self, message):
        try:
            self.MidiOut.sendMessage(message)
        except:
            None
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
        #print list(hex(ord (i)) for i in data.getRawData())
        return data
            
    def refresh_connections(self):
        #connect to input port wishes
        for input_port in range(self.MidiIn.getPortCount()):
            input_port_name = self.MidiIn.getPortName(input_port)
            #~ print input_port_name
            #~ print self.port_in_wishes
            #~ if input_port_name in self.port_in_wishes:
                #~ print("Port found")
            if input_port_name in self.port_in_wishes and input_port_name not in self.in_ports_connexions:
                print("Midi Input %s found" % input_port_name)
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
            #~ print output_port_name
            if output_port_name in self.port_out_wishes and output_port_name not in self.out_ports_connexions:
                print("Midi Output %s found" % output_port_name)
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
