""""
This program was written by Winkelmann17. 
Github: https://github.com/Winkelmann17

This code serves as the UI interaction code for the main budget 
screen. 

Last Updated: 29 October 2026
Recent Changes:
- Preparing for final release
"""
# ===================================================================
#           Imports
# ===================================================================
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout, QMenu
from PyQt6.QtGui import QColor, QAction
from PyQt6.QtCore import Qt, QPoint
from PyQt6.uic import loadUi

from constants import *
from screens.popups import ExpensePopUp, EditCategoryPopUp
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
        self.serializer = Serializer(month, year)
        self.month = self.serializer.deserialize()
        if self.month == None:
            self.statusbar.showMessage("No saved month found, new month created!")
            self.month = Month(month, year)    
        self.ignore_cell_changes = True
        self.catmap = self.loadtable()
        self.reverse_catmap = self.build_reverse_catmap()
        self.last_exp = None

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
        self.saveButton.clicked.connect(self.save_data)
        self.addExpenseButton.clicked.connect(self.show_expense_popup)
        self.copyLastMonthButton.clicked.connect(self.copy_last_month)
        self.editCategoryButton.clicked.connect(self.show_edit_expense_type_popup) 

        # Connect events to functions
        self.budgetTable.itemChanged.connect(self.update_planned)
        self.budgetTable.cellClicked.connect(self.update_expense_list_tab)
        self.budgetTable.verticalHeader().sectionClicked.connect(self.update_expense_list_tab)
        self.notesTextBox.textChanged.connect(self.update_notes)

        # Expense List Context Menu
        self.expList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.expList.customContextMenuRequested.connect(self.expense_list_context_menu)
# ----------------------------------------------------------------------------
    def loadtable(self):    # TODO: New Row function, generic enough for other functions to use
        """Function that loads all table values from the stored data
        within the loaded month object. Returns the category map for 
        the working month for better data editing."""
        working_catmap = {}
        row = 0
        self.budgetTable.setRowCount(0)
        self.budgetTable.setHorizontalHeaderItem(0, QTableWidgetItem("Planned"))
        self.budgetTable.setHorizontalHeaderItem(1, QTableWidgetItem("Actual"))
        self.budgetTable.setHorizontalHeaderItem(2, QTableWidgetItem("Difference"))

        # Get categories from loaded month
        for category in self.month.categories.keys():
            # Add category row for dilineation
            working_catmap[category] = row
            self.budgetTable.insertRow(row)
            self.budgetTable.setSpan(row, 0, 1, 3)
            item = QTableWidgetItem(category.upper())
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setBackground(QColor("#43AED8"))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.budgetTable.setItem(row, 0, item)
            # row_name = f"_{category.upper()}_"
            self.budgetTable.setVerticalHeaderItem(row, QTableWidgetItem())

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
        
        return working_reverse

# ----------------------------------------------------------------------------
    def update_planned(self, item):
        """Function that updates the planned values in the table after
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
        self.last_exp = exp_type

        # Don't update if a "Total" is selected
        if exp_type != "Total" and exp_type != "":
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

        # Display Data
        print(f"planned = {planned}, actual {expenses}, diff = {diff}")
        self.overviewPlannedAmount.setText(f" ${planned}")
        self.overviewActualAmount.setText(f" ${expenses}")
        self.overviewDifferentialAmount.setText(f" ${diff:.2f}")
        self.overviewIncomeAmount.setText(f" ${income}")
        self.window().setWindowTitle(f"{MAINTITLE} - {self.month.name} {self.month.year} *")

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
        self.month.update_queue = []
        for cat in self.month.categories.keys():
            self.update_total(cat)
        self.month.calculate_totals()
        self.bargraph.create(self.month)
        self.piechart.create(self.month)
        self.update_overview_tab()

        self.statusbar.showMessage("Expenses added.")

# ----------------------------------------------------------------------------
    def update_notes(self):
        """Func that stores updated notes into the month object."""
        self.month.notes = self.notesTextBox.toPlainText()

# ----------------------------------------------------------------------------
    def copy_last_month(self):
        index = MONTHS.index(self.month.name)
        if index == 0:
            prev_month = MONTHS[11]
            year = self.year - 1
        else:
            prev_month = MONTHS[index - 1]
            print(f"type of year {type(self.month.year)}")
            year = self.month.year
        self.import_data_from(prev_month, year)
        
# ----------------------------------------------------------------------------
    def import_data_from(self, month, year):
        """Function that imports the planned values of a different month
        into the current one, saves on time for the user having to renter 
        everything."""
        # Load the old month via Serializer
        target = Serializer(month, year)
        target_data = target.deserialize()
        if target_data == None:
            self.statusbar.showMessage("Chosen month to import from does not exist.")
        else:
            for cat in target_data.categories.keys():
                current_expenses = self.month.cat_exp_listing[cat]
                for exp in current_expenses:
                    try:
                        new_planned = target_data.categories[cat].expenses[exp].planned
                        exp_obj = self.month.categories[cat].expenses[exp]
                        exp_obj.set_planned(new_planned)
                        self.update_row(self.catmap[exp], exp_obj)
                    except Exception as e:
                        print(f"Exception {e} occurred.")
                        self.statusbar.showMessage(f"Error copying {exp} under the {cat} category.")
                self.update_total(cat)
            self.month.calculate_totals()
            self.update_overview_tab()

        self.statusbar.showMessage(f"Loaded data from {month} {year}.")

# ----------------------------------------------------------------------------
    def expense_list_context_menu(self, position: QPoint):
        """Function that establishes the context menu for the expense list"""
        print("DELETE EXPENSE BRUH")
        # Find what item is being right-clicked
        item = self.expList.itemAt(position)
        if not item:
            return  # clicked empty space, ignore
        row = self.expList.row(item)

        # Create the context menu
        menu = QMenu(self)
        # Define actions
        edit_action = QAction("Edit <Not Implemented!>", self)
        delete_action = QAction("Delete", self)
        # Connect them to handlers
        edit_action.triggered.connect(lambda: self.edit_expense(item, row))
        delete_action.triggered.connect(lambda: self.delete_expense(item, row))
        # Add to the menu
        menu.addAction(edit_action)
        menu.addSeparator()
        menu.addAction(delete_action)
        # Show at mouse cursor position
        menu.exec(self.expList.viewport().mapToGlobal(position))

# ----------------------------------------------------------------------------
    def delete_expense(self, item, index):
        """Function that implements the delete action from the expense
        list context menu."""   
        # Remove from the expense object
        print(f"Target position: {index}")

        # Pull what category the associated expense is in
        cat = self.reverse_catmap[self.last_exp]
        exp_obj = self.month.categories[cat].expenses[self.last_exp]
        costs = exp_obj.costs
        removed = costs.pop(index)
        self.expList.takeItem(index)
        exp_obj.set_actual(exp_obj.actual - removed.cost_value)
        row = self.catmap[self.last_exp]

        # Update UI
        self.update_row(row, exp_obj)
        self.update_total(cat)
        self.month.calculate_totals()
        self.update_overview_tab()
        self.bargraph.create(self.month)
        self.piechart.create(self.month)

        self.statusbar.showMessage(f"Expense named {exp_obj.name} removed.")

# ----------------------------------------------------------------------------
    def edit_expense(self, item, row):
        self.statusbar.showMessage("This feature is not fully implemented yet. Sorry!")

# ----------------------------------------------------------------------------
    def save_data(self):
        """Changes window title to have an asterisk when it is not saved."""
        self.window().setWindowTitle(f"{MAINTITLE} - {self.month.name} {self.month.year}")
        self.serializer.serialize(self.month)
        self.statusbar.showMessage("Data saved.")

# ----------------------------------------------------------------------------
    def show_edit_expense_type_popup(self):
        """Function that calls the add expense popup object and executes it.
        Handles any data returned from it."""
        # Update status bar
        self.statusbar.showMessage("Editing expense type categories via popup...")

        # Run popup code
        popup = EditCategoryPopUp(self.month)
        popup.exec()

        # Update the screen
        if popup.change_made:
            self.ignore_cell_changes = True
            print("YED")
            print(self.month.categories["Income"].expenses)
            self.budgetTable.clear()
            self.catmap = self.loadtable()
            self.reverse_catmap = self.build_reverse_catmap()
            self.update_overview_tab()
            self.ignore_cell_changes = False

        self.statusbar.showMessage("Categories updated.")
# EOF   
