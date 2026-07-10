""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the owner for the screens and loads them from
their respective classes

Last Updated: 10 July 2026
Recent Changes:
- Overhauling UI
- Simplifying code
"""
# ===================================================================
#           Imports
# ===================================================================
from constants import *
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

# ===================================================================
#           Classes
# ===================================================================
class MainWindow(QMainWindow):
    """
    Implementation of the MainWindow class. This class handles all
    windows and screens of the program. Loads the inital window and
    then handles all other screens via a stacked widget.
    """
    def __init__(self):
        super().__init__()

        # Load the First UI Page
        loadUi(BUDGETSCREEN_UI, self)

        self.
