""""
This program was written by Winkelmann17. 
Github: https://github.com/Winkelmann17

This code serves as the code for various helper functions that make 
the code clearer in the screen files.

Last Updated: 29 October 2026
Recent Changes:
- Preparing for final release
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
 