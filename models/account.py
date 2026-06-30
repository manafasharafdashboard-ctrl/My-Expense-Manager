"""Account Model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Account:
    """Represents a financial account"""
    id: Optional[int] = None
    name: str = ""
    type: str = "bank"  # bank, cash, credit_card
    balance: float = 0.0
    currency: str = "USD"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True
    notes: str = ""

    def __str__(self):
        return f"{self.name} ({self.type})"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'balance': self.balance,
            'currency': self.currency,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'is_active': self.is_active,
            'notes': self.notes,
        }
