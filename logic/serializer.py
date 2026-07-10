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
        self.copyname = f"./data/{year}/COPY_{month}.dat"
        self.backup_path = f"./data/backup/{year}/{month}.dat"

    
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


# EOF
