"""Beautiful UI Styles with Indian Theme Colors"""

# Indian Theme Colors
COLORS = {
    'saffron': '#FF9933',      # Saffron (Orange)
    'white': '#FFFFFF',         # White
    'green': '#138808',          # Green
    'dark_blue': '#1A3A52',      # Dark Blue
    'light_bg': '#F5F5F5',       # Light Background
    'accent': '#FF6B6B',         # Red Accent
    'success': '#51CF66',        # Success Green
    'warning': '#FFD93D',        # Warning Yellow
    'error': '#FF6B6B',          # Error Red
    'info': '#4ECDC4',           # Info Cyan
    'text_dark': '#2C3E50',      # Dark Text
    'text_light': '#95A5A6',     # Light Text
    'card_bg': '#FFFFFF',        # Card Background
    'hover': '#F0F0F0',          # Hover State
}

# Gradient Colors
GRADIENTS = {
    'income': 'linear-gradient(135deg, #51CF66 0%, #37B24D 100%)',
    'expense': 'linear-gradient(135deg, #FF6B6B 0%, #FA5252 100%)',
    'balance': 'linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%)',
    'primary': 'linear-gradient(135deg, #FF9933 0%, #FFA500 100%)',
}

# Global Application Stylesheet
GLOBAL_STYLESHEET = f"""
* {{
    margin: 0;
    padding: 0;
    border: none;
}}

QMainWindow {{
    background-color: {COLORS['light_bg']};
}}

QWidget {{
    background-color: {COLORS['light_bg']};
    color: {COLORS['text_dark']};
}}

QLabel {{
    color: {COLORS['text_dark']};
    font-family: 'Segoe UI', Arial;
}}

QPushButton {{
    background-color: {COLORS['saffron']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 11px;
    font-family: 'Segoe UI', Arial;
    transition: all 0.3s ease;
}}

QPushButton:hover {{
    background-color: #FF8C1F;
    transform: translateY(-2px);
}}

QPushButton:pressed {{
    background-color: #E67E22;
    transform: translateY(0px);
}}

QPushButton#success {{
    background-color: {COLORS['success']};
}}

QPushButton#success:hover {{
    background-color: #40C057;
}}

QPushButton#error {{
    background-color: {COLORS['error']};
}}

QPushButton#error:hover {{
    background-color: #FA5252;
}}

QLineEdit, QTextEdit {{
    background-color: {COLORS['card_bg']};
    color: {COLORS['text_dark']};
    border: 2px solid #E0E0E0;
    border-radius: 6px;
    padding: 8px;
    font-family: 'Segoe UI', Arial;
}}

QLineEdit:focus, QTextEdit:focus {{
    border: 2px solid {COLORS['saffron']};
    background-color: #FFFBF8;
}}

QComboBox {{
    background-color: {COLORS['card_bg']};
    color: {COLORS['text_dark']};
    border: 2px solid #E0E0E0;
    border-radius: 6px;
    padding: 6px;
    font-family: 'Segoe UI', Arial;
}}

QComboBox:focus {{
    border: 2px solid {COLORS['saffron']};
}}

QDateEdit {{
    background-color: {COLORS['card_bg']};
    color: {COLORS['text_dark']};
    border: 2px solid #E0E0E0;
    border-radius: 6px;
    padding: 6px;
    font-family: 'Segoe UI', Arial;
}}

QDateEdit:focus {{
    border: 2px solid {COLORS['saffron']};
}}

QTabWidget {{
    background-color: {COLORS['light_bg']};
}}

QTabBar::tab {{
    background-color: {COLORS['hover']};
    color: {COLORS['text_dark']};
    padding: 10px 20px;
    border-radius: 4px 4px 0 0;
    font-weight: bold;
    font-family: 'Segoe UI', Arial;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['saffron']};
    color: white;
}}

QTableWidget {{
    background-color: {COLORS['card_bg']};
    gridline-color: #E0E0E0;
    border: 1px solid #E0E0E0;
    border-radius: 4px;
}}

QTableWidget::item {{
    padding: 6px;
    border-bottom: 1px solid #F0F0F0;
}}

QTableWidget::item:selected {{
    background-color: #FFF3E0;
    color: {COLORS['text_dark']};
}}

QHeaderView::section {{
    background-color: {COLORS['saffron']};
    color: white;
    padding: 6px;
    border: none;
    font-weight: bold;
    font-family: 'Segoe UI', Arial;
}}

QMenuBar {{
    background-color: {COLORS['card_bg']};
    color: {COLORS['text_dark']};
    border-bottom: 2px solid {COLORS['saffron']};
}}

QMenuBar::item:selected {{
    background-color: #FFF3E0;
}}

QMenu {{
    background-color: {COLORS['card_bg']};
    color: {COLORS['text_dark']};
    border: 1px solid #E0E0E0;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background-color: {COLORS['saffron']};
    color: white;
}}

QScrollBar:vertical {{
    background-color: {COLORS['light_bg']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['saffron']};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: #FF8C1F;
}}

QMessageBox {{
    background-color: {COLORS['light_bg']};
}}

QMessageBox QLabel {{
    color: {COLORS['text_dark']};
}}
"""

# Card Style for Dashboard
CARD_STYLE = f"""
background-color: {COLORS['card_bg']};
border: 1px solid #E0E0E0;
border-radius: 8px;
padding: 16px;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
"""

# Header Style
HEADER_STYLE = f"""
background: linear-gradient(135deg, {COLORS['saffron']} 0%, {COLORS['green']} 100%);
color: white;
padding: 20px;
border-radius: 8px;
font-weight: bold;
font-size: 16px;
"""

# Stat Box Style
STAT_BOX_INCOME = f"""
background: linear-gradient(135deg, #51CF66 0%, #37B24D 100%);
color: white;
border: none;
border-radius: 8px;
padding: 16px;
font-weight: bold;
"""

STAT_BOX_EXPENSE = f"""
background: linear-gradient(135deg, #FF6B6B 0%, #FA5252 100%);
color: white;
border: none;
border-radius: 8px;
padding: 16px;
font-weight: bold;
"""

STAT_BOX_BALANCE = f"""
background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
color: white;
border: none;
border-radius: 8px;
padding: 16px;
font-weight: bold;
"""

STAT_BOX_STYLE = f"""
color: white;
border: none;
border-radius: 8px;
padding: 20px;
font-weight: bold;
font-size: 14px;
"""
