############################################################################################################
# Nicholas Winkelmann
# Desc: Year Class Code
# Last Updated: 10 Jul 2025
############################################################################################################
# ==========================================================================================================
#           Imports and Globals
# ==========================================================================================================

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
CATEGORIES = ["Income", "Savings", "Giving", "Housing", "Transportation", "Food", "Personal", "Insurance", "Other"]
PLANNED = 0
ACTUAL = 1

# ==========================================================================================================
#           Classes
# ==========================================================================================================
class Expense():
    """Implements the Expense object that holds its name, planned 
    expense, and actual expense."""
    def __init__(self, name="<Empty Expense>", planned=0, actual=0, income=False):
        self.name = name
        self.planned = planned
        self.actual = actual
        self.date = ""
        self.income = income

    def set_planned(self, new_planned):
        self.planned = new_planned

    def set_actual(self, new_actual):
        self.actual = new_actual

    def set_date(self):
        pass

# -------------------------------------------------------------------

class Category():
    """Implements the Category object that holds the expenses per """
    def __init__(self, name):
        self.name = name
        self.expenses = []
        self.planned_total = 0
        self.actual_total = 0

    def add_expense(self):
        pass

    def remove_expense(self):
        pass

    def sum_planned(self):
        pass

    def sum_actual(self):
        pass

# -------------------------------------------------------------------

class Month():
    """Implement the Month object that holds its name, Expense 
    Categories and arrays of the expenses."""
    def __init__(self, name):
        self.name = name
        self.notes = "Notes"
        self.income_total = 0
        self.expense_total = 0
        self.planned_total = 0
        self.categories = self.initialize_cats()

    def initialize_cats(self):
        temp = {}
        for cat in CATEGORIES:
            temp[cat] = Category(cat)
        return temp

    def sum_income_total(self):
        pass

    def sum_expenses(self):
        pass

    def copy_previous_month(self):
        pass

    def update_notes(self):
        pass


# -------------------------------------------------------------------

class Year():
    """Implements the Year object that holds the array of months."""
    def __init__(self, name="0000"):
        self.name = name
        self.months = self.populate_months()

    def populate_months(self):
        """Function that populates months for the year."""
        temp = {}
        for month in MONTHS:
            temp[month] = Month(month)
        return temp

# -------------------------------------------------------------------
