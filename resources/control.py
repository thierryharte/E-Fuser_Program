import time
import sys

sys.path.append('../')  

from resources.lpGBT_constants import lpGBT_constants
from resources.components import components
from resources.utils import u32_to_bytes, reg_data_to_int
from resources.fuse_constants import *

lpGBT_reg_addr = lpGBT_constants()      # load class of all lpGBT register addresses

#When debugging the program, more text can be printed out to see the behaviour in more detail. But it slows down the program.
debug = False

global ser

#This document represents the heart of the program. There are functions for communication between the Computer program and the Arduino defined.
#It has a lot of functions, that call each other and are called from different documents.

#========================

#This function is called by @init_config from the @config.py file.
#The sole purpose is to give the same serial communication to this document as there is in each other files.
def init_control(serial):
    global ser
    ser = serial

#========================

#In this function, a start-sequence is added to the string that is to be sent. With this start sequence, the Arduino knows, where the command begins.
def sendToArduino(stringToSend):
    stringToSend.insert(0,0x3C) #start marker: "<"
    if debug==True:
        print("Sending: " + str(stringToSend))
    ser.write(stringToSend) # encode needed for Python3


#====================

#Reads back from the arduino and waits until it got an answer or the timelimit is reached.
#The timelimit is 2 seconds, therefore, this should only be reached, if there is a serious issue in the connection.
def get_answer():
    received = ""
    duration = 0
    timestamp = time.time()
    while(received == "" and duration<2):
        received = read_arduino()  
        duration = time.time() - timestamp
    return received

#==================

#This function is called by @get_answer.
#It defines the process of receiving a reply by reading byte by byte and searching for a start sequence ("<").
#After the start sequence, the stack of bytes, that arrive from the Arduino is read out until it is empty. This means, that also longer sequences can be read out.
#The presence of a start sequence asserts the boolean @dataStarted. If this is asserted, a data buffer is filled and after the read out, the buffer is returned.
def read_arduino():

    dataStarted = False
    messageComplete = False

    dataBuf = ""

    time.sleep(0.001)

    while ser.inWaiting() > 0:
        x = ser.read().decode("ascii") # decode needed for Python3
        if dataStarted == True:
            dataBuf = dataBuf + x
        elif x == chr(0x3C): #start marker: "<"
            dataBuf = ""
            dataStarted = True

    return dataBuf

#====================

#To send a command to the arduino, there is a fixed structure to be considered. This structure is ensured by the following function.
#The structure (Without the start sequence "<" which is added in @sendToArduino), looks as follows:
# - @Mode: The sort of command. (Write read, Write, Read, Fuse, Configure fusepad to lpGBT connection, Power off/on of the E-Fuser, Turning BootCNF on or off)
# - @dev_addr: The Address of the slave to be targetted. This will in most cases be 0x74 through 0x77
# - @reg_addr: The register addresses of the lpGBT are always 16bit long. Therefore, the function @u32_to_bytes is used to split it in bytes.
# - @data: The last part of the message is the value to be stored. This is only used, when a write happens and is set to 0 otherwise.
# The messages for the fusepad configuration, the power on/off and the BootCNF on/off are a bit different. They use the respective positions in the message for all needed information and otherwise contain 0s.
def dev_config(dev_addr, reg_addr, reg_data, reg_wr):

    dev_addr = int(dev_addr)

    if isinstance(reg_addr, str): # in case @reg_addr is a @string, it is converted to @int
        reg_addr = int(reg_addr,16)
    else:
        reg_addr = int(reg_addr)

    if isinstance(reg_data, str): # in case @reg_data is a @string, it is converted to @int
        reg_data = int(reg_data,16)
    else:
        reg_data = int(reg_data)

    addr_low = chr(0x00)
    addr_high = chr(0x00)
    data = reg_data
    read_back = None

    control_w = chr(0x00)

    if reg_wr=="wr":
        mode = 0x41 # 0x41 is A - write/read
    elif reg_wr=="w":
        mode = 0x57 #0x57 is W - write
    elif reg_wr=="r":
        mode = 0x52 # 0x52 is R - read
    elif reg_wr=="f":
        mode = 0x46 # 0x46 is F - fuse (whole process of fusing is directed directly by the arduino)
    elif reg_wr=="c":
        mode = 0x43 # 0x43 is C - to map the fusepads/Arduino pinouts to the respective lpGBTs
    elif reg_wr=="p":
        mode = 0x50 # 0x50 is P - to turn on or turn off the power
    elif reg_wr=="b":
        mode = 0x42 # 0x42 is B - to pull the BOOTCONF0 pad up or down
    elif reg_wr=="t":
        mode = 0x54 # 0x54 is T - to test the FusePins
    else:
        raise Exception('register_data needs to be wr, r, w, f, c, p b or t')

    # divide address into high and low part
    _,_,addr_low,addr_high = u32_to_bytes(reg_addr)

    message = bytearray([mode, dev_addr, addr_high, addr_low, data])

    sendToArduino(message)

#====================

#Prepares the pattern for write/read out a register.
#@component is the slave address to write to
#@reg_addr is the register that is to be written (16bits).
#@reg_data is the data to be written in.
def write_read_reg(component, reg_addr, reg_data):

    dev_addr = components[component]["dev_addr"]

    dev_config(dev_addr, reg_addr, reg_data, "wr")

    read = get_answer()

    return int(read,16)

#====================

#Prepares the write command.
def write_reg(component, reg_addr, reg_data):

    dev_addr = components[component]["dev_addr"]

    dev_config(dev_addr, reg_addr, reg_data, "w")

    return -1

#====================

#Prepares the read command.
def read_reg(component, reg_addr):

    dev_addr = components[component]["dev_addr"]

    dev_config(dev_addr, reg_addr, 0, "r")

    read = get_answer()

    return int(read,16)

#====================

#This function starts the fusing process.
#It is designed to have the command for the fuse start itself sent with it:
# fuse(component,FUSECONTROL, 12<<FUSECONTROL_FUSEBLOWPULSELENGTH_of | FUSECONTROL_FUSEBLOW_bm)
#This is a sort of saveguard that the function is only executed, when desired and it offers debug options, where the fusing does not need to be executed.
def fuse(component, reg_addr, reg_data):

    dev_addr = components[component]["dev_addr"]

    dev_config(dev_addr, reg_addr, reg_data, "f")
    time.sleep(0.1)
    read = get_answer()
    print(read)

    return read

#====================

def test_fuses(component):
    dev_addr = components[component]["dev_addr"]

    dev_config(dev_addr, 0, 0,"t")

    read = get_answer()
    print(read)

    return read

#====================

#The switching of the power connector helps in normal debugging processes.
#Also it enables to test the loaded registers directly after the fusing.
#When the power is turned off, the Arduino is the only component of the E-Fuser still receiving power. This will be used to power cycle the Optoboard.
def switchPower(onoff):
    if onoff=="off":
        command = 0
    else:
        command = 1

    dev_config(command, 0, 0, "p")

    read = get_answer()
    print(read)

    return read

#====================

#This function helps pulling up/down the pin @BOOTCONF0 on the Optoboard.
#The purpose of this is to change the starting behaviour of the optoboard. 
#When the BOOTCONF0 is pulled up, the fuses are not loaded (intended for the fusing process)
#When the BOOTCONF0 is pulled down, the fuses are loaded. - Normal working mode.
def switchBootCNF(onoff):
    if onoff=="off":
        command = 0
    else:
        command = 1
        
    dev_config(command, 0, 0, "b")

    read = get_answer()
    print(read)

    return read

#====================

#The following functions are wrapper functions. Their main use is debugging and adding tests, if the desired process worked.
#@Write_read_reg_wrapper is a wrapper function for the @write_read_reg function.
#@read_back is the main addition, testing, if the write really worked and otherwise repeating the write/read.
def write_read_reg_wrapper(component,addr, val):

    read_back = -1
    duration = 0

    timestamp = time.time()
    while not read_back==val and duration<3:   # in case writing or read-back failes

        read_back = write_read_reg(component, addr, val)
        if debug==True:
            print("value to write :" + hex(val) + " readback: " + hex(read_back))
        duration = time.time()-timestamp

    if duration>=3:
        raise Exception("Wrong answer performing write/read on: " + str(component) + " Register: "+ str(addr) + " Value: " + str(val) + " Read back: " + str(read_back))

    if debug == True:
        print("Write register: " + lpGBT_reg_addr.REG2STR[addr] + "\twith val: " + str(val) + " (" + str(hex(val)) + ")" + "\tread back:\t" + str(read_back)  + " (" + hex(read_back) + ")")
        
    return read_back
#====================

#@read_reg_wrapper is the wrapper function for @read_reg.
#Here only a debug text is added.
def read_reg_wrapper(component,addr):
    read = read_reg(component, addr)

    if debug==True:
        print("Read register: \t" + lpGBT_reg_addr.REG2STR[addr] + "\t\t\t\tread:\t\t" + str(read)  + " (" + hex(read) + ")")

    return read

#====================

#This is the main function for the fusing process.
#First, the bank to be fused is read out with @fuses_read_bank.
#Then the magic number is written to enable the fusing.
#After that, the desired address and values are loaded into the bank registers. 
#Finally the fusing is started using @fuse function. The rest is directed on the Arduino.
#After the fusing, the banks are read out again.
#For further information, see the manual: https://lpgbt.web.cern.ch/lpgbt/v1/configuration.html#e-fuse-programming
def fuses_burn_bank(component,bank_str, address, value_bank):

    print("Efusing bank " + bank_str + "..")

    print("Read " + hex(address) + " before:\t" + str([hex(x) for x in fuses_read_bank(component,address)]))

    print("Values to be fused:\t" + str([hex(x) for x in value_bank]))

    """Burn fuses bank"""
    if address%4 != 0:
        raise Exception("Incorrect address for burn bank! (address=0x%02x)"%address) #check, if the modulo 4 of the address is 0 (only every 4th register is the beginning of a fuse bank.)
    _, _, address_high, address_low = u32_to_bytes(address)

    write_read_reg_wrapper(component,FUSEMAGIC, FUSE_MAGIC_NUMBER)

    write_read_reg_wrapper(component,FUSEBLOWADDH, address_high)
    write_read_reg_wrapper(component,FUSEBLOWADDL, address_low)

    print("Writing FUSEBLOWDATA \n")
    write_read_reg_wrapper(component,FUSEBLOWDATAA, value_bank[0])
    write_read_reg_wrapper(component,FUSEBLOWDATAB, value_bank[1])
    write_read_reg_wrapper(component,FUSEBLOWDATAC, value_bank[2])
    write_read_reg_wrapper(component,FUSEBLOWDATAD, value_bank[3])

    time.sleep(1)

    print("Start Fusing process")
    fuse(component,FUSECONTROL, 12<<FUSECONTROL_FUSEBLOWPULSELENGTH_of | 1)

    print("Read " + hex(address) + " after:\t" + str([hex(x) for x in fuses_read_bank(component,address)]))

    print("\n" + "-"*80 + "\n")

#====================

#With this function, the fuse banks are read out. This is especially practical to check, if the fusing worked without restarting the Optoboard / without having it load the fuses.
#Again the procedure follows to a high degree the manual: https://lpgbt.web.cern.ch/lpgbt/v1/configuration.html#e-fuse-reading
#@return: the values stored in the respective bank as an array
def fuses_read_bank(component,address, timeout=0.05):
    """Read fuses bank"""

    bank_val = [0,0,0,0]

    if address%4 != 0:
        raise Exception("Incorrect address for burn bank! (address=0x%02x)"%address)
        
    _, _, address_high, address_low = u32_to_bytes(address)

    write_read_reg_wrapper(component,FUSECONTROL, FUSECONTROL_FUSEREAD_bm)

    timeout_time = time.time() + timeout

    while True:
        status = read_reg_wrapper(component,FUSESTATUS)
        if status & FUSESTATUS_FUSEDATAVALID_bm:
            #write_read_reg_wrapper(component,FUSECONTROL, 0)
            break

        if time.time() > timeout_time:
            write_read_reg_wrapper(component,FUSECONTROL, 0)
            raise Exception("Timeout while waiting for burning fuses")

    write_read_reg_wrapper(component,FUSEBLOWADDH, address_high)
    write_read_reg_wrapper(component,FUSEBLOWADDL, address_low)

    bank_val[0] = read_reg_wrapper(component,FUSEVALUESA)
    bank_val[1] = read_reg_wrapper(component,FUSEVALUESB)
    bank_val[2] = read_reg_wrapper(component,FUSEVALUESC)
    bank_val[3] = read_reg_wrapper(component,FUSEVALUESD)

    write_read_reg_wrapper(component,FUSECONTROL, 0)

    return bank_val

#====================

#Not every Optoboard has the same amount of lpGBT on it. The numbers are stored in @components.py. From there, the information is read out and a list of active lpGBTs is created.
#Also, the fuse pads are assigned to the respective number of lpGBT and its slave address.
#@return: a array of lpGBT names mounted on the Optoboard.
def load_lpGBT_list(component_name):
    optoboard = components[component_name]
    prefix = ""
    if optoboard["optoboard_v"] == 0:
        set_fuse_channel(component_name, 0x01)
        return [component_name]
    else:
        prefix = "V" + str(optoboard["optoboard_v"]) + "_"
        lpGBT_pattern = [optoboard["lpGBT1"],optoboard["lpGBT2"],optoboard["lpGBT3"],optoboard["lpGBT4"]]
        lpGBT_list=[]

        for i in range(len(lpGBT_pattern)):
            if lpGBT_pattern[i]==1:
                if i == 0:
                    purpose = "master"
                else:
                    purpose = "slave"
                name = prefix + "lpGBT" + str(i+1) + "_" + purpose
                set_fuse_channel(name,i+1)
                time.sleep(0.1)
                lpGBT_list.append(name)

        return lpGBT_list

def load_lpGBT_list_light(component_name):
    optoboard = components[component_name]
    prefix = ""
    if optoboard["optoboard_v"] == 0:
        return [component_name]
    else:
        prefix = "V" + str(optoboard["optoboard_v"]) + "_"
    lpGBT_pattern = [optoboard["lpGBT1"],optoboard["lpGBT2"],optoboard["lpGBT3"],optoboard["lpGBT4"]]
    lpGBT_list=[]

    for i in range(len(lpGBT_pattern)):
        if lpGBT_pattern[i]==1:
            if i == 0:
                purpose = "master"
            else:
                purpose = "slave"
            name = prefix + "lpGBT" + str(i+1) + "_" + purpose
            lpGBT_list.append(name)

    return lpGBT_list

#====================

#Used during the assigning of the lpGBTs mounted on the Optoboard.
#Assignes the corresponding fuse pad to the slave address of the respective lpGBT.
def set_fuse_channel(component, pin_number):

    dev_addr = components[component]["dev_addr"]

    dev_config(dev_addr, pin_number << 8, 0, "c")

    read = get_answer()
    print(read)

    return read

#====================

#Used to enforce a certain state of the Optoboard. This helps the lpGBT to go in a state, in which it can receive a command.
#Until now, it is not needed, but it could become useful one day.
#First function is just a wrapper of the second one. It handles iteration through the full lpGBT_list and issues print statements.
#@lpGBT_list: list of lpGBT on Optoboard
#@state: desired state of PUSM. - 7 is the state WAIT_POWER_GOOD
#@component: one element of lpGBT_list

def force_pusm_state_wrapper(lpGBT_list, state=0x07):
    
    for lpGBT in lpGBT_list:
        status_read = read_reg_wrapper(lpGBT, 0x1d9)
        print("PUSM state before forcing lpGBT "+ lpGBT+": " + str(status_read))
        force_pusm_state(lpGBT, state)
        status_read = read_reg_wrapper(lpGBT, 0x1d9)
        print("PUSM state after forcing lpGBT "+ lpGBT+": " + str(status_read))


def force_pusm_state(component, state):
    FORCESTATE_MAGIC_NUMBER = 0xa3
    POWERUP3_PUSMFORCESTATE_bm = 0x80
    # POWERUP3 = 0x12f # for lpGBTv0
    # POWERUP4 = 0x130
    POWERUP3 = 0x03f
    POWERUP4 = 0x140
    POWERUP3_PUSMSTATEFORCED_of = 0
    write_read_reg_wrapper(component,POWERUP4, FORCESTATE_MAGIC_NUMBER)
    write_read_reg_wrapper(component,POWERUP3, POWERUP3_PUSMFORCESTATE_bm | state << POWERUP3_PUSMSTATEFORCED_of)

#====================

#This function performs a full fusing process based on the .json file loaded in the main function. 
#It will sweep through all the @bank_addr and check in the list, if there is a register to be fused. If not, it will skip the @bank_addr and continue with the next.
#@lpGBT_list: contains the addresses of the lpGBTs mounted on the optoboard. Values typically extracted from @cmponents.py with @load_lpGBT_list
#@fuse_list: contains a data base of the registers and values to be fused. Entries are converted to useful values with @reg_data_to_int.
def full_fuse(lpGBT_list, fuse_list):
    for comp in lpGBT_list:
        for bank_addr in range(64):
            current_bank = "{0:#0{1}x}".format(4*bank_addr,5)
            reg_bank = [0x00,0x00,0x00,0x00]
            fuse_available = False #If this boolean is set True, it means, that the bank needs to be written - that there are registers in it, that need fusing
            for reg in fuse_list:
                if fuse_list[reg]["bank_addr"] == current_bank and fuse_list[reg]["dev"] in comp:
                    if fuse_available == False:
                        print("\n" + "-"*80 + "\n") #print line of dashes to signal the beginn of a new to be fused bank
                    fuse_available = True
                    print(reg)
                    reg_bank[int(fuse_list[reg]["reg_addr"],16)%4] = reg_data_to_int(fuse_list, reg) #store value in corresponding bank register
                    print("Register Address: " + fuse_list[reg]["reg_addr"] +" Register value: "+ str(reg_data_to_int(fuse_list,reg)))
            if fuse_available == False:
                print("No fusing needed for bank: " + str(current_bank))
            else:
                print("fusing is performed")
                fuses_burn_bank(comp, current_bank, int(current_bank,16), reg_bank) #perform the fusing

def full_read_banks(lpGBT_list):
    for component in lpGBT_list:
        print("Banks of component: " + component)
        for reg in range(60): #60 for lpGBT_V0, 64 for lpGBT_V1
            read = fuses_read_bank(component,4*reg) #reading out the fusebanks
            print(str(reg) + ": " +read)

def search_slaves():
    for i in range(256):
        dev_config(i,0x1d7,0,"r") #read ROM
        read = get_answer()
        print("contacting: " + str(i) + " reply: " + str(read))

def full_write(lpGBT_list, fuse_list):
    for comp in lpGBT_list:
        print("Configuring " + comp)
        for reg in fuse_list:
            addr = int(fuse_list[reg]["reg_addr"],16)
            val = reg_data_to_int(fuse_list,reg)
            print("writing register: " + hex(addr) + " with value: " + hex(val))
            write_read_reg_wrapper(comp, addr, val)
