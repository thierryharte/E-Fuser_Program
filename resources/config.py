import serial
import serial.tools.list_ports
import time
import termios
import sys
import json

sys.path.append('../')  

from resources.control import init_control

debug = False

#This document only contains the configuration settings for the Serial line and the setup of the config_file.
#====================

#This function has to be called at the beginning of the program. There, the serial line is opened and with a delay, it is ensured, that the line is established.
#The information of the Serial line is then sent to @control.py by the @init_control function. As the commands are sent from there, the serial line is needed there.
#@return: serial line and config file for the communication and configuration.
def init_setup(baudRate,serName=""):
    if serName=="":
        serName = find_arduino_port()
    f = open(serName)
    attrs = termios.tcgetattr(f)
    attrs[2] = attrs[2] & ~termios.HUPCL
    termios.tcsetattr(f, termios.TCSAFLUSH, attrs)
    f.close()
    
    ser = serial.Serial(port= serName, baudrate = baudRate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

    print("Serial port " + serName + " opened  Baudrate " + str(baudRate))
    print("Wait for Serial port to open")
    
    time.sleep(3)

    init_control(ser)

    return ser

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if '0403' in p[2]:
            print("Arduino found in: ")
            print(p.name)
            ser_name = '/dev/' + p.name
            return ser_name
        else:
            print("Arduino not found in: ")
            print(p.name)
    return ""
