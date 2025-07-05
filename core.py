############################################################################################################
# Nicholas Winkelmann
# Desc: Backend UI Code
# Last Updated: 5 Jul 2025
############################################################################################################
# ==========================================================================================================
#           Imports
# ==========================================================================================================
import sys
from time import sleep
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QStackedWidget, QDialog
from objects import *
from load import *
from constants import * 
from helper import *


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
        self.response_text = self.lineEdit.text()
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

        # Connect Action menu items to respective functions
        self.actionBack.triggered.connect(goback)
        self.actionHome.triggered.connect(goback)

        # Connect all months to load respective budget UI
        self.jan.clicked.connect(lambda: self.gotobudget(self.year, "jan"))
        self.feb.clicked.connect(lambda: self.gotobudget(self.year, "feb"))
        self.mar.clicked.connect(lambda: self.gotobudget(self.year, "mar"))
        self.apr.clicked.connect(lambda: self.gotobudget(self.year, "apr"))
        self.may.clicked.connect(lambda: self.gotobudget(self.year, "may"))
        self.jun.clicked.connect(lambda: self.gotobudget(self.year, "jun"))
        self.jul.clicked.connect(lambda: self.gotobudget(self.year, "jul"))
        self.aug.clicked.connect(lambda: self.gotobudget(self.year, "aug"))
        self.sep.clicked.connect(lambda: self.gotobudget(self.year, "sep"))
        self.oct.clicked.connect(lambda: self.gotobudget(self.year, "oct"))
        self.nov.clicked.connect(lambda: self.gotobudget(self.year, "nov"))
        self.dec.clicked.connect(lambda: self.gotobudget(self.year, "dec"))

    def gotobudget(self, year, month):
        """Function that loads the budget screen. Takes in the respective
        year and month values to load the correct budget."""
        print(f"{year}, {month}")
        budgetscreen = BudgetScreen()
        widget.addWidget(budgetscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# ----------------------------------------------------------------------------------------------------------

class BudgetScreen(QMainWindow):
    """Class that implements the Budget Screen. Loads in the 'budget.ui'
    file. This is the most important screen that allows the user to 
    actually budget and update real files."""
    def __init__(self):
        super(BudgetScreen, self).__init__()
        loadUi("rsrc/UI/budget.ui", self)

        # Connect Action menu items to respective functions
        self.actionSave.triggered.connect(self.gosave)
        self.actionBack.triggered.connect(goback)
        self.actionHome.triggered.connect(lambda: gohome())

    def gosave(self):
        """Function that implements the save and update feature."""
        print("SAVE!")

# ==========================================================================================================
#         Functions
# ==========================================================================================================
def goback():
    """Function that implements the back feature."""
    print("Back!")
    widget.setCurrentIndex(widget.currentIndex() - 1)

def gohome():
    """Function that implements the home feature."""
    print("Home!")
    widget.setCurrentIndex(widget.currentIndex() - 2)


# ==========================================================================================================
#           Main
# ==========================================================================================================
# Setup Code
data = Serializer()
data.startup()
if DEBUG:
    print("Startup complete.")
    print(data.keys)

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