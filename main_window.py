""""
This program was written by Winkelmann17. 
Github: https://github.com/Winkelmann17

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
from datetime import datetime as dt
import os

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
        self.year = year
        self.month = month

        self.setWindowTitle(f"{MAINTITLE} - {month} {year}")
        self.budget_screen = BudgetScreen(month, year, self.statusbar)
        self.stackedWidget.addWidget(self.budget_screen)
        #self.stackedWidget.setCurrentIndex(0)

    def closeEvent(self, event):
        self.cleanup()
        event.accept()

    def cleanup(self):
        # Prune backups to most recent 3
        try:
            print("Closing")
            folder = f"./data/backups/{self.year}/{self.month}"

            # Sort the files 
            files = os.listdir(folder)
            files.sort()
            remove_files = files[:-3]
            for file in remove_files:
                os.remove(f"{folder}/{file}")
                
        except FileNotFoundError as e:
            print(f"Exception occurred: {e}")
        except Exception as e:
            print(f"Exception occurred: {e}")
        
# EOF
