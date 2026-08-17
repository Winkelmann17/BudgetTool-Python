""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves all constants used within the WinkelBudget program.

Last Updated: 10 July 2026
Recent Changes:
- Dedicated File
"""
# Screen paths
MAINWINDOW_UI = "./rsrc/UI/MainWindow.ui"
BUDGETSCREEN_UI = "./rsrc/UI/BudgetScreenWidget.ui"

# Object Data
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DEFAULT_CATEGORIES = ["Income", "Savings", "Giving", "Housing", "Transportation", "Food", "Personal", "Insurance", "Other"]
DEFAULT_TYPE_DICT = {
    "Income"            : ["Paycheck 1", "Paycheck 2", "Paycheck 3", "Paycheck 4", "Extra/Other 1", "Extra/Other 2"],
    "Savings"           : ["Car", "ROTHs", "Flights", "Gifts"],
    "Giving"            : ["Church", "Focus"],
    "Housing"           : ["Mortgage", "Water", "Electricity", "Phone", "Internet"],
    "Transportation"    : ["Gas", "Maintenance"],
    "Food"              : ["Groceries", "Restaurants"],
    "Personal"          : ["V-Fun", "N-Fun", "Subscriptions"],
    "Insurance"         : ["Car", "Health", "Dental", "Vision"],
    "Other"             : ["Cats", "Misc"] 
}
PLANNED = 0
ACTUAL = 1

# EOF
