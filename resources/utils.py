import time

debug = False

#This document contains some small functions, that execute a certain task, that does not need more information than given from the variables.
#They help the rest of the code to be a bit cleaner.
#====================

#If there is anything from the arduino to the pc in the line, it is read out here and discarded. The goal is to clean the line and see, if any information is missed.
#This prevents the "contamination" of one run to the next.
#@ser: the serial line to be flushed.
def serFlush(ser):
    while ser.inWaiting() > 0:
        flush = ""
        flush += ser.read().decode("utf-8")
        print("flush " + flush)

#====================

#This splits the @val up into up to 4 bytes in order for them to be sent one by one to the arduino.
#Main application is the splitting of the register address (1 time 16bits to 2 times 8bits)
def u32_to_bytes(val):
    """Converts u32 to 4 bytes"""
    byte3 = (val >> 24) & 0xff
    byte2 = (val >> 16) & 0xff
    byte1 = (val >> 8) & 0xff
    byte0 = (val >> 0) & 0xff
    return (byte3, byte2, byte1, byte0)

#====================

#The register data in the .json file are stored sometimes over several different entries when one register contains several configurations in one. This improves readability of the .json file.
#For the program, these values have to be concatenated to one. This happens in this function.
def reg_data_to_int(config_file, reg):

    if isinstance(config_file[reg]["reg_data"], list):
        reg_data = 0
        position = 8    # marks the position of the current bit value in the config
        
        for register in config_file[reg]["reg_data"]:
            position = position - register["size"]
            reg_data = reg_data | register["value"] << position
    else:
        if isinstance(config_file[reg]["reg_data"], int):
            reg_data = config_file[reg]["reg_data"]
        elif (isinstance(config_file[reg]["reg_data"], str) and len(config_file[reg]["reg_data"]) != 8):        # used if register data is written in hex e.g. "0x02" (JSON loads in strings)
            reg_data = int(config_file[reg]["reg_data"],16)
        else:                               # used if register data is written in a string binary e.g. "10101010"
            reg_data = int(config_file[reg]["reg_data"],2)

    return reg_data