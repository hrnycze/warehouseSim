import FOCAS
import time
import subprocess           # to open cnc_emulator
import sys                  # pro ukončení funkce v případě chyby

##################################################################################################
# Program manipulation
##################################################################################################

def Download(FlibHndl: int, filePath: str, dir_name: str = "//CNC_MEM/USER/PATH1/", sType: int = 0) -> bool:
    '''
    This function download NC program into machine.

    # Parameters:

        FlibHndl (int):     Library handle.
        file_path (string): Addresss of NC program in PC.  (C:/Users/NC program/O0031.txt") 
        dir_name (string):  Specify a destination folder name for download. ("//CNC_MEM/USER/PATH2/")
        sType (short):      Specify the kind of the data.
            - 0:    NC program
            - 1:	Tool offset data
            - 2:	Parameter
            - 3:	Pitch error compensation data
            - 4:	Custom macro variables
            - 5:	Work zero offset data
            - 18:	Rotary table dynamic fixture offset
    Returns:

        (bool): True/False
    
    '''
    # sequence of FOCAS functions which downloads the function
    ret = FOCAS.DwnStart4(FlibHndl, dir_name, sType)
    # Check the return value
    if ret != 0:
        print("Error in cnc_dwnstart4. Error number", ret)
        #detailed error info
        FOCAS.get_detailed_err(FlibHndl)
        return False

    ret = FOCAS.Download4(FlibHndl, filePath)
    # Check the return value
    if ret != 0:
        print("Error in cnc_download4. Error number", ret)
        #detailed error info
        FOCAS.get_detailed_err(FlibHndl)
        return False

    ret = FOCAS.DwnEnd4(FlibHndl)
    # Check the return value
    if ret != 0:
        print("Error in cnc_dwnend4. Error number", ret)
        #detailed error info
        FOCAS.get_detailed_err(FlibHndl)
        return False

    return True

def VerifyProg(FlibHndl: int, file_path: str, dir_name: str = "//CNC_MEM/USER/PATH1/") -> bool:
    '''
    This function verifies NC program in PC with NC program downloaded into CNC.
    
    # Parameters:

        FlibHndl (int):     Library handle.
        file_path (string): Addresss of NC program in PC.  (C:/Users/NC program/O0031.txt")  
        dir_name (string):  Specify a destination folder name for verifying. ("//CNC_MEM/USER/PATH2/")  
    
    # Return:

        (bool):             True/False

    '''
    # sequence of FOCAS functions which downloads the function
    #verification start
    ret = FOCAS.VrfStart4(FlibHndl, dir_name)

    # Check the return value
    if ret != 0:
        print(f"Error in cnc_vrfstart4: {ret}")
        #detailed error info
        FOCAS.get_detailed_err(FlibHndl)
        return False

    # verification            
    ret = FOCAS.Vrf4(FlibHndl, file_path)

    # Check the return value
    if ret != 0:
        print("Error in cnc_verify4. Error number ", ret)
        #detailed error info
        FOCAS.get_detailed_err(FlibHndl)
        return False

    # verification end
    ret = FOCAS.VrfEnd4(FlibHndl)
    # Check the return value
    if ret != 0:
        print(f"Error in cnc_vrfend4: {ret}")
        #detailed error info
        FOCAS.get_detailed_err(FlibHndl)
        return False
    else:
        return True

def SelectMain(FlibHndl: int, file_path: str) -> bool:
    '''
    This function selects main program in CNC and after selection it checks actual selected program. 

    # Important!!!

    There is unsolved problem with decoding when the number of NC program in i format O0031 it decodes returned address in following format: O31. Therefore its important to write NC program name with full with number as long as number of its digits like O3001.

    # Parameters:

        FlibHndl (int):     Library handle.
        file_path (string): Specify a destination folder name for verifying. ("//CNC_MEM/USER/PATH2/O3100")  
    
    # Returns:
    
        (bool):             True/False function succesful/unsuccesful

    '''
    ret = FOCAS.SlctMain(FlibHndl, file_path)
    if ret != 0:
        print(f"Error in cnc_pdf_slctmain: {ret}")
        #detailed error info
        FOCAS.get_detailed_err(FlibHndl)
        return False
    
    # validation of main program
    main_path, ret = FOCAS.RdMain(FlibHndl)

    # error 
    if main_path == file_path and ret == 0:
        # print("Main program control succesful.")
        return True
    elif main_path != file_path and ret == 0:
        print("Main program is not selected.")
        return False
    else:
        print(f"Error in cnc_pdf_rdmain: {ret}")
        #detailed error info
        FOCAS.get_detailed_err(FlibHndl)
        return False

def DeleteProg(FlibHndl: int, file_path: str) -> bool:
    '''
    Deletes the folder or file under the specified folder.

    # Parameters:

        FlibHndl (int):     Library handle.
        file_path (string): Specify a NC program destination in format "Current drive + folder + file name". ("//CNC_MEM/USER/PATH2/O3000")  
    
    # Returns:

        (bool):             True/False

    '''

    # doplnit bezpečnostní prvky


    ret = FOCAS.Delete(FlibHndl, file_path)
    if ret != 0:
        print(f"Error in cnc_pdf_del: {ret}")
        #detailed error info
        FOCAS.get_detailed_err(FlibHndl)
        return False
    else:
        return True
    
##################################################################################################
# CNC control
##################################################################################################

def System_state(FlibHndl: int)->int:
    '''
    Function returns state of the CNC system.

    # Parametres:

        FlibHndl (int):   Library handle.

    # Returns:

        state: state of the CNC
        - 0: CNC is ready to start NC program state detection 
        - 1: CNC is in operation mode
        - 2: CNC is in automatic cycle mode and CYCLE stop is on
        - 3: CNC fail mode detection (CNC is in different not ordinary state)
    '''

    data,ret = FOCAS.read_pmc_data_adress(FlibHndl, 2, 8)
    if ret != True :
        # validation of data
        print("read PMC address fail")
        state = 3
        return state 
    
    SPL = True_bit_detect(data,0)   # Feed hold signal (CNC will inform the PLC that feed hold is given by user)
    STL = True_bit_detect(data,1)   # Cycle start signal ( Through this signal, CNC will inform the PMC that automatic operation is started.)
    SA  = True_bit_detect(data,4)   # Servo ready signal (Through this signal, CNC will inform the PMC that servo system is ready  to operate. Apply brake to servo motors, when this signal is 0)
    MA  = True_bit_detect(data,5)   # Machine ready (Through this signal, CNC will inform to PMC that CNC is read to operate)    
    OP  = True_bit_detect(data,6)   # Automatic operation signal (This signal gets ON, when the automatic cycle is in progress)
    AL  = True_bit_detect(data,7)   # Alarm signal

    # ready to start NC program state detection
    if SPL == False and STL == False and SA == True and MA == True and OP == False and AL == False:
        state = 0
    # CNC is in operation mode detection
    elif SPL == False and STL == True and SA == True and MA == True and OP == True and AL == False:
        state = 1
    # CNC automatic cycle CYCLE stop detection
    elif SPL == True and STL == False and SA == True and MA == True and OP == True and AL == False:
        state = 2
    # fail mode detection
    else:
        state = 3
    return state

def PmcButtonPush(FlibHndl: int, adr_type: int, AdressNum: int, data: bytes, delay: int = 1) -> bool:
    '''
    This function simulates button push. Because some subprogram program start after button is pushed back.
       
    # Parameters:

        FlibHndl (int):     Library handle.
        adr_type (int):     Identification code for the kind of PMC address
            - 0: G
            - 1: F
            - 2: Y
            - 3: X

        AdressNum (int):    Specify the PMC address number.
        data:               Write data (format: bytes([0]))
        delay (int):        Time delay between data writing operations in sec. 

    # Returns:
    
        (bool):             Function switched successfuly return value True/False
    '''
    # write data into register
    ret = FOCAS.write_pmc_data(FlibHndl, adr_type, AdressNum, data)      
    time.sleep(delay)                                                       # delay is here because function is too fast for CNC (i don't know if it is good idea to use time.sleep())
    ret = FOCAS.write_pmc_data(FlibHndl, adr_type, AdressNum, bytes([0])) 
    # waiting for PMC reaction on  writen PMC input
    time.sleep(delay)

        # Check the return value
    if ret == 0:
        # print("PMC data written successfully.")
        state = True
    else:
        print(f"Error in pmc_wrpmcrng. Error number: {ret}")
        state = False
    
    return state
  
def PmcAUTO(FlibHndl: int) -> bool:
    '''
    This function switches FANUC CNC into AUTO mode.
       
    # Parameters:
        FlibHndl (int): Library handle.

    # Returns:
        (bool):         Function switched successfuly return value True/False
    '''

    PmcButtonPush(FlibHndl, 3, 10, bytes([1]))

    # Controlling operation success from output register
    state = PmcBitDetection(FlibHndl, 2, 0, 0)

    # validation of data
    if state == False:
        print("AUTO mode switch unsuccesfull")

    return state

def PmcEDIT(FlibHndl: int) -> bool:
    '''
    This function switches FANUC CNC into EDIT mode.
       
    # Parameters:
        FlibHndl (int): Library handle.

    # Returns:
        (bool):         Function switched successfuly return value True/False
    '''

    PmcButtonPush(FlibHndl, 3, 10, bytes([2]))

    # Controlling operation success from output register
    state = PmcBitDetection(FlibHndl, 2, 0, 1)

    # validation of data
    if state == False:
        print("EDIT mode switch unsuccesfull")

    return state

def PmcMDI(FlibHndl: int) -> bool:
    '''
    This function switches FANUC CNC into MDI mode.
       
    # Parameters:
        FlibHndl (int): Library handle.

    # Returns:
        (bool):         Function switched successfuly return value True/False
    '''

    PmcButtonPush(FlibHndl, 3, 10, bytes([4]))

    # Controlling operation success from output register
    state = PmcBitDetection(FlibHndl, 2, 0, 2)

    # validation of data
    if state == False:
        print("MDI mode switch unsuccesfull")

    return state

def PmcRMT(FlibHndl: int) -> bool:
    '''
    This function switches FANUC CNC into RMT mode.
       
    # Parameters:
        FlibHndl (int): Library handle.

    # Returns:
        (bool):         Function switched successfuly return value True/False
    '''

    PmcButtonPush(FlibHndl, 3, 10, bytes([8]))

    # Controlling operation success from output register
    state = PmcBitDetection(FlibHndl, 2, 0, 3)

    # validation of data
    if state == False:
        print("RMT mode switch unsuccesfull")

    return state

def PmcCSP(FlibHndl: int) -> bool:
    '''
    This function FANUC CNC remotely starts CYCLE STOP sequence.
       
    # Parameters:
        FlibHndl (int): Library handle.

    # Returns:
        (bool):         Function switched successfuly return value True/False
    '''

    PmcButtonPush(FlibHndl, 3, 12, bytes([1]))

    # Controlling operation success from output register
    state = PmcBitDetection(FlibHndl, 2, 2, 0)

    # validation of data
    if state == False:
        print("CYCLE STOP unsuccesfull")

    return state

def PmcCST(FlibHndl: int) -> bool:
    '''
    This function FANUC CNC remotely starts CYCLE START sequence.
       
    # Parameters:
        FlibHndl (int): Library handle.

    # Returns:
        (bool):         Function switched successfuly return value True/False
    '''

    PmcButtonPush(FlibHndl, 3, 12, bytes([2]))

    # Controlling operation success from output register
    state = PmcBitDetection(FlibHndl, 2, 2, 1)

    # validation of data
    if state == False:
        print("CYCLE START unsuccesfull")

    return state

def PmcPSP(FlibHndl: int) -> bool:
    '''
    This function FANUC CNC remotely starts PROGRAM STOP sequence.
       
    # Parameters:
        FlibHndl (int): Library handle.

    # Returns:
        (bool):         Function switched successfuly return value True/False
    '''

    PmcButtonPush(FlibHndl, 3, 12, bytes([4]))

    # Controlling operation success from output register
    state = PmcBitDetection(FlibHndl, 2, 2, 2)

    # validation of data
    if state == False:
        print("PROGRAM STOP unsuccesfull")

    return state

def Feed_rate(FlibHndl: int, feed_rate: int) -> bool:
    '''
    This function changes feedrate of cnc.

    !! this function will work only when CNC is not connected to Operators panel with feed rate switch. (analogic signal from panel will autimatically change value of feedrate)
    # Parameter:
    
        FlibHndl (int):     Library handle.
        feed_rate (int):    feedrate number in procent(0,30,60,90,100,120)

    # Return:

        (bool):             Function switched successfuly return value True/False
    
     
    '''
    data, state = FOCAS.read_pmc_data_adress(FlibHndl, 3, 6)
    
    if state == False:
        return False
    
    SPOV_part = data[-8:-6]     # feed_rate data are only in first 6 bit so at first function has to read rest of data in 8 bit register
    # data for different feed rates
    if feed_rate == 0:
        feed_rate_bin = "000000"
    elif feed_rate == 30:  
        feed_rate_bin = "101101"
    elif feed_rate == 60:  
        feed_rate_bin = "001010"    
    elif feed_rate == 90:  
        feed_rate_bin = "101000" 
    elif feed_rate == 100:  
        feed_rate_bin = "111001"
    elif feed_rate == 120:  
        feed_rate_bin = "011110" 
    else:
        feed_rate_bin = "111001"
        print("Wrong number: Feed rate override set to 100 %")   

    bin_data = SPOV_part + feed_rate_bin        # data connected together
    dec_data = binaryToDecimal(bin_data)
    # data written into CNC
    ret = FOCAS.write_pmc_data(FlibHndl, 3, 6, bytes([dec_data]))
    
    # Function validated
    if ret == 0:
       state = True
    else:
        print(f"Error in pmc_wrpmcrng. Error number: {ret}")
        state = False

    return True

def read_alarm(FlibHndl: int, Type: int = -1, num: int = 10):
    '''
    This function writes alarm data into command line.

    # Parameters:
        FlibHndl (int):   Library handle.
        Type (int):       Specify the type of alarm.
            0 	: 	Parameter switch on 	(SW)
            1 	: 	Power off parameter set 	(PW)
            2 	: 	I/O error 	(IO)
            3 	: 	Foreground P/S 	(PS)
            4 	: 	Overtravel,External data 	(OT)
            5 	: 	Overheat alarm 	(OH)
            6 	: 	Servo alarm 	(SV)
            7 	: 	Data I/O error 	(SR)
            8 	: 	Macro alarm 	(MC)
            9 	: 	Spindle alarm 	(SP)
            10 	: 	Other alarm(DS) 	(DS)
            11 	: 	Alarm concerning Malfunction prevent functions 	(IE)
            12 	: 	Background P/S 	(BG)
            13 	: 	Syncronized error 	(SN)
            14 	: 	(reserved) 	
            15 	: 	External alarm message 	(EX)
            16 	: 	(reserved) 	
            17 	: 	(reserved) 	
            18 	: 	(reserved) 	
            19 	: 	PMC error 	(PC)
            20-31 	: 	(not used) 	
            -1 	: 	All type
        num (int):  Pointer to the number of alarm messages to be read. Specify the number of alarm messages to be read before function call and actual number of data being read is stored after the function call.
    
    # Return:

        (bool):             Function switched successfuly return value True/False
    
    '''

    ret, alarm_data = FOCAS.rdalmmsg2(FlibHndl, Type, num)      # function reads data

    # Function validated
    if ret == 0:
       state = True
    else:
        print(f"Error in cnc_rdalmmsg2. Error number: {ret}")
        state = False

    print_alarm_data(alarm_data)        # this function print data into output

    return state

##################################################################################################
# Automatic control
##################################################################################################

def RunProgram(FlibHndl: int, NcProgramPath: str, cnc_folder_path: str, file_name: str,delay: int = 0) -> bool:
    '''
    This function automates download of NC program from PC to CNC.
       
    # Parameters:
        FlibHndl (int):             Library handle.
        NcProgramPath (string):     Addresss of NC program in PC.  (C:/Users/NC program/O0031.txt")  
        cnc_folder_path (string):   Specify a destination folder name for verifying. ("//CNC_MEM/USER/PATH2/")  
        file_name (string):         Name of the NC program file. ("O4100") Start numbers from left. If you name your program like this O0041 the program will erase 00 and control will fail.

    # Returns:
        (bool):                     Function switched successfuly return value True/False
    '''

    cnc_file_path = cnc_folder_path + file_name

    # CNC state control
    ret = System_state(FlibHndl)

    if ret != 0:
        return False


    time.sleep(delay)
    # change of cnc mode
    ret = PmcEDIT(FlibHndl)

    if ret != True:
        return False
    
    print("EDIT mode selected")
      
    time.sleep(delay)
    # Old NC program is deleted
    ret = DeleteProg(FlibHndl, cnc_file_path)

    if ret != True:
        return False
    print("NC program O4100 deleted successfully.")

    time.sleep(delay)
    # NC program download in to CNC 
    ret = Download(FlibHndl, NcProgramPath, cnc_folder_path)

    if ret != True:
        return False
    
    print("NC program O4100 download successfully")
    
    time.sleep(delay)
    # Program verified
    ret = VerifyProg(FlibHndl, NcProgramPath, cnc_folder_path)
    
    if ret != True:
        return False
    print("NC program O4100 verified")

    time.sleep(delay)

    # Selection of main program
    ret = SelectMain(FlibHndl, cnc_file_path)

    if ret != True:
        return False
    print("O4100 selected as Main program.")
    
    time.sleep(delay)

    ret = PmcAUTO(FlibHndl)
    
    if ret != True:
        return False
    
    print("AUTO mode selected")
    time.sleep(delay)
    
    # CNC state control
    ret = System_state(FlibHndl)

    if ret != 0:
        return False
    print("SYSTEM STATE: CNC is ready to CYCLE START")
    time.sleep(delay)

    ret = PmcCST(FlibHndl)

    if ret != True:
        return False
    print("CYCLE START")

    time.sleep(1)
    state = 1
    while state == 1 or state == 2:
        state = System_state(FlibHndl)
        time.sleep(2)
        if state == 0:
            print("SYSTEM STATE: CNC is ready to CYCLE START")
        if state == 1:
            print("SYSTEM STATE: CNC automatic cycle is in progress")
        if state == 2:
            print("SYSTEM STATE: CNC automatic cycle is in progress cycle STOP is on")
        if state == 3:
            print("SYSTEM STATE: Any valid condition is not met")
        if state == 0: 
            return True
        elif state == 3:                    # this is in occasion when state is read in moment when cnc is hcanging state from run to ready to run
            time.sleep(1)
            state = System_state(FlibHndl)
            if state == 0:
                return True
            else:
                return False

###################################################################################################
# Other
################################################################################################### 
 
def True_bit_detect(binary_str: str, bit_num: int) -> bool:
    """
    This functionchecks value of concrete bit in 8-bit binary string.

    # Parameters:

        binary_st (string): Binary string.
        bit_num (int):      Number of controled bit [0-7].
    
    # Returns:

        (bool):             True/False
    """
    n = bit_num 
    # Reverse the string because bit positions are usually counted from right to left
    reversed_str = binary_str[::-1]
    # Check if the n-th bit is 1
    if len(reversed_str) >= 7 and reversed_str[n] == '1':
        return True
    else:
        return False

def PmcBitDetection(FlibHndl: int, adr_type: int, AdressNum: int, bitnum: int) -> bool:
    '''
    This function reads PMC data from concrete adress and checks state of concrete bit signal.

    # Parameters:

        FlibHndl (int):     Library handle.
        adr_type (int):     Identification code for the kind of PMC address.
            - 0: G
            - 1: F
            - 2: Y
            - 3: X
        AdressNum (int):    Specify the PMC address number.
        bit_num (int):      Number of controled bit [0-7].

    # Returns:
 
        bit (bool):         bit is equal to 1 
    '''

    data,state = FOCAS.read_pmc_data_adress(FlibHndl, adr_type, AdressNum)

    if state == True:
        bit = True_bit_detect(data,bitnum)
        return bit
    else:
        return False

def binaryToDecimal(binary): 
    '''
    This function converts binary number to decimal.

    # Parameters:

        binnary (bin): 8bit bin number
    
    '''
    decimal = 0

    for digit in binary:                        # binary to bit data conversion
        decimal = decimal*2 + int(digit)

    return decimal

def print_alarm_data(alarm_data: FOCAS.ODBALMMSG2):
    '''
    This function prints alarm data located in FOCAS.ODBALMMSG2 structure

    # Parameters:

        alarm_data (ODBALMMSG2): alarm data in structure format from rdalmmsg2 function in FOCAS.py library.
    
    '''

    # Check if alarm_data is not empty
    if alarm_data:
        print(f"Number of alarms: {len(alarm_data)}")
        for i, alarm in enumerate(alarm_data):
            print(f"Alarm {i+1}:")
            print(f"\tAlarm number: {alarm.alm_no}")
            # print(f"\tAlarm type: {alarm.type}")                      # this variable is not useful for basic alarm identification 
            # print(f"\tAxis number: {alarm.axis}")                     # this variable is not useful for basic alarm identification
            # print(f"\tMessage length: {alarm.msg_len}")               # this variable is not useful for basic alarm identification
            print(f"\tAlarm message: {alarm.alm_msg.decode('utf-8')}")
    else:
        print("No alarm data available.")


###################################################################################################
# Trash
################################################################################################### 
 
# Function for openning files related with CNC guide
def open_CNC_guide(name):
    '''
    This function opens CNC guide and its applications.
    
    '''

    # Define the mapping of names to executable files
    executables = {
        "CNCGuide": r"C:/Program Files (x86)/FANUC2/CNC GUIDE 2/NCGuide FS31i-B/Simbase.exe",
        "MachineSet": r"C:/Program Files (x86)/FANUC2/CNC GUIDE 2/NCGuide FS31i-B/MachineSetting.exe",
        "OptionSet": r"C:/Program Files (x86)/FANUC2/CNC GUIDE 2/NCGuide FS31i-B/OptionSetting.exe"
    }

    # Check if the provided name is in the dictionary
    if name in executables:
        try:
            # Attempt to open the executable file
            subprocess.Popen(executables[name])
            print(f"{name} executable opened successfully.")
        except Exception as e:
            # Handle exceptions if the executable fails to open
            print(f"An error occurred while opening {name}: {e}")
    else:
        print(f"No executable found for the name: {name}")

'''
#  REF button
def PmcREF(FlibHndl):
    FOCAS.write_pmc_data(FlibHndl, 3, 12, bytes([16]))
    FOCAS.write_pmc_data(FlibHndl, 3, 12, bytes([0]))
# JOG button    
def PmcJOG(FlibHndl):
    FOCAS.write_pmc_data(FlibHndl, 3, 12, bytes([32]))
    FOCAS.write_pmc_data(FlibHndl, 3, 12, bytes([0]))
# INC button
def PmcINC(FlibHndl):
    FOCAS.write_pmc_data(FlibHndl, 3, 12, bytes([64]))
    FOCAS.write_pmc_data(FlibHndl, 3, 12, bytes([0]))  
# HND button
def PmcHND(FlibHndl):
    FOCAS.write_pmc_data(FlibHndl, 3, 12, bytes([128]))
    FOCAS.write_pmc_data(FlibHndl, 3, 12, bytes([0])) 

'''

'''

I need to call cpp function from dll file in python through ctype. The functions name is CNC_VRFSTART4. Here is link to function documentation: https://www.inventcom.net/fanuc-focas-library/Program/cnc_vrfstart4
This is what i made:
import ctypes               # library for loading cpp files


# Load the DLL
focas = ctypes.CDLL("C:/Users/lukpi/Documents/Obsidian_brain/Sešity/Práce/Houfek a.s/Projekt/Cpp wrapper/FOCAS2_Library/Fwlib64/Fwlib64.dll")
  
Wrap this function into python function.

'''