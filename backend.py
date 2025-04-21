############################################################################################################
# Nicholas Winkelmann
# Desc: Year Class Code
# Last Updated: 21 Apr 2025
############################################################################################################
# ==========================================================================================================
#           Imports
# ==========================================================================================================
from objects import Year, Month, Expense
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

# ==========================================================================================================
#           Classes
# ==========================================================================================================
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

class Screen(QtWidgets.QWidget):
    def __init__(self, text=None):
        super().__init__()
        
        self.layout = QtWidgets.QVBoxLayout(self)
        if text != None:
            self.text = QtWidgets.QLabel(text, alignment=QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.text)
        


# ==========================================================================================================
#           Main
# ==========================================================================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Screen("Chungus")
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())