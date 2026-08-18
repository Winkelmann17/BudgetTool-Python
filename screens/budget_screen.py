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
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

from constants import *
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

    default_text = "$ - "
    total_text = "Total"
    bg_red = QColor(222, 78, 81)
    bg_green =  QColor(118, 222, 115)
    bg_white = QColor(255, 255, 255)

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
        # self.copyLastMonthButton.clicked.connect()
        # self.newCategoryButton.clicked.connect()
        # self.removeButton.clicked.connect()
        # self.futureButton.clicked.connect()

        # Connect menu bar options to functions
        # self.actionSave.triggered.connect(self.go_save_month_data)
        # self.actionBack.triggered.connect(go_back)
        # self.actionHome.triggered.connect(go_back)      #TODO: Broken when set to go_home, can't open months

        # Connect events to functions
        self.budgetTable.itemChanged.connect(self.update_planned)
        # self.budgetTable.cellClicked.connect(self.go_update_list)

        # Other
        # self.expList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.expList.customContextMenuRequested.connect(self.open_list_menu)
# ----------------------------------------------------------------------------
    # def loadtable_defaults(self):                                   # POSSIBLE CODE REUSE FOR LOADING FROM SAVED TABLE
    #     """Function that loads all boxes with the default text. 
    #     Creates the months cat_map and returns it."""
    #     print("[+] Loading Table Defaults and Creating Cat Map...")
    #     temp = {}
    #     for row in range(self.month.rows):
    #         temp[self.budgetTable.verticalHeaderItem(row).text()] = row
    #         for col in range(self.month.cols):
    #             self.budgetTable.setItem(row, col, QTableWidgetItem(self.default_text))
    #     self.ignore_cell_changes = False
        
    #     # Save the cat map for the new month
    #     self.month.cat_map = temp


    def loadtable(self):    # TODO: Ridiculously long, put somewhere else via functions
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

                # Setup table
                self.budgetTable.insertRow(row)
                self.budgetTable.setVerticalHeaderItem(row, QTableWidgetItem(exp))

                planned = self.month.categories[category].expenses[exp].planned
                actual = self.month.categories[category].expenses[exp].actual
                diff = planned - actual
                if planned == 0:
                    planned_text= self.default_text
                else:
                    planned_text = f"${planned:.2f}"
                if actual == 0: 
                    actual_text = self.default_text
                else:
                    actual_text = f"${actual:.2f}"
                if diff == 0:
                    diff_text = self.default_text
                else:
                    diff_text = f"${diff:.2f}"
                self.budgetTable.setItem(row, 0, QTableWidgetItem(planned_text))
                item = QTableWidgetItem(actual_text)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.budgetTable.setItem(row, 1, item)
                item = QTableWidgetItem(diff_text)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.budgetTable.setItem(row, 2, item)

                row+= 1
            # Add Total for Category
            total_key = f"{category}_total"
            temp[total_key] = row
            self.budgetTable.insertRow(row)
            self.budgetTable.setVerticalHeaderItem(row, QTableWidgetItem(self.total_text))

            planned = self.month.categories[category].planned_total
            actual = self.month.categories[category].actual_total
            diff = planned - actual
            if planned == 0:
                planned_text= self.default_text
            else:
                planned_text = f"${planned:.2f}"
            if actual == 0: 
                actual_text = self.default_text
            else:
                actual_text = f"${actual:.2f}"
            if diff == 0:
                diff_text = self.default_text
            else:
                diff_text = f"${diff:.2f}"
            item = QTableWidgetItem(planned_text)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.budgetTable.setItem(row, 0, item)
            item = QTableWidgetItem(actual_text)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.budgetTable.setItem(row, 1, item)
            item = QTableWidgetItem(diff_text)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.budgetTable.setItem(row, 2, item)
            
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
        planned = self.budgetTable.item(row, 0)
        actual = self.budgetTable.item(row, 1)
        difference = self.budgetTable.item(row, 2)
        diff_calc = expense.planned - expense.actual

        # Check for text
        if expense.planned != 0.00:
            planned.setText(f"${expense.planned}")
        else:
            planned.setText(self.default_text)
        if expense.actual != 0.00:
            actual.setText(f"${expense.actual}")
        else:
            actual.setText(self.default_text)
        difference.setText(f"${diff_calc}")        

        # Change color of cell
        if diff_calc < 0.00:
            difference.setBackground(self.bg_red)
        elif diff_calc > 0.00:
            difference.setBackground(self.bg_green)
        else:
            difference.setBackground(self.bg_white)
            difference.setText(self.default_text)

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
        total_planned = self.budgetTable.item(row, 0)
        total_actual = self.budgetTable.item(row, 1)
        total_diff = self.budgetTable.item(row, 2)
        diff_calc = category.planned_total - category.actual_total
        if category.planned_total != 0.0:
            total_planned.setText(f"${category.planned_total:.2f}")
        else:
            total_planned.setText(self.default_text)
        if category.actual_total != 0.00:
            total_actual.setText(f"${category.actual_total:.2f}")
        else:
            total_actual.setText(self.default_text)
        total_diff.setText(f"${diff_calc:.2f}")        

        # Update colors
        # Change color of cell
        if diff_calc < 0.00:
            total_diff.setBackground(self.bg_red)
        elif diff_calc > 0.00:
            total_diff.setBackground(self.bg_green)
        else:
            total_diff.setBackground(self.bg_white)
            total_diff.setText(self.default_text)      

        # Update bool
        self.ignore_cell_changes = False  
# EOF
