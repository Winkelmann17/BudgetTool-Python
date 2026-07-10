""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the main entry point for WinkelBudget

Last Updated: 10 July 2026
Recent Changes:
- Overhauling UI
- Simplifying code
"""
# ===================================================================
#           Imports
# ===================================================================
import sys
from PyQt6.QtWidgets import QApplication

from main_window import MainWindow
# ===================================================================
#           Functions
# ===================================================================

# ===================================================================
#           Main
# ===================================================================
def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()