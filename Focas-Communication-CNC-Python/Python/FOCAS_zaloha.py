import ctypes               # library for loading cpp files
import subprocess           # to open cnc_emulator


# Load the DLL
focas = ctypes.CDLL("C:/Users/lukpi/Documents/Obsidian_brain/Sešity/Práce/Houfek a.s/Projekt/Cpp wrapper/FOCAS2_Library/Fwlib64/Fwlib64.dll")

# Function for openning files related with CNC guide
def open_CNC_guide(name):
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



# Function connects pc with cnc through ethernet
def connect_to_cnc(strHost, sPort, lTimeout):
    # Define the argument types and return type for the cnc_allclibhndl3 function
    focas.cnc_allclibhndl3.argtypes = [ctypes.c_char_p, ctypes.c_short, ctypes.c_long, ctypes.POINTER(ctypes.c_ushort)]
    focas.cnc_allclibhndl3.restype = ctypes.c_short

    # Prepare the arguments
    strHost_encoded = strHost.encode('utf-8')  # Convert string to byte string
    sPort = ctypes.c_short(sPort)  # Ensure port is a short
    lTimeout = ctypes.c_long(lTimeout)  # Ensure timeout is a long
    m_FlibHndl = ctypes.c_ushort()

    # Call the function
    ret = focas.cnc_allclibhndl3(strHost_encoded, sPort, lTimeout, ctypes.byref(m_FlibHndl))

    # Check the return value
    if ret == 0:
        print("Connection successful, handle value:", m_FlibHndl.value)
        return m_FlibHndl.value
    else:
        print("Connection failed with error code:", ret)
        return None

def DwnStart(sType, pDir,m_FlibHndl):

    focas.cnc_dwnstart4.argtypes = [ctypes.c_ushort,ctypes.c_short, ctypes.c_char_p]
    focas.cnc_dwnstart4.restype = ctypes.c_short

    sType = ctypes.c_short(sType)  # Ensure sType is a short
    pDir_e = pDir.encode('utf-8')  # Convert string to byte string
    # m_FlibHndl = ctypes.c_ushort()

    # Call the function
    ret = focas.cnc_dwnstart4(m_FlibHndl,sType, pDir_e)

    # Check the return value
    if ret == 0:
        print("DwnStart successful")
        return None
    else:
        print("Error in cnc_dwnstart4. Error number", ret)
        return None

def Download(filePath, m_FlibHndl):

    focas.cnc_download4.argtypes = [ctypes.c_ushort,ctypes.POINTER(ctypes.c_long), ctypes.c_char_p]
    focas.cnc_download4.restype = ctypes.c_short

    with open(filePath, 'r') as file:
        pBuf = file.read()

    pBuf_e = pBuf.encode('ascii')
    p_Len = ctypes.c_long(len(pBuf_e)) 
    # p_Len = ctypes.c_long(2048) 
    # m_FlibHndl = ctypes.c_ushort()


    # Call the function
    ret = focas.cnc_download4(m_FlibHndl,ctypes.byref(p_Len), pBuf_e)

    # Check the return value
    if ret == 0:
        print("Download successful")
        return None
    else:
        print("Error in cnc_download4. Error number", ret)
        return None

def DwnEnd(m_FlibHndl):

    focas.cnc_dwnend4.argtypes = [ctypes.c_ushort]
    focas.cnc_dwnend4.restype = ctypes.c_short

    # Call the function
    ret = focas.cnc_dwnend4(m_FlibHndl)

    # Check the return value
    if ret == 0:
        print("cnc_download4 successful")
        return None
    else:
        print("Error in cnc_dwnend4. Error number", ret)
        return None

# Define the function prototype

def sel_main_prog(file_path, m_FlibHndl):
    
    focas.cnc_pdf_slctmain.argtypes = [ctypes.c_ushort, ctypes.c_char_p]
    focas.cnc_pdf_slctmain.restype = ctypes.c_short

    # Convert the file path to a byte string
    file_path_encoded = file_path.encode('utf-8')

    # Call the cnc_pdf_slctmain function
    ret = focas.cnc_pdf_slctmain(m_FlibHndl, file_path_encoded)

    # Check the return value
    if ret == 0:
        print("Main program selected successfully.")
    else:
        print(f"Error in selecting main program. Error number: {ret}")


def delete_nc_program(nc_data_address, m_FlibHndl):
   
    # Define the function prototype
    focas.cnc_pdf_del.argtypes = [ctypes.c_ushort, ctypes.c_char_p]
    focas.cnc_pdf_del.restype = ctypes.c_short   
   
    # Convert the NC data address to a byte string
    nc_data_address_encoded = nc_data_address.encode('ascii')

    # Call the cnc_pdf_del function
    ret = focas.cnc_pdf_del(m_FlibHndl, nc_data_address_encoded)

    # Check the return value
    if ret == 0:
        print("NC program deleted successfully.")
    else:
        print(f"Error in deleting NC program. Error number: {ret}")




class IODBPMC(ctypes.Structure):
    _fields_ = [
        ("type_a", ctypes.c_short),
        ("type_d", ctypes.c_short),
        ("datano_s", ctypes.c_short),
        ("datano_e", ctypes.c_short),
        ("u", ctypes.c_char * 1)  # Adjust the size as needed
    ]


# class IODBPMC(ctypes.Structure):
#     class _u(ctypes.Union):
#         _fields_ = [
#             ("cdata", ctypes.c_char * 1),    # The PMC data(byte type)
#             ("idata", ctypes.c_short * 1),   # (word type)
#             ("ldata", ctypes.c_long * 1),    # (long type)
#             ("fdata", ctypes.c_float * 1),   # (32-bit floating-point type)
#             ("dfdata", ctypes.c_double * 1)  # (64-bit floating-point type)
#         ]

#     _fields_ = [
#         ("type_a", ctypes.c_short),         # Kind of PMC address
#         ("type_d", ctypes.c_short),         # Type of the PMC data
#         ("datano_s", ctypes.c_ushort),      # Start PMC address number
#         ("datano_e", ctypes.c_ushort),      # End PMC address number
#         ("u", _u)                           # Union
#     ]

def write_pmc_data(m_FlibHndl, AdressInx, AdressNum, data):
    # Define the function prototype
    focas.pmc_wrpmcrng.argtypes = [ctypes.c_ushort, ctypes.c_short, ctypes.POINTER(IODBPMC)]
    focas.pmc_wrpmcrng.restype = ctypes.c_short

    # Create an instance of IODBPMC
    buf = IODBPMC()
    buf.type_a = AdressInx
    buf.type_d = 0              # sDataType
    buf.datano_s = AdressNum
    buf.datano_e = AdressNum

    # Ensure data is a byte string
    # if not isinstance(data, bytes) or len(data) != 1:
    #     raise ValueError("Data must be a single byte.")

    # Assign the byte directly to the first element of the 'u' array
    # buf.u[0] = ctypes.pointer(data)
    # print(data)
    # ctypes.memmove(buf.u, data, len(data))
    buf.u = data
    length = ctypes.sizeof(buf)  # The length should be the size of the IODBPMC structure
    # print(buf.u)
    # print(buf.datano_e)
    # print(buf)
    # Call the pmc_wrpmcrng function
    ret = focas.pmc_wrpmcrng(m_FlibHndl, length, buf)

    # Check the return value
    if ret == 0:
        print("PMC data written successfully.")
        print(buf.u)
    else:
        print(f"Error in writing PMC data. Error number: {ret}")


def read_pmc_data_adress(m_FlibHndl, adr_type, data_type, s_number, e_number):
    '''
    This function reads the PMC data of the specified PMC address/range.

    Parametres:

    m_FlibHndl (int):   Library handle.
    adr_type (int):     Identification code for the kind of PMC address
        - 0: G
        - 1: F
        - 2: Y
        - 3: X

    data_type (int):    Data type 
        - 0: byte type
        - 1: word type
        - 2: long type

    s_number (int):     Specify the start PMC address number.
    e_number (int):     Specify the end PMC address number.
    
    Returns:

    Returns adress value in byte format.
    '''

    # Define the function prototype
    focas.pmc_rdpmcrng.argtypes = [ctypes.c_ushort, ctypes.c_short, ctypes.c_short, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ushort, ctypes.POINTER(IODBPMC)]
    focas.pmc_rdpmcrng.restype = ctypes.c_short

    # Create an instance of IODBPMC
    buf = IODBPMC()
    buf.type_a = adr_type
    buf.type_d = data_type
    buf.datano_s = s_number
    buf.datano_e = e_number
    buf.u = bytes([0])
    print(buf.u)
    length = ctypes.sizeof(buf) 
    # length = 9
    # Call the pmc_rdpmcrng function
    ret = focas.pmc_rdpmcrng(m_FlibHndl, adr_type, data_type, s_number, e_number, length , buf)

    # Check the return value
    if ret == 0:
        print("PMC data read successfully.")

        # load data from buf.u
        data = buf.u                    
        binary_str = bin(ord(data))     
        # Remove the '0b' prefix
        binary_str = binary_str[2:]
        # Pad with zeros to get 8 bits
        binary_str = binary_str.zfill(8)
        
        return binary_str
    else:
        print(f"Error in reading PMC data. Error number: {ret}")
        return None







# AUTO mode button
def PmcAUTO(m_FlibHndl):
    write_pmc_data(m_FlibHndl, 3, 10, bytes([1]))
    write_pmc_data(m_FlibHndl, 3, 10, bytes([0]))
# EDIT mode button    
def PmcEDIT(m_FlibHndl):
    write_pmc_data(m_FlibHndl, 3, 10, bytes([2]))
    write_pmc_data(m_FlibHndl, 3, 10, bytes([0]))
# MDI button
def PmcMDI(m_FlibHndl):
    write_pmc_data(m_FlibHndl, 3, 10, bytes([4]))
    write_pmc_data(m_FlibHndl, 3, 10, bytes([0]))  
# REMOTE mode button
def PmcRMT(m_FlibHndl):
    write_pmc_data(m_FlibHndl, 3, 10, bytes([8]))
    write_pmc_data(m_FlibHndl, 3, 10, bytes([0]))  
#cycle stop button
def PmcCSP(m_FlibHndl):
    write_pmc_data(m_FlibHndl, 3, 12, bytes([1]))
    write_pmc_data(m_FlibHndl, 3, 12, bytes([0]))
#cycle start button
def PmcCST(m_FlibHndl):
    write_pmc_data(m_FlibHndl, 3, 12, bytes([2]))
    write_pmc_data(m_FlibHndl, 3, 12, bytes([0]))
#program stop button
def PmcPSP(m_FlibHndl):
    write_pmc_data(m_FlibHndl, 3, 12, bytes([4]))
    write_pmc_data(m_FlibHndl, 3, 12, bytes([0]))
#  REF button
def PmcREF(m_FlibHndl):
    write_pmc_data(m_FlibHndl, 3, 12, bytes([16]))
    write_pmc_data(m_FlibHndl, 3, 12, bytes([0]))
# JOG button    
def PmcJOG(m_FlibHndl):
    write_pmc_data(m_FlibHndl, 3, 12, bytes([32]))
    write_pmc_data(m_FlibHndl, 3, 12, bytes([0]))
# INC button
def PmcINC(m_FlibHndl):
    write_pmc_data(m_FlibHndl, 3, 12, bytes([64]))
    write_pmc_data(m_FlibHndl, 3, 12, bytes([0]))  
# HND button
def PmcHND(m_FlibHndl):
    write_pmc_data(m_FlibHndl, 3, 12, bytes([128]))
    write_pmc_data(m_FlibHndl, 3, 12, bytes([0]))  

