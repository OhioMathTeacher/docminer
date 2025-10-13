#!/usr/bin/env python3
"""
Simplified DocMiner for testing executable creation
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class SimpleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocMiner Test")
        self.setGeometry(100, 100, 400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        label = QLabel("DocMiner is working!")
        label.setStyleSheet("font-size: 18px; padding: 20px;")
        layout.addWidget(label)

def main():
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()