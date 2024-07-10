##
# \brief The Class provide access to desks data
#
# The Class provide access to desks data
#

from hfdb.DBConnection import DBConnection
from hfdb.DBConnector import DBConnector

##
# \brief The Class provide access to jobs data
#
# The Class provide access to jobs data
#
class DBJob(DBConnector):

    ##
    # \brief 
    #    
    def __init__(self, connection):
        DBConnector.__init__(self, connection)
    
    ##
    # \brief
    #
    def getJobByID(self, JobID):
        # Check input parameter, should be number
        if isinstance(JobID, int):
            # Setup query string
            query_str = f"SELECT * FROM jobs WHERE \"JobID\"='{JobID}'"
            data = self.query(query_str)
        else:
            # provide response
            pass
        
        return data

        pass
    
    ##
    # \brief
    #
    def getAllJobs(self):
        query_str = f"SELECT * FROM jobs"
        data = self.query(query_str)
        
        return data
        

        