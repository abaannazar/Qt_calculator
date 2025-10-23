import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
from ui_form import Ui_Widget  # Make sure this is generated from your .ui file

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.setWindowTitle("Calculator")

        # Apply rounded bottom corners to the main window
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 20px;
                border-bottom-right-radius: 20px;
            }
        """)

        self.init_signals()

    def init_signals(self):
        # Connect digit buttons
        for i in range(10):
            button = getattr(self.ui, f"b_{i}")
            button.clicked.connect(lambda checked, i=i: self.append(str(i)))

        # Connect operators
        self.ui.b_a.clicked.connect(lambda: self.append(" + "))
        self.ui.b_s.clicked.connect(lambda: self.append(" - "))
        self.ui.b_m.clicked.connect(lambda: self.append(" x "))
        self.ui.b_d.clicked.connect(lambda: self.append(" ÷ "))

        # Connect clear and equals
        self.ui.b_c.clicked.connect(self.clear)
        self.ui.b_e.clicked.connect(self.calculate)

    def append(self, value):
        current_text = self.ui.screen.text()

        # Prevent appending multiple operators
        if value in " + - X ÷":
            if current_text and current_text[-1] in " + - X ÷":
                return

        # Append the value to the screen
        self.ui.screen.setText(current_text + value)

    def clear(self):
        self.ui.screen.clear()

    def calculate(self):
        try:
            expression = self.ui.screen.text()

            # Replace display symbols with valid Python operators
            expression = expression.replace("x", "*").replace("÷", "/")
            
            # Evaluate the expression safely
            result = eval(expression)

            # Ensure that the result is formatted with a decimal point if necessary
            if isinstance(result, float):
                result = "{:.6f}".format(result).rstrip('0').rstrip('.')  # Remove unnecessary trailing zeros

            # Display the result
            self.ui.screen.setText(str(result))

        except (SyntaxError, ZeroDivisionError):
            # Handle syntax errors or division by zero
            self.ui.screen.setText("Error")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
