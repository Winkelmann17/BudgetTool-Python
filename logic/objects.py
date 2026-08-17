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
from constants import *

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
        self.planned_total = 0
        self.rows = 48
        self.cols = 3
        self.categories = {}
        self.cat_map = {}

# -------------------------------------------------------------------
    def initialize_cats(self):
        temp = {}
        for cat in DEFAULT_CATEGORIES:
            temp[cat] = Category(cat)
        
        return temp
# ===================================================================
#           Category
# ===================================================================
class Category():
    def __init__(self, name):
        self.name = name
        self.expenses = self.initialize_expenses()

# -------------------------------------------------------------------
    def initialize_expenses(self):
        temp = {}
        for expense in DEFAULT_TYPE_DICT[self.name]:
            temp[expense] = Expense(expense)
        
        return temp

# ===================================================================
#           Expense
# ===================================================================
class Expense():
    """Implements the Expense object, this tracks the individual 
    values of a specific expense on the chart. This object holds
    an array of cost objects that give the total planned and actual
    expense values to be displayed on the table."""
    def __init__(self, name="<Empty Expense>", income=False):
        self.name = name
        self.costs = []
        self.planned = 0
        self.actual = 0
        self.income = income

# -------------------------------------------------------------------
    def set_planned(self, new_planned):
        self.planned = new_planned

    def set_actual(self, new_actual):
        self.actual = new_actual

    def add_cost(self, name, cost_value, date):
        self.costs.append(Cost(name, cost_value, date))
        print(f"Cost named {name} added!")
        self.actual += cost_value

# ===================================================================
#            Cost
# ===================================================================
class Cost():
    """Implements the cost object. Basically a container for 
    specific purcahses within a specified expense category. Holds 
    the actual cost value, the name, and the date it occurred."""
    def __init__(self, name, cost_value, date):
        self.name = name
        self.cost_value = cost_value
        self.date = date

# -------------------------------------------------------------------

# EOF
