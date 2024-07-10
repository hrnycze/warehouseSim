## 
# \brief The Class defines database connection parameters
#
# The Class defines database connection parameters
#
class DBConnection:

    ##
    # \bruef Implicit constructor
    #
    # Implicit constructor defines implicit values for database connection.
    # These are:
    # - host = 'localhost'
    # - port = 5432
    # - databs=ase = ''
    # - user = ''
    # - passwd = ''
    # 
    # These values can be overwritten by specialized calls.
    #
    def __init__(self):
        '''
        Constructor
        '''
        self.host = 'localhost';
        self.port = 5432;
        self.database = '';
        self.user = '';
        self.passwd = '';
 
    #
    # Setter functins first
    #
 
    ##
    # \brief This method sets database host
    #
    # This method sets database host.
    # \param dbhost - Database host, which is string
    #
    def setDBHost(self, dbhost):
        
        # Check data types and check for empty values
        if isinstance(dbhost, str):
            self.host = dbhost;
        else:
            pass;

    ##
    # \brief This method sets database port.
    #
    # This method sets database port.
    # \param dbport - Database port, which is int
    #
    def setDBPort(self, dbport):
        
        # Check data types and check for empty values
        if  isinstance(dbport, int):
            self.port = dbport;
        else:
            pass;


    ##
    # \brief This method sets database name to be connected
    #
    # This method sets database name to be connected.
    # \param database- Database name, which is string
    #
    def setDatabase(self, database):
        
        # Check data types and check for empty values
        if isinstance(database, str):
            self.database = database;
        else:
            pass;

    ##
    # \brief This method sets database user
    #
    # This method sets database user. The user must exists within the database
    # and has to have appropriate access permitions for selected database.
    # \param dbuser - Database user, which is string
    #
    def setDBUser(self, dbuser):
        
        # Check data types and check for empty values
        if isinstance(dbuser, str):
            self.user = dbuser;
        else:
            pass;

    ##
    # \brief This method sets database users password
    #
    # This method sets database users password.
    # \param dbpasswd - Database user password
    #
    def setDBPassword(self, dbpasswd):
        
        # Check data types and check for empty values
        if isinstance(dbpasswd,str):
            self.passwd = dbpasswd;
        else:
            pass;
    
    ##
    # \brief This method sets all values of connection
    #
    # This method sets all values of connection. These are:
    # \param dbhost - Database host, which is string
    # \param dbport - Database port, which is int
    # \param database- Database name, which is string
    # \param dbuser - Database user, which is string
    # \param dbpasswd - Database user password
    #
    def setConnection(self, dbhost, dbport, database, dbuser, dbpasswd):
        
        # Check data types and check for empty values
        if isinstance(dbhost, str) and\
              isinstance(database, str) and\
              isinstance(dbuser, str) and\
              isinstance(dbpasswd,str) and\
              isinstance(dbport, int):
            self.host = dbhost;
            self.port = dbport;
            self.database = database;
            self.user = dbuser;
            self.passwd = dbpasswd;
        else:
            pass;
        
    #
    # Getter functions
    #
    ##
    # \brief This method sets database host
    #
    # This method sets database host.
    # \param dbhost - Database host, which is string
    #
    def getDBHost(self):
        return self.host

    ##
    # \brief This method sets database port.
    #
    # This method sets database port.
    # \param dbport - Database port, which is int
    #
    def getDBPort(self):
        return self.port

    ##
    # \brief This method sets database name to be connected
    #
    # This method sets database name to be connected.
    # \param database- Database name, which is string
    #
    def getDatabase(self):
        return self.database

    ##
    # \brief This method sets database user
    #
    # This method sets database user. The user must exists within the database
    # and has to have appropriate access permitions for selected database.
    # \param dbuser - Database user, which is string
    #
    def getDBUser(self):    
        return self.user
    
    ##
    # \brief This method sets all values of connection
    #
    # This method sets all values of connection. These are:
    # \param dbhost - Database host, which is string
    # \param dbport - Database port, which is int
    # \param database- Database name, which is string
    # \param dbuser - Database user, which is string
    # \param dbpasswd - Database user password
    #
    def getConnection(self):
        return self.host, self.port, self.database, self.user, self.passwd
