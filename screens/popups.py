""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the UI interaction code for popup regarding
adding expenses to the table.

Last Updated: 10 July 2026
Recent Changes:
- Overhauling UI
- Simplifying code
"""
# ===================================================================
#           Imports
# ===================================================================
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

from constants import *
from logic.screenhelp import *
from logic.objects import Month
from logic.serializer import Serializer

import re
# ===================================================================
#           Expense Popup
# ===================================================================
class ExpensePopUp(QDialog):
    """Class that implements the various PopUp objects. Loads in a specified
    ui file in order to be as generic as possible. Takes in the proper UI file
    as a parameter."""
    def __init__(self):
        super(ExpensePopUp, self).__init__()
        self.response_code = 0
        self.response_text = ""
        loadUi(EXPENSE_POPUP_UI, self)

        # Button binding

# -------------------------------------------------------------------

# -------------------------------------------------------------------

# -------------------------------------------------------------------

# -------------------------------------------------------------------


# EOF
