import FOCAS
import FanucCNC
import ctypes
import sys
import time

# Inicializace CNC guide
# FanucCNC.open_CNC_guide("CNCGuide")

# FanucCNC.open_CNC_guide("MachineSet")

# File name definition
file_name = "name"
NcProgramPath = "C:/Users/Jan-Lenovo/Documents/HoufekGJ/Fanuc/1_Lukas/FANUC/Generátor Gcode/name.txt"
# NcProgramPath = "C:/Users/lukpi/Documents/Diplomova_prace_velke_soubory/Diplomova prace kod/FOCAS_connect/Data/Internal_data/NC program/"+file_name+".txt"
#cnc_folder_path = "//CNC_MEM/USER/PATH1/"
cnc_folder_path = "//CNC_MEM/USER/LIBRARY/"




#m_FlibHndl,ret = FOCAS.ConnectToCNC("192.168.1.10", 8193)
m_FlibHndl,ret = FOCAS.ConnectToCNC("127.0.0.1", 8193)

#FOCAS.StartProgram(m_FlibHndl)

ret = FOCAS.check_cnc_run_status(m_FlibHndl)
print(f"RUN MODE: {ret}")
ret = FOCAS.check_cnc_mode_status(m_FlibHndl)
print(f"CNC MODE: {ret}")
print("---------")


#exit(10)

# while True:
#     ret = FOCAS.check_cnc_run_status(m_FlibHndl)
#     print(f"RUN MODE: {ret}")
#     ret = FOCAS.check_cnc_mode_status(m_FlibHndl)
#     print(f"CNC MODE: {ret}")
#     print("---------")
#     time.sleep(0.1)

#FOCAS.runDNC(m_FlibHndl)

# if ret:
#     print("NC was downloaded succesfully")

#FanucCNC.PmcMDI(m_FlibHndl)
#FanucCNC.PmcAUTO(m_FlibHndl)

#FanucCNC.SelectMain(m_FlibHndl, cnc_folder_path+file_name)

#FanucCNC.PmcCST(m_FlibHndl)
# time.sleep(5)
#FanucCNC.PmcCSP(m_FlibHndl)

# ret = FanucCNC.RunProgram(m_FlibHndl, NcProgramPath, cnc_folder_path, file_name)
# if ret is not True:
#     print("FAIL: Run program")

# ret = FOCAS.write_pmc_data(m_FlibHndl, 3, 10, bytes([2]))

# state = FanucCNC.Feed_rate(m_FlibHndl,80)
num = 1

#FanucCNC.read_alarm(m_FlibHndl, -1, 1)


