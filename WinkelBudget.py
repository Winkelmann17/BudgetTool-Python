""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the main entry point for WinkelBudget.

Last Updated: 10 July 2026
Recent Changes:
- Simplifying code
- Made this the main entry point of WinkelBudget
"""
# ===================================================================
#           Imports
# ===================================================================
import sys
from PyQt6.QtWidgets import QApplication

from main_window import MainWindow

# ===================================================================
#           Main
# ===================================================================
def main():
    app = QApplication(sys.argv)

    window = MainWindow(int(sys.argv[1]), int(sys.argv[2])) # Change this later
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

# EOF
