# auth.py - simple auth dialog using local SQLite users table
from PySide6 import QtWidgets, QtCore
from db import get_user, create_user, verify_password, log_action
from PySide6.QtGui import QPixmap
import os

class AuthDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login - Fuel Invoices")
        self.setModal(True)
        self.username = None
        self.resize(420, 300)
        layout = QtWidgets.QVBoxLayout(self)

        # background/branding (simple label with pixmap if exists)
        assets = os.path.join(os.path.dirname(__file__), "assets")
        bg_path = os.path.join(assets, "refinery_bg.jpg")
        if os.path.exists(bg_path):
            lbl = QtWidgets.QLabel(self)
            pix = QPixmap(bg_path).scaledToWidth(380, QtCore.Qt.SmoothTransformation)
            lbl.setPixmap(pix)
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(lbl)

        form = QtWidgets.QFormLayout()
        self.user_edit = QtWidgets.QLineEdit()
        self.pw_edit = QtWidgets.QLineEdit()
        self.pw_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        form.addRow("Username:", self.user_edit)
        form.addRow("Password:", self.pw_edit)
        layout.addLayout(form)

        btns = QtWidgets.QHBoxLayout()
        self.login_btn = QtWidgets.QPushButton("Login")
        self.register_btn = QtWidgets.QPushButton("Create account")
        btns.addWidget(self.login_btn)
        btns.addWidget(self.register_btn)
        layout.addLayout(btns)

        self.login_btn.clicked.connect(self.do_login)
        self.register_btn.clicked.connect(self.do_register)

    def do_login(self):
        u = self.user_edit.text().strip()
        p = self.pw_edit.text().strip()
        row = get_user(u)
        if not row:
            QtWidgets.QMessageBox.warning(self, "Login failed", "User not found")
            log_action("login_failed", user=u, details={"reason":"not_found"})
            return
        if verify_password(p, row['password_hash'], row['salt']):
            log_action("login_success", user=u)
            self.username = u
            self.accept()
        else:
            log_action("login_failed", user=u, details={"reason":"bad_password"})
            QtWidgets.QMessageBox.warning(self, "Login failed", "Bad credentials")

    def do_register(self):
        u = self.user_edit.text().strip()
        p = self.pw_edit.text().strip()
        if not u or not p:
            QtWidgets.QMessageBox.warning(self, "Validation", "Please fill username & password")
            return
        ok, msg = create_user(u, p)
        if ok:
            QtWidgets.QMessageBox.information(self, "Created", "User created successfully. You may login now.")
        else:
            QtWidgets.QMessageBox.warning(self, "Create failed", msg)
