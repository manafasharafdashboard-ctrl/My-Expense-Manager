"""Initialize default data on first run"""
from database import DatabaseManager
from models import Category, Account
from config import DEFAULT_CATEGORIES, DEFAULT_ACCOUNTS

def init_default_data():
    """Initialize database with default categories and accounts"""
    db = DatabaseManager()
    
    # Add default categories
    existing_categories = db.get_all_categories()
    if not existing_categories:
        print("Adding default categories...")
        for cat_name, cat_info in DEFAULT_CATEGORIES.items():
            category = Category(
                name=cat_name,
                type='income' if cat_name == 'Income' else 'expense',
                color=cat_info['color'],
                icon=cat_info['icon']
            )
            db.add_category(category)
    
    # Add default accounts
    existing_accounts = db.get_all_accounts()
    if not existing_accounts:
        print("Adding default accounts...")
        for acc_info in DEFAULT_ACCOUNTS:
            account = Account(
                name=acc_info['name'],
                type=acc_info['type'],
                currency=acc_info['currency'],
                balance=0.0
            )
            db.add_account(account)
    
    db.close()
    print("✅ Default data initialized!")

if __name__ == '__main__':
    init_default_data()
