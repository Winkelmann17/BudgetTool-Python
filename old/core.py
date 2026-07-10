############################################################################################################
# Nicholas Winkelmann
# Desc: Backend UI Code
# Last Updated: 16 Oct 2025
############################################################################################################
# ==========================================================================================================
#           Imports
# ==========================================================================================================
import sys
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QStackedWidget, QDialog, QMenu
from PyQt6.QtGui import QColor, QBrush, QAction
from PyQt6.QtCore import Qt, QPoint
from code.objects import *
from code.serializer import *
from constants import * 
from helper import *
from copy import deepcopy
import re

DEBUG = True
# ==========================================================================================================
#           Classes
# ==========================================================================================================
class MainWindow(QMainWindow):
    """Function that implements the Main Menu screen. Loads in the
    'main.ui' file. Allows user to select what year of budget data
    they want to access."""
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(MAIN, self)
        self.years = {}
        
        # NewYear Button
        self.NewYear.clicked.connect(self.showpopup)

        # Year Buttons
        self.MMXXV.clicked.connect(lambda: self.gotoyear(2025))

# ----------------------------------------------------------------------

    def showpopup(self):
        """Function that loads the `newyear.ui` file and takes
        input from the user to create the new year object."""
        newyear = PopUp(CREATE_YEAR)
        valid = False
        while not valid:
            newyear.exec()
            if newyear.response_code == CANCEL:
                break
            valid = IsNum(newyear.response_text)
        self.years[newyear.response_text] = Year(newyear.response_text)
        # TODO: When a new year is created, add a new button

    def gotoyear(self, year):
        """Function that loads the month select screen for 
        the chosen year."""
        print(year)
        monthscreen = MonthSelectScreen(year)
        widget.addWidget(monthscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# ==========================================================================================================

class PopUp(QDialog):
    """Class that implements the various PopUp objects. Loads in a specified
    ui file in order to be as generic as possible. Takes in the proper UI file
    as a parameter."""
    def __init__(self, ui):
        super(PopUp, self).__init__()
        self.ui = ui
        self.response_code = 0
        self.response_text = ""
        loadUi(self.ui, self)

        # Ok button custom binding
        self.ok = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.ok.clicked.connect(self.handle_ok)
        self.cancel = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.cancel.clicked.connect(self.handle_cancel)

# ----------------------------------------------------------------------

    def handle_ok(self):
        """Function that handles ok button press. Pulls text and sets 
        response code."""
        # self.response_text = self.lineEdit.text()
        self.response_code = OK
        if DEBUG:
            print(self.response_text)
            print(self.response_code)

    def handle_cancel(self):
        """Function that handles cancel button press. Sets response code."""
        self.response_code = CANCEL
        if DEBUG:
            print(self.response_code)

# ==========================================================================================================

class MonthSelectScreen(QMainWindow):
    """Class that implements the Month Selection Screen. Loads in
    the 'months.ui' file. Allows user to select what month of budget
    data they want to access."""
    def __init__(self, year):
        super(MonthSelectScreen, self).__init__()
        
        loadUi("rsrc/UI/months.ui", self)
        self.old_budget = None
        self.serializer = Serializer(year)
        self.year = self.serializer.deserialize()
        if self.year == None:
            self.year = Year(year)
        # Connect Action menu items to respective functions
        self.actionBack.triggered.connect(go_back)
        self.actionHome.triggered.connect(go_back)

        # Connect all months to load respective budget UI
        self.jan.clicked.connect(lambda: self.gotobudget(self.year, "Jan"))
        self.feb.clicked.connect(lambda: self.gotobudget(self.year, "Feb"))
        self.mar.clicked.connect(lambda: self.gotobudget(self.year, "Mar"))
        self.apr.clicked.connect(lambda: self.gotobudget(self.year, "Apr"))
        self.may.clicked.connect(lambda: self.gotobudget(self.year, "May"))
        self.jun.clicked.connect(lambda: self.gotobudget(self.year, "Jun"))
        self.jul.clicked.connect(lambda: self.gotobudget(self.year, "Jul"))
        self.aug.clicked.connect(lambda: self.gotobudget(self.year, "Aug"))
        self.sep.clicked.connect(lambda: self.gotobudget(self.year, "Sep"))
        self.oct.clicked.connect(lambda: self.gotobudget(self.year, "Oct"))
        self.nov.clicked.connect(lambda: self.gotobudget(self.year, "Nov"))
        self.dec.clicked.connect(lambda: self.gotobudget(self.year, "Dec"))

# ----------------------------------------------------------------------

    def gotobudget(self, year, month):
        """Function that loads the budget screen. Takes in the respective
        year and month values to load the correct budget."""
        print(f"{year}, {month}")
        if self.old_budget != None:
            widget.removeWidget(self.old_budget)
        budgetscreen = BudgetScreen(self.serializer, self.year, month)
        widget.addWidget(budgetscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.old_budget = widget.currentWidget()


# ==========================================================================================================

class BudgetScreen(QMainWindow):
    """Class that implements the Budget Screen. Loads in the 'budget.ui'
    file. This is the most important screen that allows the user to 
    actually budget and update real files."""

    # Class vars
    default_text = "$ - "
    default_rows = 52

    def __init__(self, serializer, year, month_name):
        # UI Stuff
        super(BudgetScreen, self).__init__()
        loadUi("rsrc/UI/budget.ui", self)

        # Connect Action menu items to respective functions
        self.newexpense.clicked.connect(self.go_newexpense)
        self.actionSave.triggered.connect(self.go_save_month_data)
        self.actionBack.triggered.connect(go_back)
        self.actionHome.triggered.connect(go_back)      #TODO: Broken when set to go_home, can't open months
        self.table.itemChanged.connect(self.go_update_planned)
        self.table.cellClicked.connect(self.go_update_list)
        self.expList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.expList.customContextMenuRequested.connect(self.open_list_menu)

        self.ignore_cell_changes = True

        # Object Setups
        self.serializer = serializer
        self.year = year
        self.saved_month = self.year.months[month_name]

        # If the month is completely new
        if self.saved_month.new:
            self.working_month = Month(month_name)
            self.rows = self.default_rows
            self.loadtable_defaults()

        # Month is not new, and has prior data. Copy to working month
        else:
            self.working_month = deepcopy(self.saved_month)
            self.load_from_file()

        # Memory?
        self.last_exp = None
        self.last_cat = None

# ----------------------------------------------------------------------

    def loadtable_defaults(self):
        """Function that loads all boxes with the default text.
        Creates the months cat_map and returns it."""
        print("[+] Loading Table Defaults and Creating Cat Map...")
        temp = {}
        for row in range(self.rows):
            temp[self.table.verticalHeaderItem(row).text()] = row
            for col in range(3):
                item = self.table.item(row, col)
                # Put the default text in every single cell
                item.setText(self.default_text)
        self.ignore_cell_changes = False
        
        # Return the cat_map
        self.working_month.cat_map = temp
    

    def load_from_file(self):
        """Function that loads the data for the saved_month from disk
        and displays to the table"""
        print("[+] Loading data from stored year object...")

        # Iterate through data and display it to the table.
        for cat in self.working_month.categories.keys():
            category = self.working_month.categories[cat]
            for exp in category.expenses.keys():
                expense = category.expenses[exp]
                row = self.working_month.cat_map[exp]
                self.go_update_row(row, expense)
            self.go_update_totals(cat)

        # Put the prior information
        self.go_overview_update()
        self.notesBox.setText(self.working_month.notes)

        # Update cell change bool
        self.ignore_cell_changes = False
        

    def go_update_planned(self, item):
        """Function that updates the values in the table 
        after a new planned value is set by the user."""
        if self.ignore_cell_changes:
            return
        print(f"[+] Edit for cell found in {item.row()}, {item.column()}")
        cell_text = item.text()
        try:
            amount = float(re.findall(COST_REGEX, cell_text)[0])
        except:
            print("[-] Bad input, setting to zero")
            amount = 0.00

        exp = self.table.verticalHeaderItem(item.row()).text()
        print(f"Expense_type edited: {exp}")

        # Get the cat and the expense type
        cat = None
        for key, value in TYPE_DICT.items():
            if exp in value:
                cat = key
                break
        print(f"Category: {cat}")
        expense_type = self.working_month.categories[cat].expenses[exp]

        # Set the expense type and then update cell
        expense_type.set_planned(amount)
        self.go_update_row(item.row(), expense_type)
        self.go_update_totals(cat)
    

    def go_update_list(self, row):
        """Function that updates the list of expenses for each
        expense category when clicked on."""   
        print(f"This row was selected: {row}")
        exp_type = self.table.verticalHeaderItem(row).text()
        print(exp_type)

        if exp_type != "Total":
            # Clear for updating
            self.expList.clear()
            self.last_exp = exp_type

            # Add each expense with the associated data.
            for cost in self.working_month.categories[REVERSE_TYPE_DICT[exp_type]].expenses[exp_type].costs:
                print(f"We are in the for loop: {cost.name}")
                self.expList.addItem(f"{cost.date} - {cost.name} - ${cost.cost}")
        else:
            self.last_exp = None

    def open_list_menu(self, position: QPoint):
        print("DELETE EXPENSE BRUH")
        item = self.expList.itemAt(position)
        if not item:
            return  # clicked empty space, ignore
        row = self.expList.row(item)
        # Create the context menu
        menu = QMenu(self)

        # Define actions
        edit_action = QAction("Edit", self)
        delete_action = QAction("Delete", self)
        

        # Connect them to handlers
        edit_action.triggered.connect(lambda: self.rename_item(item, row))
        delete_action.triggered.connect(lambda: self.delete_item(item, row))

        # Add to the menu
        menu.addAction(edit_action)
        menu.addSeparator()
        menu.addAction(delete_action)

        # Show at mouse cursor position
        menu.exec(self.expList.viewport().mapToGlobal(position))

    def edit_item(self, item, position):
        #TODO: Make another popup instance that handles changing the information about an expense
        print("Editing item in Expense List!")

    def delete_item(self, item, index):
        # Remove from the expense object
        data = item.text().split(" - ")

        print(f"Target position: {index}")
        cat = self.working_month.categories[REVERSE_TYPE_DICT[self.last_exp]]
        exp = cat.expenses[self.last_exp]
        costs = exp.costs
        removed = costs.pop(index)

        exp.set_actual(exp.actual - removed.cost)

        row = self.working_month.cat_map[self.last_exp]
        self.go_update_row(row, exp)

        # Remove from List
        row = self.expList.row(item)
        self.expList.takeItem(row)
        self.go_update_totals(cat.name)


    def go_newexpense(self):
        """Function that implements the code to perform creating new expense."""
        print("[+] Opening new expense window...")

        # Create the Window
        newexpense = PopUp(CREATE_EXPENSE)
        newexpense.catBox.currentTextChanged.connect(lambda: self.go_update_type_list(newexpense, newexpense.catBox.currentText()))
        newexpense.typeBox.addItems(TYPE_DICT["Income"])        # Default

        while True:
            # Loop checking for valid values
            valid = False
            cost = 0
            while not valid:
                exited = newexpense.exec()

                # Leave the function if cancel or the X is clicked
                if newexpense.response_code == CANCEL or exited == 0:
                    return

                # TODO: Update handling of dates. Date regex?
                # TODO: Add a way for the user to know that what they are entering sucks eggs

                # OK was clicked, some checks for validity
                cost_text = newexpense.amountBox.text()
                if cost_text == "":
                    continue
                cost = float(re.findall(COST_REGEX, cost_text)[0])
                if cost < 0.00:
                    continue
                date = newexpense.dateBox.text()
                desc = newexpense.descBox.text()
                # All checks passed, break the loop
                break

            # Gather the data from what the user entered
            cat = newexpense.catBox.currentText()
            exp = newexpense.typeBox.currentText()
            expense_type = self.working_month.categories[cat].expenses[exp]
            # Add the cost
            expense_type.add_cost(desc, cost, date)

            # Get the specific row for the desired expense_type and update it.
            row = self.working_month.cat_map[exp]
            self.go_update_row(row, expense_type)

            # Update total for the category
            self.go_update_totals(cat)
            


    def go_update_row(self, row, expense_type):
        """Function that updates the rows and performs the math
        necessary for proper tracking and display."""
        self.ignore_cell_changes = True

        planned = self.table.item(row, 0)
        actual = self.table.item(row, 1)
        difference = self.table.item(row, 2)
        diff_calc = expense_type.planned -  expense_type.actual

        # Do the checks for text
        if expense_type.planned != 0.00:
            planned.setText(f"${expense_type.planned}")
        else:
            planned.setText(self.default_text)
        if expense_type.actual != 0.00:
            actual.setText(f"${expense_type.actual}")
        else:
            actual.setText(self.default_text)
        difference.setText(f"${diff_calc}")
        
        # TODO: Make the colors nicer to look at
        # Update the colors of the cells
        if diff_calc < 0.00:
            difference.setBackground(QBrush(QColor("red")))
        elif diff_calc > 0.00:
            difference.setBackground(QBrush(QColor("green")))
        else:
            difference.setBackground(QBrush(QColor("white")))
            difference.setText(self.default_text)

        # Change bool back
        self.ignore_cell_changes = False


    def go_update_type_list(self, dialog, cat):
        """Function that updates the second combo box with the appropriate options, when selected."""
        type_list = self.working_month.categories[cat].expenses
        dialog.typeBox.clear()
        dialog.typeBox.addItems(type_list.keys())    


    def go_update_totals(self, cat):
        """Function that calculates the totals for the category."""
        self.ignore_cell_changes = True
        # Get the category and update the totals.
        category = self.working_month.categories[cat]
        category.sum_planned()
        category.sum_actual()
        print(f"cat_planned_sum: {category.planned_total}, cat_actual_sum: {category.actual_total}")
        row = self.working_month.cat_map[cat + "_"]

        # Find next Total instance
        while self.table.verticalHeaderItem(row).text() != "Total":
            row += 1
            
        # Now at the Total, set items
        total_planned = self.table.item(row, 0)
        total_actual = self.table.item(row, 1)
        total_difference = self.table.item(row, 2)
        diff_calc = category.planned_total - category.actual_total
        if category.planned_total != 0.0:
            total_planned.setText(f"${category.planned_total}")
        else:
            total_planned.setText(self.default_text)
        if category.actual_total != 0.00:
            total_actual.setText(f"${category.actual_total}")
        else:
            total_actual.setText(self.default_text)
        total_difference.setText(f"${diff_calc}")

        # TODO: Make the colors nicer to look at
        # Update the colors of the cells
        if diff_calc < 0.00:
            total_difference.setBackground(QBrush(QColor("red")))
        elif diff_calc > 0.00:
            total_difference.setBackground(QBrush(QColor("green")))
        else:
            total_difference.setBackground(QBrush(QColor("white")))
            total_difference.setText(self.default_text)

        # Update bool
        self.ignore_cell_changes = False



    def go_overview_update(self):
        """Function that updates the overview data in the tabs to the right of 
        of the screen."""
        self.plannedBox.setText(f"Planned Total: ${self.saved_month.planned_total}")
        self.actualBox.setText(f"Actual Total: ${self.saved_month.expense_total}")
        self.leftoverBox.setText(f"Leftover: ${self.saved_month.planned_total - self.saved_month.expense_total}")


        
    def go_save_month_data(self):
        """Function that writes the working month to the current year object, 
        and then writes that year object to disk. Also updates the saved_month
        to allow for continued work."""
        print("[+] Attempting to save...")

        # Update Month totals
        self.working_month.income_total = self.working_month.categories["Income"].planned_total
        self.working_month.planned_total = 0
        self.working_month.expense_total = 0
        for cat in CATEGORIES:
            if cat !=  "Income":
                self.working_month.planned_total += self.working_month.categories[cat].planned_total
                self.working_month.expense_total += self.working_month.categories[cat].actual_total
            
        # Save the notes
        self.working_month.notes = self.notesBox.toPlainText()
        print(self.working_month.notes)

        # Update working month to year object and then save it to disk.
        self.working_month.new = False
        self.year.months[self.saved_month.name] = self.working_month
        val = self.serializer.serialize(self.year)

        # Check for Errors
        if val <= 0:
            print("[-] Error occurred while saving.")
            self.year.months[self.saved_month.name] = self.saved_month  # Restore old data
        else:
            print(f"[+] Save complete. {val} bytes written to disk at {self.serializer.file}.")
            self.saved_month = self.working_month
        
        # Update the overview tab
        self.go_overview_update()


# ==========================================================================================================
#         Generic Functions
# ==========================================================================================================
def go_back():
    """Function that implements the back feature."""
    print("Back!")
    widget.setCurrentIndex(widget.currentIndex() - 1)

def go_home():
    """Function that implements the home feature."""
    print("Home!")
    widget.setCurrentIndex(widget.currentIndex() - 2)


# ==========================================================================================================
#           Main
# ==========================================================================================================
# Application Run Code
app = QApplication(sys.argv)
welcome=MainWindow()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec())
except:
    print("Exiting")

