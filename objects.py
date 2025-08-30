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
TYPE_DICT = {
    "Income"            : ["Paycheck 1", "Paycheck 2", "Paycheck 3", "Paycheck 4", "Extra"],
    "Savings"           : ["House", "Car", "ROTHs", "Flights", "Gifts"],
    "Giving"            : ["Church", "Patrick"],
    "Housing"           : ["Mortgage", "Rent", "Water", "Natural Gas", "Electricity", "Phone", "Internet"],
    "Transportation"    : ["Gas", "Maintenance", "Car Loan"],
    "Food"              : ["Groceries", "Restaurants"],
    "Personal"          : ["V-Fun", "N-Fun", "Subscriptions", "Hair"],
    "Insurance"         : ["Auto", "Health", "Dental"],
    "Other"             : ["Cats", "Misc"] 
}
PLANNED = 0
ACTUAL = 1

# ==========================================================================================================
#           Classes
# ==========================================================================================================
class Cost():
    """Implements the Cost object that holds the name, data, and cost amount"""
    def __init__(self, name, cost, date):
        self.name = name
        self.cost = cost
        self.date = date
        print(f"{self.name}, {self.cost}, {self.date}")
        
class Expense_Type():
    """Implements the Expense object that holds its name, planned 
    expense, and actual expense."""
    def __init__(self, name="<Empty Expense>", planned=0, actual=0, income=False):
        self.name = name
        self.costs = []
        self.planned = planned
        self.actual = actual
        self.income = income

    def set_planned(self, new_planned):
        self.planned = new_planned

    def set_actual(self, new_actual):
        self.actual = new_actual

    def add_cost(self, name, cost, date):
        self.costs.append(Cost(name, cost, date))
        print(f"Cost named {name} added!")
        self.actual += cost

# -------------------------------------------------------------------

class Category():
    """Implements the Category object that holds the expenses per """
    def __init__(self, name):
        self.name = name
        self.expenses = self.initialize_expenses()
        self.planned_total = 0
        self.actual_total = 0

    def initialize_expenses(self):
        temp = {}
        for expense in TYPE_DICT[self.name]:
            temp[expense] = Expense_Type(expense)
        
        return temp

    def add_expense(self, name):
        pass

    def remove_expense(self):
        pass

    def sum_planned(self):
        """Sum the planned values in each expense type."""
        print("PLANNED")
        temp = 0.00
        for exp in TYPE_DICT[self.name]:
            print(f"{self.expenses[exp].planned}")
            temp += self.expenses[exp].planned
        self.planned_total = temp

    def sum_actual(self):
        """Sum the actual values in each expense type."""
        print("ACTUAL")
        temp = 0.00
        for exp in TYPE_DICT[self.name]:
            for cost in self.expenses[exp].costs:
                print(f"{cost.cost}")
                temp += cost.cost
        self.actual_total = temp

    def add_exp_type(self, name):
        pass

    def remove_exp_type(self, name):
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
        self.cat_map = {}
        self.new = True

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
