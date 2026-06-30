"""Add Category Dialog"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QDoubleSpinBox, QColorDialog
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from database import DatabaseManager
from models import Category

class AddCategoryDialog(QDialog):
    """Dialog for managing categories"""

    def __init__(self, db: DatabaseManager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Categories")
        self.setGeometry(100, 100, 700, 500)
        self.db = db
        self.selected_color = "#6c757d"
        self.init_ui()
        self.load_categories()

    def init_ui(self):
        """Initialize dialog UI"""
        layout = QVBoxLayout()
        
        # Add category form
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Add New Category:"))
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Category Name:"))
        self.edit_name = QLineEdit()
        name_layout.addWidget(self.edit_name)
        form_layout.addLayout(name_layout)
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type:"))
        self.combo_type = QComboBox()
        self.combo_type.addItems(['expense', 'income'])
        type_layout.addWidget(self.combo_type)
        form_layout.addLayout(type_layout)
        
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        self.edit_color = QLineEdit()
        self.edit_color.setText(self.selected_color)
        self.edit_color.setReadOnly(True)
        color_layout.addWidget(self.edit_color)
        btn_color = QPushButton("🎨 Choose Color")
        btn_color.clicked.connect(self.choose_color)
        color_layout.addWidget(btn_color)
        form_layout.addLayout(color_layout)
        
        budget_layout = QHBoxLayout()
        budget_layout.addWidget(QLabel("Budget Limit (optional):"))
        self.spin_budget = QDoubleSpinBox()
        self.spin_budget.setMinimum(0.0)
        self.spin_budget.setMaximum(9999999.99)
        self.spin_budget.setDecimals(2)
        budget_layout.addWidget(self.spin_budget)
        form_layout.addLayout(budget_layout)
        
        btn_add = QPushButton("➕ Add Category")
        btn_add.clicked.connect(self.add_category)
        form_layout.addWidget(btn_add)
        
        layout.addLayout(form_layout)
        layout.addSpacing(20)
        
        # Categories table
        layout.addWidget(QLabel("Existing Categories:"))
        self.table_categories = QTableWidget()
        self.table_categories.setColumnCount(6)
        self.table_categories.setHorizontalHeaderLabels(
            ['ID', 'Name', 'Type', 'Color', 'Budget Limit', 'Actions']
        )
        self.table_categories.setColumnHidden(0, True)
        layout.addWidget(self.table_categories)
        
        # Close button
        btn_close = QPushButton("❌ Close")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        self.setLayout(layout)

    def choose_color(self):
        """Open color picker dialog"""
        color = QColorDialog.getColor(QColor(self.selected_color), self, "Choose Color")
        if color.isValid():
            self.selected_color = color.name()
            self.edit_color.setText(self.selected_color)

    def load_categories(self):
        """Load categories into table"""
        categories = self.db.get_all_categories()
        self.table_categories.setRowCount(0)
        
        for i, category in enumerate(categories):
            self.table_categories.insertRow(i)
            self.table_categories.setItem(i, 0, QTableWidgetItem(str(category.id)))
            self.table_categories.setItem(i, 1, QTableWidgetItem(category.name))
            self.table_categories.setItem(i, 2, QTableWidgetItem(category.type))
            
            color_item = QTableWidgetItem()
            color_item.setBackground(QColor(category.color))
            color_item.setText(category.color)
            self.table_categories.setItem(i, 3, color_item)
            
            budget_text = f"{category.budget_limit:.2f}" if category.budget_limit else "None"
            self.table_categories.setItem(i, 4, QTableWidgetItem(budget_text))
            
            btn_delete = QPushButton("🗑️")
            btn_delete.clicked.connect(lambda checked, cid=category.id: self.delete_category(cid))
            self.table_categories.setCellWidget(i, 5, btn_delete)

    def add_category(self):
        """Add new category"""
        if not self.edit_name.text().strip():
            return
        
        category = Category(
            name=self.edit_name.text(),
            type=self.combo_type.currentText(),
            color=self.selected_color,
            budget_limit=self.spin_budget.value() if self.spin_budget.value() > 0 else None
        )
        
        self.db.add_category(category)
        self.edit_name.clear()
        self.spin_budget.setValue(0.0)
        self.selected_color = "#6c757d"
        self.edit_color.setText(self.selected_color)
        self.load_categories()

    def delete_category(self, category_id: int):
        """Delete category"""
        self.db.delete_category(category_id)
        self.load_categories()
