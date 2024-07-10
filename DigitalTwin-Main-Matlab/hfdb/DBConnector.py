##
#
#
import psycopg2

# Local imports
from hfdb.DBConnection import DBConnection
#from future.builtins.misc import isinstance

##
# \brief The Class services connection to database
#
# The Class services connection to database
#
class DBConnector(object):
   
    ##
    # \brief Implicit constructor
    #
    # Connector is initialized by connection object.
    # \param connection - Database connection
    #
    def __init__(self, connection):
        if isinstance(connection,DBConnection):
            self.connection = connection;
        else:
            pass    # Some exception here
            
    ##
    # \brief The method connects to database 
    #
    # The method connects to database.
    #
    def connect(self):
        self.conn = psycopg2.connect(host=self.connection.host, \
                                     dbname=self.connection.database, \
                                     user=self.connection.user, \
                                     password=self.connection.passwd,\
                                     port=self.connection.port)
    
    ##
    # \brief The method closes open connection
    #
    # The function closes open connection.
    #
    def close(self):
        self.conn.close()
    
    ##
    # \brief The method runs query and returns results
    #
    # The method runs query and returns results.
    #
    def query(self, query):
        if isinstance(query, str):
            if self.conn.closed == 0:
                #print(f"Query: {query}")
                cur = self.conn.cursor()
                cur.execute(query)
                if cur.description is None:
                    data = []
                else:
                    data = cur.fetchall()
                
        else:
            # Send response
            pass
        
        return data
    
    ##
    # \brief The mothod make schanges in the database persistent
    #
    # The mothod make schanges in the database persistent. Should be called
    # when there are made changes in the database tables.
    #
    def commit(self):
        if self.conn.closed == 0:
            self.conn.commit()
        
        