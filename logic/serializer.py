""""
This program was written by Nicholas Winkelmann. 
Github: https://github.com/Winkelmann17

This code serves as the code for the Serializer class that handles 
the writing of budget data to disk for persistence.

Last Updated: 18 September 2026
Recent Changes:
- Updating code to adhere to newer norms and standards
- fixed backup directory failure errors
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
        self.folder = f"./data/{year}"
        self.filepath = f"./data/{year}/{month}.dat"
        self.backups_folder = f"./data/backups/{year}"
        self.backup_file_prefix = f"./data/backups/{year}/{month}/backup"

    
    def serialize(self, obj):
        """
        Pickles the associated object and writes it at the specified
        file location provided at intitialization.
        """
        # Move previous to backups (if present)
        self.move_to_backups()

        # Check that a directory for the year exists
        year_folder = os.path.isdir(self.folder)
        if not year_folder:
            os.mkdir(self.folder)

        # Load pickled contents
        contents = pickle.dumps(obj)
        if None == contents:
            return 0
        
        # Store data in file
        bytes_written = 0
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
        # Check if year folder exists, make if not
        year_backup = os.path.isdir(self.backups_folder)
        if not year_backup:
            os.mkdir(self.backups_folder)
        month_backup = os.path.isdir(f"{self.backups_folder}/{self.month}")
        if not month_backup:
            os.mkdir(f"{self.backups_folder}/{self.month}")

        date = dt.datetime.now()
        backup_name = f"{self.backup_file_prefix}_{date.day}_{date.month}_{date.strftime('%H%M%S')}.dat"
        try:
            os.rename(self.filepath, backup_name)
        except FileNotFoundError as e:
            print(f"Original data for {self.year} {self.month} does not exist, abandoning backup.")
        except Exception as e:
            print(f"{e}: Error occured when creating backup.")
            return False
        return True


    def prune_backups():
        """Function that prunes the backup files to the newest 5 after the 
        program is closed"""
        pass
# EOF
