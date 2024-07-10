"""
Some Documentation
"""

import FOCAS
import FanucCNC
import ctypes
import sys
import time
import nc_generator

LOCALHOST = "127.0.0.1"
IP_FANUC_CNC = "192.168.1.10"

# Connect to FANUC CNC
m_FlibHndl,ret = FOCAS.ConnectToCNC(LOCALHOST, 8193)

# From given 3 points generate NC code

# Upload NC code to FANUC CNC

# Select Main NC Program

# Run NC code on FANUC CNC
FOCAS.StartProgram(m_FlibHndl)
time.sleep(0.1)

# Wait until operation has been finished or error has occured
while True:
    ret = FOCAS.check_cnc_run_status(m_FlibHndl)

    print(f"RUN MODE: {ret}") # debug only

    if ret == 0:
        exit(0)

    time.sleep(0.1)

# Return proper feedback

