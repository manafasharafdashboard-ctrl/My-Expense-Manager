"""Category Model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Category:
    """Represents an expense category"""
    id: Optional[int] = None
    name: str = ""
    type: str = "expense"  # expense, income
    color: str = "#6c757d"
    icon: str = "other"
    budget_limit: Optional[float] = None
    created_at: Optional[datetime] = None
    is_active: bool = True

    def __str__(self):
        return self.name

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'color': self.color,
            'icon': self.icon,
            'budget_limit': self.budget_limit,
            'created_at': self.created_at,
            'is_active': self.is_active,
        }
