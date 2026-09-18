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
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        # Adding Figure to the Specific Tab Widget
        self.plot = self.figure.add_subplot()
        # Create the histogram
        self.create(month)

    def create(self, month):
        # Clear plot for updating
        self.plot.clear()
        # Get data by category
        amounts = []
        for cat in GRAPH_CATS:
                amounts.append(month.categories[cat].actual_total)
        bars = self.plot.bar(GRAPH_CATS, amounts)
        self.plot.bar_label(bars)
        # Update plot metadata
        self.plot.set_title(GRAPHTITLE)
        self.plot.set_xlabel(XAXIS)
        self.plot.set_ylabel(YAXIS)
        self.plot.margins(y=0.15)
        # Draw the new plot with updated data
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
