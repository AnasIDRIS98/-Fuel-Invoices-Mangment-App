# main.py - Entry point for PySide6 desktop app for Fuel Invoices Management
from PySide6 import QtWidgets, QtCore, QtGui
from auth import AuthDialog
from ui_components import MainWindow
from db import init_db
import sys
import os

APP_NAME = "Fuel Invoices Management App"

def main():
    # Ensure DB exists
    init_db()

    app = QtWidgets.QApplication(sys.argv)
    # Set basic app style
    app.setStyle('Fusion')

    # Authentication dialog centered
    auth = AuthDialog()
    if auth.exec() == QtWidgets.QDialog.Accepted:
        username = auth.username
        # open main window
        win = MainWindow(user=username)
        win.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
