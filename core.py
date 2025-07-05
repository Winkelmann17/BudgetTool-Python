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
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QStackedWidget
from objects import *
from load import *

# ==========================================================================================================
#           Classes
# ==========================================================================================================
class MainWindow(QMainWindow):
    """Function that implements the Main Menu screen. Loads in the
    'main.ui' file. Allows user to select what year of budget data
    they want to access."""
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("rsrc/UI/main.ui", self)
        
        # NewYear Button
        self.NewYear.clicked.connect()

        # Year Buttons
        self.MMXXV.clicked.connect(lambda: self.gotoyear(2025))

    def createnewyear(self):
        """Function that loads the `newyear.ui` file and takes
        input from the user to create the new year object."""
        


    def gotoyear(self, year):
        """Function that loads the month select screen for 
        the chosen year."""
        print(year)
        monthscreen = MonthSelectScreen(year)
        widget.addWidget(monthscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# ----------------------------------------------------------------------------------------------------------

class MonthSelectScreen(QMainWindow):
    """Class that implements the Month Selection Screen. Loads in
    the 'months.ui' file. Allows user to select what month of budget
    data they want to access."""
    def __init__(self, year):
        self.year = year
        super(MonthSelectScreen, self).__init__()
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
    print("exiting")