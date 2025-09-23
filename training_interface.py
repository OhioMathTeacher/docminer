#!/usr/bin/env python3
"""
Interactive Training Interface for Search Buddy Positionality Detection

This creates a GUI interface for human experts to label papers and provide
training feedback directly within the application.
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QButtonGroup, QRadioButton,
    QScrollArea, QProgressBar, QMessageBox, QFileDialog, QCheckBox,
    QComboBox, QSpinBox, QGroupBox, QGridLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QTextCursor

import pdfplumber
from metadata_extractor import extract_positionality

class TrainingInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Buddy Training Interface")
        self.setGeometry(100, 100, 1200, 900)
        
        # Training data storage
        self.training_data = []
        self.current_paper_index = 0
        self.papers_list = []
        self.pdf_folder = ""
        
        # Load existing training data if available
        self.training_file = "training_data.json"
        self.load_training_data()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create the training interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Header with progress
        header_layout = QHBoxLayout()
        
        # Folder selection
        folder_btn = QPushButton("Select PDF Folder")
        folder_btn.clicked.connect(self.select_folder)
        header_layout.addWidget(folder_btn)
        
        # Progress tracking
        self.progress_label = QLabel("No papers loaded")
        self.progress_bar = QProgressBar()
        header_layout.addWidget(self.progress_label)
        header_layout.addWidget(self.progress_bar)
        
        layout.addLayout(header_layout)
        
        # Main content area
        content_layout = QHBoxLayout()
        
        # Left panel: Paper content
        left_panel = QGroupBox("Paper Content")
        left_panel.setMaximumWidth(500)
        left_layout = QVBoxLayout(left_panel)
        
        # Paper info
        self.paper_info = QLabel("No paper selected")
        self.paper_info.setFont(QFont("Arial", 10, QFont.Bold))
        left_layout.addWidget(self.paper_info)
        
        # Text display
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFont(QFont("Consolas", 9))
        left_layout.addWidget(self.text_display)
        
        # AI Detection Results
        ai_group = QGroupBox("Current AI Detection")
        ai_layout = QVBoxLayout(ai_group)
        self.ai_results = QLabel("No detection results")
        self.ai_results.setWordWrap(True)
        ai_layout.addWidget(self.ai_results)
        left_layout.addWidget(ai_group)
        
        content_layout.addWidget(left_panel)
        
        # Right panel: Training interface
        right_panel = QGroupBox("Human Expert Labeling")
        right_layout = QVBoxLayout(right_panel)
        
        # Positionality judgment
        judgment_group = QGroupBox("Does this paper contain positionality statements?")
        judgment_layout = QVBoxLayout(judgment_group)
        
        self.judgment_group = QButtonGroup()
        self.judgment_buttons = {}
        
        judgments = [
            ("positive_explicit", "✅ Yes - Explicit positionality statements"),
            ("positive_subtle", "🔍 Yes - Subtle/implicit positionality"), 
            ("negative", "❌ No positionality statements"),
            ("uncertain", "❓ Uncertain/borderline case")
        ]
        
        for value, text in judgments:
            btn = QRadioButton(text)
            self.judgment_buttons[value] = btn
            self.judgment_group.addButton(btn)
            judgment_layout.addWidget(btn)
            
        right_layout.addWidget(judgment_group)
        
        # Evidence collection
        evidence_group = QGroupBox("Evidence (if positionality found)")
        evidence_layout = QVBoxLayout(evidence_group)
        
        evidence_layout.addWidget(QLabel("Quote the specific text:"))
        self.evidence_text = QTextEdit()
        self.evidence_text.setMaximumHeight(100)
        evidence_layout.addWidget(self.evidence_text)
        
        # Location dropdown
        location_layout = QHBoxLayout()
        location_layout.addWidget(QLabel("Location:"))
        self.location_combo = QComboBox()
        self.location_combo.addItems([
            "Introduction/Background", "Methods/Methodology", 
            "Discussion/Conclusion", "Author Note", "Other"
        ])
        location_layout.addWidget(self.location_combo)
        evidence_layout.addLayout(location_layout)
        
        right_layout.addWidget(evidence_group)
        
        # Pattern type checkboxes
        pattern_group = QGroupBox("Type of Positionality (check all that apply)")
        pattern_layout = QGridLayout(pattern_group)
        
        self.pattern_checkboxes = {}
        patterns = [
            ("identity", "Identity disclosure"),
            ("researcher_pos", "Researcher positioning"),
            ("bias_ack", "Bias acknowledgment"),
            ("reflexive", "Reflexive awareness"),
            ("methodological", "Methodological reflexivity"),
            ("social_location", "Social location/standpoint"),
            ("other", "Other")
        ]
        
        for i, (key, label) in enumerate(patterns):
            cb = QCheckBox(label)
            self.pattern_checkboxes[key] = cb
            pattern_layout.addWidget(cb, i // 2, i % 2)
            
        right_layout.addWidget(pattern_group)
        
        # Confidence rating
        confidence_layout = QHBoxLayout()
        confidence_layout.addWidget(QLabel("Confidence:"))
        self.confidence_spin = QSpinBox()
        self.confidence_spin.setRange(1, 5)
        self.confidence_spin.setValue(3)
        self.confidence_spin.setSuffix("/5")
        confidence_layout.addWidget(self.confidence_spin)
        confidence_layout.addStretch()
        right_layout.addLayout(confidence_layout)
        
        # Explanation
        right_layout.addWidget(QLabel("Explanation (why this does/doesn't count):"))
        self.explanation_text = QTextEdit()
        self.explanation_text.setMaximumHeight(80)
        right_layout.addWidget(self.explanation_text)
        
        # Pattern suggestions
        right_layout.addWidget(QLabel("Pattern suggestions for AI:"))
        self.pattern_suggestions = QTextEdit()
        self.pattern_suggestions.setMaximumHeight(60)
        right_layout.addWidget(self.pattern_suggestions)
        
        content_layout.addWidget(right_panel)
        layout.addLayout(content_layout)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        prev_btn = QPushButton("← Previous")
        prev_btn.clicked.connect(self.previous_paper)
        button_layout.addWidget(prev_btn)
        
        save_btn = QPushButton("💾 Save & Next")
        save_btn.clicked.connect(self.save_and_next)
        save_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        button_layout.addWidget(save_btn)
        
        skip_btn = QPushButton("Skip →")
        skip_btn.clicked.connect(self.next_paper)
        button_layout.addWidget(skip_btn)
        
        button_layout.addStretch()
        
        export_btn = QPushButton("📤 Export Training Data")
        export_btn.clicked.connect(self.export_training_data)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
    def select_folder(self):
        """Select folder containing PDFs to train on"""
        folder = QFileDialog.getExistingDirectory(self, "Select PDF Folder")
        if folder:
            self.pdf_folder = folder
            self.papers_list = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]
            self.current_paper_index = 0
            self.update_progress()
            self.load_current_paper()
            
    def update_progress(self):
        """Update progress indicators"""
        if not self.papers_list:
            self.progress_label.setText("No papers loaded")
            self.progress_bar.setValue(0)
            return
            
        current = self.current_paper_index + 1
        total = len(self.papers_list)
        self.progress_label.setText(f"Paper {current} of {total}")
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        
    def load_current_paper(self):
        """Load and display the current paper"""
        if not self.papers_list or self.current_paper_index >= len(self.papers_list):
            return
            
        filename = self.papers_list[self.current_paper_index]
        filepath = os.path.join(self.pdf_folder, filename)
        
        # Update paper info
        self.paper_info.setText(f"📄 {filename}")
        
        # Extract and display text
        try:
            with pdfplumber.open(filepath) as pdf:
                text = ""
                # Show first 3 pages
                for i, page in enumerate(pdf.pages[:3]):
                    page_text = page.extract_text() or ""
                    text += f"\n--- PAGE {i+1} ---\n{page_text}\n"
                    
            self.text_display.setText(text)
            
            # Run AI detection
            ai_result = extract_positionality(filepath)
            score = ai_result.get("positionality_score", 0.0)
            tests = ai_result.get("positionality_tests", [])
            
            ai_summary = f"AI Score: {score:.3f}\n"
            ai_summary += f"Tests: {', '.join(tests) if tests else 'None'}\n"
            ai_summary += f"Prediction: {'POSITIVE' if score > 0.2 else 'NEGATIVE'}"
            
            self.ai_results.setText(ai_summary)
            
        except Exception as e:
            self.text_display.setText(f"Error loading paper: {e}")
            self.ai_results.setText("AI detection failed")
        
        # Clear previous inputs
        self.clear_inputs()
        
        # Load existing training data for this paper if available
        self.load_existing_label(filename)
        
    def clear_inputs(self):
        """Clear all input fields"""
        for btn in self.judgment_buttons.values():
            btn.setChecked(False)
        self.evidence_text.clear()
        self.explanation_text.clear()
        self.pattern_suggestions.clear()
        for cb in self.pattern_checkboxes.values():
            cb.setChecked(False)
        self.confidence_spin.setValue(3)
        
    def load_existing_label(self, filename):
        """Load existing training label for this paper if available"""
        for entry in self.training_data:
            if entry["filename"] == filename:
                # Restore previous inputs
                if entry["judgment"] in self.judgment_buttons:
                    self.judgment_buttons[entry["judgment"]].setChecked(True)
                self.evidence_text.setText(entry.get("evidence", ""))
                self.explanation_text.setText(entry.get("explanation", ""))
                self.pattern_suggestions.setText(entry.get("pattern_suggestions", ""))
                self.confidence_spin.setValue(entry.get("confidence", 3))
                
                # Restore pattern checkboxes
                patterns = entry.get("pattern_types", [])
                for key, cb in self.pattern_checkboxes.items():
                    cb.setChecked(key in patterns)
                break
        
    def save_and_next(self):
        """Save current training data and move to next paper"""
        self.save_current_training()
        self.next_paper()
        
    def save_current_training(self):
        """Save training data for current paper"""
        if not self.papers_list:
            return
            
        filename = self.papers_list[self.current_paper_index]
        
        # Get judgment
        judgment = None
        for key, btn in self.judgment_buttons.items():
            if btn.isChecked():
                judgment = key
                break
                
        if not judgment:
            QMessageBox.warning(self, "Missing Data", "Please select a judgment before saving.")
            return
        
        # Get pattern types
        pattern_types = [key for key, cb in self.pattern_checkboxes.items() if cb.isChecked()]
        
        # Create training entry
        entry = {
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
            "judgment": judgment,
            "evidence": self.evidence_text.toPlainText().strip(),
            "location": self.location_combo.currentText(),
            "pattern_types": pattern_types,
            "confidence": self.confidence_spin.value(),
            "explanation": self.explanation_text.toPlainText().strip(),
            "pattern_suggestions": self.pattern_suggestions.toPlainText().strip(),
        }
        
        # Remove existing entry for this file if present
        self.training_data = [d for d in self.training_data if d["filename"] != filename]
        
        # Add new entry
        self.training_data.append(entry)
        
        # Save to file
        self.save_training_data()
        
        QMessageBox.information(self, "Saved", f"Training data saved for {filename}")
        
    def next_paper(self):
        """Move to next paper"""
        if self.current_paper_index < len(self.papers_list) - 1:
            self.current_paper_index += 1
            self.update_progress()
            self.load_current_paper()
        else:
            QMessageBox.information(self, "Complete", "All papers have been reviewed!")
            
    def previous_paper(self):
        """Move to previous paper"""
        if self.current_paper_index > 0:
            self.current_paper_index -= 1
            self.update_progress()
            self.load_current_paper()
            
    def load_training_data(self):
        """Load existing training data"""
        if os.path.exists(self.training_file):
            try:
                with open(self.training_file, 'r') as f:
                    self.training_data = json.load(f)
            except Exception as e:
                print(f"Error loading training data: {e}")
                self.training_data = []
                
    def save_training_data(self):
        """Save training data to file"""
        try:
            with open(self.training_file, 'w') as f:
                json.dump(self.training_data, f, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Could not save training data: {e}")
            
    def export_training_data(self):
        """Export training data for analysis"""
        if not self.training_data:
            QMessageBox.information(self, "No Data", "No training data to export.")
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Training Data", 
            f"training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.training_data, f, indent=2)
                QMessageBox.information(self, "Exported", f"Training data exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Could not export: {e}")

def main():
    app = QApplication(sys.argv)
    window = TrainingInterface()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()