############################################################################################################
# Nicholas Winkelmann
# Desc: Serializer Class Code
# Last Updated: 10 Jul 2025
############################################################################################################
# ==========================================================================================================
#           Imports
# ==========================================================================================================
import pickle
import os
import datetime as dt

FAIL = -1
# ==========================================================================================================
#           Classes
# ==========================================================================================================
class Serializer():
    """Class the implements the serilaizer. This is responsible for pickling and depickling the array of 
    year objects which is the way all the information is stored. Handles the filewriting and backup
    process as well."""
    def __init__(self, year="0000"):
        self.year = year
        self.file = f"data/years/{year}.dat"
        self.copy = f"data/years/{year}_copy.dat"
        self.backup_location = f"data/backup/{year}"


    def serialize(self, obj):
        """Pickles the associated LL object and stores it into a file.
        Handles partial writes to the storage file."""
        # Load pickled contents
        contents = pickle.dumps(obj)
        if None == contents:
            return None
        bytes_written = 0
        # store in copy file
        with open(self.file, "w") as f:
            bytes_written = f.write(contents)
        return bytes_written


    def deserialize(self):
        """Loads the pickled object and calls the print_list LL function 
        to show proper. Handles partial reads from the storage file. """
        # Read contents of the file
        contents = self.open_read_close(self.file)
        # Load and print the data
        try:
            loaded_target = pickle.loads(contents)
        except Exception as e:
            print(f"{e} : error loading or printing data.")
            return None
        return loaded_target


    def open_read_close(self, name):
        """Function that opens a file, reads, writes, and closes the file.
        Uses try, except, finally to show the open-close process in full."""
        # Open the file, read, and then print the contents, and close.
        try:
            size = self.file_size(name)
            f = open(self, "r")
            # Account for partial reads
            text = ""
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
            #print(f"{file} size in bytes: {size}")
            return size
        except Exception as e:
            print(f"{e} : Error occurred finding file information.")


    def move_to_backups(self):
        """Function that moves old Year objects to the backup folder in order
        to preserve their values in case anything bad occurs during saves.
        Able to be loaded later by dragging into proper file location."""
        date = dt.datetime.now()
        backup_name = f"{self.backup_location}_{date.day}_{date.month}_{date.time()}.dat"
        try:
            os.rename(self.file, backup_name)
        except Exception as e:
            print(f"{e}: Error occured when creating backup.")


    def close_out(self):
        """Function called on close out of the program. Saves copy.dat file 
        that has stored all changes to the original file name. Then stores
        backup."""
        self.move_to_backups()
        try:
            os.rename(self.copy, self.file)
        except Exception as e:
            print(f"{e}: Error renaming file to proper name.")
        

    # def startup(self):
    #     """Function that loads the list of named years stored on the system."""
    #     try:
    #         data = self.deserialize()
    #     except Exception as e:
    #         print(f"Error occurred: {e}")
            
        
# ==========================================================================================================
#           Main
# ==========================================================================================================