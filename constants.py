""""
This program was written by Winkelmann17. 
Github: https://github.com/Winkelmann17

This code serves all constants used within the WinkelBudget program.

Last Updated: 29 October 2026
Recent Changes:
- Preparing for final release
"""
# Screen paths
MAINWINDOW_UI = "./rsrc/UI/MainWindow.ui"
BUDGETSCREEN_UI = "./rsrc/UI/BudgetScreen.ui"
ADD_EXPENSE_POPUP_UI = "./rsrc/UI/ExpensePopUp.ui"
EDIT_CATEGORY_POPUP_UI = "./rsrc/UI/EditCategoryPopUp.ui"

# Window Titles
MAINTITLE = "WinkelBudget 1.0"
STYLE = "windowsvista"

# Object Data
MONTHS = ["January", 
          "February", 
          "March", 
          "April", 
          "May", 
          "June", 
          "July", 
          "August", 
          "September", 
          "October", 
          "November", 
          "December"]
DEFAULT_CATEGORIES = ["Income", "Savings", "Giving", "Housing", "Transportation", "Food", "Personal", "Insurance", "Other"]
DEFAULT_TYPE_DICT = {
    "Income"            : ["Paycheck 1", "Paycheck 2", "Paycheck 3", "Paycheck 4", "Extra/Other 1", "Extra/Other 2"],
    "Savings"           : ["New Car", "ROTHs", "Flights", "Gifts"],
    "Giving"            : ["Church", "Food Bank"],
    "Housing"           : ["Mortgage", "Water", "Electricity", "Phone", "Internet"],
    "Transportation"    : ["Gas", "Maintenance"],
    "Food"              : ["Groceries", "Restaurants"],
    "Personal"          : ["Fun", "Subscriptions"],
    "Insurance"         : ["Car", "Health", "Dental", "Vision"],
    "Other"             : ["Pets", "Misc"] 
}
PLANNED = 0
ACTUAL = 1

# REGEX 
COST_REGEX = r"(-?(?:\d+\.\d{1,2}|\d+\.|\.\d{1,2}|\d+))"

# Graphs
GRAPHTITLE = "Spending by Category"
XAXIS = "Category"
YAXIS = "Money Spent"
GRAPH_CATS = ["Savings", "Giving", "Housing", "Transportation", "Food", "Personal", "Insurance", "Other"]
DISPLAY_CATS = ["Savings", "Giving", "Housing", "Trans", "Food", "Person", "Insur", "Other"]
FORMAT = "%1.2f%%"

# Argparse
DESC = "Custom Python, QT Budget Application built by Winkelmann17."
EPILOG = "How to use the program:\n" \
"python WinkelBudget.py Jan 2026\n" \
"    - Open the application for editing the month of January in the year 2026\n" \
"python WinkelBudget.py 11 2007\n" \
"    - Open the application for editing the month of November in 2007\n"
VERSION = "WinkelBudget 1.0"
RECENT_CHANGES = "Recent Changes:\n" \
"- Complete redone codebase from ground up" \
"- New resizable UI, graphs, and dialog box for more intuitive use"
MONTH_INPUT_DICTIONARY = {
    "1":"January",
    "jan":"January",
    "january":"January",

    "2":"February",
    "feb":"February",
    "february":"February",

    "3":"March",
    "mar":"March",
    "march":"March",

    "4":"April",
    "apr":"April",
    "april":"April",

    "5":"May",
    "may":"May",

    "6":"June",
    "jun":"June",
    "june":"June",

    "7":"July",
    "jul":"July",
    "july":"July",

    "8":"August",
    "aug":"August",
    "august":"August",

    "9":"September",
    "sep":"September",
    "september":"September",

    "10":"October",
    "oct":"October",
    "october":"October",

    "11":"November",
    "nov":"November",
    "november":"November",

    "12":"December",
    "dec":"December",
    "December":"December"
}
MIN_YEAR = 1
MAX_YEAR = 9999
NUM_ARGS = 4
EXP_NAME_LEN = 32
EXP_DESC_LEN = 32

# EOF
