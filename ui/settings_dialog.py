"""Settings Dialog"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTabWidget, QWidget
)
from PyQt5.QtCore import Qt

from database import DatabaseManager
from config import APP_NAME, APP_VERSION, APP_COPYRIGHT

class SettingsDialog(QDialog):
    """Dialog for application settings"""

    def __init__(self, db: DatabaseManager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 600, 400)
        self.db = db
        self.init_ui()

    def init_ui(self):
        """Initialize dialog UI"""
        layout = QVBoxLayout()
        
        tabs = QTabWidget()
        
        # General settings tab
        general_tab = QWidget()
        general_layout = QVBoxLayout()
        
        info_label = QLabel(
            f"{APP_NAME}\n"
            f"Version: {APP_VERSION}\n"
            f"{APP_COPYRIGHT}\n\n"
            "A portable personal expense manager for Windows."
        )
        general_layout.addWidget(info_label)
        general_layout.addStretch()
        
        general_tab.setLayout(general_layout)
        tabs.addTab(general_tab, "General")
        
        # About tab
        about_tab = QWidget()
        about_layout = QVBoxLayout()
        
        about_text = QLabel(
            "Features:\n"
            "✓ Track income and expenses\n"
            "✓ Manage multiple accounts\n"
            "✓ Create custom categories\n"
            "✓ Monthly reports and analytics\n"
            "✓ Export data to CSV\n"
            "✓ Automatic backups\n"
            "✓ 100% offline - No internet required\n"
            "✓ Portable - No installation needed\n\n"
            "Database: SQLite (local storage)\n"
            "All data is stored securely on your computer."
        )
        about_layout.addWidget(about_text)
        about_layout.addStretch()
        
        about_tab.setLayout(about_layout)
        tabs.addTab(about_tab, "About")
        
        layout.addWidget(tabs)
        
        # Close button
        btn_close = QPushButton("❌ Close")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        self.setLayout(layout)
