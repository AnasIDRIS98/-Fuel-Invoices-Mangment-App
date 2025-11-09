# ui_components.py - PySide6 widgets for main window layout
from PySide6 import QtWidgets, QtCore
from db import fetch_all, insert_invoice, log_action
from utils import to_decimal
from PySide6.QtWidgets import QFileDialog, QMessageBox
from decimal import Decimal

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, user=None):
        super().__init__()
        self.user = user or "unknown"
        self.setWindowTitle("Fuel Invoices - Desktop")
        self.resize(1000, 700)
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        # Top header
        header = QtWidgets.QLabel("<h1>Fuel Invoices</h1>", alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(header)

        # Actions
        actions = QtWidgets.QHBoxLayout()
        self.view_btn = QtWidgets.QPushButton("View Previous Invoices")
        self.add_btn = QtWidgets.QPushButton("Add Invoice")
        self.export_btn = QtWidgets.QPushButton("Export Excel")
        actions.addWidget(self.view_btn); actions.addWidget(self.add_btn); actions.addWidget(self.export_btn)
        layout.addLayout(actions)

        # Area (placeholder)
        self.area = QtWidgets.QStackedWidget()
        layout.addWidget(self.area)

        # Connect
        self.view_btn.clicked.connect(self.show_list)
        self.add_btn.clicked.connect(self.show_add)
        self.export_btn.clicked.connect(self.export_excel)

        # prepare pages
        self.prepare_add_page()
        self.prepare_list_page()

    def prepare_add_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(page)
        self.inv_id = QtWidgets.QLineEdit()
        self.company = QtWidgets.QLineEdit()
        self.branch = QtWidgets.QLineEdit("Main")
        self.date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.recipient = QtWidgets.QLineEdit()
        self.quantity = QtWidgets.QDoubleSpinBox(); self.quantity.setDecimals(2); self.quantity.setRange(0,1e9)
        self.price = QtWidgets.QDoubleSpinBox(); self.price.setDecimals(2); self.price.setRange(0,1e9)
        self.notes = QtWidgets.QPlainTextEdit()
        layout.addRow("Invoice ID:", self.inv_id)
        layout.addRow("Company:", self.company)
        layout.addRow("Branch:", self.branch)
        layout.addRow("Date:", self.date)
        layout.addRow("Recipient:", self.recipient)
        layout.addRow("Quantity (L):", self.quantity)
        layout.addRow("Price / L:", self.price)
        layout.addRow("Notes:", self.notes)
        submit = QtWidgets.QPushButton("Add")
        layout.addRow(submit)
        submit.clicked.connect(self.add_invoice)
        self.area.addWidget(page)
        self.add_page = page

    def prepare_list_page(self):
        page = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(page)
        self.table = QtWidgets.QTableWidget()
        v.addWidget(self.table)
        self.area.addWidget(page)
        self.list_page = page

    def show_add(self):
        self.area.setCurrentWidget(self.add_page)

    def show_list(self):
        self.area.setCurrentWidget(self.list_page)
        self.refresh_list()

    def refresh_list(self):
        df = fetch_all()
        if df.empty:
            self.table.setRowCount(0); self.table.setColumnCount(0)
            return
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels(df.columns.tolist())
        for r in range(len(df)):
            for c, col in enumerate(df.columns):
                item = QtWidgets.QTableWidgetItem(str(df.iloc[r][col]))
                self.table.setItem(r, c, item)

    def add_invoice(self):
        inv = self.inv_id.text().strip()
        if not inv:
            inv = f"INV-{int(QtCore.QDateTime.currentMSecsSinceEpoch()/1000)}"
        company = self.company.text().strip()
        if not company:
            QMessageBox.warning(self, "Validation", "Company is required")
            return
        qty = to_decimal(self.quantity.value())
        pr = to_decimal(self.price.value())
        total = (qty * pr).quantize(Decimal('0.01'))
        row = {'invoice_id': inv, 'company': company, 'branch': self.branch.text(), 'date': self.date.date().toString("yyyy-MM-dd"),
               'recipient': self.recipient.text(), 'quantity': str(qty), 'price': str(pr), 'total': str(total), 'notes': self.notes.toPlainText()}
        insert_invoice(row, user=self.user)
        log_action("ui", user=self.user, details={'event':'invoice_added','invoice_id':inv})
        QMessageBox.information(self, "Added", "Invoice added successfully")
        self.inv_id.clear(); self.company.clear(); self.recipient.clear(); self.notes.clear(); self.quantity.setValue(0); self.price.setValue(0)
