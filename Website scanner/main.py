from PySide6.QtWidgets import QApplication
from gui.main_window import SafeStreamApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SafeStreamApp()
    window.show()
    sys.exit(app.exec())
