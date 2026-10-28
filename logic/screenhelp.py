""""
This program was written by Nicholas Winkelmann. 
Github: https://github.com/Winkelmann17

This code serves as the code for various helper functions that make 
the code clearer in the screen files.

Last Updated: 19 August 2026
Recent Changes:
- Creation
"""
# ===================================================================
#           Imports
# ===================================================================
from PyQt6.QtGui import QColor

default_text = "$ - "
total_text = "Total"
bg_red = QColor(222, 78, 81)
bg_green =  QColor(118, 222, 115)
bg_white = QColor(255, 255, 255)
# ===================================================================
#          Functions
# ===================================================================
def add_table_row():
    pass

def process_cell_text(table, row, planned_val, actual_val):
        planned_cell = table.item(row, 0)
        actual_cell = table.item(row, 1)
        diff_cell = table.item(row, 2)
        diff_calc = planned_val - actual_val

        if planned_val != 0.0:
            planned_cell.setText(f"${planned_val:.2f}")
        else:
            planned_cell.setText(default_text)
        if actual_val != 0.00:
            actual_cell.setText(f"${actual_val:.2f}")
        else:
            actual_cell.setText(default_text)
        diff_cell.setText(f"${diff_calc:.2f}")  
        # Update colors
        # Change color of cell
        if diff_calc < 0.00:      
            diff_cell.setBackground(bg_red)
        elif diff_calc > 0.00:
                  
            diff_cell.setBackground(bg_green)
        else:
            diff_cell.setBackground(bg_white)
            diff_cell.setText(default_text) 


# EOF

# ROW UPDATES
        # planned = self.budgetTable.item(row, 0)
        # actual = self.budgetTable.item(row, 1)
        # difference = self.budgetTable.item(row, 2)
        # diff_calc = expense.planned - expense.actual

        # Check for text
        # if expense.planned != 0.00:
        #     planned.setText(f"${expense.planned}")
        # else:
        #     planned.setText(self.default_text)
        # if expense.actual != 0.00:
        #     actual.setText(f"${expense.actual}")
        # else:
        #     actual.setText(self.default_text)
        # difference.setText(f"${diff_calc}")        

        # # Change color of cell
        # if diff_calc < 0.00:
        #     difference.setBackground(self.bg_red)
        # elif diff_calc > 0.00:
        #     difference.setBackground(self.bg_green)
        # else:
        #     difference.setBackground(self.bg_white)
        #     difference.setText(self.default_text)

# TOTAL UPDATES
        # total_planned = self.budgetTable.item(row, 0)
        # total_actual = self.budgetTable.item(row, 1)
        # total_diff = self.budgetTable.item(row, 2)
        # diff_calc = category.planned_total - category.actual_total
        # if category.planned_total != 0.0:
        #     total_planned.setText(f"${category.planned_total:.2f}")
        # else:
        #     total_planned.setText(self.default_text)
        # if category.actual_total != 0.00:
        #     total_actual.setText(f"${category.actual_total:.2f}")
        # else:
        #     total_actual.setText(self.default_text)
        # total_diff.setText(f"${diff_calc:.2f}")        

        # # Update colors
        # # Change color of cell
        # if diff_calc < 0.00:
        #     total_diff.setBackground(self.bg_red)
        # elif diff_calc > 0.00:
        #     total_diff.setBackground(self.bg_green)
        # else:
        #     total_diff.setBackground(self.bg_white)
        #     total_diff.setText(self.default_text)   