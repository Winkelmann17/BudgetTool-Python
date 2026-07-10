""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the owner for the screens and loads them from
their respective classes.

Last Updated: 10 July 2026
Recent Changes:
- Overhauling UI
- Simplifying code
"""
# ===================================================================
#           Imports
# ===================================================================
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

from constants import *
from logic.objects import Month
from logic.serializer import Serializer

# ===================================================================
#           Classes
# ===================================================================
class MainWindow(QMainWindow):
    """
    Implementation of the MainWindow class. This class handles all
    windows and screens of the program. Loads the inital window and
    then handles all other screens via a stacked widget.
    """
    def __init__(self, month, year):
        super().__init__()

        # Load the First UI Page
        loadUi(BUDGETSCREEN_UI, self)




        print(f"The month is {MONTHS[month]} and the year is {year}.")  # Delete this later

        self.statusbar.showMessage(f"Welcome! This is the budget for {MONTHS[month]} in {year}")

        self.month = Month(MONTHS[month], year) # this will be decided by UI later, placeholder for now
        self.serializer = Serializer(self.month.name, self.month.year)

        self.serializer.serialize(self.month)
# EOF
