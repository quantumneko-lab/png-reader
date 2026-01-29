"""
Main application entry point with PyQt6 configuration
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from src.ui import MainWindow


def main():
    """Start the application"""
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
