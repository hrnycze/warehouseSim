"""
Some Documentation
"""

import os
import FOCAS
import FanucCNC
import ctypes
import sys
import time
from nc_generator import generate_save_nc_txt

LOCALHOST = "127.0.0.1"
IP_FANUC_CNC = "192.168.1.10"

# File name definition
NC_FILE_NAME = "DIGITAL_TWIN_MOVE"
NcProgramPath = "C:/Users/Jan-Lenovo/Documents/HoufekGJ/Fanuc/1_Lukas/FANUC/Generátor Gcode/name.txt"
# NcProgramPath = "C:/Users/lukpi/Documents/Diplomova_prace_velke_soubory/Diplomova prace kod/FOCAS_connect/Data/Internal_data/NC program/"+file_name+".txt"
cnc_folder_path = "//CNC_MEM/USER/PATH1/"
#cnc_folder_path = "//CNC_MEM/USER/LIBRARY/"


def main():
    arrgs = sys.argv[1].split(',')
    if len(arrgs) != 4:
        print("Wrong number of arrgs!")
        print("Format: Matlab2FocasCallback.py z1,x2,x2,z3")
        sys.exit(1)
    #print(f"Arrgs: {arrgs}")

    # Connect to FANUC CNC
    m_FlibHndl,ret = FOCAS.ConnectToCNC(LOCALHOST, 8193)

    # From given 3 points generate NC code
    fdirpath = os.getcwd()
    generate_save_nc_txt(NC_FILE_NAME, fdirpath, arrgs[0], arrgs[1],arrgs[2],arrgs[3])
    fpath = fdirpath + "/" + NC_FILE_NAME + ".txt"


    # Upload NC code to FANUC CNC
    res = FanucCNC.PmcEDIT(m_FlibHndl)
    if not res:
        print("ERRNO(105): FAIL to set EDIT!")
        exit(105)

    res = FanucCNC.DeleteProg(m_FlibHndl, cnc_folder_path+NC_FILE_NAME)
    if not res:
        print("ERRNO(101): FAIL to Remove old NC code!")
        exit(101)
    res = FanucCNC.Download(m_FlibHndl,fpath)
    if not res:
        print("ERRNO(102): FAIL to Upload NC code!")
        exit(102)

    # Select Main NC Program
    res = FanucCNC.SelectMain(m_FlibHndl,cnc_folder_path+NC_FILE_NAME)
    if not res:
        print("ERRNO(103): FAIL to Select main NC code!")
        exit(103)




    # Run NC code on FANUC CNC
    res = FanucCNC.PmcAUTO(m_FlibHndl)
    if not res:
        print("ERRNO(106): FAIL to set EDIT!")
        exit(106)

    res = FOCAS.StartProgram(m_FlibHndl)
    if not res:
        print("ERRNO(104): FAIL to RUN main NC code!")
        exit(104)

    time.sleep(0.1)

    # Wait until operation has been finished or error has occured
    while True:
        ret = FOCAS.check_cnc_run_status(m_FlibHndl)

        print(f"RUN MODE: {ret}") # debug only

        if ret == 0:
            exit(0)

        time.sleep(0.1)

    # Return proper feedback

if __name__ == "__main__":
    main()

