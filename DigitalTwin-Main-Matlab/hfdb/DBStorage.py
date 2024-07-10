##
# \brief The Class provide access to storage data
#
# The Class provide access to storage data.
#

from hfdb.DBConnection import DBConnection
from hfdb.DBConnector import DBConnector
#from debugpy._vendored.pydevd.pydevd_attach_to_process.winappdbg.win32.defines import FALSE

##
# \brief The Class provide access to storage data
#
# The Class provide access to storage data
#
class DBStorage(DBConnector):
    
    ##
    # \brief Constructor
    #
    # Constructor initializes HFDBStorage object.
    #
    # \param connection - Object of type DBConnector
    #
    def __init__(self, connection):
        DBConnector.__init__(self, connection)
    
    ##
    # \brief Get storage state saved at specified timestamp
    #
    # Get storage state saved at specified timestamp. The timestamp value
    # is amount of second since epoch (1.1.1970).
    #
    # \param tstamp - Time stamp for which the storage values should be returned
    #
    # \return The function returns storage data for specified timestamp or 'None'
    #         when no data has been found 
    def getStorageByTStamp(self, tstamp):
        # Setup query string
        query_str = f"SELECT * FROM storage WHERE tstamp='{tstamp}'"
        storage_data = self.query(query_str)
        # Check size of returned data
        if len(storage_data) > 0:
            # Setup data output variable
            data = storage_data
            # Get the position of returned data
            buffer_index = storage_data[0][0]
            # Setup new position for circular buffer
            query_str = f"UPDATE cbuffer SET \"POS\"='{buffer_index}'"
            self.query(query_str)
            # Make changes persistent
            self.commit()
        else:
            # Data with provide tstamp does not exists, keep the data empty
            data = []
        # Save new buffer position?
        return data

    ##
    # \brief The function returns storage data from buffer.
    #
    # The function returns storage data from buffer.
    #
    # \return The function returns storage data for specified timestamp or 'None'
    #         when no data has been found 
    def getStorage(self):
        # Setup query for circular buffer
        query_str    = f"SELECT * FROM cbuffer"
        buffer_data  = self.query(query_str)
        buffer_index = buffer_data[0][1]
        # Setup query string
        query_str = f"SELECT * FROM storage WHERE pos='{buffer_index}'"
        data = self.query(query_str)
        # Return data
        return data
    
    ##
    # \brief The method saves storage data with given timestamp to buffer
    #
    # The method saves storage data with given timestamp to buffer
    #
    # \param tstamp - Time stamp which will be saved with provided data
    # \param storage_data - Storage data saved in the buffer with provided timestamp
    #
    # \return The function returns 'True' when operation succeded or 'False' othervise
    def setStorage(self, tstamp, storage_data):
        # DB storage line data size -> amount of items in each line
        storage_items = 4
        # Setup 'status' of function call
        status = True
        # Check data sizes
        if (len(storage_data) > 0 and isinstance(tstamp, int)):
            # Go through all lines and check its sizes, there are not allowed 
            # null data in the database, therefore reject everything what does
            # not have consistent all items
            for line in storage_data:
                if len(line) != storage_items:
                    status = False
                    print("Storage items")
            
        else:
            status = False
            print("Storage data")
        
        # Write new data only if there are new consistent data set
        if status:
            # Setup query for circular buffer
            query_str    = f"SELECT * FROM cbuffer"
            buffer_data  = self.query(query_str)
            buffer_index = buffer_data[0][1]
            buffer_min   = buffer_data[0][2]
            buffer_max   = buffer_data[0][3]
            # Setup new index for Circular buffer
            buffer_index = buffer_index + 1
            
            if buffer_index > buffer_max:
                buffer_index = buffer_min
            
            # Delete all data in new circullar buffer position
            query_str = f"DELETE FROM storage WHERE pos='{buffer_index}'"
            self.query(query_str)
            # Save storage data into buffer
            for i in range(len(storage_data)):
                data_sidx   = storage_data[i][0]
                data_uid    = storage_data[i][1]
                data_tid    = storage_data[i][2]
                data_sstamp = storage_data[i][3]
                query_str = f"INSERT INTO storage(pos, tstamp, sidx, uid, tid, sstamp) \
                VALUES({buffer_index}, {tstamp}, {data_sidx}, {data_uid}, {data_tid},{data_sstamp})"
                self.query(query_str)
            
            # Save new index of Circular buffer
            query_str = f"UPDATE cbuffer SET \"POS\"='{buffer_index}'"
            buffer_data = self.query(query_str)
            # Commit changes to database
            self.commit()
        # Return status of the write
        return status
        