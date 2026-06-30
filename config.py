"""Application Configuration"""
import os
from pathlib import Path

# Application Info
APP_NAME = "My Expense Manager"
APP_VERSION = "1.0.0"
APP_COPYRIGHT = "© 2026 - Manaf Asharaf"

# Paths
if os.path.exists(os.path.join(os.path.dirname(__file__), 'expenses.db')):
    # Running from development folder or USB
    DATA_DIR = os.path.dirname(__file__)
else:
    # Running as installed app
    DATA_DIR = os.path.join(os.getenv('APPDATA'), 'MyExpenseManager')

Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

DATABASE_PATH = os.path.join(DATA_DIR, 'expenses.db')
BACKUP_DIR = os.path.join(DATA_DIR, 'backups')
EXPORT_DIR = os.path.join(DATA_DIR, 'exports')

Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)
Path(EXPORT_DIR).mkdir(parents=True, exist_ok=True)

# UI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = f"{APP_NAME} - {APP_VERSION}"

# Currency
CURRENCY_SYMBOL = "$"
DECIMAL_PLACES = 2

# Default Categories
DEFAULT_CATEGORIES = {
    'Income': {'color': '#28a745', 'icon': 'income'},
    'Food & Dining': {'color': '#ffc107', 'icon': 'food'},
    'Transportation': {'color': '#17a2b8', 'icon': 'transport'},
    'Shopping': {'color': '#e83e8c', 'icon': 'shopping'},
    'Entertainment': {'color': '#6f42c1', 'icon': 'entertainment'},
    'Utilities': {'color': '#fd7e14', 'icon': 'utilities'},
    'Healthcare': {'color': '#dc3545', 'icon': 'health'},
    'Education': {'color': '#0dcaf0', 'icon': 'education'},
    'Other': {'color': '#6c757d', 'icon': 'other'},
}

# Default Accounts
DEFAULT_ACCOUNTS = [
    {'name': 'Cash', 'type': 'cash', 'currency': 'USD'},
    {'name': 'Bank Account', 'type': 'bank', 'currency': 'USD'},
]
