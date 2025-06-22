import sys
from time import sleep
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QStackedWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("rsrc/UI/main.ui", self)

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