"""Database Manager - Handles all database operations"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
import shutil

from config import DATABASE_PATH, BACKUP_DIR
from models import Account, Category, Transaction
from .schema import SCHEMA_SQL

class DatabaseManager:
    """Manages SQLite database operations"""

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.connection = None
        self.init_db()

    def init_db(self):
        """Initialize database with schema"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            cursor = self.connection.cursor()
            cursor.executescript(SCHEMA_SQL)
            self.connection.commit()
            print(f"Database initialized at {self.db_path}")
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

    def backup_database(self) -> str:
        """Create a backup of the database"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = Path(BACKUP_DIR) / f"expenses_backup_{timestamp}.db"
            shutil.copy2(self.db_path, backup_path)
            return str(backup_path)
        except Exception as e:
            print(f"Backup error: {e}")
            return ""

    # ==================== ACCOUNT OPERATIONS ====================

    def add_account(self, account: Account) -> int:
        """Add a new account"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO accounts (name, type, balance, currency, is_active, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (account.name, account.type, account.balance, account.currency, 
                   account.is_active, account.notes))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding account: {e}")
            return -1

    def get_all_accounts(self) -> List[Account]:
        """Get all accounts"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM accounts WHERE is_active = 1 ORDER BY name")
            accounts = []
            for row in cursor.fetchall():
                account = Account(
                    id=row['id'],
                    name=row['name'],
                    type=row['type'],
                    balance=row['balance'],
                    currency=row['currency'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    is_active=bool(row['is_active']),
                    notes=row['notes']
                )
                accounts.append(account)
            return accounts
        except Exception as e:
            print(f"Error getting accounts: {e}")
            return []

    def update_account(self, account: Account) -> bool:
        """Update an account"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE accounts 
                SET name = ?, type = ?, balance = ?, currency = ?, is_active = ?, notes = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (account.name, account.type, account.balance, account.currency,
                   account.is_active, account.notes, account.id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating account: {e}")
            return False

    def delete_account(self, account_id: int) -> bool:
        """Soft delete an account"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE accounts SET is_active = 0 WHERE id = ?", (account_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting account: {e}")
            return False

    # ==================== CATEGORY OPERATIONS ====================

    def add_category(self, category: Category) -> int:
        """Add a new category"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO categories (name, type, color, icon, budget_limit, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (category.name, category.type, category.color, category.icon,
                   category.budget_limit, category.is_active))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding category: {e}")
            return -1

    def get_all_categories(self, category_type: str = None) -> List[Category]:
        """Get all categories, optionally filtered by type"""
        try:
            cursor = self.connection.cursor()
            if category_type:
                cursor.execute(
                    "SELECT * FROM categories WHERE is_active = 1 AND type = ? ORDER BY name",
                    (category_type,)
                )
            else:
                cursor.execute("SELECT * FROM categories WHERE is_active = 1 ORDER BY type, name")
            
            categories = []
            for row in cursor.fetchall():
                category = Category(
                    id=row['id'],
                    name=row['name'],
                    type=row['type'],
                    color=row['color'],
                    icon=row['icon'],
                    budget_limit=row['budget_limit'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    is_active=bool(row['is_active'])
                )
                categories.append(category)
            return categories
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []

    def update_category(self, category: Category) -> bool:
        """Update a category"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE categories 
                SET name = ?, type = ?, color = ?, icon = ?, budget_limit = ?, is_active = ?
                WHERE id = ?
            """, (category.name, category.type, category.color, category.icon,
                   category.budget_limit, category.is_active, category.id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating category: {e}")
            return False

    def delete_category(self, category_id: int) -> bool:
        """Soft delete a category"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE categories SET is_active = 0 WHERE id = ?", (category_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False

    # ==================== TRANSACTION OPERATIONS ====================

    def add_transaction(self, transaction: Transaction) -> int:
        """Add a new transaction"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO transactions 
                (type, amount, category_id, account_id, date, description, notes, is_recurring, recurring_frequency)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (transaction.type, transaction.amount, transaction.category_id, 
                   transaction.account_id, transaction.date, transaction.description,
                   transaction.notes, transaction.is_recurring, transaction.recurring_frequency))
            self.connection.commit()
            
            # Update account balance
            self._update_account_balance(transaction.account_id)
            
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return -1

    def get_all_transactions(self, start_date: datetime = None, end_date: datetime = None) -> List[Transaction]:
        """Get all transactions, optionally filtered by date range"""
        try:
            cursor = self.connection.cursor()
            
            if start_date and end_date:
                cursor.execute("""
                    SELECT t.*, c.name as category_name, a.name as account_name 
                    FROM transactions t
                    JOIN categories c ON t.category_id = c.id
                    JOIN accounts a ON t.account_id = a.id
                    WHERE t.date >= ? AND t.date <= ?
                    ORDER BY t.date DESC
                """, (start_date, end_date))
            else:
                cursor.execute("""
                    SELECT t.*, c.name as category_name, a.name as account_name 
                    FROM transactions t
                    JOIN categories c ON t.category_id = c.id
                    JOIN accounts a ON t.account_id = a.id
                    ORDER BY t.date DESC
                """)
            
            transactions = []
            for row in cursor.fetchall():
                transaction = Transaction(
                    id=row['id'],
                    type=row['type'],
                    amount=row['amount'],
                    category_id=row['category_id'],
                    category_name=row['category_name'],
                    account_id=row['account_id'],
                    account_name=row['account_name'],
                    date=datetime.fromisoformat(row['date']),
                    description=row['description'],
                    notes=row['notes'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at']),
                    is_recurring=bool(row['is_recurring']),
                    recurring_frequency=row['recurring_frequency']
                )
                transactions.append(transaction)
            return transactions
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []

    def update_transaction(self, transaction: Transaction) -> bool:
        """Update a transaction"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE transactions 
                SET type = ?, amount = ?, category_id = ?, account_id = ?, date = ?,
                    description = ?, notes = ?, is_recurring = ?, recurring_frequency = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (transaction.type, transaction.amount, transaction.category_id,
                   transaction.account_id, transaction.date, transaction.description,
                   transaction.notes, transaction.is_recurring, transaction.recurring_frequency,
                   transaction.id))
            self.connection.commit()
            self._update_account_balance(transaction.account_id)
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False

    def delete_transaction(self, transaction_id: int, account_id: int) -> bool:
        """Delete a transaction"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            self.connection.commit()
            self._update_account_balance(account_id)
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False

    def _update_account_balance(self, account_id: int):
        """Recalculate account balance from transactions"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END), 0)
                FROM transactions
                WHERE account_id = ?
            """, (account_id,))
            balance = cursor.fetchone()[0]
            
            cursor.execute(
                "UPDATE accounts SET balance = ? WHERE id = ?",
                (balance, account_id)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error updating balance: {e}")

    # ==================== REPORTING OPERATIONS ====================

    def get_monthly_summary(self, year: int, month: int) -> Dict[str, Any]:
        """Get monthly expense and income summary"""
        try:
            cursor = self.connection.cursor()
            
            # Total income and expenses
            cursor.execute("""
                SELECT type, SUM(amount) as total
                FROM transactions
                WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
                GROUP BY type
            """, (str(year).zfill(4), str(month).zfill(2)))
            
            summary = {'income': 0, 'expense': 0}
            for row in cursor.fetchall():
                summary[row['type']] = row['total']
            
            # By category breakdown
            cursor.execute("""
                SELECT c.name, t.type, SUM(t.amount) as total
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                WHERE strftime('%Y', t.date) = ? AND strftime('%m', t.date) = ?
                GROUP BY c.id, t.type
                ORDER BY t.type, total DESC
            """, (str(year).zfill(4), str(month).zfill(2)))
            
            by_category = {}
            for row in cursor.fetchall():
                key = f"{row['type']}_{row['name']}"
                by_category[key] = row['total']
            
            return {
                'total_income': summary['income'],
                'total_expense': summary['expense'],
                'net': summary['income'] - summary['expense'],
                'by_category': by_category
            }
        except Exception as e:
            print(f"Error getting monthly summary: {e}")
            return {}

    def export_to_csv(self, output_path: str, start_date: datetime = None, end_date: datetime = None) -> bool:
        """Export transactions to CSV file"""
        try:
            import csv
            transactions = self.get_all_transactions(start_date, end_date)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Type', 'Category', 'Account', 'Amount', 'Description', 'Notes'])
                
                for t in transactions:
                    writer.writerow([
                        t.date.strftime('%Y-%m-%d'),
                        t.type,
                        t.category_name,
                        t.account_name,
                        f"{t.amount:.2f}",
                        t.description,
                        t.notes
                    ])
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
