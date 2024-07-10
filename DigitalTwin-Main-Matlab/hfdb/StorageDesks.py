##
# \file StorageDesks.py
#
# The module creates static access to Desks database
#

from hfdb.DBConnection import DBConnection
from hfdb.DBConnector import DBConnector
from hfdb.DBDesks import DBDesks

#
# Connection settings 
#
__host = "localhost"
__port = 5432
__user = "pguser"
__password = "pguser"
__database = "dbdesk"

#
# Create connection class and its settings
#
__connection = DBConnection()

__connection.setConnection(__host, __port, __database, __user, __password)

__dbdesks = DBDesks(__connection)

##
# \brief The function connects to database
#
def connect():
    __dbdesks.connect()

##
# \brief The function disconnects from database
#
def close():
    __dbdesks.close()

##
#
#
def getDeskByTypeID(TypeID):
    data = __dbdesks.getDeskByTypeID(TypeID)    
    return data

##
#
#    
def getDeskPhysByTypeID(TypeID):
    data = __dbdesks.getDeskPhysByTypeID(TypeID)
    return data
    
##
#
#   
def getAllDesks():
    data = __dbdesks.getAllDesks()    
    return data
