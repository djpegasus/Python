import sys
from PyQt6.QtWidgets import QApplication
from loginMain import Crm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = Crm()
    login_window.show()
    sys.exit(app.exec())