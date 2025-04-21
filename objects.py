############################################################################################################
# Nicholas Winkelmann
# Desc: Year Class Code
# Last Updated: 5 Apr 2025
############################################################################################################
# ==========================================================================================================
#           Imports and Globals
# ==========================================================================================================


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
CATEGORIES = ["Savings", "Giving", "Housing", "Transportation", "Food", "Personal", "Insurance", "Other"]
PLANNED = 0
ACTUAL = 1
# TODO: Change this to datetime code to give the current year
CURRENT_YEAR = "2025"

# ==========================================================================================================
#           Classes
# ==========================================================================================================
class Expense():
    """Implements the Expense object that holds its name, planned 
    expense, and actual expense."""
    def __init__(self, name="<Empty Expense>", planned=0, actual=0):
        self.name = name
        self.planned = planned
        self.actual = actual

    def set_planned(self, new_planned):
        self.planned = new_planned

    def set_actual(self, new_actual):
        self.actual = new_actual
    
# -------------------------------------------------------------------

class Month():
    """Implement the Month object that holds its name, Expense 
    Categories and arrays of the expenses."""
    def __init__(self, name="<New Month>"):
        self.name = name
        self.categories = self.new_category_dict()
        self.totals = self.new_category_dict() # Planned is index 0, actual is 1
        self.notes = self.new_notes_dict()
        self.income_total = 0
        self.expense_total = 0


    def new_category_dict(self):
        """Function that creates a new category dictionary for every new month."""
        new_dict = {}
        for cat in CATEGORIES:
            new_dict[cat] = []
        return new_dict
    

    def new_notes_dict():
        """Function that creates a new category dictionary for the names of the 
        notes per category. These will be displayed via UI"""
        new_dict = {}
        for cat in CATEGORIES:
            new_dict[cat] = f"{cat}.txt"
    

    def add_new_expense(self, category, expense_name):
        """Function that adds a new expense to the category list."""
        self.categories.get(category).append(Expense(expense_name))


    def remove_expense(self, category, expense_name):
        """Function that rmeoves an expense from the chosen category."""
        expenses_list = self.categories.get(category)
        expenses_list.remove(expense_name)


    def copy_previous_month_data(self, prev_month):
        """Function that populates the chosen month with the previous months
        data."""
        # TODO: Add functionality to copy values from previous month
        pass

# -------------------------------------------------------------------

class Year():
    """Implements the Year object that holds the array of months."""
    def __init__(self, year=0000):
        self.months = self.populate_months()
        self.year = year

    def populate_months(self):
        """Function that populates months for the year."""
        temp = {}
        for month in MONTHS:
            temp[month] = Month(month)
        return temp


