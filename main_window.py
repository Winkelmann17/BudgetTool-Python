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

from screens.budget_screen import BudgetScreen

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

        # Load the MainWindow UI 
        loadUi(MAINWINDOW_UI, self)

        # Add the BudgetScreen UI into the stacked widget for screen changing
        # Pass in the statusbar so it can be used
        self.budget_screen = BudgetScreen(month, year, self.statusbar)
        self.stackedWidget.addWidget(self.budget_screen)

        #self.stackedWidget.setCurrentIndex(0)
# EOF
