"""Main Application Entry Point"""
import sys
from PyQt5.QtWidgets import QApplication
from config import APP_NAME, APP_VERSION, APP_COPYRIGHT
from ui import MainWindow

def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
