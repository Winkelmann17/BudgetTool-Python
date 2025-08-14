############################################################################################################
# Nicholas Winkelmann
# Desc: Backend UI Code
# Last Updated: 10 Jul 2025
############################################################################################################
# ==========================================================================================================
#           Imports
# ==========================================================================================================
import sys
from time import sleep
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QStackedWidget, QDialog, QTableWidget, QTableWidgetItem
from objects import *
from serializer import *
from constants import * 
from helper import *
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


# ----------------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------------

class MonthSelectScreen(QMainWindow):
    """Class that implements the Month Selection Screen. Loads in
    the 'months.ui' file. Allows user to select what month of budget
    data they want to access."""
    def __init__(self, year):
        super(MonthSelectScreen, self).__init__()
        self.year = year
        loadUi("rsrc/UI/months.ui", self)

        self.serializer = Serializer(year)

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

    def gotobudget(self, year, month):
        """Function that loads the budget screen. Takes in the respective
        year and month values to load the correct budget."""
        print(f"{year}, {month}")
        budgetscreen = BudgetScreen(self.serializer, year, month)
        widget.addWidget(budgetscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# ----------------------------------------------------------------------------------------------------------

class BudgetScreen(QMainWindow):
    """Class that implements the Budget Screen. Loads in the 'budget.ui'
    file. This is the most important screen that allows the user to 
    actually budget and update real files."""
    def __init__(self, serializer, year, month):
        super(BudgetScreen, self).__init__()
        loadUi("rsrc/UI/budget.ui", self)
        self.serializer = serializer
        self.year = self.serializer.deserialize()
        if self.year == None:
            self.year = Year(year)
        self.month = self.year.months[month]
        
        print(f"Serializer: {self.serializer}. Year: {self.year}. Month: {self.month}")
        # Connect Action menu items to respective functions
        self.newexpense.clicked.connect(self.go_newexpense)
        self.actionSave.triggered.connect(self.go_save)
        self.actionBack.triggered.connect(go_back)
        self.actionHome.triggered.connect(lambda: go_home())
        self.table.cellClicked.connect(self.go_cellclick)

        # Load table data
        self.loadtable_defaults()

    def go_cellclick(self, row, col):
        """Function implements the cell clicked function."""
        print(f"Cell clicked in {row}, {col}")
        #TODO: Implement handling of updating Expense List Tab

    def go_save(self):
        """Function that implements the save and update feature."""
        print("SAVE!")
        #TODO: Build the save function which will store the data in its appropriate areas and then 
        self.go_cellmath()
        #self.loadtable()

    def loadtable_defaults(self):
        """Function that loads in the initial values."""
        print("LOADING TABLE!")
        #self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(item))
        # Iterate through the table and set default values.
        for row in range(43):
            for col in range(3):
                #print(f"{row}, {col}")
                item = self.table.item(row, col)
                if item.text() == "x":
                    continue
                item.setText("$ - ")


            
    def go_cellmath(self):
        """Function that implements the calculations of the budget sheet cells."""
        print("Math")

    def go_newexpense(self):
        """Function that implements the code to perform creating new expense."""
        print("NEw expense!")

        newexpense = PopUp(CREATE_EXPENSE)
        valid = False
        while not valid:
            newexpense.exec()
            if newexpense.response_code == CANCEL:
                break
            
            # TODO: Handle dates differently?
            cost_text = newexpense.amountBox.text()
            if cost_text == "":
                continue
            cost = float(re.findall(AMOUNT, cost_text)[0])
            if cost < 0.00:
                continue
            date = newexpense.dateBox.text()
            break
        cat = newexpense.catBox.currentText()
        # exp = newexpense.typeBox.currentText()
        exp = "Paycheck1"
        self.month.categories[cat].expenses[exp].add_cost(exp, cost, date)
        

    def go_update_expense_list(self):
        pass 
            

        

# ==========================================================================================================
#         Functions
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
# Setup Code

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

