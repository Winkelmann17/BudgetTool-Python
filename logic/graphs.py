""""
This program was written by Nicholas Winkelmann. 
Github:

This code serves as the code for various helper functions that make 
the code clearer in the screen files.

Last Updated: 17 September 2026
Recent Changes:
- Creation
"""
# ===================================================================
#           Imports
# ===================================================================
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from constants import *

# ===================================================================
#          Classes
# ===================================================================
class BarGraph(QWidget):
    """Class that implements the histogram of each major category and 
    saves the image so that it can be displayed in the respective 
    tab."""
    def __init__(self, month):
        super().__init__()

        # Creating MatPlot figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        # Adding Figure to the Specific Tab Widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        # Create the histogram
        self.create(month)

    def create(self, month):
        # Create plot
        plot = self.figure.add_subplot()

        # Sort through Data Category by Category
        amounts = []
        cats = DEFAULT_CATEGORIES
        cats.pop()      # removing income as a cat for graph
        for cat in cats:
            amounts.append(month.categories[cat].actual_total)

        # Make the plot
        plot.set_title(GRAPHTITLE)
        plot.set_xlabel(XAXIS)
        plot.set_ylabel(YAXIS)

        # Place on widget
        self.figure.tight_layout()
        self.canvas.draw()


class PieChart():
    pass

def piechart():
    """Function that creates a piechart of spending for each major
    category and saves the image so that it can be displayed in the 
    respective tab."""
    pass


# EOF
