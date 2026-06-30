"""Add Transaction Dialog"""
from datetime import datetime
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QDateTimeEdit, QTextEdit, QCheckBox, QPushButton, QSpinBox, QDoubleSpinBox
)
from PyQt5.QtCore import QDateTime

from database import DatabaseManager
from models import Transaction, Category, Account

class AddTransactionDialog(QDialog):
    """Dialog for adding/editing transactions"""

    def __init__(self, db: DatabaseManager, trans_type: str = 'expense', parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add {trans_type.capitalize()}")
        self.setGeometry(100, 100, 500, 400)
        self.db = db
        self.trans_type = trans_type
        self.init_ui()

    def init_ui(self):
        """Initialize dialog UI"""
        layout = QVBoxLayout()
        
        # Category
        cat_layout = QHBoxLayout()
        cat_layout.addWidget(QLabel("Category:"))
        self.combo_category = QComboBox()
        categories = self.db.get_all_categories(self.trans_type)
        for cat in categories:
            self.combo_category.addItem(cat.name, cat.id)
        cat_layout.addWidget(self.combo_category)
        layout.addLayout(cat_layout)
        
        # Account
        acc_layout = QHBoxLayout()
        acc_layout.addWidget(QLabel("Account:"))
        self.combo_account = QComboBox()
        accounts = self.db.get_all_accounts()
        for acc in accounts:
            self.combo_account.addItem(acc.name, acc.id)
        acc_layout.addWidget(self.combo_account)
        layout.addLayout(acc_layout)
        
        # Amount
        amt_layout = QHBoxLayout()
        amt_layout.addWidget(QLabel("Amount:"))
        self.spin_amount = QDoubleSpinBox()
        self.spin_amount.setMinimum(0.01)
        self.spin_amount.setMaximum(9999999.99)
        self.spin_amount.setDecimals(2)
        amt_layout.addWidget(self.spin_amount)
        layout.addLayout(amt_layout)
        
        # Date
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Date:"))
        self.edit_date = QDateTimeEdit()
        self.edit_date.setDateTime(QDateTime.currentDateTime())
        date_layout.addWidget(self.edit_date)
        layout.addLayout(date_layout)
        
        # Description
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Description:"))
        self.edit_description = QLineEdit()
        desc_layout.addWidget(self.edit_description)
        layout.addLayout(desc_layout)
        
        # Notes
        notes_layout = QVBoxLayout()
        notes_layout.addWidget(QLabel("Notes:"))
        self.edit_notes = QTextEdit()
        self.edit_notes.setMaximumHeight(100)
        notes_layout.addWidget(self.edit_notes)
        layout.addLayout(notes_layout)
        
        # Recurring
        self.check_recurring = QCheckBox("Make this recurring")
        layout.addWidget(self.check_recurring)
        
        rec_layout = QHBoxLayout()
        rec_layout.addWidget(QLabel("Frequency:"))
        self.combo_frequency = QComboBox()
        self.combo_frequency.addItems(['daily', 'weekly', 'monthly', 'yearly'])
        self.combo_frequency.setEnabled(False)
        rec_layout.addWidget(self.combo_frequency)
        self.check_recurring.stateChanged.connect(lambda: self.combo_frequency.setEnabled(self.check_recurring.isChecked()))
        layout.addLayout(rec_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("💾 Save")
        btn_save.clicked.connect(self.save_transaction)
        btn_cancel = QPushButton("❌ Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def save_transaction(self):
        """Save transaction"""
        transaction = Transaction(
            type=self.trans_type,
            amount=self.spin_amount.value(),
            category_id=self.combo_category.currentData(),
            account_id=self.combo_account.currentData(),
            date=self.edit_date.dateTime().toPyDateTime(),
            description=self.edit_description.text(),
            notes=self.edit_notes.toPlainText(),
            is_recurring=self.check_recurring.isChecked(),
            recurring_frequency=self.combo_frequency.currentText() if self.check_recurring.isChecked() else None
        )
        
        trans_id = self.db.add_transaction(transaction)
        if trans_id > 0:
            self.accept()
