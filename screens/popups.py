""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the UI interaction code for popup regarding
adding expenses to the table.

Last Updated: 19 August 2026
Recent Changes:
- Creating new Popup class for use in budget screen
"""
# ===================================================================
#           Imports
# ===================================================================
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

from constants import *
# ===================================================================
#           Expense Popup
# ===================================================================
class ExpensePopUp(QDialog):
    """Class that implements the various PopUp objects. Loads in a specified
    ui file in order to be as generic as possible. Takes in the proper UI file
    as a parameter."""
    def __init__(self, month):
        super(ExpensePopUp, self).__init__()
        self.response_code = 0
        self.response_text = ""
        self.default_cat = "Income"
        self.month = month
        loadUi(EXPENSE_POPUP_UI, self)

        # Update Exp Dropdown
        self.update_exp_dropdown(self.default_cat)

        # Drop down binding
        self.catBox.currentTextChanged.connect(lambda: self.update_exp_dropdown(self.catBox.currentText()))

        # Button binding
        self.addButton.clicked.connect(self.handle_add)
        self.clearButton.clicked.connect(self.handle_clear)
        self.doneButton.clicked.connect(self.close)


# -------------------------------------------------------------------
    def handle_add(self):
        """Function that handles the "add" button press. Pulls text
        and updates the table accordinly."""
        # Pull everything from the boxes
        catname = self.catBox.currentText()
        expname = self.expBox.currentText()
        cost = round(float(self.amountBox.text()), 2)
        date = self.dateBox.text()
        name = self.descBox.text()
        error = self.input_validation(catname, expname, cost, date, name)
        if error:
            self.feedbackLabel.setText(error)
        else:
            expense_obj = self.month.categories[catname].expenses[expname]
            expense_obj.add_cost(name, cost, date)
            self.feedbackLabel.setText(f"New ${cost} expense added to {expname} under {catname}!")

# -------------------------------------------------------------------
    def handle_clear(self):
        """Function clears all boxes restores the default
        text in case the user wants to start from scratch."""
        self.catBox.setCurrentIndex(0)  # Cat Box
        self.expBox.setCurrentIndex(0)  # Exp Box
        self.amountBox.setText("$0.00") # Amount Line Edit
        self.dateBox.setText("Month/Day") # Date Box
        self.descBox.setText("")          # Desc box
        self.feedbackLabel.setText("")    # Feedback Label

# -------------------------------------------------------------------
    def input_validation(self, cat, exp, cost, date, name):
        """Function that handles all input validation and ensures
        that everything is correct before attempting to modify
        the month object."""
        return None
    
# -------------------------------------------------------------------
    def update_exp_dropdown(self, cat):
        """Function that updates the expense drop down box whenever
        the text changes in the category box"""
        type_list = self.month.categories[cat].expenses
        self.expBox.clear()
        self.expBox.addItems(type_list.keys())
        
# EOF
