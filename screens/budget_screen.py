""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the UI interaction code for the main budget 
screen. 

Last Updated: 10 July 2026
Recent Changes:
- Overhauling UI
- Simplifying code
"""
# ===================================================================
#           Imports
# ===================================================================
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.uic import loadUi

from constants import *
from logic.objects import Month
from logic.serializer import Serializer

# ===================================================================
#           Classes
# ===================================================================
class BudgetScreen(QWidget):
    """
    Implementation of the BudgetScreen class that serves as the
    source of the interactive code for the Budget Screen. Loaded by
    main_window.py.
    """

    default_text = "$ - "
    total_text = "Total"

    def __init__(self, month, year, statusbar):
        super().__init__()

        # Load the First UI Page
        loadUi(TEST_UI, self)
        self.statusbar = statusbar

        # Setup Month handler data
        self.old_budget = None
        self.serializer = Serializer(month, year)
        self.month = self.serializer.deserialize()
        if self.month == None:
            self.statusbar.showMessage("LIGMA! No months :((((")
            self.month = Month(month, year)
            #self.loadtable_defaults()
        self.catmap = self.loadtable()
  
        # Connect buttons to functions
        self.saveButton.clicked.connect(lambda: self.serializer.serialize(self.month))
        # self.copyLastMonthButton.clicked.connect()
        # self.newCategoryButton.clicked.connect()
        # self.removeButton.clicked.connect()
        # self.futureButton.clicked.connect()

        # Connect menu bar options to functions
        # self.actionSave.triggered.connect(self.go_save_month_data)
        # self.actionBack.triggered.connect(go_back)
        # self.actionHome.triggered.connect(go_back)      #TODO: Broken when set to go_home, can't open months

        # Connect events to functions
        # self.budgetTable.itemChanged.connect(self.go_update_planned)
        # self.budgetTable.cellClicked.connect(self.go_update_list)

        # Other
        # self.expList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.expList.customContextMenuRequested.connect(self.open_list_menu)
# ----------------------------------------------------------------------------
    def loadtable_defaults(self):                                   # POSSIBLE CODE REUSE FOR LOADING FROM SAVED TABLE
        """Function that loads all boxes with the default text. 
        Creates the months cat_map and returns it."""
        print("[+] Loading Table Defaults and Creating Cat Map...")
        temp = {}
        for row in range(self.month.rows):
            temp[self.budgetTable.verticalHeaderItem(row).text()] = row
            for col in range(self.month.cols):
                self.budgetTable.setItem(row, col, QTableWidgetItem(self.default_text))
        self.ignore_cell_changes = False
        
        # Save the cat map for the new month
        self.month.cat_map = temp


    def loadtable(self):
        """Function that loads all table values from the stored data
        within the loaded month object. Returns the category map for 
        the working month for better data editing."""
        temp = {}
        row = 0
        # Get categories from loaded month
        for category in self.month.categories.keys():
            # Add category row for dilineation
            temp[category] = row
            row_name = f"_{category.upper()}_"
            self.budgetTable.insertRow(row)
            self.budgetTable.setVerticalHeaderItem(row, QTableWidgetItem(row_name))
            row += 1

            expenses = self.month.cat_exp_listing[category]
            for exp in expenses:
                temp[exp] = row

                # Setup table
                self.budgetTable.insertRow(row)
                self.budgetTable.setVerticalHeaderItem(row, QTableWidgetItem(exp))

                planned = self.month.categories[category].expenses[exp].planned
                actual = self.month.categories[category].expenses[exp].actual
                diff = planned - actual
                if planned == 0:
                    planned_text= self.default_text
                else:
                    planned_text = f"${planned:.2f}"
                if actual == 0: 
                    actual_text = self.default_text
                else:
                    actual_text = f"${actual:.2f}"
                if diff == 0:
                    diff_text = self.default_text
                else:
                    diff_text = f"${diff:.2f}"
                self.budgetTable.setItem(row, 0, QTableWidgetItem(planned_text))
                self.budgetTable.setItem(row, 1, QTableWidgetItem(actual_text))
                self.budgetTable.setItem(row, 2, QTableWidgetItem(diff_text))

                row+= 1
            # Add Total for Category
            total_key = f"{category}_total"
            temp[total_key] = row
            self.budgetTable.insertRow(row)
            self.budgetTable.setVerticalHeaderItem(row, QTableWidgetItem(self.total_text))

            planned = self.month.categories[category].planned_total
            actual = self.month.categories[category].actual_total
            diff = planned - actual
            if planned == 0:
                planned_text= self.default_text
            else:
                planned_text = f"${planned:.2f}"
            if actual == 0: 
                actual_text = self.default_text
            else:
                actual_text = f"${actual:.2f}"
            if diff == 0:
                diff_text = self.default_text
            else:
                diff_text = f"${diff:.2f}"
            self.budgetTable.setItem(row, 0, QTableWidgetItem(planned_text))
            self.budgetTable.setItem(row, 1, QTableWidgetItem(actual_text))
            self.budgetTable.setItem(row, 2, QTableWidgetItem(diff_text))
            row += 1

        return temp

# ----------------------------------------------------------------------------

# EOF
