##
# \brief The Class provide access to desks data
#
# The Class provide access to desks data
#

from hfdb.DBConnection import DBConnection
from hfdb.DBConnector import DBConnector

##
#
#
class DBDesks(DBConnector):
    
    ##
    # \brief Constructor
    #
    def __init__(self, connection):
        DBConnector.__init__(self, connection)
        
    
    ##
    # \brief
    #
    def getDeskByTypeID(self, TypeID):
        # Check input parameter, should be number
        if isinstance(TypeID, int):
            # Setup query string
            query_str = f"SELECT * FROM desks WHERE \"TypeID\"='{TypeID}'"
            data = self.query(query_str)
        else:
            # provide response
            pass
        
        return data
    
    ##
    # \brief
    #
    def getDeskPhysByTypeID(self, TypeID):
        # Check input parameter, should be number
        if isinstance(TypeID, int):
            # Setup query string
            query_str = f"SELECT \"Length\",\"Width\",\"Thickness\",\"Density\" FROM desks WHERE \"TypeID\"='{TypeID}'"
            data = self.query(query_str)
        else:
            # provide response
            pass
        
        return data

    ##
    # \brief
    #
    def getAllDesksPhys(self):
        # Setup query string
        query_str = f"SELECT \"Length\",\"Width\",\"Thickness\",\"Density\" FROM desks"
        data = self.query(query_str)
        
        return data

    
    ##
    # \brief 
    #
    def getAllDesks(self):
        query_str = f"SELECT * FROM desks"
        data = self.query(query_str)
        
        return data
