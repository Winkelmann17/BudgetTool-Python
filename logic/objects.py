""""
This program was written by Nicholas Winkelmann. 
Github: https://github.com/Winkelmann17

This code serves as the primary location of the main objects and 
logic used by this program for the budget calculations.

Last Updated: 15 September 2026
Recent Changes:
- Updated total calculations for months
- Added tracking for highest expense in month object
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
        self.notes = ""
        self.income_total = 0
        self.expense_total = 0
        self.planned_total = 0
        self.highest_cost = Cost("None", 0, "--/--/--")
        self.rows = 48
        self.cols = 3
        self.categories = self.initialize_cats()
        self.cat_exp_listing = DEFAULT_TYPE_DICT

        # Working variables
        self.update_queue = []

# -------------------------------------------------------------------
    def initialize_cats(self):
        temp = {}
        for cat in DEFAULT_CATEGORIES:
            temp[cat] = Category(cat)
        
        return temp

# -------------------------------------------------------------------
    def calculate_totals(self):
        """Function calls all category objects and sums their 
        totals."""
        self.income_total = 0
        self.planned_total = 0
        self.expense_total = 0
        for cat in self.categories.keys():
            if cat != "Income":
                self.planned_total += self.categories[cat].planned_total
                self.expense_total += self.categories[cat].actual_total
            else:
                self.income_total = self.categories[cat].actual_total
        print(f"Calculated: planned = {self.planned_total} actual = {self.expense_total} income = {self.income_total}")

# -------------------------------------------------------------------
    def set_highest_cost(self, name, cost_value, date):
        """Setter function for highest_cost."""
        self.highest_cost = Cost(name, cost_value, date)

# ===================================================================
#           Category
# ===================================================================
class Category():
    def __init__(self, name):
        self.name = name
        self.planned_total = 0
        self.actual_total = 0
        self.expenses, self.expense_list = self.initialize_expenses()

# -------------------------------------------------------------------
    def initialize_expenses(self):
        temp = {}
        temp2 = []
        for expense in DEFAULT_TYPE_DICT[self.name]:
            temp[expense] = Expense(expense)
            temp2.append(expense)
        
        return temp, temp2

# -------------------------------------------------------------------
    def sum_planned(self):
        temp = 0.00
        for exp in self.expense_list:
            temp += self.expenses[exp].planned
        print(temp)
        self.planned_total = temp

    def sum_actual(self):
        temp = 0.00
        for exp in self.expense_list:
            temp += self.expenses[exp].actual
        print(temp)
        self.actual_total = temp

# -------------------------------------------------------------------
    def add_expense(self, expense):
        self.expenses[expense] = Expense(expense)
        self.expense_list.append(expense)

# -------------------------------------------------------------------
    def remove_expense(self, expense):
        removed = self.expenses.pop(expense)
        self.expense_list.remove(expense)
        return removed

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
