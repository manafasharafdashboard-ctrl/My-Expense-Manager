"""Transaction Model (Income/Expense)"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Transaction:
    """Represents an income or expense transaction"""
    id: Optional[int] = None
    type: str = "expense"  # expense, income
    amount: float = 0.0
    category_id: Optional[int] = None
    category_name: str = ""
    account_id: Optional[int] = None
    account_name: str = ""
    date: Optional[datetime] = None
    description: str = ""
    notes: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_recurring: bool = False
    recurring_frequency: Optional[str] = None  # daily, weekly, monthly, yearly

    def __str__(self):
        return f"{self.type.capitalize()}: {self.amount} - {self.category_name}"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'type': self.type,
            'amount': self.amount,
            'category_id': self.category_id,
            'category_name': self.category_name,
            'account_id': self.account_id,
            'account_name': self.account_name,
            'date': self.date,
            'description': self.description,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'is_recurring': self.is_recurring,
            'recurring_frequency': self.recurring_frequency,
        }
