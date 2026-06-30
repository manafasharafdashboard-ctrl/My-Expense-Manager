"""Install dependencies and setup script"""
import subprocess
import sys
import os

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Dependencies installed successfully!")

def run_app():
    """Run the application"""
    print("Starting My Expense Manager...")
    subprocess.call([sys.executable, "main.py"])

if __name__ == '__main__':
    try:
        install_dependencies()
        run_app()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
