"""Dashboard Widget with Comprehensive Statistics"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QIcon, QPalette
from datetime import datetime
from styles import STAT_BOX_INCOME, STAT_BOX_EXPENSE, STAT_BOX_BALANCE, COLORS

class StatBox(QFrame):
    """Custom stat box widget"""
    def __init__(self, title, value, subtitle="", style_bg=""):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {style_bg if style_bg else COLORS['card_bg']};
                border: none;
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(False)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: rgba(255, 255, 255, 0.8); font-weight: normal;")
        
        # Value
        value_label = QLabel(str(value))
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: white;")
        
        # Subtitle
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_font = QFont()
            subtitle_font.setPointSize(9)
            subtitle_label.setFont(subtitle_font)
            subtitle_label.setStyleSheet(f"color: rgba(255, 255, 255, 0.7);")
            layout.addWidget(subtitle_label)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setMinimumHeight(140)

class DashboardWidget(QWidget):
    """Enhanced Dashboard with comprehensive stats"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        """Initialize dashboard UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📊 Financial Dashboard")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {COLORS['text_dark']};")
        main_layout.addWidget(title)
        
        # Current Month Label
        current_date = QLabel(f"📅 {datetime.now().strftime('%B %Y')}")
        date_font = QFont()
        date_font.setPointSize(11)
        current_date.setFont(date_font)
        current_date.setStyleSheet(f"color: {COLORS['text_light']};")
        main_layout.addWidget(current_date)
        
        # Stats Grid
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)
        
        # Create stat boxes
        self.income_box = StatBox(
            "💰 Total Income",
            "₹0.00",
            "This Month",
            "linear-gradient(135deg, #51CF66 0%, #37B24D 100%)"
        )
        
        self.expense_box = StatBox(
            "💸 Total Expense",
            "₹0.00",
            "This Month",
            "linear-gradient(135deg, #FF6B6B 0%, #FA5252 100%)"
        )
        
        self.balance_box = StatBox(
            "💳 Net Balance",
            "₹0.00",
            "Income - Expense",
            "linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%)"
        )
        
        stats_layout.addWidget(self.income_box, 0, 0)
        stats_layout.addWidget(self.expense_box, 0, 1)
        stats_layout.addWidget(self.balance_box, 0, 2)
        
        main_layout.addLayout(stats_layout)
        
        # Counter Stats
        counter_layout = QGridLayout()
        counter_layout.setSpacing(15)
        
        self.income_count_box = StatBox(
            "📈 Income Transactions",
            "0",
            "This Month",
            f"background-color: {COLORS['saffron']};"
        )
        
        self.expense_count_box = StatBox(
            "📉 Expense Transactions",
            "0",
            "This Month",
            f"background-color: #FF9500;"
        )
        
        self.total_transactions_box = StatBox(
            "📋 Total Transactions",
            "0",
            "This Month",
            f"background-color: #6C63FF;"
        )
        
        counter_layout.addWidget(self.income_count_box, 0, 0)
        counter_layout.addWidget(self.expense_count_box, 0, 1)
        counter_layout.addWidget(self.total_transactions_box, 0, 2)
        
        main_layout.addLayout(counter_layout)
        
        # Category Summary
        category_layout = QVBoxLayout()
        
        category_title = QLabel("📂 Category Breakdown")
        cat_title_font = QFont()
        cat_title_font.setPointSize(14)
        cat_title_font.setBold(True)
        category_title.setFont(cat_title_font)
        category_title.setStyleSheet(f"color: {COLORS['text_dark']}; margin-top: 20px;")
        category_layout.addWidget(category_title)
        
        self.category_container = QVBoxLayout()
        category_layout.addLayout(self.category_container)
        
        main_layout.addLayout(category_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def format_currency(self, amount):
        """Format amount as Indian Rupee"""
        return f"₹{amount:,.2f}"
    
    def update_stats(self, transactions):
        """Update dashboard statistics"""
        from datetime import datetime
        now = datetime.now()
        
        # Filter this month's transactions
        month_transactions = [
            t for t in transactions 
            if t.date.year == now.year and t.date.month == now.month
        ]
        
        # Calculate totals
        total_income = sum(t.amount for t in month_transactions if t.type.lower() == 'income')
        total_expense = sum(t.amount for t in month_transactions if t.type.lower() == 'expense')
        net_balance = total_income - total_expense
        
        # Count transactions
        income_count = sum(1 for t in month_transactions if t.type.lower() == 'income')
        expense_count = sum(1 for t in month_transactions if t.type.lower() == 'expense')
        total_count = len(month_transactions)
        
        # Update boxes
        self.income_box.findChildren(QLabel)[1].setText(self.format_currency(total_income))
        self.expense_box.findChildren(QLabel)[1].setText(self.format_currency(total_expense))
        
        # Balance color based on positive/negative
        if net_balance >= 0:
            self.balance_box.setStyleSheet("""
                QFrame {
                    background: linear-gradient(135deg, #51CF66 0%, #37B24D 100%);
                    border: none;
                    border-radius: 12px;
                    padding: 20px;
                }
            """)
        else:
            self.balance_box.setStyleSheet("""
                QFrame {
                    background: linear-gradient(135deg, #FF6B6B 0%, #FA5252 100%);
                    border: none;
                    border-radius: 12px;
                    padding: 20px;
                }
            """)
        
        self.balance_box.findChildren(QLabel)[1].setText(self.format_currency(abs(net_balance)))
        
        # Update counters
        self.income_count_box.findChildren(QLabel)[1].setText(str(income_count))
        self.expense_count_box.findChildren(QLabel)[1].setText(str(expense_count))
        self.total_transactions_box.findChildren(QLabel)[1].setText(str(total_count))
        
        # Update category breakdown
        self.update_category_breakdown(month_transactions)
    
    def update_category_breakdown(self, transactions):
        """Update category breakdown"""
        # Clear existing
        while self.category_container.count():
            self.category_container.takeAt(0).widget().deleteLater()
        
        # Group by category
        categories = {}
        for t in transactions:
            cat = t.category_name
            if cat not in categories:
                categories[cat] = {'income': 0, 'expense': 0, 'count': 0}
            
            if t.type.lower() == 'income':
                categories[cat]['income'] += t.amount
            else:
                categories[cat]['expense'] += t.amount
            categories[cat]['count'] += 1
        
        # Display categories
        if not categories:
            no_data = QLabel("No transactions this month")
            no_data.setStyleSheet(f"color: {COLORS['text_light']};")
            self.category_container.addWidget(no_data)
            return
        
        for category, data in sorted(categories.items()):
            cat_widget = self.create_category_item(
                category, 
                data['income'], 
                data['expense'],
                data['count']
            )
            self.category_container.addWidget(cat_widget)
    
    def create_category_item(self, category, income, expense, count):
        """Create category item widget"""
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['card_bg']};
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px;
                margin: 5px 0px;
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 12, 15, 12)
        
        # Category name
        cat_label = QLabel(f"📁 {category}")
        cat_font = QFont()
        cat_font.setPointSize(11)
        cat_font.setBold(True)
        cat_label.setFont(cat_font)
        cat_label.setStyleSheet(f"color: {COLORS['text_dark']};")
        layout.addWidget(cat_label)
        
        layout.addStretch()
        
        # Stats
        if income > 0:
            income_label = QLabel(f"💰 {self.format_currency(income)}")
            income_label.setStyleSheet("color: #51CF66; font-weight: bold;")
            layout.addWidget(income_label)
        
        if expense > 0:
            expense_label = QLabel(f"💸 {self.format_currency(expense)}")
            expense_label.setStyleSheet("color: #FF6B6B; font-weight: bold;")
            layout.addWidget(expense_label)
        
        count_label = QLabel(f"({count})")
        count_label.setStyleSheet(f"color: {COLORS['text_light']};")
        layout.addWidget(count_label)
        
        widget.setLayout(layout)
        return widget
