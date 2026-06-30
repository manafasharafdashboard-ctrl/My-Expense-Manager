# Quick Start Guide

## Development Mode

### 1. Install Python
Download Python 3.8+ from https://www.python.org/

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Default Data
```bash
python init_data.py
```

### 4. Run Application
```bash
python main.py
```

## Create Standalone Executable

### 1. Install PyInstaller
```bash
pip install pyinstaller
```

### 2. Build Executable
```bash
python build_exe.py
```

### 3. Locate .exe
The executable will be created in `dist/MyExpenseManager.exe`

## Running the Portable Executable

1. **From Windows:**
   - Double-click `MyExpenseManager.exe`
   - No installation required
   - Data stored in `%APPDATA%/MyExpenseManager/`

2. **From USB Drive:**
   - Copy `MyExpenseManager.exe` to USB
   - Run from any Windows computer
   - Data stored in same folder as .exe

## Features

✅ **Expense Tracking**
- Add income and expenses
- Track by category
- Multiple accounts

✅ **Account Management**
- Create multiple accounts (Bank, Cash, Credit Card)
- Track account balances
- Edit/Delete accounts

✅ **Custom Categories**
- Create unlimited categories
- Assign colors and icons
- Set budget limits
- Edit/Delete categories anytime

✅ **Reports & Analytics**
- Monthly summaries
- Category breakdown
- Income vs Expenses
- Export to CSV

✅ **Data Management**
- Automatic backups
- Export/Import data
- Local SQLite database
- 100% offline

## File Structure

```
My-Expense-Manager/
├── main.py              # Start here
├── config.py            # Settings
├── requirements.txt     # Dependencies
├── build_exe.py         # Build script
├── init_data.py         # Initialize defaults
├── models/              # Data models
├── ui/                  # User interface
├── database/            # Database operations
├── utils/               # Helper functions
├── resources/           # Icons & styles
└── data/                # Local storage
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'PyQt5'"
```bash
pip install PyQt5
```

### "Database locked" error
- Close all instances of the application
- Delete `.db-journal` file if it exists
- Restart the application

### Executable won't run
- Check if Windows Defender is blocking it
- Try running as Administrator
- Verify Python 3.8+ is installed

## Support

For issues or feature requests, please open an issue on GitHub.

© 2026 - Manaf Asharaf
