""""
This program was written by Winkelmann17. 
Github: https://github.com/Winkelmann17

This code serves as the main entry point for WinkelBudget.

Last Updated: 29 October 2026
Recent Changes:
- Preparing for final release
"""
# ===================================================================
#           Imports
# ===================================================================
import argparse
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QApplication, QStyleFactory

from constants import *
from main_window import MainWindow

# ===================================================================
#               Functions
# ===================================================================
def get_inputs():
    """Function that handles command line inputs for the specific 
    months and years that will be used. Will be replaced with an
    all UI solution in a future release.
    """
    # Parser and argument setup
    parser = argparse.ArgumentParser(
        prog="python WinkelBudget.py",
        description=DESC,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
        )
    parser.add_argument(
        "-m",
        "--month",
        required=True,
        help="The month that you wish to edit [1,2..12 OR Jan,Feb,...Dec OR January,February,...December]"
    )
    parser.add_argument(
        "-y", 
        "--year", 
        required=True,
        type=int,
        help="The year that the month you wish to edit is in. [2026, 2027, etc]"
    )

    # Parse the args
    args = parser.parse_args()
    month : str = args.month
    year : int = args.year
    total_args = len(sys.argv) - 1 # 1 is the source file, subtract that
    
    # Check all inputs are valid via a variety of checks
    errors = []
    # Arg number checks
    if total_args < NUM_ARGS:
        errors.append("Not enough args specified. At least an image and a " \
        "-m <messagepath> or -e for extraction are required") 
    elif total_args > NUM_ARGS:
        errors.append("Too many arguments specified.")

    # Check that years and months are valid
    month = MONTH_INPUT_DICTIONARY.get(month.lower())
    if month == None:
        errors.append("Invalid month specified, please choose a valid month.")
    if year < MIN_YEAR or year > MAX_YEAR:
        errors.append("Invalid year specified, please choose a year above 1" \
        "and below 9999")
    else: 
        year = int(year)

    # Print the erros underneath the help message. Helps make it more clear
    # what the actual problem is.
    if errors:
        parser.print_help()
        print("\nThe following errors with your input were found:")
        for error in errors:
            print(f"- {error}")
        print()
        exit()

    # All is good, return data to main
    else:
        return month, year
    
# ===================================================================
#           Main
# ===================================================================
def main():

    # Get inputs from command line
    month, year = get_inputs()

    # Start QT Application and call the MainWindow
    app = QApplication(sys.argv)
    app.setStyle(STYLE)
    window = MainWindow(month, year)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

# EOF
