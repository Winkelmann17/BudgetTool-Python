""""
This program was written by Winkelmann17. 
Github: https://github.com/Winkelmann17

This code serves as the UI interaction code for popup regarding
adding expenses to the table.

Last Updated: 20 September 2026
Recent Changes:
- Added new popup for editing expense categories
"""
# ===================================================================
#           Imports
# ===================================================================
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi
import re

from constants import *
# ===================================================================
#           Expense Popup
# ===================================================================
class ExpensePopUp(QDialog):
    """Class that implements the Expense Popup object. Handles all
    specifications for the popup that is used to add expenses to the
    program."""
    def __init__(self, month):
        super(ExpensePopUp, self).__init__()
        self.response_code = 0
        self.response_text = ""
        self.default_cat = "Income"
        self.month = month
        loadUi(ADD_EXPENSE_POPUP_UI, self)

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
        amount = re.findall(COST_REGEX, self.amountBox.text())[0]
        cost = round(float(amount), 2)
        date = self.dateBox.text()
        name = self.descBox.text()
        error = self.input_validation(catname, expname, cost, date, name)
        if error:
            self.feedbackLabel.setText(error)
        else:
            expense_obj = self.month.categories[catname].expenses[expname]
            self.month.update_queue.append(expense_obj)
            expense_obj.add_cost(name, cost, date)
            if cost > self.month.highest_cost.cost_value and catname != "Income":
                if name == "":
                    name = expname
                self.month.set_highest_cost(name, cost, date)
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
        # Char limit
        if len(name) > EXP_DESC_LEN:
            return "Description exceeds 32 char limit. Please change."

        # Ensure Positive Cost
        if cost <= 0.00:
            return "Cost input is zero or negative. Please change."

        return None

    
# -------------------------------------------------------------------
    def update_exp_dropdown(self, cat):
        """Function that updates the expense drop down box whenever
        the text changes in the category box"""
        type_list = self.month.categories[cat].expenses
        self.expBox.clear()
        self.expBox.addItems(type_list.keys())


# ===================================================================
#           Edit Category Type Popup
# ===================================================================
class EditCategoryPopUp(QDialog):
    """Class that implements the various PopUp objects. Loads in a specified
    ui file in order to be as generic as possible. Takes in the proper UI file
    as a parameter."""
    def __init__(self, month):
        super(EditCategoryPopUp, self).__init__()
        self.response_text = ""
        self.default_cat = "Income"
        self.month = month
        self.change_made = False
        loadUi(EDIT_CATEGORY_POPUP_UI, self)

        # Drop down binding
        self.update_exp_dropdown(self.rmCatBox.currentText())
        self.rmCatBox.currentTextChanged.connect(lambda: self.update_exp_dropdown(self.rmCatBox.currentText()))

        # Button Bindings
        self.addButton.clicked.connect(self.handle_add)
        self.rmButton.clicked.connect(self.handle_remove)
        self.addClearButton.clicked.connect(self.handle_add_clear)
        self.rmClearButton.clicked.connect(self.handle_rm_clear)
        self.doneButton.clicked.connect(self.close)

# -------------------------------------------------------------------
    def update_exp_dropdown(self, cat):
        """Function that updates the expense drop down box whenever
        the text changes in the category box"""
        type_list = self.month.categories[cat].expenses
        self.rmExpBox.clear()
        self.rmExpBox.addItems(type_list.keys())

# -------------------------------------------------------------------
    def handle_add_clear(self):
        """Function clears all boxes restores the default
        text in case the user wants to start from scratch."""
        self.addCatBox.setCurrentIndex(0)  # Cat Box
        self.nameBox.setText("") # nameBox
        self.addFeedbackLabel.setText("")    # Feedback Label

# -------------------------------------------------------------------
    def handle_rm_clear(self):
        """Function clears all boxes restores the default
        text in case the user wants to start from scratch."""
        self.rmCatBox.setCurrentIndex(0)  # Cat Box
        self.rmExpBox.setCurrentIndex(0)  # Exp Box
        self.rmFeedbackLabel.setText("")    # Feedback Label

# -------------------------------------------------------------------
    def handle_add(self):
        """Function that handles adding the new expense type to the
        months data."""
        cat = self.addCatBox.currentText()
        exp = self.nameBox.text()
        # Add to month data
        error = self.input_validation(exp)
        if error:
            self.addFeedbackLabel.setText(error)
        else:
            self.month.categories[cat].add_expense(exp)
            self.month.cat_exp_listing[cat].append(exp)
            self.addFeedbackLabel.setText(f"{exp} expense added under {cat}.")
            self.change_made = True

# -------------------------------------------------------------------
    def handle_remove(self):
        """Function that hadnles removing the new expense type from
        the months data."""
        cat = self.rmCatBox.currentText()
        exp = self.rmExpBox.currentText()
        self.month.categories[cat].remove_expense(exp)
        self.month.cat_exp_listing[cat].remove(exp)
        self.rmFeedbackLabel.setText(f"{exp} expense removed from {cat}.")
        self.change_made = True

# -------------------------------------------------------------------
    def input_validation(self, exp_to_add):
        """Function that handles all input validation and ensures
        that everything is correct before attempting to modify
        the month object."""
        # Checking length
        if len(exp_to_add) > EXP_NAME_LEN:
            return f"Expense name exceeds {EXP_NAME_LEN} char limit."\

        # Checking for duplicat names
        for cat in self.month.cat_exp_listing.keys():
            for exp_name in self.month.cat_exp_listing[cat]:
                if exp_to_add == exp_name:
                    return "Expense name is shared with another expense. Choose another name."

        # Success
        return None
    
# EOF
