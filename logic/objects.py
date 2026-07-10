""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the primary location of the main objects and 
logic used by this program for the budget calculations.

Last Updated: 10 July 2026
Recent Changes:
- Simplifying and Reorganizing Code
"""
# ===================================================================
#           Imports
# ==================================================================

# ===================================================================
#           Months
# ===================================================================
class Month():
    """
    Implements the Month object that holds its name, Expense 
    Categories, Notes, and Path to stored data (if any).
    """
    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.notes = "Notes"
        self.income_total = 0
        self.expense_total = 0
        self.categories = {}


# -------------------------------------------------------------------

# ===================================================================
#           Category
# ===================================================================
class Category():
    def __init__(self):
        pass

# -------------------------------------------------------------------

# ===================================================================
#            Cost
# ===================================================================
class Cost():
    def __init__(self):
        pass

# -------------------------------------------------------------------


# EOF
