import pytest
from PySide6.QtWidgets import QApplication
from test_function_solver import FunctionSolverApp
from PySide6.QtCore import Qt

@pytest.fixture
def app(qtbot):
    """Fixture to initialize the application."""
    test_app = QApplication.instance()
    if test_app is None:
        test_app = QApplication([])
    window = FunctionSolverApp()
    qtbot.addWidget(window)
    return window

def test_input_validation(app, qtbot):
    """Test input validation for empty fields."""
    qtbot.keyClicks(app.function1_input, "")
    qtbot.keyClicks(app.function2_input, "")
    qtbot.mouseClick(app.solve_button, Qt.LeftButton)
    assert "Please enter both functions" in app.statusBar().currentMessage()

def test_solution_and_plot(app, qtbot):
    """Test solving and plotting valid functions."""
    qtbot.keyClicks(app.function1_input, "x^2 - 4")
    qtbot.keyClicks(app.function2_input, "2*x")
    qtbot.mouseClick(app.solve_button, Qt.LeftButton)
    assert len(app.ax.lines) > 0  # Ensure plots are drawn