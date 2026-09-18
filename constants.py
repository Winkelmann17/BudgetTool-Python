""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves all constants used within the WinkelBudget program.

Last Updated: 17 September 2026
Recent Changes:
- Added constants for graphs
"""
# Screen paths
MAINWINDOW_UI = "./rsrc/UI/MainWindow.ui"
BUDGETSCREEN_UI = "./rsrc/UI/BudgetScreenWidget.ui"
TEST_UI = "./rsrc/UI/TableTest.ui"
EXPENSE_POPUP_UI = "./rsrc/UI/ExpensePopUp.ui"

# DIALOG
OK = 0
CANCEL = 1

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

# REGEX 
COST_REGEX = r"(-?(?:\d+\.\d{1,2}|\d+\.|\.\d{1,2}|\d+))"

# Graphs
GRAPHTITLE = "Spending by Category"
XAXIS = "Category"
YAXIS = "Money Spent"

# EOF
