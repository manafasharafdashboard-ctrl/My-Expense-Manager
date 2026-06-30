# My Expense Manager

**© 2026 - Manaf Asharaf**

A portable, offline Windows application for managing personal finances. Works completely standalone with no internet connection required.

## 🚀 Quick Start

1. Download `MyExpenseManager.exe`
2. Double-click to run
3. Start tracking expenses immediately

## ✨ Features

- 💰 Track Income and Daily Expenses
- 📂 Custom Categories (Create/Edit/Delete)
- 🏦 Multiple Accounts Management
- 📊 Monthly Reports and Analytics
- 📈 Visual Charts and Graphs
- 💾 SQLite Database (100% Local Storage)
- 📤 Export to CSV/Excel
- 🔄 Data Backup/Restore
- 🎨 Professional UI
- 🔓 No Installation Required
- 📦 Portable (USB Drive Compatible)
- 🌐 100% Offline (No Internet Needed)

## 📋 System Requirements

- Windows 7 or later
- 100MB RAM minimum
- 50MB free disk space

## 💾 Data Storage

All data is stored locally in:
- `%APPDATA%\MyExpenseManager\` (Windows standard location)
- Or same folder as .exe if running from USB
- SQLite database - completely self-contained

## 🔧 Development Setup

```bash
pip install -r requirements.txt
python main.py
```

## 📦 Build to Executable

```bash
pip install pyinstaller
python build_exe.py
```

## 📁 Project Structure

```
My-Expense-Manager/
├── main.py
├── requirements.txt
├── config.py
├── build_exe.py
├── models/
├── ui/
├── database/
├── utils/
└── resources/
```

---

**© 2026 - Manaf Asharaf**
