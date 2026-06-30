"""Helper Functions"""
from datetime import datetime, timedelta
from config import CURRENCY_SYMBOL, DECIMAL_PLACES

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"{CURRENCY_SYMBOL}{amount:,.{DECIMAL_PLACES}f}"

def get_month_range(year: int, month: int) -> tuple:
    """Get start and end datetime for a month"""
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = datetime(year, month + 1, 1) - timedelta(days=1)
    end = end.replace(hour=23, minute=59, second=59)
    return start, end

def get_current_month_range() -> tuple:
    """Get start and end datetime for current month"""
    now = datetime.now()
    return get_month_range(now.year, now.month)
