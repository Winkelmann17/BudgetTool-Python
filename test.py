import sys
from time import sleep
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QStackedWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("rsrc/UI/main.ui", self)
        self.MMXXV.clicked.connect(lambda: self.gotoyear(2025))
        # TODO: Add about 5 months to choose from. 

    def gotoyear(self, year):
        print(year)
        monthscreen = MonthSelectScreen()
        widget.addWidget(monthscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class MonthSelectScreen(QMainWindow):
    def __init__(self, year):
        self.year = year
        super(MonthSelectScreen, self).__init__()
        loadUi("rsrc/UI/months.ui", self)
        self.jan.clicked.connect(lambda: self.gotobudget(year))

    def gotobudget(self, year):
        print(year)
        budgetscreen =

class BudgetScreen(QMainWindow):
    def __init__(self):
        super(BudgetScreen, self).__init__()
        loadUi("rsrc/UI/budget.ui", self)
        

# Main
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