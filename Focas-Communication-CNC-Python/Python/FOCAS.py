import ctypes               # library for loading cpp files

# Load the DLL file (Fwlib64.dll)
#focas = ctypes.CDLL("C:/Users/lukpi/Documents/Obsidian_brain/Sešity/Práce/Houfek a.s/Projekt/Cpp wrapper/FOCAS2_Library/Fwlib64/Fwlib64.dll")
focas = ctypes.CDLL("C:/Users/Jan-Lenovo/Documents/HoufekGJ/Fanuc/1_Lukas/FANUC/FOCAS2_Library/Fwlib/Fwlib32.dll")

class IODBPMC(ctypes.Structure):                # PMC data structure
    _fields_ = [
        ("type_a", ctypes.c_short),
        ("type_d", ctypes.c_short),
        ("datano_s", ctypes.c_short),
        ("datano_e", ctypes.c_short),
        ("u", ctypes.c_char * 1)                # Adjust the size as needed
    ]

# Define the ODBERR structure
class ODBERR(ctypes.Structure):                 # structure for detail error data
    _fields_ = [                                # Detailed error
        ("err_no", ctypes.c_short),     
        ("err_dtno", ctypes.c_short)]           # Data number on error

class ODBALMMSG2(ctypes.Structure):             # structure for alarm data
    _fields_ = [
        ("alm_no", ctypes.c_long),              # alarm number
        ("type", ctypes.c_short),               # alarm type
        ("axis", ctypes.c_short),               # axis number
        ("dummy", ctypes.c_short),              # reserved
        ("msg_len", ctypes.c_short),            # message length
        ("alm_msg", ctypes.c_char * 64)         # alarm message
    ]

##################################################################################################
# Program manipulation - Download
##################################################################################################

def DwnStart4(FlibHndl: int, dir_name: str, sType: int) -> int:
    '''
    Notifies the start of uploading NC data (NC program, tool offset, etc.) to the internal logic of the Data window library.
    (This function must be executed before cnc_download4.)

    In case of download for NC programs, a destination folder can be specified.

    cnc_download4 function and cnc_dwnend4 function will return EW_FUNC in case that cnc_dwnstart4 function is not executed. 
        
    # Parameters:

        FlibHndl (int):     Library handle.
        sType (short):      Specify the kind of the data.
            - 0: NC program
            - 1:	Tool offset data
            - 2:	Parameter
            - 3:	Pitch error compensation data
            - 4:	Custom macro variables
            - 5:	Work zero offset data
            - 18:	Rotary table dynamic fixture offset
        dir_name (string):  Specify a destination folder name for download. ("//CNC_MEM/USER/PATH2/")
    
    # Return:

        ret (int): Error info. (if ret = 0 everything succesfull else error)

    '''
    # Defines function arguments
    focas.cnc_dwnstart4.argtypes = [ctypes.c_ushort,ctypes.c_short, ctypes.c_char_p]
    # Define the return type of the cnc_dwnstart4 function
    focas.cnc_dwnstart4.restype = ctypes.c_short

    sType = ctypes.c_short(sType)           # Ensure sType is a short
    dir_name_e = dir_name.encode('utf-8')   # Convert string to byte string

    # Call the function
    ret = focas.cnc_dwnstart4(FlibHndl,sType, dir_name_e)
    # returns error message
    return ret

def Download4(FlibHndl: int, filePath: str) -> int:
    '''
    Output NC data to be registered (downloading).
        
    # Parameters:

        FlibHndl (int):     Library handle.
        file_path (string): Addresss of NC program in PC.  (C:/Users/NC program/O0031.txt") 
    
    # Return:

        ret (int):          Error info. (if ret = 0 everything succesfull else error)

    '''
    # Defines function arguments
    focas.cnc_download4.argtypes = [ctypes.c_ushort,ctypes.POINTER(ctypes.c_long), ctypes.c_char_p]
    # Define the return type of the cnc_download4 function
    focas.cnc_download4.restype = ctypes.c_short
    # Read the NC data from the file
    with open(filePath, 'r') as file:
        pBuf = file.read()

    pBuf_e = pBuf.encode('ascii')
    p_Len = ctypes.c_long(len(pBuf_e)) 

    # Call the function
    ret = focas.cnc_download4(FlibHndl,ctypes.byref(p_Len), pBuf_e)

    # returns error message
    return ret

def DwnEnd4(FlibHndl: int) -> int:
    '''
    Notifies the end of downloading NC data to CNC.
    (This function must be executed after cnc_download4.)

    There are cases where errors(EW_DATA,EW_OVRFLOW, etc.) during execution of downloading NC program are returned by this function.

    Further, this function does not return until the registration of the output data by cnc_download4 is completed.

    # Parameters:

        FlibHndl (int):   Library handle.
    
    # Return:

        ret (int): Error info. (if ret = 0 everything succesfull else error)
    
    '''
    # Defines function arguments
    focas.cnc_dwnend4.argtypes = [ctypes.c_ushort]
    # Define the return type of the cnc_dwnend4 function
    focas.cnc_dwnend4.restype = ctypes.c_short

    # Call the function
    ret = focas.cnc_dwnend4(FlibHndl)

    # returns error message
    return ret

##################################################################################################
# Program manipulation - Verification
##################################################################################################

# Python wrapper function for cnc_vrfstart4
def VrfStart4(FlibHndl: int, dir_name: str) -> int:
    '''
    Requests CNC to start verification of NC program. (This function must be executed before cnc_verify4)

    cnc_verify4 function and cnc_vrfend4 function will return EW_FUNC in case that cnc_vrfstart4 function is not executed. 
    
    # Example:

        FOCAS.VrfStart4(FlibHndl,"//CNC_MEM/USER/PATH2/")
    
    # Parameters:

        FlibHndl (int):     Library handle.
        dir_name (string):  Specify a destination folder name for verifying. ("//CNC_MEM/USER/PATH2/")  
    
    # Returns:

        ret (int):          Error info. (if ret = 0 everything succesfull else error)
    
    '''
    # Arguments: library handle (unsigned short), destination folder name (char)
    focas.cnc_vrfstart4.argtypes = [ctypes.c_ushort, ctypes.c_char_p]

    # Define the return type of the cnc_vrfstart4 function
    focas.cnc_vrfstart4.restype = ctypes.c_short

    # Convert the directory name to bytes
    dir_name_bytes = dir_name.encode('ascii')

    # Call the cnc_vrfstart4 function
    ret = focas.cnc_vrfstart4(FlibHndl, dir_name_bytes)

    # returns error message
    return ret
# Python wrapper function for cnc_verify4
def Vrf4(FlibHndl: int, file_path: str) -> int:
    '''
    Outputs NC program to be compared with already registered one to CNC.

    This function outputs the characters of NC program as long as it is specified by '*length'.
    However, if there is no room to store the specified number of character, this function stores the characters as many as possible to fill the buffer and then sets '*length' with the real number of characters which are stored in the buffer.

    In case that this function cannot output at least one character, it returns EW_BUFFER, so again call this function with the same arguments. 
    
    # Example:

        FOCAS.Vrf4(FlibHndl, "C:/Users/lukpi/Documents/Diplomova_prace_velke_soubory/Diplomova prace kod/FOCAS_connect/Data/Internal_data/NC program/O0031.txt")
    
    # Parameters:

        FlibHndl (int):     Library handle.
        file_path (string): Addresss of NC program in PC.  ("C:/Users/NC program/O0031.txt")  
    
    # Returns:

        ret (int):          Error info. (if ret = 0 everything succesfull else error)
    
    '''
    # Define the prototype of the cnc_verify4 function
    # Arguments: library handle (unsigned short), pointer to length (long), pointer to data (char)
    focas.cnc_verify4.argtypes = [ctypes.c_ushort, ctypes.POINTER(ctypes.c_long), ctypes.c_char_p]

    # Define the return type of the cnc_verify4 function
    focas.cnc_verify4.restype = ctypes.c_short

    # Read the NC data from the file
    with open(file_path, 'r') as file:
        pBuf = file.read()

    # Convert the NC data to bytes and get the length
    pBuf_e = pBuf.encode('ascii')
    p_Len = ctypes.c_long(len(pBuf_e))

    # Call the cnc_verify4 function
    ret = focas.cnc_verify4(FlibHndl, ctypes.byref(p_Len), pBuf_e)

    # returns error message
    return ret
# Python wrapper function for cnc_vrfend4
def VrfEnd4(FlibHndl: int) -> int:
    '''
    Notifies the end of verification of NC program to CNC.
    (This function must be executed after cnc_verify4.)

    There are cases where errors(EW_DATA, etc.) during execution of verifying NC program are returned by this function.

    Further, this function does not return until the verification of the output data by cnc_verify4 is completed.


    # Parametres:

        FlibHndl (int):     Library handle.

    # Returns:

        ret (int):          Error info. (if ret = 0 everything succesfull else error)
    
    '''
    # Argument: library handle (unsigned short)
    focas.cnc_vrfend4.argtypes = [ctypes.c_ushort]

    # Define the return type of the cnc_vrfend4 function
    focas.cnc_vrfend4.restype = ctypes.c_short

    # Call the cnc_vrfend4 function
    ret = focas.cnc_vrfend4(FlibHndl)

    # returns error message
    return ret

##################################################################################################
# Program manipulation - Main program
##################################################################################################

# Python wrapper function for cnc_pdf_slctmain
def SlctMain(FlibHndl: int, file_path: str) -> int:
    '''
    Selects the file under the specified folder as the main program.
    Execution of this function is kept waiting when CNC is in editing (including the background edit state).
    
    # Parameters:

        FlibHndl (int):     Library handle.
        file_path (string): Specify a NC program destination in format "Current drive + folder + file name". ("//CNC_MEM/USER/PATH2/O3000")  
    
    # Returns:

        ret (int):          Error info. (if ret = 0 everything succesfull else error)

    '''
    focas.cnc_pdf_slctmain.argtypes = [ctypes.c_ushort, ctypes.c_char_p]
    focas.cnc_pdf_slctmain.restype = ctypes.c_short

    # Convert the file path to a byte string
    file_path_e = file_path.encode('utf-8')

    # Call the cnc_pdf_slctmain function
    ret = focas.cnc_pdf_slctmain(FlibHndl, file_path_e)

    # returns error message
    return ret
# Python wrapper function for cnc_pdf_rdmain
def RdMain(FlibHndl: int):
    '''
    Reads the file information that is select currently as the main program.

    # Important!!!

    There is unsolved problem with decoding when the number of NC program in format O0031 it decodes returned address in following format: O31. Therefore its important to write NC program name with full with number as long as number of its digits like O3001.

    # Parameters:

        FlibHndl (int):     Library handle.
    
    # Returns:

        file_path (string): Main program path. 
        ret (int):          Error info. (if ret = 0 everything succesfull else error)
    '''
    
    # Arguments: library handle (unsigned short), pointer to file path (char)
    focas.cnc_pdf_rdmain.argtypes = [ctypes.c_ushort, ctypes.c_char_p]
    # Define the return type of the cnc_pdf_rdmain function
    focas.cnc_pdf_rdmain.restype = ctypes.c_short
     
    # Create a buffer for the file path
    file_path = ctypes.create_string_buffer(244)
 
    ret = focas.cnc_pdf_rdmain(FlibHndl, file_path)
    file_path_de = file_path.value.decode('utf-8')

    # print(f"Main program file info: {file_path.value.decode('utf-8')}")
    # returns error message
    return file_path_de, ret



##################################################################################################
# Program manipulation - Other
##################################################################################################

# Python wrapper function for cnc_pdf_del
def Delete(FlibHndl: int, file_path: str) -> int:
    '''
    Deletes the folder or file under the specified folder.
    Execution of this function is kept waiting when CNC is in editing including the background edit state).

    When the specified file is used for NC operation or selected at foreground, the file cannot be deleted. And in case of the protected file, the file cannot be deleted.

    When the specified folder is selected as the current folder, the folder cannot be deleted. And in case that the folder is not vacant, the folder cannot be deleted.

    # Parameters:

        FlibHndl (int):     Library handle.
        file_path (string): Specify a NC program destination in format "Current drive + folder + file name". ("//CNC_MEM/USER/PATH2/O3000")  
    
    # Returns:

        ret (int):          Error info. (if ret = 0 everything succesfull else error)

    '''
    # Define the function prototype
    focas.cnc_pdf_del.argtypes = [ctypes.c_ushort, ctypes.c_char_p]
    focas.cnc_pdf_del.restype = ctypes.c_short   
   
    # Convert the NC data address to a byte string
    file_path_encoded = file_path.encode('ascii')

    # Call the cnc_pdf_del function
    ret = focas.cnc_pdf_del(FlibHndl, file_path_encoded)
    
    # returns error message
    return ret

##################################################################################################
# PMC data
##################################################################################################

def write_pmc_data(FlibHndl: int, adr_type: int, AdressNum: int, data: bytes) -> int:
    '''
    This function writes the PMC data of the specified PMC address.
    Simplyfied version of pmc_wrpmcrng() function only for one adress in predefined char type.
         
    # Parametres:

        FlibHndl (int):     Library handle.
        adr_type (int):     Identification code for the kind of PMC address
            - 0: G
            - 1: F
            - 2: Y
            - 3: X
    
        AdressNum (int):    Specify the PMC address number.
        data:               Write data (format: bytes([0]))

    # Returns:

        ret (int):          Error info. (if ret = 0 everything succesfull else error)
    
    '''
    # Define the function prototype
    focas.pmc_wrpmcrng.argtypes = [ctypes.c_ushort, ctypes.c_short, ctypes.POINTER(IODBPMC)]
    focas.pmc_wrpmcrng.restype = ctypes.c_short

    # Create an instance of IODBPMC
    buf = IODBPMC()
    buf.type_a = adr_type
    buf.type_d = 0              # sDataType
    buf.datano_s = AdressNum
    buf.datano_e = AdressNum

    # Assign the byte directly to the first element of the 'u' array
    buf.u = data
    length = ctypes.sizeof(buf)  # The length should be the size of the IODBPMC structure

    # Call the pmc_wrpmcrng function
    ret = focas.pmc_wrpmcrng(FlibHndl, length, buf)
    
    return ret

def read_pmc_data_adress(FlibHndl: int, adr_type: int, AdressNum: int):
    '''
    This function reads the PMC data of the specified PMC address.
    Simplyfied version of pmc_rdpmcrng() function only for one adress in predefined char type.

    # Parametres:

        FlibHndl (int):     Library handle.
        adr_type (int):     Identification code for the kind of PMC address
            - 0: G
            - 1: F
            - 2: Y
            - 3: X
    
        AdressNum (int):    Specify the PMC address number.
    
    # Returns:

        binary_str, state
        Returns adress value in byte format and state (successful/unsuccessful)
    '''

    # Define the function prototype
    focas.pmc_rdpmcrng.argtypes = [ctypes.c_ushort, ctypes.c_short, ctypes.c_short, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ushort, ctypes.POINTER(IODBPMC)]
    focas.pmc_rdpmcrng.restype = ctypes.c_short

    # Create an instance of IODBPMC
    buf = IODBPMC()
    buf.type_a = adr_type
    buf.type_d = 0
    buf.datano_s = AdressNum
    buf.datano_e = AdressNum
    buf.u = bytes([0])
    length = ctypes.sizeof(buf) 
    
    # Call the pmc_rdpmcrng function
    ret = focas.pmc_rdpmcrng(FlibHndl, adr_type, 0, AdressNum, AdressNum, length , buf)

    # Check the return value
    if ret == 0:
        # print("PMC data read successfully.")

        # load data from buf.u
        data = buf.u                    
        binary_str = bin(ord(data))
        # Remove the '0b' prefix
        binary_str = binary_str[2:]
        # Pad with zeros to get 8 bits
        binary_str = binary_str.zfill(8)
        
        return binary_str, True
    else:
        print(f"Error in reading PMC data. Error number: {ret}")
        state = False
        return None , False

##################################################################################################
# Other
##################################################################################################

def ConnectToCNC(strHost: str, sPort: int, lTimeout: int = 10):
    '''
    This function allocates the library handle and connects to CNC that has the specified IP address or the Host Name through Ethernet. 

    # Parameters:
    
        strHost (string):   Specify character string of CNC's IP address or Host Name to connect.
        sPort (int):        Specify port number of the FOCAS1/Ethernet or FOCAS2/Ethernet (TCP) function.
        lTimeout (int):     Specify seconds for timeout. If specify 0, timeout process is ignored and the library functions wait infinity.
    
    # Returns:

        FlibHndl (int):     Library handle. 
        ret (int):          Error info. (if ret = 0 everything succesfull else error)
    '''
    # Define the argument types and return type for the cnc_allclibhndl3 function
    focas.cnc_allclibhndl3.argtypes = [ctypes.c_char_p, ctypes.c_short, ctypes.c_long, ctypes.POINTER(ctypes.c_ushort)]
    focas.cnc_allclibhndl3.restype = ctypes.c_short

    # Prepare the arguments
    strHost_encoded = strHost.encode('utf-8')  # Convert string to byte string
    sPort = ctypes.c_short(sPort)  # Ensure port is a short
    lTimeout = ctypes.c_long(lTimeout)  # Ensure timeout is a long
    FlibHndl = ctypes.c_ushort()

    # Call the function
    ret = focas.cnc_allclibhndl3(strHost_encoded, sPort, lTimeout, ctypes.byref(FlibHndl))

    # Check the return value
    if ret == 0:
        print("Connection successful, handle value:", FlibHndl.value)
        return FlibHndl.value , ret
    else:
        print("Connection failed with error code:", ret)
        return None, ret

def get_detailed_err(FlibHndl: int) -> None:
    '''
    Gets the detailed error information after the function has been executed.

    # Parametres:

        FlibHndl (int):   Library handle.
    
    '''
    # Arguments: library handle (unsigned short), pointer to ODBERR structure (ODBERR)
    focas.cnc_getdtailerr.argtypes = [ctypes.c_ushort, ctypes.POINTER(ODBERR)]

    # Define the return type of the cnc_getdtailerr function
    focas.cnc_getdtailerr.restype = ctypes.c_short
    # Create an instance of ODBERR
    err = ODBERR()

    # Call the cnc_getdtailerr function
    ret = focas.cnc_getdtailerr(FlibHndl, ctypes.byref(err))

    # Check the result
    if ret != 0:
        print(f"Error in cnc_getdtailerr: {ret}")
    else:
        print(f"Detailed error: {err.err_no}, Data number on error: {err.err_dtno}")

def rdalmmsg2(FlibHndl: int, Type: int, num: int):
    '''
    Reads the currently arising CNC alarm messages. All alarm messages can be read at once.
    Differing from cnc_rdalminfo fucntion, the axis name is inserted in the axis-type alarm message.
    This function wraps cnc_rdalmmsg2 FOCAS2 function into python.

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
        ret (int):                  Error info.
        alarm_data (ODBALMMSG2):    Alarm data
    '''
    # Define the argument types and the return type of the function
    focas.cnc_rdalmmsg2.argtypes = [ctypes.c_ushort, ctypes.c_short, ctypes.POINTER(ctypes.c_short), ctypes.POINTER(ODBALMMSG2)]
    focas.cnc_rdalmmsg2.restype = ctypes.c_short

    # Create a short variable for 'num' and get its pointer
    
    # Create an array of ODBALMMSG2 instances
    alarm_data = (ODBALMMSG2 * num)()
    num_short = ctypes.c_short(num)
    # Call the function
    ret = focas.cnc_rdalmmsg2(FlibHndl, Type, num_short, alarm_data)
    # Print the return value, the number of alarms read, and the alarm number of each alarm
    print(f"Return value: {ret}")
    # print(f"Number of alarms read: {num_p.contents.value}")
    # for i in range(num_p.contents.value):
    print(f"Alarm number of the alarm {0}: {alarm_data[0].alm_no}")

    return ret, alarm_data

def runDNC(FlibHndl: int):
    # Define the cnc_dncstart function prototype
    focas.cnc_dncstart.restype = ctypes.c_short
    focas.cnc_dncstart.argtypes = [ctypes.c_ushort]

    # Define the cnc_dnc function prototype
    focas.cnc_dnc.restype = ctypes.c_short
    focas.cnc_dnc.argtypes = [ctypes.c_ushort, ctypes.c_char_p, ctypes.c_ushort]

    # Define the cnc_dncend function prototype
    focas.cnc_dncend.restype = ctypes.c_short
    focas.cnc_dncend.argtypes = [ctypes.c_ushort]

    # Function to send NC code
    def send_nc_code(handle, code):
        code_bytes = code.encode('ascii')
        number = len(code_bytes)
        result = focas.cnc_dnc(handle, code_bytes, number)
        if result != 0:
            print(f"Error sending NC code '{code}': {result}")
        return result

    # Start DNC operation
    result = focas.cnc_dncstart(FlibHndl)
    if result == 0:
        print("DNC start successful.")

        # Send the NC code commands
        nc_commands = [
            "\n",
            "M3S2000\n",
            "T14\n",
            "G0X10.\n",
            "G0Z-5.\n",
            "M30\n",
            "%"
        ]

        for command in nc_commands:
            if send_nc_code(FlibHndl, command) != 0:
                break

        # End DNC operation
        result = focas.cnc_dncend(FlibHndl)
        if result == 0:
            print("DNC end successful.")
        else:
            print(f"Error ending DNC operation: {result}")
    else:
        print(f"Error starting DNC operation: {result}")


# Define the constant for EW_OK (replace with the actual value from the FOCAS library)
EW_OK = 0  # Example value, adjust as needed

def StartProgram(handler):
    if handler == 0:
        return False
    
    # Define the cnc_start function prototype
    focas.cnc_start.restype = ctypes.c_short
    focas.cnc_start.argtypes = [ctypes.c_ushort]
    
    result = focas.cnc_start(handler)
    
    if result != EW_OK:
        return False
    else:
        return True
    
# # Define the ODBST structure
# class ODBST(ctypes.Structure):
#     _fields_ = [
#         ("dummy", ctypes.c_short * 2),
#         ("aut", ctypes.c_short),
#         ("manual", ctypes.c_short),
#         ("run", ctypes.c_short),
#         ("edit", ctypes.c_short),
#         ("motion", ctypes.c_short),
#         ("mstb", ctypes.c_short),
#         ("emergency", ctypes.c_short),
#         ("write", ctypes.c_short),
#         ("labelskip", ctypes.c_short),
#         ("alarm", ctypes.c_short),
#         ("warning", ctypes.c_short),
#         ("battery", ctypes.c_short)
#     ]
class ODBST(ctypes.Structure):
    _fields_ = [
        ("dummy", ctypes.c_short * 2),
        ("aut", ctypes.c_short),
        ("run", ctypes.c_short),
        ("motion", ctypes.c_short),
        ("mstb", ctypes.c_short),
        ("emergency", ctypes.c_short),
        ("alarm", ctypes.c_short),
        ("edit", ctypes.c_short)
    ]

def check_cnc_status(handler) -> ODBST:
    # Define the cnc_statinfo function prototype
    focas.cnc_statinfo.restype = ctypes.c_short
    focas.cnc_statinfo.argtypes = [ctypes.c_ushort, ctypes.POINTER(ODBST)]

    status = ODBST()
    result = focas.cnc_statinfo(handler, ctypes.byref(status))
    if result != EW_OK:
        print(f"Error checking CNC status: {result}")
        return None
    return status

def check_cnc_run_status(handler):
    """
    Retrieves the current RUN status of the CNC machine.

    Parameters:
        handler (unsigned short): A handle to the CNC machine.

    Returns:
        int: The run status of the CNC machine.
             "0"  - Not running.
             "2"  - Paused.
             "3"  - Running.
             "None" - Status could not be retrieved.
    """
    status = check_cnc_status(handler)

    if status is not None:
        return status.run
    else:
        return None
    
def check_cnc_mode_status(handler):
    """
    Retrieves the current MODE status of the CNC machine.

    Parameters:
        handler (unsigned short): A handle to the CNC machine.

    Returns:
        int: The MODE status of the CNC machine.
            0	:	MDI
            1	:	MEMory
            2	:	****
            3	:	EDIT
            4	:	HaNDle
            5	:	JOG
            6	:	Teach in JOG
            7	:	Teach in HaNDle
            8	:	INC·feed
            9	:	REFerence
            10	:	ReMoTe
            "None" - Status could not be retrieved.
    """
    status = check_cnc_status(handler)

    if status is not None:
        return status.aut
    else:
        return None
    

# class IODBSGNL(ctypes.Structure):
#     _fields_ = [
#         ('datano', ctypes.c_short),
#         ('type', ctypes.c_short),
#         ('mode', ctypes.c_short),
#         ('hndl_ax', ctypes.c_short),
#         ('hndl_mv', ctypes.c_short),
#         ('rpd_ovrd', ctypes.c_short),
#         ('jog_ovrd', ctypes.c_short),
#         ('feed_ovrd', ctypes.c_short),
#         ('spdl_ovrd', ctypes.c_short),
#         ('blck_del', ctypes.c_short),
#         ('sngl_blck', ctypes.c_short),
#         ('machn_lock', ctypes.c_short),
#         ('dry_run', ctypes.c_short),
#         ('mem_prtct', ctypes.c_short),
#         ('feed_hold', ctypes.c_short),
#         ('manual_rpd', ctypes.c_short),
#         ('dummy', ctypes.c_short * 2)
#     ]

class IODBSGNL(ctypes.Structure):
    _fields_ = [
        ('datano', ctypes.c_short),
        ('type', ctypes.c_short),
        ('mode', ctypes.c_short),
        ('hndl_ax', ctypes.c_short),
        ('hndl_mv', ctypes.c_short),
        ('rpd_ovrd', ctypes.c_short),
        ('jog_ovrd', ctypes.c_short),
        ('feed_ovrd', ctypes.c_short),
        ('spdl_ovrd', ctypes.c_short),
        ('blck_del', ctypes.c_short),
        ('sngl_blck', ctypes.c_short),
        ('machn_lock', ctypes.c_short),
        ('dry_run', ctypes.c_short),
        ('mem_prtct', ctypes.c_short),
        ('feed_hold', ctypes.c_short)
    ]



def set_mode_to_edit(flib_hndl):
    # Function prototype
    focas.cnc_wropnlsgnl.argtypes = [ctypes.c_ushort, ctypes.POINTER(IODBSGNL)]
    focas.cnc_wropnlsgnl.restype = ctypes.c_short

    signal = IODBSGNL()
    signal.mode = 4  # Assuming 1 is EDIT mode
    
    ret = focas.cnc_wropnlsgnl(flib_hndl, ctypes.byref(signal))
    if ret != 0:  # EW_OK is usually 0
        raise Exception(f"Error setting mode to EDIT: {ret}")
    else:
        print("Mode set to EDIT successfully.")


def read_mode_signal(flib_hndl):
    # Function prototype
    focas.cnc_rdopnlsgnl.argtypes = [ctypes.c_ushort, ctypes.c_short, ctypes.POINTER(IODBSGNL)]
    focas.cnc_rdopnlsgnl.restype = ctypes.c_short
    signal = IODBSGNL()
    slct_data = 0x0001  # Set bit 0 to read the mode signal

    ret = focas.cnc_rdopnlsgnl(flib_hndl, slct_data, ctypes.byref(signal))
    if ret != 0:  # EW_OK is usually 0
        raise Exception(f"Error reading mode signal: {ret}")
    return signal.mode