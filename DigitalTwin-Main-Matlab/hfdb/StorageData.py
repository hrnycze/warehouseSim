##
# \file StorageData.py
#
# The module creates static access to Job database
#

from hfdb.DBConnection import DBConnection
from hfdb.DBConnector import DBConnector
from hfdb.DBStorage import DBStorage

#
# Connection settings 
#
__host = "localhost"
__port = 5433
__user = "pguser"
__password = "pguser"
__database = "dbstorage"

#
# Create connection class and its settings
#
__connection = DBConnection()

__connection.setConnection(__host, __port, __database, __user, __password)

__dbstorage = DBStorage(__connection)

##
# \brief The function connects to database
#
def connect():
    __dbstorage.connect()

##
# \brief The function disconnects from database
#
def close():
    __dbstorage.close()


##
#
#
def getStorageByTStamp(tstamp):
    data = __dbstorage.getStorageByTStamp(tstamp)
    return data

##
#
#
def getStorage():
    data = __dbstorage.getStorage()
    return data

##
#
#
def setStorage(tstamp, storage_data):
    data = __dbstorage.setStorage(tstamp, storage_data)
    return data
        