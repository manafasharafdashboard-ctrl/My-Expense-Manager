"""Main Application Window"""
import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget,
    QTableWidget, QTableWidgetItem, QLabel, QComboBox, QDateEdit, QMessageBox,
    QMenu, QAction, QFileDialog
)
from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtGui import QIcon, QColor, QFont

from config import APP_NAME, APP_VERSION, APP_COPYRIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from database import DatabaseManager
from models import Transaction, Account, Category
from utils import format_currency, get_current_month_range
from .dialogs import (
    AddTransactionDialog, AddAccountDialog, AddCategoryDialog,
    ReportsDialog, SettingsDialog
)

class MainWindow(QMainWindow):
    """Main Application Window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {APP_VERSION}")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Database
        self.db = DatabaseManager()
        
        # Initialize UI
        self.init_ui()
        self.load_data()

    def init_ui(self):
        """Initialize user interface"""
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # Header
        header = self.create_header()
        main_layout.addLayout(header)
        
        # Tab Widget
        self.tabs = QTabWidget()
        self.dashboard_tab = self.create_dashboard_tab()
        self.transactions_tab = self.create_transactions_tab()
        
        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        self.tabs.addTab(self.transactions_tab, "📝 Transactions")
        
        main_layout.addWidget(self.tabs)
        
        # Footer
        footer = self.create_footer()
        main_layout.addLayout(footer)
        
        central_widget.setLayout(main_layout)
        
        # Menu Bar
        self.create_menu_bar()

    def create_header(self) -> QHBoxLayout:
        """Create header with quick actions"""
        layout = QHBoxLayout()
        
        title = QLabel(f"{APP_NAME}")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        
        layout.addWidget(title)
        layout.addStretch()
        
        # Quick action buttons
        btn_add_expense = QPushButton("➕ Add Expense")
        btn_add_expense.clicked.connect(self.add_expense)
        
        btn_add_income = QPushButton("➕ Add Income")
        btn_add_income.clicked.connect(self.add_income)
        
        btn_accounts = QPushButton("🏦 Accounts")
        btn_accounts.clicked.connect(self.manage_accounts)
        
        btn_categories = QPushButton("📂 Categories")
        btn_categories.clicked.connect(self.manage_categories)
        
        btn_reports = QPushButton("📈 Reports")
        btn_reports.clicked.connect(self.show_reports)
        
        layout.addWidget(btn_add_expense)
        layout.addWidget(btn_add_income)
        layout.addWidget(btn_accounts)
        layout.addWidget(btn_categories)
        layout.addWidget(btn_reports)
        
        return layout

    def create_dashboard_tab(self) -> QWidget:
        """Create dashboard tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary stats
        stats_layout = QHBoxLayout()
        
        self.label_total_income = QLabel("Total Income: $0.00")
        self.label_total_expense = QLabel("Total Expense: $0.00")
        self.label_balance = QLabel("Balance: $0.00")
        
        for lbl in [self.label_total_income, self.label_total_expense, self.label_balance]:
            font = lbl.font()
            font.setPointSize(12)
            font.setBold(True)
            lbl.setFont(font)
            stats_layout.addWidget(lbl)
        
        layout.addLayout(stats_layout)
        layout.addSpacing(10)
        
        # Recent transactions table
        self.table_recent = QTableWidget()
        self.table_recent.setColumnCount(7)
        self.table_recent.setHorizontalHeaderLabels(
            ['Date', 'Type', 'Category', 'Account', 'Amount', 'Description', 'Notes']
        )
        self.table_recent.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(QLabel("Recent Transactions:"))
        layout.addWidget(self.table_recent)
        
        widget.setLayout(layout)
        return widget

    def create_transactions_tab(self) -> QWidget:
        """Create transactions tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Filters
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("From:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        filter_layout.addWidget(self.date_from)
        
        filter_layout.addWidget(QLabel("To:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        filter_layout.addWidget(self.date_to)
        
        btn_filter = QPushButton("🔍 Filter")
        btn_filter.clicked.connect(self.filter_transactions)
        filter_layout.addWidget(btn_filter)
        
        filter_layout.addWidget(QLabel("Type:"))
        self.combo_type = QComboBox()
        self.combo_type.addItems(["All", "Expense", "Income"])
        filter_layout.addWidget(self.combo_type)
        
        layout.addLayout(filter_layout)
        
        # Transactions table
        self.table_transactions = QTableWidget()
        self.table_transactions.setColumnCount(8)
        self.table_transactions.setHorizontalHeaderLabels(
            ['ID', 'Date', 'Type', 'Category', 'Account', 'Amount', 'Description', 'Actions']
        )
        self.table_transactions.setColumnHidden(0, True)  # Hide ID column
        self.table_transactions.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.table_transactions)
        
        widget.setLayout(layout)
        return widget

    def create_footer(self) -> QHBoxLayout:
        """Create footer"""
        layout = QHBoxLayout()
        
        label = QLabel(f"{APP_COPYRIGHT}")
        label_font = label.font()
        label_font.setPointSize(9)
        label.setFont(label_font)
        
        layout.addStretch()
        layout.addWidget(label)
        
        return layout

    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        
        action_backup = QAction("💾 Backup Data", self)
        action_backup.triggered.connect(self.backup_data)
        file_menu.addAction(action_backup)
        
        action_export = QAction("📤 Export to CSV", self)
        action_export.triggered.connect(self.export_data)
        file_menu.addAction(action_export)
        
        file_menu.addSeparator()
        
        action_exit = QAction("❌ Exit", self)
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)
        
        # Settings menu
        settings_menu = menubar.addMenu("⚙️ Settings")
        
        action_settings = QAction("Settings", self)
        action_settings.triggered.connect(self.show_settings)
        settings_menu.addAction(action_settings)
        
        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        
        action_about = QAction("About", self)
        action_about.triggered.connect(self.show_about)
        help_menu.addAction(action_about)

    def load_data(self):
        """Load and display data"""
        self.update_dashboard()
        self.load_transactions()

    def update_dashboard(self):
        """Update dashboard statistics"""
        start, end = get_current_month_range()
        transactions = self.db.get_all_transactions(start, end)
        
        total_income = sum(t.amount for t in transactions if t.type == 'income')
        total_expense = sum(t.amount for t in transactions if t.type == 'expense')
        balance = total_income - total_expense
        
        self.label_total_income.setText(f"Total Income: {format_currency(total_income)}")
        self.label_total_expense.setText(f"Total Expense: {format_currency(total_expense)}")
        self.label_balance.setText(f"Balance: {format_currency(balance)}")
        
        # Recent transactions
        self.table_recent.setRowCount(0)
        for i, transaction in enumerate(transactions[-10:]):
            self.table_recent.insertRow(i)
            self.table_recent.setItem(i, 0, QTableWidgetItem(transaction.date.strftime('%Y-%m-%d')))
            self.table_recent.setItem(i, 1, QTableWidgetItem(transaction.type.capitalize()))
            self.table_recent.setItem(i, 2, QTableWidgetItem(transaction.category_name))
            self.table_recent.setItem(i, 3, QTableWidgetItem(transaction.account_name))
            self.table_recent.setItem(i, 4, QTableWidgetItem(format_currency(transaction.amount)))
            self.table_recent.setItem(i, 5, QTableWidgetItem(transaction.description))
            self.table_recent.setItem(i, 6, QTableWidgetItem(transaction.notes))

    def load_transactions(self):
        """Load all transactions"""
        transactions = self.db.get_all_transactions()
        self.table_transactions.setRowCount(0)
        
        for i, transaction in enumerate(transactions):
            self.table_transactions.insertRow(i)
            self.table_transactions.setItem(i, 0, QTableWidgetItem(str(transaction.id)))
            self.table_transactions.setItem(i, 1, QTableWidgetItem(transaction.date.strftime('%Y-%m-%d')))
            self.table_transactions.setItem(i, 2, QTableWidgetItem(transaction.type.capitalize()))
            self.table_transactions.setItem(i, 3, QTableWidgetItem(transaction.category_name))
            self.table_transactions.setItem(i, 4, QTableWidgetItem(transaction.account_name))
            self.table_transactions.setItem(i, 5, QTableWidgetItem(format_currency(transaction.amount)))
            self.table_transactions.setItem(i, 6, QTableWidgetItem(transaction.description))
            
            # Delete button
            btn_delete = QPushButton("🗑️ Delete")
            btn_delete.clicked.connect(lambda checked, tid=transaction.id, aid=transaction.account_id: self.delete_transaction(tid, aid))
            self.table_transactions.setCellWidget(i, 7, btn_delete)

    def filter_transactions(self):
        """Filter transactions by date and type"""
        start_date = datetime.combine(self.date_from.date().toPyDate(), datetime.min.time())
        end_date = datetime.combine(self.date_to.date().toPyDate(), datetime.max.time())
        
        transactions = self.db.get_all_transactions(start_date, end_date)
        
        type_filter = self.combo_type.currentText()
        if type_filter != "All":
            transactions = [t for t in transactions if t.type.lower() == type_filter.lower()]
        
        self.table_transactions.setRowCount(0)
        for i, transaction in enumerate(transactions):
            self.table_transactions.insertRow(i)
            self.table_transactions.setItem(i, 0, QTableWidgetItem(str(transaction.id)))
            self.table_transactions.setItem(i, 1, QTableWidgetItem(transaction.date.strftime('%Y-%m-%d')))
            self.table_transactions.setItem(i, 2, QTableWidgetItem(transaction.type.capitalize()))
            self.table_transactions.setItem(i, 3, QTableWidgetItem(transaction.category_name))
            self.table_transactions.setItem(i, 4, QTableWidgetItem(transaction.account_name))
            self.table_transactions.setItem(i, 5, QTableWidgetItem(format_currency(transaction.amount)))
            self.table_transactions.setItem(i, 6, QTableWidgetItem(transaction.description))
            
            btn_delete = QPushButton("🗑️ Delete")
            btn_delete.clicked.connect(lambda checked, tid=transaction.id, aid=transaction.account_id: self.delete_transaction(tid, aid))
            self.table_transactions.setCellWidget(i, 7, btn_delete)

    def add_expense(self):
        """Add new expense"""
        dialog = AddTransactionDialog(self.db, 'expense')
        if dialog.exec_():
            self.load_data()
            QMessageBox.information(self, "Success", "Expense added successfully!")

    def add_income(self):
        """Add new income"""
        dialog = AddTransactionDialog(self.db, 'income')
        if dialog.exec_():
            self.load_data()
            QMessageBox.information(self, "Success", "Income added successfully!")

    def manage_accounts(self):
        """Manage accounts"""
        dialog = AddAccountDialog(self.db, parent=self)
        if dialog.exec_():
            self.load_data()

    def manage_categories(self):
        """Manage categories"""
        dialog = AddCategoryDialog(self.db, parent=self)
        if dialog.exec_():
            self.load_data()

    def delete_transaction(self, transaction_id: int, account_id: int):
        """Delete a transaction"""
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            'Are you sure you want to delete this transaction?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_transaction(transaction_id, account_id)
            self.load_data()
            QMessageBox.information(self, "Success", "Transaction deleted successfully!")

    def show_reports(self):
        """Show reports dialog"""
        dialog = ReportsDialog(self.db, parent=self)
        dialog.exec_()

    def backup_data(self):
        """Backup database"""
        backup_path = self.db.backup_database()
        if backup_path:
            QMessageBox.information(self, "Success", f"Database backed up to:\n{backup_path}")
        else:
            QMessageBox.warning(self, "Error", "Failed to create backup")

    def export_data(self):
        """Export data to CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Data", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            if self.db.export_to_csv(file_path):
                QMessageBox.information(self, "Success", f"Data exported to:\n{file_path}")
            else:
                QMessageBox.warning(self, "Error", "Failed to export data")

    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.db, parent=self)
        if dialog.exec_():
            self.load_data()

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, "About",
            f"{APP_NAME}\nVersion {APP_VERSION}\n\n{APP_COPYRIGHT}\n\n"
            "A portable personal expense manager for Windows.\n\n"
            "Features:\n"
            "• Track income and expenses\n"
            "• Manage multiple accounts\n"
            "• Custom categories\n"
            "• Monthly reports\n"
            "• Data export\n\n"
            "All data is stored locally - no internet required."
        )

    def closeEvent(self, event):
        """Handle application close"""
        self.db.close()
        event.accept()
