""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the UI interaction code for the main budget 
screen. 

Last Updated: 10 July 2026
Recent Changes:
- Overhauling UI
- Simplifying code
"""
# ===================================================================
#           Imports
# ===================================================================
from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

from constants import *
from logic.objects import Month
from logic.serializer import Serializer

# ===================================================================
#           Classes
# ===================================================================
class BudgetScreen(QWidget):
    """
    Implementation of the BudgetScreen class that serves as the
    source of the interactive code for the Budget Screen. Loaded by
    main_window.py.
    """
    def __init__(self, month, year):
        super().__init__()

        # Load the First UI Page
        loadUi(BUDGETSCREEN_UI, self)

        # Setup Month handler data
        self.month = Month(MONTHS[month], year) # this will be decided by UI later, placeholder for now
        self.serializer = Serializer(self.month.name, self.month.year)

        # Connect buttons to functions
        self.pushButton_0.clicked.connect(lambda: self.serializer.serialize(self.month))
# EOF
