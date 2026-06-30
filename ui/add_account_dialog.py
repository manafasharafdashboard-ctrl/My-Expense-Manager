"""Add Account Dialog"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QDoubleSpinBox
)
from PyQt5.QtCore import Qt

from database import DatabaseManager
from models import Account

class AddAccountDialog(QDialog):
    """Dialog for managing accounts"""

    def __init__(self, db: DatabaseManager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Accounts")
        self.setGeometry(100, 100, 700, 500)
        self.db = db
        self.init_ui()
        self.load_accounts()

    def init_ui(self):
        """Initialize dialog UI"""
        layout = QVBoxLayout()
        
        # Add account form
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Add New Account:"))
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Account Name:"))
        self.edit_name = QLineEdit()
        name_layout.addWidget(self.edit_name)
        form_layout.addLayout(name_layout)
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Account Type:"))
        self.combo_type = QComboBox()
        self.combo_type.addItems(['bank', 'cash', 'credit_card'])
        type_layout.addWidget(self.combo_type)
        form_layout.addLayout(type_layout)
        
        balance_layout = QHBoxLayout()
        balance_layout.addWidget(QLabel("Initial Balance:"))
        self.spin_balance = QDoubleSpinBox()
        self.spin_balance.setMinimum(0.0)
        self.spin_balance.setMaximum(9999999.99)
        self.spin_balance.setDecimals(2)
        balance_layout.addWidget(self.spin_balance)
        form_layout.addLayout(balance_layout)
        
        notes_layout = QVBoxLayout()
        notes_layout.addWidget(QLabel("Notes:"))
        self.edit_notes = QTextEdit()
        self.edit_notes.setMaximumHeight(80)
        notes_layout.addWidget(self.edit_notes)
        form_layout.addLayout(notes_layout)
        
        btn_add = QPushButton("➕ Add Account")
        btn_add.clicked.connect(self.add_account)
        form_layout.addWidget(btn_add)
        
        layout.addLayout(form_layout)
        layout.addSpacing(20)
        
        # Accounts table
        layout.addWidget(QLabel("Existing Accounts:"))
        self.table_accounts = QTableWidget()
        self.table_accounts.setColumnCount(6)
        self.table_accounts.setHorizontalHeaderLabels(
            ['ID', 'Name', 'Type', 'Balance', 'Currency', 'Actions']
        )
        self.table_accounts.setColumnHidden(0, True)
        layout.addWidget(self.table_accounts)
        
        # Close button
        btn_close = QPushButton("❌ Close")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        self.setLayout(layout)

    def load_accounts(self):
        """Load accounts into table"""
        accounts = self.db.get_all_accounts()
        self.table_accounts.setRowCount(0)
        
        for i, account in enumerate(accounts):
            self.table_accounts.insertRow(i)
            self.table_accounts.setItem(i, 0, QTableWidgetItem(str(account.id)))
            self.table_accounts.setItem(i, 1, QTableWidgetItem(account.name))
            self.table_accounts.setItem(i, 2, QTableWidgetItem(account.type))
            self.table_accounts.setItem(i, 3, QTableWidgetItem(f"{account.balance:.2f}"))
            self.table_accounts.setItem(i, 4, QTableWidgetItem(account.currency))
            
            btn_delete = QPushButton("🗑️")
            btn_delete.clicked.connect(lambda checked, aid=account.id: self.delete_account(aid))
            self.table_accounts.setCellWidget(i, 5, btn_delete)

    def add_account(self):
        """Add new account"""
        if not self.edit_name.text().strip():
            return
        
        account = Account(
            name=self.edit_name.text(),
            type=self.combo_type.currentText(),
            balance=self.spin_balance.value(),
            currency='USD',
            notes=self.edit_notes.toPlainText()
        )
        
        self.db.add_account(account)
        self.edit_name.clear()
        self.spin_balance.setValue(0.0)
        self.edit_notes.clear()
        self.load_accounts()

    def delete_account(self, account_id: int):
        """Delete account"""
        self.db.delete_account(account_id)
        self.load_accounts()
