import time
import sys
import os
import json
import getopt

sys.path.append('../')  

from resources.config import init_setup
from resources.control import * #many of these functions are imported for debug purposes.
from resources.utils import serFlush, reg_data_to_int
from resources.fuse_constants import *

#To be adapted according to needs

#@ser_name is to be adapted depending on USB connection. Also it can change in some cases for the same USB port
#BAUD rate has to be in common with the value on the firmware of the Arduino. - Should be good as is.
# ser_name = "/dev/ttyUSB0" #only needed if Arduino not automatically detected.
BAUD = 115200
component_name = "20-U-PG-OB-2400000"
# component_name = "optoboar"
fuse_path = "/V21_fuse_registers.json"


debug = False 

#Sets up the serial communication with the Arduino
ser = init_setup(BAUD)

lpGBT_list = load_lpGBT_list(component_name)
print(lpGBT_list)


#Main program of the E-fuser.
#Depending on the current needs, this function is filled with different functions that execute fusing, reading or any further need.
def main():

    global ser_name
    global config_path
    global component_name
    global fuse_path

    # try:
    #     options, remainder = getopt.getopt(sys.argv[1:],'-o:-s:-f:',['optoboard=','serial=','file'])

    # except:
    #     print("wrong argument")

    # for opt, arg in options:
    #     if opt in ['-o','--optoboard']:
    #         component_name = arg
    #     if opt in ['-s','--serial']:
    #         ser_name = arg
    #     if opt in ['-c','--conffile']:
    #         config_path = os.getcwd() + arg
    #     if opt in ['-f', '--fusefile']:
    #         fuse_path = arg
    
    # #load the fuse registers. This is a list of all registers to be fused with their corresponding values. 
    # with open(os.getcwd() + "/../script" +fuse_path) as g:
    #     fuse_list = json.load(g)

    #Name of the component to be written at. Depending on Optoboard version, this has to be changed.
    #@Adresses of these components are stored in @components.py and already imported in control.py
    
    
    #Just to be sure, clean the line
    serFlush(ser)

    #We force the lpGBT into a state, where it can be fused. Should also work without this. -> Use only, if it doesn't reply otherwise.
    # force_pusm_state_wrapper(lpGBT_list, STATE_WAIT_POWER_GOOD)

    #This checks the value of a crucial register for the lpGBT_V0. If bit0 of this register is =1, fusing is not possible anymore. No issue anymore for lpGBT_V1.
    # read = read_reg_wrapper(lpGBT_list[0],0x0ef) #read Update enable
    # print(read)

    #Read out all the settings in the banks. This is to check the success of the fusing (lpGBT_V0 has 60 banks, lpGBT_V1 has 64)
    # full_read_banks(lpGBT_list)

    #For the search of a slave address. Sweeps over all the possible slave addresses and asks them to print the value sored in ROM. (This value is the same for each lpGBT)
    # for i in range(256):
    #     dev_config(i,0x1d7,0,"r") #read ROM
    #     read = get_answer()
    #     print("contacting: " + str(i) + " reply: " + str(read))

    # fuses_burn_bank(lpGBT_list[0], "0x00", 0x00, [0x00,0x00,0x00,0x00])

    # switchPower("off")
    # switchBootCNF("on")
    # time.sleep(1)
    # switchPower("on")

    # for lpGBT in lpGBT_list:
    #     write_read_reg_wrapper(lpGBT, 0x0f9, 0x0f)
    #     write_read_reg_wrapper(lpGBT, 0x0fa, 0xff)
    #     write_read_reg_wrapper(lpGBT, 0x036, 0x00)
        
    #full_write(lpGBT_list,fuse_list)
	
    # for lpGBT in lpGBT_list:
    #     print("Registers of lpGBT " + lpGBT)
    #     for i in range(471,494):
	   #      value = read_reg(lpGBT, i)
	   #      print("Register: " + hex(i) + " Value: " + hex(value))

    # test_fuses(lpGBT_list[1])

    # switchBootCNF("off")
    # time.sleep(3)
    # switchPower("off")
    # time.sleep(3)
    # switchPower("on")


    #Receive rest of returns for the case, that somehow text was missed.
    time.sleep(1)
    while ser.inWaiting():
        answer = get_answer()
        print(answer)

    return "Executed"



    
main()
