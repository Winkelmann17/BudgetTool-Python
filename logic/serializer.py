""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the code for the Serializer class that handles 
the writing of budget data to disk for persistence.

Last Updated: 10 July 2026
Recent Changes:
- Overhauling code and simplicity
"""
# ===================================================================
#           Imports
# ===================================================================
import datetime as dt
import os
import pickle

# ===================================================================
#           Serializer
# ===================================================================
class Serializer():
    """
    Class implements the serializer. This is created for each month
    object. Receives the proper year to locate the proper folder and 
    the proper name of the month it is connected to in order to write
    the correct data to the correct location. 
    """
    def __init__(self, month, year="2026"):
        self.month = month
        self.year = year
        self.filepath = f"./data/{year}/{month}.dat"
        self.copypath = f"./data/{year}/COPY_{month}.dat"
        self.backup_path = f"./data/backup/{year}/{month}"

    
    def serialize(self, obj):
        """
        Pickles the associated object and writes it at the specified
        file location provided at intitialization.
        """
        # Move previous to backups (if present)
        self.move_to_backups()

        # Load pickled contents
        contents = pickle.dumps(obj)
        if None == contents:
            return None
        bytes_written = 0

        # Store data in file
        with open(self.filepath, "wb") as f:
            bytes_written = f.write(contents)
        
        return bytes_written
    

    def deserialize(self):
        """
        Loads the pickled object on disk into a usable python object.
        """
        # Read the contents
        contents = self.open_read_close(self.filepath)
        # Load the data
        try: 
            print("IN PICKLE LOADS")
            loaded_target = pickle.loads(contents)
        except Exception as e:
            print(f"{e} : error loading or printing data.")
            return None
        return loaded_target


    def open_read_close(self, name):
        """
        Function that opens a file, reads, writes, and closes the file.
        """
        # Open the file, read, and then print the contents, and close.
        print("IN OPEN READ")
        try:
            size = self.file_size(name)
            f = open(name, "rb")
            # Account for partial reads
            text= bytearray()
            while len(text) < size:
                text += f.read()
            f.close()
            return text
            
        except Exception as e:
            print(f"Exception occurred in file opening. {e}")
            return None
        

    def file_size(self, name):
        # Return file size
        try :
            size = os.stat(name).st_size
            return size
        except Exception as e:
            print(f"{e} : Error occurred finding file information.")


    def move_to_backups(self):
        """Function that moves old Year objects to the backup folder in order
        to preserve their values in case anything bad occurs during saves.
        Able to be loaded later by dragging into proper file location."""
        date = dt.datetime.now()
        backup_name = f"{self.backup_path}_{date.year}_{date.day}_{date.month}_{date.time()}.dat"
        try:
            os.rename(self.filepath, backup_name)
            return True
        except Exception as e:
            print(f"{e}: Error occured when creating backup.")
            return False
        

    def close_out(self):
        """Function called on close out of the program. Saves copy.dat file 
        that has stored all changes to the original file name. Then stores
        backup."""
        self.move_to_backups()
        try:
            os.rename(self.copypath, self.filepath)
        except Exception as e:
            print(f"{e}: Error renaming file to proper name.")
# EOF
