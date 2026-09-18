""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the UI interaction code for the main budget 
screen. 

Last Updated: 17 September 2026
Recent Changes:
- Added bargraph tab functionality
- Added pie chart tab functionality
- Fixed bugs
"""
# ===================================================================
#           Imports
# ===================================================================
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

from constants import *
from screens.popups import ExpensePopUp
from logic.screenhelp import *
from logic.objects import Month
from logic.serializer import Serializer
from logic.graphs import BarGraph, PieChart

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
        self.ignore_cell_changes = True
        self.catmap = self.loadtable()
        self.reverse_catmap = self.build_reverse_catmap()
        self.update_overview_tab()

        # Graphs
        self.bargraph = BarGraph(self.month)
        self.bargraph_layout = QVBoxLayout(self.barGraphTab)
        self.bargraph_layout.addWidget(self.bargraph)
        self.piechart = PieChart(self.month)
        self.piechart_layout = QVBoxLayout(self.pieChartTab)
        self.piechart_layout.addWidget(self.piechart)

        # Notes 
        self.notesTextBox.setPlainText(self.month.notes)

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
        self.budgetTable.cellClicked.connect(self.update_expense_list_tab)
        self.budgetTable.verticalHeader().sectionClicked.connect(self.update_expense_list_tab)
        self.notesTextBox.textChanged.connect(self.update_notes)
        # Other
        # self.expList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.expList.customContextMenuRequested.connect(self.open_list_menu)
# ----------------------------------------------------------------------------
    def loadtable(self):    # TODO: New Row function, generic enough for other functions to use
        """Function that loads all table values from the stored data
        within the loaded month object. Returns the category map for 
        the working month for better data editing."""
        working_catmap = {}
        row = 0
        # Get categories from loaded month
        for category in self.month.categories.keys():
            # Add category row for dilineation
            working_catmap[category] = row
            row_name = f"_{category.upper()}_"
            self.budgetTable.insertRow(row)
            self.budgetTable.setVerticalHeaderItem(row, QTableWidgetItem(row_name))
            row += 1

            expenses = self.month.cat_exp_listing[category]
            for exp in expenses:
                working_catmap[exp] = row
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
            working_catmap[total_key] = row
            self.month.categories[category].sum_planned()
            self.month.categories[category].sum_actual()
            self.month.calculate_totals()

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
        return working_catmap

# ----------------------------------------------------------------------------
    def build_reverse_catmap(self):
        """Function builds a reverse dictionary that pairs expense types 
        to their respective categories"""
        working_reverse = {}
        for key in self.month.cat_exp_listing.keys():
            for exp_type in self.month.cat_exp_listing[key]:
                working_reverse[exp_type] = key
        print(working_reverse)
        return working_reverse

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
        self.month.calculate_totals()
        self.update_overview_tab()

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
    def update_expense_list_tab(self, row):
        """Function that populates the expense list tab on the 
        combo box when a type is clicked on for easy viewing."""
        # Get the row and expense type
        print(f"This row was selected: {row}")
        exp_type = self.budgetTable.verticalHeaderItem(row).text()

        # Don't update if a "Total" is selected
        if exp_type != "Total":
            self.expList.clear()
            # Add each expense with associated data
            cat = self.reverse_catmap[exp_type]
            for cost in self.month.categories[cat].expenses[exp_type].costs:
                print(f"We are in the loop for: {cost.name}")
                self.expList.addItem(f"{cost.name} - {cost.date} - ${cost.cost_value}")

# ----------------------------------------------------------------------------
    def update_overview_tab(self):
        """Function that updates the data in the overview tab to match
        current data stored in the month object."""
        # Get Data
        income = self.month.income_total
        planned = self.month.planned_total
        expenses = self.month.expense_total
        diff = planned - expenses
        name = self.month.highest_cost.name
        cost_value = self.month.highest_cost.cost_value
        date = self.month.highest_cost.date

        # Display Data
        print(f"planned = {planned}, actual {expenses}, diff = {diff}")
        self.overviewPlannedAmount.setText(f" ${planned}")
        self.overviewActualAmount.setText(f" ${expenses}")
        self.overviewDifferentialAmount.setText(f" ${diff:.2f}")
        self.overviewIncomeAmount.setText(f" ${income}")
        self.overviewHighestData.setText(f" {name} - {cost_value} - {date}")

# ----------------------------------------------------------------------------
    def show_expense_popup(self):
        """Function that calls the add expense popup object and executes it.
        Handles any data returned from it."""
        # Update status bar
        self.statusbar.showMessage("Adding expense via popup...")

        # Run popup code
        popup = ExpensePopUp(self.month)
        popup.exec()

        # Update the screen
        print(self.catmap)
        print(self.month.update_queue)
        for exp_obj in self.month.update_queue:
            self.update_row(self.catmap[exp_obj.name], exp_obj)
        for cat in self.month.categories.keys():
            self.update_total(cat)
        self.month.calculate_totals()
        self.bargraph.create(self.month)
        self.piechart.create(self.month)
        self.update_overview_tab()


    def update_notes(self):
        """Func that stores updated notes into the month object."""
        self.month.notes = self.notesTextBox.toPlainText()

# EOF
