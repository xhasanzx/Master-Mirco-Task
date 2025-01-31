import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sympy import symbols, sympify, solve

# Define the main application window
class FunctionSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Solver and Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input fields for the functions
        self.function1_input = QLineEdit(self)
        self.function1_input.setPlaceholderText("Enter the first function of x, e.g., 5*x^3 + 2*x")
        layout.addWidget(QLabel("Function 1:"))
        layout.addWidget(self.function1_input)

        self.function2_input = QLineEdit(self)
        self.function2_input.setPlaceholderText("Enter the second function of x, e.g., x^2 - 4")
        layout.addWidget(QLabel("Function 2:"))
        layout.addWidget(self.function2_input)

        # Solve and plot button
        self.solve_button = QPushButton("Solve and Plot", self)
        self.solve_button.clicked.connect(self.solve_and_plot)
        layout.addWidget(self.solve_button)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def solve_and_plot(self):
        """Solve the functions and plot them."""
        try:
            # Get user input
            func1_str = self.function1_input.text().strip()
            func2_str = self.function2_input.text().strip()

            # Validate input
            if not func1_str or not func2_str:
                raise ValueError("Please enter both functions.")

            # Define the symbol x
            x = symbols('x')

            # Parse the functions
            func1 = sympify(func1_str)
            func2 = sympify(func2_str)

            # Solve the functions
            solution = solve(func1 - func2, x)
            if not solution:
                raise ValueError("No solution found for the given functions.")

            # Convert solutions to float
            solution = [float(sol.evalf()) for sol in solution]

            # Generate x values for plotting
            x_vals = np.linspace(-10, 10, 400)
            y1_vals = [func1.subs(x, val).evalf() for val in x_vals]
            y2_vals = [func2.subs(x, val).evalf() for val in x_vals]

            # Clear the previous plot
            self.ax.clear()

            # Plot the functions
            self.ax.plot(x_vals, y1_vals, label=f"Function 1: {func1_str}")
            self.ax.plot(x_vals, y2_vals, label=f"Function 2: {func2_str}")

            # Plot the solution points
            for sol in solution:
                y_sol = func1.subs(x, sol).evalf()
                self.ax.plot(sol, y_sol, 'ro')  # Red dot for solution
                self.ax.annotate(f"({sol:.2f}, {y_sol:.2f})", (sol, y_sol), textcoords="offset points", xytext=(10, 10), ha='center')

            # Add labels and legend
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.legend()
            self.ax.grid(True)

            # Refresh the canvas
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionSolverApp()
    window.show()
    sys.exit(app.exec())
    