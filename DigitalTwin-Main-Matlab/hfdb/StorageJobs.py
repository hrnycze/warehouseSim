##
# \file StorageJob.py
#
# The module creates static access to Job database
#

from hfdb.DBConnection import DBConnection
from hfdb.DBConnector import DBConnector
from hfdb.DBJob import DBJob

#
# Connection settings 
#
__host = "localhost"
__port = 5432
__user = "pguser"
__password = "pguser"
__database = "dbjob"

#
# Create connection class and its settings
#
__connection = DBConnection()

__connection.setConnection(__host, __port, __database, __user, __password)

__dbjob = DBJob(__connection)

##
# \brief The function connects to database
#
def connect():
    __dbjob.connect()

##
# \brief The function disconnects from database
#
def close():
    __dbjob.close()

##
#
#
def getJobByID(JobID):
    data = __dbjob.getJobByID(JobID)    
    return data

##
#
#   
def getAllJobs():
    data = __dbjob.getAllJobs()    
    return data
        