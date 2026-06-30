"""PyInstaller Build Script - Creates standalone .exe executable"""
import PyInstaller.__main__
import os
import sys
from pathlib import Path

def build_exe():
    """Build standalone executable"""
    
    # Get project root
    project_root = Path(__file__).parent
    
    # PyInstaller arguments
    args = [
        'main.py',
        '--name=MyExpenseManager',
        '--onefile',  # Single executable file
        '--windowed',  # No console window
        '--icon=resources/icon.ico',  # Application icon (if exists)
        f'--distpath={project_root}/dist',
        f'--buildpath={project_root}/build',
        f'--specpath={project_root}/build',
        '--hidden-import=PyQt5',
        '--hidden-import=sqlite3',
        '--hidden-import=csv',
        '--hidden-import=shutil',
        '--collect-all=PyQt5',
    ]
    
    print("\n" + "="*60)
    print("My Expense Manager - Building Executable")
    print("="*60)
    print(f"Output: {project_root}/dist/MyExpenseManager.exe")
    print("="*60 + "\n")
    
    try:
        PyInstaller.__main__.run(args)
        print("\n" + "="*60)
        print("✅ Build Complete!")
        print("="*60)
        print(f"\nExecutable created at: dist/MyExpenseManager.exe")
        print("\nTo use:")
        print("1. Copy MyExpenseManager.exe to desired location")
        print("2. Double-click to run (no installation required)")
        print("3. Application data stored in %APPDATA%/MyExpenseManager/")
        print("\nOr run from USB drive for portable use!")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n❌ Build Failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    build_exe()
