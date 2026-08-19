""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the UI interaction code for the main budget 
screen. 

Last Updated: 19 August 2026
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
from screens.popups import ExpensePopUp
from logic.screenhelp import *
from logic.objects import Month
from logic.serializer import Serializer

import re
# ===================================================================
#           Classes
# ===================================================================
class BudgetScreen(QWidget):
    """
    Implementation of the BudgetScreen class that serves as the
    source of the interactive code for the Budget Screen. Loaded by
    main_window.py.
    """
    total_text = "Total"

    def __init__(self, month, year, statusbar):
        super().__init__()

        # Load the First UI Page
        loadUi(TEST_UI, self)
        self.statusbar = statusbar

        # Setup Month handler data
        self.old_budget = None
        self.serializer = Serializer(month, year)
        self.month = self.serializer.deserialize()
        if self.month == None:
            self.statusbar.showMessage("No saved month found, new month created!")
            self.month = Month(month, year)
            #self.loadtable_defaults()
        self.ignore_cell_changes = True
        self.catmap = self.loadtable()
        # Connect buttons to functions
        self.saveButton.clicked.connect(lambda: self.serializer.serialize(self.month))
        self.addExpenseButton.clicked.connect(self.show_expense_popup)
        # self.copyLastMonthButton.clicked.connect()
        # self.newCategoryButton.clicked.connect()
        # self.removeButton.clicked.connect()
        # self.futureButton.clicked.connect()

        # Connect menu bar options to functions
        # self.actionSave.triggered.connect(self.go_save_month_data)
        # self.actionBack.triggered.connect(go_back)
        # self.actionHome.triggered.connect(go_back)   

        # Connect events to functions
        self.budgetTable.itemChanged.connect(self.update_planned)
        # self.budgetTable.cellClicked.connect(self.go_update_list)

        # Other
        # self.expList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.expList.customContextMenuRequested.connect(self.open_list_menu)
# ----------------------------------------------------------------------------
    def loadtable(self):    # TODO: New Row function, generic enough for other functions to use
        """Function that loads all table values from the stored data
        within the loaded month object. Returns the category map for 
        the working month for better data editing."""
        temp = {}
        row = 0
        # Get categories from loaded month
        for category in self.month.categories.keys():
            # Add category row for dilineation
            temp[category] = row
            row_name = f"_{category.upper()}_"
            self.budgetTable.insertRow(row)
            self.budgetTable.setVerticalHeaderItem(row, QTableWidgetItem(row_name))
            row += 1

            expenses = self.month.cat_exp_listing[category]
            for exp in expenses:
                temp[exp] = row

                # Insert Row to table
                self.budgetTable.insertRow(row)
                self.budgetTable.setVerticalHeaderItem(row, QTableWidgetItem(exp))
                self.budgetTable.setItem(row, 0, QTableWidgetItem())
                item = QTableWidgetItem()
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.budgetTable.setItem(row, 1, item)
                item = QTableWidgetItem()
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.budgetTable.setItem(row, 2, item)

                # Update text
                planned = self.month.categories[category].expenses[exp].planned
                actual = self.month.categories[category].expenses[exp].actual
                process_cell_text(self.budgetTable, row, planned, actual)

                row+= 1

            # Add Total for Category
            total_key = f"{category}_total"
            temp[total_key] = row
            self.month.categories[category].sum_planned()
            self.month.categories[category].sum_actual()

            # Insert Row
            self.budgetTable.insertRow(row)
            self.budgetTable.setVerticalHeaderItem(row, QTableWidgetItem(self.total_text))
            item = QTableWidgetItem()
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.budgetTable.setItem(row, 0, item)
            item = QTableWidgetItem()
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.budgetTable.setItem(row, 1, item)
            item = QTableWidgetItem()
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.budgetTable.setItem(row, 2, item)

            # Update text
            planned = self.month.categories[category].planned_total
            actual = self.month.categories[category].actual_total
            process_cell_text(self.budgetTable, row, planned, actual)

            row += 1

        # Return catmap
        self.ignore_cell_changes = False
        return temp

# ----------------------------------------------------------------------------
    def update_planned(self, item):
        """Function that updates the planned values in teh table after
        a new planned value is set by the user."""
        if self.ignore_cell_changes:
            return
        print(f"[+] Edit for cell found in {item.row}, {item.column}")

        # Get the value and check it via regex
        cell_text = item.text()
        try:
            amount = float(re.findall(COST_REGEX, cell_text)[0])
            if amount < 0.00:
                amount = 0.00
        except:
            self.statusbar.showMessage(":( Bad input, setting to zero.")
            amount = 0.00
        
        # Pull the exp name
        exp = self.budgetTable.verticalHeaderItem(item.row()).text()
        print(f"Expense_type edited: {exp}")

        # Get the cat and expense type
        # TODO: Have this expense type -> Category mapping done at month init
        cat = None
        for key, value in self.month.cat_exp_listing.items():
            if exp in value:
                cat = key
                break
        print(f"Category: {cat}")
        if cat == None:
            self.statusbar.showMessage(":( Invalid expense type -> category mapping.")
            return

        # Pull expense object from the month and update it
        expense_obj = self.month.categories[cat].expenses[exp]
        expense_obj.set_planned(amount)

        # Call other update functions
        self.update_row(item.row(), expense_obj)
        self.update_total(cat)

# ----------------------------------------------------------------------------
    def update_row(self, row, expense):
        """Function that updates the rows and performs the math for proper
        tracking and display."""
        # Pull table items and calculate new diff
        self.ignore_cell_changes = True
        # Check for text
        process_cell_text(self.budgetTable, row, expense.planned, expense.actual)
        # Change bool back
        self.ignore_cell_changes = False

# ----------------------------------------------------------------------------
    def update_total(self, cat):
        """Function that calculates the totals for the category and updates 
        the table."""
        self.ignore_cell_changes = True
        # Get the category and update the totals, find where row is
        category = self.month.categories[cat]
        category.sum_planned()
        category.sum_actual()
        row = self.catmap[f"{cat}_total"]
        # Set the data
        process_cell_text(self.budgetTable, row, category.planned_total, category.actual_total)   
        # Update bool
        self.ignore_cell_changes = False  

# ----------------------------------------------------------------------------
    def show_expense_popup(self):
        """Function that calls the add expense popup object and executes it.
        Handles any data returned from it."""
        # Update status bar
        self.statusbar.showMessage("Adding expense via popup...")

        # Run popup code
        popup = ExpensePopUp(self.month)
        popup.exec()
        
# EOF
