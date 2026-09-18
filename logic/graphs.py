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
    """Class that implements the bar graph of each major category and 
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
        """Function that creates a new plot with the expense
        data in a month."""
        # Clear plot for updating
        self.plot.clear()
        # Get data by category
        amounts = []
        for cat in GRAPH_CATS:
                amounts.append(month.categories[cat].actual_total)
        bars = self.plot.bar(DISPLAY_CATS, amounts)
        self.plot.bar_label(bars)
        # Update plot metadata
        self.plot.set_title(GRAPHTITLE, pad=0)
        self.plot.set_xlabel(XAXIS)
        self.plot.set_ylabel(YAXIS)
        self.plot.margins(y=0.15)
        # Draw the new plot with updated data
        self.figure.tight_layout()
        self.canvas.draw()


class PieChart(QWidget):
    """Class that implements the Pie Chart of each major category 
    and saves the image so that it can be displayed in the respective 
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
        self.total = 0
        # Create the histogram
        self.create(month)

    def create(self, month):
        """Function that creates a new plot with the expense
        data in a month."""
        # Clear plot for updating
        self.plot.clear()
        self.plot.axis("off")
        # Get data by category
        amounts = []
        cats = []
        for cat in GRAPH_CATS:
                amount = month.categories[cat].actual_total
                if amount > 0:
                    cats.append(cat)
                    amounts.append(amount)
        # Create the labels and percentages
        self.total = sum(amounts)
        # # Create PieChart
        if self.total != 0:
            self.plot.pie(amounts, labels=cats, autopct=FORMAT)
        # Put No Data if you cannot make a pie chart
        else:
            self.plot.set_xlim(-1, 1)
            self.plot.set_ylim(-1, 1)
            self.plot.text(0, 0, "No Data", fontsize=16, ha="center", va="center")
            
        # Update chart metadata
        self.plot.set_title(GRAPHTITLE, pad=0)
        # Draw the new plot with updated data
        self.figure.tight_layout()
        self.canvas.draw()

# EOF
