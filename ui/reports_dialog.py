"""Reports Dialog"""
from datetime import datetime
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt

from database import DatabaseManager
from utils import format_currency

class ReportsDialog(QDialog):
    """Dialog for viewing reports"""

    def __init__(self, db: DatabaseManager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Monthly Reports")
        self.setGeometry(100, 100, 800, 600)
        self.db = db
        self.init_ui()
        self.load_report()

    def init_ui(self):
        """Initialize dialog UI"""
        layout = QVBoxLayout()
        
        # Month/Year selection
        select_layout = QHBoxLayout()
        
        select_layout.addWidget(QLabel("Select Month:"))
        self.combo_month = QComboBox()
        self.combo_month.addItems([
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ])
        self.combo_month.setCurrentIndex(datetime.now().month - 1)
        select_layout.addWidget(self.combo_month)
        
        select_layout.addWidget(QLabel("Year:"))
        self.combo_year = QComboBox()
        current_year = datetime.now().year
        for year in range(current_year - 5, current_year + 1):
            self.combo_year.addItem(str(year))
        self.combo_year.setCurrentText(str(current_year))
        select_layout.addWidget(self.combo_year)
        
        btn_load = QPushButton("📊 Load Report")
        btn_load.clicked.connect(self.load_report)
        select_layout.addWidget(btn_load)
        select_layout.addStretch()
        
        layout.addLayout(select_layout)
        layout.addSpacing(10)
        
        # Summary
        self.label_income = QLabel("Total Income: $0.00")
        self.label_expense = QLabel("Total Expense: $0.00")
        self.label_net = QLabel("Net (Income - Expense): $0.00")
        
        for lbl in [self.label_income, self.label_expense, self.label_net]:
            font = lbl.font()
            font.setPointSize(11)
            font.setBold(True)
            lbl.setFont(font)
        
        layout.addWidget(self.label_income)
        layout.addWidget(self.label_expense)
        layout.addWidget(self.label_net)
        layout.addSpacing(10)
        
        # Breakdown table
        layout.addWidget(QLabel("Breakdown by Category:"))
        self.table_breakdown = QTableWidget()
        self.table_breakdown.setColumnCount(3)
        self.table_breakdown.setHorizontalHeaderLabels(['Category', 'Type', 'Amount'])
        layout.addWidget(self.table_breakdown)
        
        # Close button
        btn_close = QPushButton("❌ Close")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        self.setLayout(layout)

    def load_report(self):
        """Load and display monthly report"""
        month = self.combo_month.currentIndex() + 1
        year = int(self.combo_year.currentText())
        
        summary = self.db.get_monthly_summary(year, month)
        
        self.label_income.setText(f"Total Income: {format_currency(summary.get('total_income', 0))}")
        self.label_expense.setText(f"Total Expense: {format_currency(summary.get('total_expense', 0))}")
        self.label_net.setText(f"Net (Income - Expense): {format_currency(summary.get('net', 0))}")
        
        # Populate breakdown table
        by_category = summary.get('by_category', {})
        self.table_breakdown.setRowCount(0)
        
        row = 0
        for key, amount in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            parts = key.split('_', 1)
            if len(parts) == 2:
                trans_type, category = parts
                self.table_breakdown.insertRow(row)
                self.table_breakdown.setItem(row, 0, QTableWidgetItem(category))
                self.table_breakdown.setItem(row, 1, QTableWidgetItem(trans_type.capitalize()))
                self.table_breakdown.setItem(row, 2, QTableWidgetItem(format_currency(amount)))
                row += 1
