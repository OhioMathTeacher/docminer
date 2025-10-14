#!/usr/bin/env python3
"""
DocMiner - Enhanced Training Interface for Positionality Detection
Copyright (c) 2025 Michael Todd Edwards (OhioMathTeacher)

Licensed under Creative Commons Attribution-NonCommercial 4.0 International License
For commercial use, please contact the copyright holder.
Academic and educational use is freely permitted.

This enhanced training interface provides a professional PDF viewer with AI-assisted
positionality detection capabilities for academic research training.
"""

import sys
import os
import json
import shutil
import subprocess
import platform
from pathlib import Path
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QButtonGroup, QRadioButton,
    QScrollArea, QProgressBar, QMessageBox, QFileDialog, QCheckBox,
    QComboBox, QSpinBox, QGroupBox, QGridLayout, QSplitter, QFrame,
    QTabWidget, QSlider, QMenu, QPlainTextEdit, QLineEdit, QSizePolicy, QDialog
)
from PySide6.QtCore import Qt, QTimer, Signal, QRect, QPoint, QUrl, QThread, QObject
from PySide6.QtGui import QFont, QTextCursor, QPixmap, QPainter, QPen, QColor, QBrush, QAction, QClipboard

# Try to import QtWebEngine, but it's optional
try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    HAS_WEBENGINE = True
except ImportError:
    HAS_WEBENGINE = False
    QWebEngineView = None  # Define as None so code doesn't break

import fitz  # PyMuPDF for PDF rendering
from utils.metadata_extractor import extract_positionality
from github_report_uploader import GitHubReportUploader
from configuration_dialog import ConfigurationDialog

def clean_extracted_text(text):
    """
    Clean up text extracted from PDFs or AI responses.
    Removes excessive whitespace, fixes line breaks, and removes redundant quotes.
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    
    import re
    
    # Remove AI quotation marks that wrap entire passages
    # (AI often returns: "This is the quote" when we just want: This is the quote)
    text = text.strip()
    if text.startswith('"') and text.endswith('"') and text.count('"') == 2:
        text = text[1:-1].strip()
    if text.startswith("'") and text.endswith("'") and text.count("'") == 2:
        text = text[1:-1].strip()
    
    # Fix PDF extraction issues:
    # 1. Remove excessive spaces (2+ spaces → single space) - PRESERVE 1 space between words!
    text = re.sub(r' {2,}', ' ', text)
    
    # 2. Fix broken line breaks (remove hyphenation at line ends)
    text = re.sub(r'-\n', '', text)
    
    # 3. Normalize line breaks (multiple blank lines → double line break)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    # 4. Remove spaces before punctuation
    text = re.sub(r' +([.,;:!?])', r'\1', text)
    
    # 5. Fix spacing after punctuation (ensure single space)
    text = re.sub(r'([.,;:!?])([A-Za-z])', r'\1 \2', text)
    
    # 6. Remove leading/trailing whitespace on each line (but preserve line structure)
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    return text.strip()

def open_pdf_with_system_viewer(pdf_path):
    """
    Open PDF with the system's default PDF viewer (cross-platform)
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        pdf_path = str(Path(pdf_path).resolve())  # Get absolute path
        
        # Cross-platform file opening
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", pdf_path], check=True)
        elif platform.system() == "Windows":  # Windows
            os.startfile(pdf_path)
        else:  # Linux and other Unix-like systems
            subprocess.run(["xdg-open", pdf_path], check=True)
        
        return True
        
    except Exception as e:
        print(f"Error opening PDF with system viewer: {e}")
        return False

def get_pdf_page_info(pdf_path, page_num=0):
    """
    Utility function to get PDF page dimensions and metadata.
    
    Args:
        pdf_path (str): Path to the PDF file
        page_num (int): Page number (0-based)
    
    Returns:
        dict: Page information including dimensions in points, pixels, inches, and aspect ratio
        None: If PDF cannot be opened or page doesn't exist
    """
    try:
        doc = fitz.open(pdf_path)
        if page_num >= len(doc):
            print(f"Page {page_num} doesn't exist in PDF (only {len(doc)} pages)")
            doc.close()
            return None
            
        page = doc[page_num]
        rect = page.rect
        
        # Calculate various dimension formats
        info = {
            'total_pages': len(doc),
            'page_number': page_num + 1,  # 1-based for display
            'dimensions': {
                'points': {'width': rect.width, 'height': rect.height},
                'inches': {'width': rect.width / 72, 'height': rect.height / 72},
                'pixels_72dpi': {'width': int(rect.width), 'height': int(rect.height)},
                'pixels_150dpi': {'width': int(rect.width * 150/72), 'height': int(rect.height * 150/72)}
            },
            'aspect_ratio': rect.width / rect.height,
            'orientation': 'portrait' if rect.height > rect.width else 'landscape'
        }
        
        doc.close()
        return info
        
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return None

class SelectablePDFLabel(QLabel):
    """Custom QLabel with text editor-style line-based text selection"""
    text_selected = Signal(str)  # text only - page handled separately
    
    def __init__(self):
        super().__init__()
        self.text_blocks = []
        self.text_lines = []  # Text organized by lines for proper selection
        self.selected_text = ""
        self.selection_start = None
        self.selection_end = None
        self.selection_rect = None
        self.selecting = False
        self.highlighted_lines = []  # Lines to highlight during active selection only
        
        # User-adjustable settings
        self.column_mode = "Auto"  # "Auto", "Single", or "Two-Column"
        self.selection_tolerance = 0.5  # Default 50% tolerance (adjustable via slider)
        
        # Style for better visual feedback
        self.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                background-color: white;
                selection-background-color: #316AC5;
                font-family: 'Courier New', monospace;
            }
        """)
        
        # Enable mouse tracking for selection
        self.setMouseTracking(True)
        
        # Context menu for copying
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def resizeEvent(self, event):
        """Clear selection when widget is resized to prevent coordinate misalignment"""
        super().resizeEvent(event)
        self.clear_selection()
        
    def clear_selection(self):
        """Clear current selection state"""
        self.selecting = False
        self.selection_start = None
        self.selection_end = None
        self.selection_rect = None
        self.selected_text = ""
        self.highlighted_lines = []
        self.text_selected.emit("")  # Notify that selection is cleared
        self.update()  # Trigger repaint to remove highlights
        
    def set_text_blocks(self, text_blocks):
        """Set the text blocks from PDF page and organize them into lines"""
        self.text_blocks = text_blocks
        print(f"DEBUG - set_text_blocks called with {len(text_blocks)} blocks")
        self.organize_text_into_lines()
        
    def organize_text_into_lines(self):
        """Organize text blocks into lines based on Y-coordinate for line-based selection"""
        if not self.text_blocks:
            self.text_lines = []
            return
            
        # Group text blocks by approximate Y-coordinate (line height tolerance)
        lines = {}
        line_height_tolerance = 5  # pixels
        
        for block in self.text_blocks:
            if not block.get('text', '').strip():
                continue
                
            bbox = block['bbox']
            y_center = (bbox[1] + bbox[3]) / 2  # Center Y coordinate
            
            # Find existing line or create new one
            line_key = None
            for existing_y in lines.keys():
                if abs(y_center - existing_y) <= line_height_tolerance:
                    line_key = existing_y
                    break
                    
            if line_key is None:
                line_key = y_center
                lines[line_key] = []
                
            lines[line_key].append({
                'text': block['text'],
                'bbox': bbox,
                'x_center': (bbox[0] + bbox[2]) / 2
            })
        
        # Sort lines by Y-coordinate (top to bottom) and blocks within lines by X-coordinate (left to right)
        self.text_lines = []
        for y_pos in sorted(lines.keys()):
            line_blocks = sorted(lines[y_pos], key=lambda b: b['x_center'])
            
            # Create line info
            line_text = ' '.join([block['text'] for block in line_blocks])
            line_bbox = self.calculate_line_bbox(line_blocks)
            
            self.text_lines.append({
                'text': line_text,
                'bbox': line_bbox,
                'blocks': line_blocks,
                'y_pos': y_pos
            })
            
        print(f"DEBUG - Organized {len(self.text_blocks)} blocks into {len(self.text_lines)} lines")
        
    def calculate_line_bbox(self, line_blocks):
        """Calculate bounding box that encompasses all blocks in a line"""
        if not line_blocks:
            return [0, 0, 0, 0]
            
        min_x = min(block['bbox'][0] for block in line_blocks)
        min_y = min(block['bbox'][1] for block in line_blocks)
        max_x = max(block['bbox'][2] for block in line_blocks)
        max_y = max(block['bbox'][3] for block in line_blocks)
        
        return [min_x, min_y, max_x, max_y]
        
    def mousePressEvent(self, event):
        """Start text selection"""
        if event.button() == Qt.LeftButton:
            self.selection_start = event.position().toPoint()
            self.selecting = True
            self.selected_text = ""
            self.highlighted_lines = []
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """Update selection"""
        if self.selecting and self.selection_start:
            self.selection_end = event.position().toPoint()
            self.update_line_selection()
            self.update()
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """Finish selection and emit selected text"""
        if event.button() == Qt.LeftButton and self.selecting:
            self.selection_end = event.position().toPoint()
            self.selecting = False
            
            # Check if this was a meaningful drag (not just a click)
            if self.selection_start and self.selection_end:
                drag_distance = (self.selection_end - self.selection_start).manhattanLength()
                
                if drag_distance > 10:  # Minimum 10 pixels to count as selection
                    self.update_line_selection()
                    
                    # Emit the final selected text (page number handled via parent window access)
                    if self.selected_text.strip():
                        self.text_selected.emit(self.selected_text.strip())
                        self.update()  # Redraw to show persistent highlight
                    else:
                        self.text_selected.emit("")
                else:
                    # Just a click, not a drag - don't clear existing highlights
                    self.selected_text = ""
                    self.selection_rect = None
                    self.update()
                
        super().mouseReleaseEvent(event)
        
    def update_line_selection(self):
        """Update selection using simple intersection detection"""
        if not self.selection_start or not self.selection_end or not self.text_blocks:
            self.selected_text = ""
            self.highlighted_lines = []
            return
            
        # Create selection rectangle
        self.selection_rect = QRect(self.selection_start, self.selection_end).normalized()
        
        # Collect all blocks that intersect with selection rectangle
        selected_blocks = []
        
        for block in self.text_blocks:
            if not block.get('text', '').strip():
                continue
                
            bbox = block['bbox']
            block_rect = QRect(
                int(bbox[0]), int(bbox[1]),
                int(bbox[2] - bbox[0]), int(bbox[3] - bbox[1])
            )
            
            # Column-aware selection with user-adjustable tolerance
            if self.selection_rect.intersects(block_rect):
                center_x = (bbox[0] + bbox[2]) / 2
                selection_left = min(self.selection_rect.left(), self.selection_rect.right())
                selection_right = max(self.selection_rect.left(), self.selection_rect.right())
                selection_width = selection_right - selection_left
                
                # Calculate tolerance based on user settings and column mode
                if self.column_mode in ["Single", "1-Col"]:
                    # Single column: Very generous tolerance, capture everything in selection
                    tolerance = selection_width * 2.0  # 200% - basically no X filtering
                elif self.column_mode in ["Two-Column", "2-Col"]:
                    # Two column: Strict tolerance to avoid adjacent columns
                    tolerance = max(selection_width * 0.2, 30)  # 20% with 30px minimum
                else:  # Auto mode
                    # Use user's slider setting (20% to 200%)
                    tolerance = max(selection_width * self.selection_tolerance, 30)  # User-defined with 30px minimum
                
                if (center_x >= selection_left - tolerance and 
                    center_x <= selection_right + tolerance):
                    selected_blocks.append({
                        'text': block['text'],
                        'bbox': bbox,
                        'x': (bbox[0] + bbox[2]) / 2,  # center X for sorting
                        'y': (bbox[1] + bbox[3]) / 2   # center Y for sorting
                    })
        
        if not selected_blocks:
            self.selected_text = ""
            self.highlighted_lines = []
            return
        
        # First sort by Y (top to bottom) to process in vertical order
        selected_blocks.sort(key=lambda b: b['y'])
        
        # Group blocks into lines - use vertical center position
        # Blocks are on same line if their Y-centers are close (within typical line height)
        lines = []
        current_line = []
        
        for block in selected_blocks:
            if not current_line:
                # Start first line
                current_line.append(block)
            else:
                # Calculate average Y-center of current line
                line_y_avg = sum(b['y'] for b in current_line) / len(current_line)
                block_y = block['y']
                
                # Typical line height is about 12-15 pixels, use half of that as threshold
                # This catches words on the same baseline even if heights vary slightly
                y_threshold = 8
                
                if abs(block_y - line_y_avg) <= y_threshold:
                    # Same line
                    current_line.append(block)
                else:
                    # New line - save current and start new
                    current_line.sort(key=lambda b: b['x'])  # Sort left to right
                    lines.append(current_line)
                    current_line = [block]
        
        # Don't forget the last line
        if current_line:
            current_line.sort(key=lambda b: b['x'])
            lines.append(current_line)
        
        # Build selected text from lines
        text_lines = []
        
        for line_blocks in lines:
            # Extract text from this line and clean up spacing
            line_text = ' '.join([b['text'] for b in line_blocks])
            # Normalize whitespace: collapse multiple spaces, strip leading/trailing
            line_text = ' '.join(line_text.split())
            if line_text:  # Only add non-empty lines
                text_lines.append(line_text)
        
        # Join lines with newlines and clean up
        self.selected_text = '\n'.join(text_lines) if text_lines else ""
        
    def paintEvent(self, event):
        """Custom paint to show active selection rectangle"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        
        # Draw selection rectangle while actively dragging - good visual feedback
        if self.selecting and self.selection_start and self.selection_end:
            painter.setBrush(QBrush(QColor(100, 149, 237, 50)))  # Light blue semi-transparent
            painter.setPen(QPen(QColor(65, 105, 225), 2, Qt.SolidLine))  # Royal blue solid border
            
            sel_rect = QRect(self.selection_start, self.selection_end).normalized()
            painter.drawRect(sel_rect)
            
        painter.end()
            
    def show_context_menu(self, position):
        """Show context menu for copying text"""
        if self.selected_text:
            menu = QMenu(self)
            
            copy_action = QAction("📋 Copy Selected Text", self)
            copy_action.triggered.connect(self.copy_selected_text)
            menu.addAction(copy_action)
            
            copy_all_action = QAction("📄 Copy All Page Text", self)
            copy_all_action.triggered.connect(self.copy_all_text)
            menu.addAction(copy_all_action)
            
            menu.exec(self.mapToGlobal(position))
    
    def copy_selected_text(self):
        """Copy selected text to clipboard"""
        if self.selected_text:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.selected_text)
            
    def copy_all_text(self):
        """Copy all text from current page to clipboard"""
        if self.text_blocks:
            all_text = "\n".join(block['text'] for block in self.text_blocks)
            clipboard = QApplication.clipboard()
            clipboard.setText(all_text)

class EmbeddedPDFViewer(QWidget):
    """Embedded PDF viewer with proper aspect ratio handling for portrait documents"""
    
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window  # Reference to main window for callbacks
        self.current_pdf_path = None
        self.current_page = 0  # Track current page
        self.total_pages = 0   # Track total pages
        self.pdf_document = None  # Store document object
        self.pdf_width = 612  # Standard letter width
        self.pdf_height = 792  # Standard letter height
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        
        # Controls - make them smaller
        controls = QHBoxLayout()
        
        # Page navigation
        self.prev_btn = QPushButton("◀")
        self.prev_btn.clicked.connect(self.previous_page)
        self.prev_btn.setMaximumWidth(30)
        self.prev_btn.setStyleSheet("QPushButton { font-size: 12px; padding: 2px; }")
        self.prev_btn.setEnabled(False)
        controls.addWidget(self.prev_btn)
        
        self.page_label = QLabel("Page 1 of 1")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setStyleSheet("QLabel { font-size: 9px; font-weight: bold; }")
        self.page_label.setMinimumWidth(80)
        controls.addWidget(self.page_label)
        
        self.next_btn = QPushButton("▶")
        self.next_btn.clicked.connect(self.next_page)
        self.next_btn.setMaximumWidth(30)
        self.next_btn.setStyleSheet("QPushButton { font-size: 12px; padding: 2px; }")
        self.next_btn.setEnabled(False)
        controls.addWidget(self.next_btn)
        
        controls.addWidget(QLabel("|"))  # Separator
        
        # Add view mode control (Letter, A4, etc.)
        view_label = QLabel("View:")
        view_label.setStyleSheet("QLabel { font-size: 9px; }")
        controls.addWidget(view_label)
        
        self.view_mode_combo = QComboBox()
        self.view_mode_combo.addItems([
            "Fit Page", "Letter", "A4", "Full Width", "Full Height", "1:1 Fixed"
        ])
        self.view_mode_combo.setCurrentText("Fit Page")
        self.view_mode_combo.setMaximumWidth(85)
        self.view_mode_combo.setStyleSheet("QComboBox { font-size: 10px; padding: 4px; }")
        self.view_mode_combo.setToolTip("1:1 Fixed = Exact PDF scale for accurate text selection | Letter: 8.5×11 | A4: European")
        self.view_mode_combo.currentTextChanged.connect(self.change_zoom)
        controls.addWidget(self.view_mode_combo)
        
        controls.addWidget(QLabel("|"))  # Separator
        
        # Add zoom control with extended range
        zoom_label = QLabel("Zoom:")
        zoom_label.setStyleSheet("QLabel { font-size: 10px; }")
        controls.addWidget(zoom_label)
        
        self.zoom_combo = QComboBox()
        self.zoom_combo.addItems([
            "Auto", "50%", "65%", "80%", "100%", "125%", "150%", "175%", "200%"
        ])
        self.zoom_combo.setCurrentText("Auto")
        self.zoom_combo.setMaximumWidth(65)
        self.zoom_combo.setStyleSheet("QComboBox { font-size: 10px; padding: 4px; }")
        self.zoom_combo.setToolTip("Adjust text size for readability (200% for small screens)")
        self.zoom_combo.currentTextChanged.connect(self.change_zoom)
        controls.addWidget(self.zoom_combo)
        
        controls.addWidget(QLabel("|"))  # Separator
        
        # Column mode selector
        col_label = QLabel("Cols:")
        col_label.setStyleSheet("QLabel { font-size: 10px; }")
        controls.addWidget(col_label)
        
        self.column_mode_combo = QComboBox()
        self.column_mode_combo.addItems(["Auto", "1-Col", "2-Col"])
        self.column_mode_combo.setCurrentText("Auto")
        self.column_mode_combo.setMaximumWidth(65)
        self.column_mode_combo.setStyleSheet("QComboBox { font-size: 10px; padding: 4px; }")
        self.column_mode_combo.setToolTip("Column Mode:\n• Auto: Smart detection\n• 1-Col: Wide tolerance (single column)\n• 2-Col: Strict (avoid adjacent columns)")
        self.column_mode_combo.currentTextChanged.connect(self.update_column_mode)
        controls.addWidget(self.column_mode_combo)
        
        controls.addWidget(QLabel("|"))  # Separator
        
        # Text selection sensitivity slider - make it prominent!
        sens_label = QLabel("Text:")
        sens_label.setStyleSheet("QLabel { font-size: 10px; }")
        sens_label.setToolTip("Text Selection Sensitivity")
        controls.addWidget(sens_label)
        
        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setMinimum(20)  # 20% tolerance
        self.sensitivity_slider.setMaximum(200)  # 200% tolerance
        self.sensitivity_slider.setValue(50)  # Start at 50%
        self.sensitivity_slider.setMinimumWidth(100)
        self.sensitivity_slider.setMaximumWidth(150)
        self.sensitivity_slider.setMinimumHeight(20)
        self.sensitivity_slider.setTickPosition(QSlider.TicksBelow)
        self.sensitivity_slider.setTickInterval(30)
        self.sensitivity_slider.setStyleSheet("QSlider::groove:horizontal { height: 6px; background: #ddd; } QSlider::handle:horizontal { width: 16px; background: #4a90e2; margin: -5px 0; border-radius: 8px; }")
        self.sensitivity_slider.setToolTip("Text Selection Sensitivity (20-200%)\nDrag left = stricter (avoid adjacent columns)\nDrag right = more generous (catch all text)")
        self.sensitivity_slider.valueChanged.connect(self.update_sensitivity_label)
        controls.addWidget(self.sensitivity_slider)
        
        self.sensitivity_label = QLabel("50%")
        self.sensitivity_label.setStyleSheet("QLabel { font-size: 12px; font-weight: bold; min-width: 45px; }")
        self.sensitivity_label.setAlignment(Qt.AlignCenter)
        controls.addWidget(self.sensitivity_label)
        
        controls.addStretch()
        
        layout.addLayout(controls)
        
        # Always use PyMuPDF for reliable aspect ratio control
        self.setup_pdf_viewer(layout)
        
    def setup_pdf_viewer(self, layout):
        """Setup PDF viewer using PyMuPDF with proper aspect ratio"""
        # Scrollable area optimized for portrait documents (8.5×11 Letter aspect ratio)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.scroll_area.setStyleSheet("QScrollArea { border: 1px solid #ccc; background-color: #f0f0f0; }")
        
        # Set portrait aspect ratio constraints for Letter-sized documents
        # Letter: 8.5×11 inches = aspect ratio of 0.773 (width/height)
        # Use minimum width but taller minimum height for portrait orientation
        self.scroll_area.setMinimumWidth(400)   # Minimum readable width
        self.scroll_area.setMaximumWidth(650)   # Limit width for portrait aspect
        self.scroll_area.setMinimumHeight(700)  # Taller for portrait (was 500)
        
        # Use SelectablePDFLabel instead of regular QLabel for text selection
        self.pdf_label = SelectablePDFLabel()
        self.pdf_label.setAlignment(Qt.AlignCenter)
        self.pdf_label.setStyleSheet("QLabel { background-color: white; border: 1px solid #ddd; margin: 5px; }")
        self.pdf_label.setScaledContents(False)  # Don't auto-scale - we'll control this
        
        self.scroll_area.setWidget(self.pdf_label)
        layout.addWidget(self.scroll_area)
        
    def change_zoom(self, zoom_text):
        """Handle zoom level changes"""
        if hasattr(self, 'pdf_document') and self.pdf_document:
            self.render_current_page()
    
    def calculate_zoom_scale(self, zoom_text):
        """Calculate scale factor based on view mode and zoom selection"""
        # Get actual available space in the PDF container
        available_width = self.scroll_area.width() - 40  # Account for scrollbars/margins
        available_height = self.scroll_area.height() - 40
        
        # First, determine base scale from view mode
        view_mode = self.view_mode_combo.currentText()
        
        if view_mode == "Fit Page":
            # Fit entire page without scrollbars - scale to fit both dimensions
            width_scale = available_width / self.pdf_width
            height_scale = available_height / self.pdf_height
            base_scale = min(width_scale, height_scale)
        elif view_mode == "1:1 Fixed":
            # No scaling - exact PDF coordinates for perfect text selection
            base_scale = 1.0
        elif view_mode == "Letter":
            # Optimize for 8.5×11 Letter paper (portrait)
            # Typical Letter PDF is 612×792 points
            width_scale = available_width / 612
            height_scale = available_height / 792
            base_scale = min(width_scale, height_scale)
        elif view_mode == "A4":
            # Optimize for A4 paper (portrait)
            # Typical A4 PDF is 595×842 points
            width_scale = available_width / 595
            height_scale = available_height / 842
            base_scale = min(width_scale, height_scale)
        elif view_mode == "Full Width":
            # Fill width, allow vertical scrolling
            base_scale = available_width / self.pdf_width
        elif view_mode == "Full Height":
            # Fill height, allow horizontal scrolling if needed
            base_scale = available_height / self.pdf_height
        else:
            # Fallback: fit to available space
            width_scale = available_width / self.pdf_width
            height_scale = available_height / self.pdf_height
            base_scale = min(width_scale, height_scale)
        
        # Then apply zoom multiplier
        if zoom_text == "Auto":
            return base_scale
        elif zoom_text.endswith("%"):
            # Parse percentage and multiply base scale
            percentage = int(zoom_text.replace("%", ""))
            zoom_multiplier = percentage / 100.0
            return base_scale * zoom_multiplier
        else:
            return base_scale
        
    def load_pdf(self, pdf_path):
        """Load PDF with proper aspect ratio calculation and page navigation"""
        self.current_pdf_path = pdf_path
        
        try:
            import fitz
            # Store document for page navigation
            if hasattr(self, 'pdf_document') and self.pdf_document:
                self.pdf_document.close()
            self.pdf_document = fitz.open(pdf_path)
            self.total_pages = len(self.pdf_document)
            self.current_page = 0  # Start with first page
            
            # Update page navigation controls
            self.update_page_controls()
            
            # Render the current page
            self.render_current_page()
            
            print(f"DEBUG: PDF loaded with {self.total_pages} pages and navigation support")
            return True
            
        except Exception as e:
            return self.handle_load_error(e)

    def extract_text_blocks(self, page, scale):
        """Extract text blocks from PDF page for text selection"""
        try:
            text_blocks = []
            
            # Extract word-level text with positions
            words = page.get_text("words")  # Returns list of (x0, y0, x1, y1, "word", block_no, line_no, word_no)
            
            for word in words:
                if len(word) >= 5:  # Ensure we have all required fields
                    x0, y0, x1, y1, text = word[:5]
                    # Scale coordinates to match display
                    text_blocks.append({
                        'bbox': (x0 * scale, y0 * scale, x1 * scale, y1 * scale),
                        'text': text
                    })
            
            print(f"DEBUG: Extracted {len(text_blocks)} text blocks for selection")
            self.pdf_label.set_text_blocks(text_blocks)
            self.pdf_label.current_page = self.current_page  # Update page number for text selection
            
        except Exception as e:
            print(f"DEBUG: Text extraction failed: {e}")
            self.pdf_label.set_text_blocks([])
            self.pdf_label.current_page = self.current_page

    def update_page_controls(self):
        """Update page navigation controls"""
        if hasattr(self, 'total_pages') and self.total_pages > 0:
            self.page_label.setText(f"Page {self.current_page + 1} of {self.total_pages}")
            self.prev_btn.setEnabled(self.current_page > 0)
            self.next_btn.setEnabled(self.current_page < self.total_pages - 1)
        else:
            self.page_label.setText("No pages")
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
    
    def previous_page(self):
        """Go to previous page"""
        if hasattr(self, 'current_page') and self.current_page > 0:
            self.current_page -= 1
            self.render_current_page()
            self.update_page_controls()
    
    def next_page(self):
        """Go to next page"""
        if hasattr(self, 'current_page') and hasattr(self, 'total_pages') and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.render_current_page()
            self.update_page_controls()
    
    def update_column_mode(self, mode):
        """Update column detection mode"""
        if hasattr(self, 'pdf_label'):
            self.pdf_label.column_mode = mode
    
    def update_sensitivity_label(self, value):
        """Update sensitivity label when slider changes"""
        self.sensitivity_label.setText(f"{value}%")
        if hasattr(self, 'pdf_label'):
            self.pdf_label.selection_tolerance = value / 100.0  # Convert to decimal
    
    def render_current_page(self):
        """Render the current page of the PDF"""
        if not hasattr(self, 'pdf_document') or not self.pdf_document or self.current_page >= self.total_pages:
            return False
            
        try:
            page = self.pdf_document[self.current_page]
            
            # Get actual PDF dimensions
            rect = page.rect
            self.pdf_width = rect.width
            self.pdf_height = rect.height
            
            # Use zoom control to determine scale
            zoom_text = self.zoom_combo.currentText()
            scale = self.calculate_zoom_scale(zoom_text)
            
            # Apply minimum/maximum constraints for usability
            min_scale = 0.3
            max_scale = 3.0
            scale = max(min_scale, min(scale, max_scale))
                
            display_width = int(self.pdf_width * scale)
            display_height = int(self.pdf_height * scale)
            
            print(f"DEBUG: Rendering page {self.current_page + 1}/{self.total_pages} at {display_width} x {display_height} (scale: {scale:.2f})")
            
            # Render at calculated size
            mat = fitz.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("ppm")
            
            from PySide6.QtGui import QPixmap
            qimg = QPixmap()
            qimg.loadFromData(img_data)
            
            # Set the pixmap and adjust label size
            self.pdf_label.setPixmap(qimg)
            self.pdf_label.resize(display_width, display_height)
            self.pdf_label.setMinimumSize(display_width, display_height)
            
            # Extract text blocks for selection
            self.extract_text_blocks(page, scale)
            
            return True
            
        except Exception as e:
            print(f"DEBUG: Error rendering page {self.current_page + 1}: {e}")
            return False

    def clear_current_output(self):
        """Clear the currently active output tab"""
        # Get the currently active tab in evidence_tabs
        evidence_tabs = self.findChild(QTabWidget)
        if evidence_tabs:
            current_tab = evidence_tabs.currentWidget()
            if current_tab:
                # Find text widgets in the current tab and clear them
                for widget in current_tab.findChildren(QTextEdit):
                    widget.clear()
                for widget in current_tab.findChildren(QPlainTextEdit):
                    widget.clear()

    def merge_outputs(self):
        """Merge AI analysis and evidence into final tab"""
        ai_content = self.ai_input.toPlainText()
        evidence_content = self.human_input.toPlainText()
        
        combined = ""
        if ai_content:
            combined += "=== AI Analysis ===\n" + ai_content + "\n\n"
        if evidence_content:
            combined += "=== Evidence ===\n" + evidence_content
            
        # For now, show in pattern suggestions area
        self.pattern_suggestions.setPlainText(combined)
        
    def handle_load_error(self, error):
        """Handle PDF loading errors"""
        print(f"DEBUG: PDF loading failed: {error}")
        self.pdf_label.setText(f"Error loading PDF: {error}")
        return False
        
    def try_fallback_load(self, pdf_path):
        """Removed - functionality integrated into load_pdf method"""
        pass

class PDFViewer(QWidget):
    """Enhanced PDF viewer widget with page navigation and text selection"""
    
    def __init__(self):
        super().__init__()
        self.pdf_document = None
        self.current_page = 0
        self.zoom_level = 1.0
        self.text_blocks = []  # Store text block positions for selection
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Controls
        controls = QHBoxLayout()
        
        self.prev_btn = QPushButton("◀ Previous")
        self.prev_btn.clicked.connect(self.previous_page)
        controls.addWidget(self.prev_btn)
        
        self.page_label = QLabel("No PDF loaded")
        self.page_label.setAlignment(Qt.AlignCenter)
        controls.addWidget(self.page_label)
        
        self.next_btn = QPushButton("Next ▶")
        self.next_btn.clicked.connect(self.next_page)
        controls.addWidget(self.next_btn)
        
        controls.addStretch()
        
        # Zoom controls
        controls.addWidget(QLabel("Zoom:"))
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(50, 200)  # 50% to 200%
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.change_zoom)
        self.zoom_slider.setMaximumWidth(100)
        controls.addWidget(self.zoom_slider)
        
        self.zoom_label = QLabel("100%")
        self.zoom_label.setMinimumWidth(40)
        controls.addWidget(self.zoom_label)
        
        # Paper size ratio controls
        controls.addWidget(QLabel("|"))  # Separator
        controls.addWidget(QLabel("Aspect:"))
        
        self.paper_ratio_combo = QComboBox()
        self.paper_ratio_combo.addItems(["Letter (8.5×11)", "A4 (210×297)", "Custom"])
        self.paper_ratio_combo.setCurrentText("Letter (8.5×11)")
        self.paper_ratio_combo.currentTextChanged.connect(self.on_paper_ratio_changed)
        self.paper_ratio_combo.setMaximumWidth(120)
        self.paper_ratio_combo.setToolTip("Optimize viewing for standard paper sizes")
        controls.addWidget(self.paper_ratio_combo)
        
        # Fit PDF button for optimal viewing
        fit_pdf_btn = QPushButton("Perfect Fit")
        fit_pdf_btn.clicked.connect(self.fit_pdf_to_window)
        fit_pdf_btn.setMaximumWidth(100)
        fit_pdf_btn.setToolTip("Snap viewing window to exact PDF page dimensions - no scrollbars needed!")
        controls.addWidget(fit_pdf_btn)
        
        layout.addLayout(controls)
        
        # PDF display area with text selection
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Allow content to resize naturally
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.pdf_label = SelectablePDFLabel()
        self.pdf_label.setText("Load a PDF document to begin analysis...")
        self.pdf_label.setAlignment(Qt.AlignCenter)
        self.pdf_label.setStyleSheet("""
            QLabel { 
                background-color: white; 
                border: 1px solid #666666; 
                color: black;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                padding: 20px;
            }
        """)
        
        # Create a simple container for the PDF
        self.pdf_widget = QWidget()
        pdf_layout = QVBoxLayout(self.pdf_widget)
        pdf_layout.setContentsMargins(10, 10, 10, 10)  # Small margins
        pdf_layout.setAlignment(Qt.AlignCenter)  # Center the PDF
        pdf_layout.addWidget(self.pdf_label)
        
        # Configure scroll area for proper display
        self.scroll_area.setWidget(self.pdf_widget)
        self.scroll_area.setWidgetResizable(True)  # Allow resizing initially
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Add scroll area directly without extra stretching containers
        layout.addWidget(self.scroll_area)
        
    def get_pdf_page_dimensions(self, page_num=0):
        """Get the exact dimensions of a PDF page in points and pixels"""
        if not self.pdf_document:
            return None
            
        try:
            page = self.pdf_document[page_num]
            rect = page.rect
            
            # Calculate pixel dimensions at current zoom
            pixel_width = rect.width * self.zoom_level
            pixel_height = rect.height * self.zoom_level
            
            return {
                'points': {'width': rect.width, 'height': rect.height},
                'pixels': {'width': int(pixel_width), 'height': int(pixel_height)},
                'aspect_ratio': rect.width / rect.height,
                'inches': {'width': rect.width / 72, 'height': rect.height / 72}
            }
        except Exception as e:
            print(f"Error getting PDF dimensions: {e}")
            return None
    
    def load_pdf(self, pdf_path):
        """Load a PDF file for viewing with proper initial sizing"""
        try:
            self.pdf_document = fitz.open(pdf_path)
            self.current_page = 0
            
            # Get page dimensions first
            dims = self.get_pdf_page_dimensions(0)
            if dims:
                print(f"DEBUG: PDF page dimensions: {dims['points']['width']:.1f}x{dims['points']['height']:.1f} points")
                print(f"DEBUG: Aspect ratio: {dims['aspect_ratio']:.3f}")
            
            # Start with a reasonable reading zoom (150%) instead of tiny 100%
            self.zoom_level = 1.5
            self.zoom_slider.setValue(150)
            
            self.render_page()
            self.update_controls()
            
            # Immediately apply perfect fit to optimize the display
            print("DEBUG: Applying initial perfect fit for optimal viewing")
            QTimer.singleShot(100, self.fit_pdf_to_window)  # Small delay for rendering
            
            return True
        except Exception as e:
            QMessageBox.critical(self, "PDF Error", f"Could not load PDF: {e}")
            return False
            
    def render_page(self):
        """Render the current page as an image and extract text blocks"""
        if not self.pdf_document:
            return
            
        try:
            page = self.pdf_document[self.current_page]
            
            # Create transformation matrix for zoom
            mat = fitz.Matrix(self.zoom_level, self.zoom_level)
            
            # Render page to pixmap
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to QPixmap
            img_data = pix.tobytes("ppm")
            qimg = QPixmap()
            qimg.loadFromData(img_data)
            
            # Set the pixmap to the label
            self.pdf_label.setPixmap(qimg)
            self.pdf_label.setAlignment(Qt.AlignCenter)
            
            # Let the label size itself naturally to the pixmap
            self.pdf_label.adjustSize()
            
            print(f"DEBUG: PDF rendered at {qimg.width()}x{qimg.height()}, zoom: {self.zoom_level:.2f}")
            
        except Exception as e:
            print(f"Error rendering page: {e}")
            
    def remove_size_constraints(self):
        """Remove any size constraints that prevent perfect PDF fitting"""
        if not hasattr(self, 'scroll_area') or not hasattr(self, 'pdf_widget'):
            print("DEBUG: Missing scroll_area or pdf_widget")
            return
            
        try:
            # Remove all size constraints to allow natural sizing
            self.pdf_widget.setMaximumSize(16777215, 16777215)  # Qt's maximum size
            self.pdf_widget.setMinimumSize(0, 0)
            
            self.scroll_area.setMaximumSize(16777215, 16777215)
            self.scroll_area.setMinimumSize(0, 0)
            
            print("DEBUG: Removed all size constraints - widgets can now size naturally")
            
        except Exception as e:
            print(f"Error removing size constraints: {e}")
            import traceback
            traceback.print_exc()
    
    def resizeEvent(self, event):
        """Handle window resize to maintain PDF proportions"""
        super().resizeEvent(event)
        # Remove size constraints to allow natural resizing
        QTimer.singleShot(50, self.remove_size_constraints)
        if not self.pdf_document:
            return
            
        try:
            page = self.pdf_document[self.current_page]
            
            # Create transformation matrix for zoom
            mat = fitz.Matrix(self.zoom_level, self.zoom_level)
            
            # Render page to pixmap
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to QPixmap
            img_data = pix.tobytes("ppm")
            qpixmap = QPixmap()
            qpixmap.loadFromData(img_data)
            
            # Extract text blocks for selection with improved coordinate mapping
            text_blocks = []
            try:
                # Get text with precise word-level positioning
                words = page.get_text("words")  # Returns list of (x0, y0, x1, y1, "word", block_no, line_no, word_no)
                
                for word_info in words:
                    if len(word_info) >= 5:
                        x0, y0, x1, y1, word_text = word_info[:5]
                        
                        if word_text.strip():  # Only process non-empty words
                            # Transform coordinates with zoom
                            transformed_bbox = [
                                x0 * self.zoom_level,
                                y0 * self.zoom_level,
                                x1 * self.zoom_level,
                                y1 * self.zoom_level
                            ]
                            
                            text_blocks.append({
                                "text": word_text,
                                "bbox": transformed_bbox
                            })
                
                print(f"Extracted {len(text_blocks)} word-level text blocks from page {self.current_page + 1}")
                
                # If word-level extraction didn't work, fall back to span-level
                if not text_blocks:
                    text_dict = page.get_text("dict")
                    
                    for block in text_dict["blocks"]:
                        if block.get("type") == 0:  # Text block (type 0)
                            for line in block.get("lines", []):
                                for span in line.get("spans", []):
                                    span_text = span.get("text", "").strip()
                                    if span_text:  # Only process non-empty text
                                        # Use span bbox, transformed with zoom
                                        bbox = span["bbox"]
                                        transformed_bbox = [
                                            bbox[0] * self.zoom_level,
                                            bbox[1] * self.zoom_level,
                                            bbox[2] * self.zoom_level,
                                            bbox[3] * self.zoom_level
                                        ]
                                        
                                        # Add individual span as text block
                                        text_blocks.append({
                                            "text": span_text,
                                            "bbox": transformed_bbox
                                        })
                    
                    print(f"Fallback: extracted {len(text_blocks)} span-level blocks")
                
                # Set text blocks for selection
                self.pdf_label.set_text_blocks(text_blocks)
                
            except Exception as text_error:
                print(f"Warning: Could not extract text blocks: {text_error}")
                # Final fallback: try simpler text extraction
                try:
                    simple_text = page.get_text()
                    if simple_text:
                        # Create one large text block for the whole page
                        page_rect = page.rect
                        transformed_bbox = [
                            page_rect.x0 * self.zoom_level,
                            page_rect.y0 * self.zoom_level, 
                            page_rect.x1 * self.zoom_level,
                            page_rect.y1 * self.zoom_level
                        ]
                        text_blocks = [{
                            "text": simple_text,
                            "bbox": transformed_bbox
                        }]
                        self.pdf_label.set_text_blocks(text_blocks)
                        print("Used final fallback: single page text block")
                except Exception as fallback_error:
                    print(f"All text extraction methods failed: {fallback_error}")
                    self.pdf_label.set_text_blocks([])
            
            # Display in label with proper sizing for scrolling
            self.pdf_label.setPixmap(qpixmap)
            self.pdf_label.setScaledContents(False)
            self.pdf_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # Switch to proper alignment
            
            # Update scroll area configuration for PDF content
            self.scroll_area.setWidgetResizable(False)  # Fixed size for PDF content
            
            # Size the label to exactly match the pixmap size for proper scrolling
            self.pdf_label.resize(qpixmap.size())
            self.pdf_label.setMinimumSize(qpixmap.size())
            self.pdf_label.setMaximumSize(qpixmap.size())
            
            # Update styling for PDF content
            self.pdf_label.setStyleSheet("""
                QLabel { 
                    background-color: white; 
                    border: 1px solid #666666;
                    font-family: 'Courier New', monospace;
                }
            """)
            
        except Exception as e:
            self.pdf_label.setText(f"Error rendering page: {e}")
            self.pdf_label.set_text_blocks([])
            
    def update_controls(self):
        """Update navigation controls"""
        if self.pdf_document:
            total_pages = len(self.pdf_document)
            self.page_label.setText(f"Page {self.current_page + 1} of {total_pages}")
            
            self.prev_btn.setEnabled(self.current_page > 0)
            self.next_btn.setEnabled(self.current_page < total_pages - 1)
        else:
            self.page_label.setText("No PDF loaded")
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            
    def previous_page(self):
        """Go to previous page"""
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            self.render_page()
            self.update_controls()
            
    def next_page(self):
        """Go to next page"""
        if self.pdf_document and self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.render_page()
            self.update_controls()
    
    def find_and_highlight_text(self):
        """Search for text in PDF using PyMuPDF and add to Human Input"""
        search_text = self.search_input.text().strip()
        if not search_text:
            QMessageBox.information(self, "No Search Text", "Please enter text to search for.")
            return
        
        if not self.pdf_document:
            QMessageBox.information(self, "No PDF", "Please load a PDF first.")
            return
        
        if not self.parent_window:
            QMessageBox.warning(self, "Error", "Parent window reference not set.")
            return
        
        try:
            # Search in current page
            import fitz
            page = self.pdf_document[self.current_page]
            
            # Search with case-insensitive and dehyphenate flags
            flags = fitz.TEXT_IGNORECASE | fitz.TEXT_DEHYPHENATE
            hits = page.search_for(search_text, flags=flags, quads=True)
            
            if hits:
                # Extract the found text instances
                found_texts = []
                for i, quads in enumerate(hits):
                    # Get the actual text from the quad coordinates
                    rect = quads.rect if hasattr(quads, 'rect') else fitz.Rect(quads)
                    found_text = page.get_textbox(rect)
                    if found_text.strip():
                        found_texts.append(found_text.strip())
                
                # Add to Human Input via parent window
                if found_texts:
                    result_text = "\n".join(found_texts)
                    self.parent_window.on_text_selected(result_text)
                    self.parent_window.statusBar().showMessage(
                        f"✅ Found {len(found_texts)} match(es) on page {self.current_page + 1}", 3000
                    )
                else:
                    self.parent_window.statusBar().showMessage("No text extracted from matches", 2000)
            else:
                self.parent_window.statusBar().showMessage(
                    f"❌ '{search_text}' not found on page {self.current_page + 1}", 3000
                )
                
        except Exception as e:
            print(f"Error searching PDF: {e}")
            QMessageBox.warning(self, "Search Error", f"Error searching PDF:\n{str(e)}")
    
    def clear_search_highlights(self):
        """Clear search input"""
        self.search_input.clear()
        if self.parent_window:
            self.parent_window.statusBar().showMessage("Search cleared", 2000)
    
    def add_highlight_annotation(self, selected_text):
        """Add a real PDF highlight annotation for the selected text"""
        if not self.pdf_document or not selected_text.strip():
            return
        
        try:
            import fitz
            page = self.pdf_document[self.current_page]
            
            # Search for the text to get accurate quad coordinates
            flags = fitz.TEXT_IGNORECASE | fitz.TEXT_DEHYPHENATE
            quads = page.search_for(selected_text.strip(), flags=flags, quads=True)
            
            if quads:
                # Add highlight annotation with yellow color
                highlight = page.add_highlight_annot(quads)
                highlight.set_colors(stroke=(1, 1, 0))  # Yellow highlight
                highlight.update()
                
                print(f"DEBUG: Added highlight annotation for {len(quads)} quad(s)")
                
                # Refresh the page display
                self.render_page()
                
                if self.parent_window:
                    self.parent_window.statusBar().showMessage("✨ Text highlighted in PDF", 2000)
            else:
                print(f"DEBUG: Could not find text to highlight: '{selected_text[:50]}'")
                
        except Exception as e:
            print(f"Error adding highlight annotation: {e}")
            
    def change_zoom(self, value):
        """Change zoom level"""
        self.zoom_level = value / 100.0  # Convert percentage to decimal
        self.zoom_label.setText(f"{value}%")
        if self.pdf_document:
            self.render_page()
    
    def fit_pdf_to_window(self):
        """Make PDF fill the available space at a readable size with proper portrait aspect ratio"""
        if not self.pdf_document or not hasattr(self, 'scroll_area'):
            print("DEBUG: Cannot fit PDF - missing document or scroll area")
            return
            
        try:
            # Get current page dimensions
            page = self.pdf_document[self.current_page]
            page_rect = page.rect
            
            print(f"DEBUG: PDF page size: {page_rect.width}x{page_rect.height} points")
            print(f"DEBUG: PDF aspect ratio: {page_rect.width/page_rect.height:.3f} (should be < 1.0 for portrait)")
            
            # Get available space in the scroll area
            available_width = self.scroll_area.width() - 60  # More margin for scrollbars
            available_height = self.scroll_area.height() - 60
            
            print(f"DEBUG: Available space: {available_width}x{available_height} pixels")
            
            # Calculate zoom to fit PDF properly - prioritize fitting width for portrait docs
            width_zoom = available_width / page_rect.width
            height_zoom = available_height / page_rect.height
            
            # For portrait PDFs, usually width is the limiting factor
            # Use width-based zoom but cap it to ensure height fits too
            if page_rect.height > page_rect.width:  # Portrait PDF
                zoom_factor = min(width_zoom, height_zoom)
                print("DEBUG: Portrait PDF detected - using optimal fit")
            else:  # Landscape or square PDF
                zoom_factor = min(width_zoom, height_zoom)
                print("DEBUG: Landscape/square PDF detected")
            
            # Ensure reasonable zoom range for readability
            zoom_factor = max(1.0, min(3.0, zoom_factor))  # Between 100% and 300%
            
            print(f"DEBUG: Calculated zoom factor: {zoom_factor:.2f}")
            
            # Apply the zoom
            self.zoom_level = zoom_factor
            zoom_percentage = int(zoom_factor * 100)
            self.zoom_slider.setValue(zoom_percentage)
            
            # Render at the new zoom level
            self.render_page()
            
            # Remove any fixed sizing constraints that prevent natural fitting
            self.scroll_area.setMaximumSize(16777215, 16777215)
            self.pdf_widget.setMaximumSize(16777215, 16777215)
            
            # Let the PDF label size itself to its content
            self.pdf_label.adjustSize()
            
            print(f"DEBUG: Perfect Fit applied at {zoom_percentage}% zoom")
            print("DEBUG: PDF should now display with proper portrait aspect ratio!")
            
        except Exception as e:
            print(f"Error fitting PDF to window: {e}")
            import traceback
            traceback.print_exc()
    
    def on_paper_ratio_changed(self):
        """Handle paper ratio selection change"""
        # Remove size constraints for new ratio
        self.remove_size_constraints()
        # Auto-fit when ratio changes
        if self.pdf_document:
            QTimer.singleShot(100, self.fit_pdf_to_window)

class EnhancedTrainingInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocMiner 6.1.0 - Professional Positionality Analysis Interface")
        # Set reasonable default size but allow user to resize freely
        self.resize(1200, 800)  # Default size - user can resize by dragging corners
        self.setMinimumSize(900, 600)  # Minimum usable size
        
        # Training data storage
        self.training_data = []
        self.current_paper_index = 0
        self.papers_list = []
        self.pdf_folder = ""
        
        # Paper state persistence - stores content for each paper
        self.paper_states = {}  # filename -> {human_text, ai_text, decision, uploaded}
        
        # Default folder in user's home directory
        self.default_pdf_folder = Path.home() / "ExtractorPDFs" 
        self.readme_pdf_path = self.default_pdf_folder / "aboutDM.pdf"
        
        # Settings file in user's config directory (works with AppImage)
        config_dir = Path.home() / ".docminer"
        config_dir.mkdir(parents=True, exist_ok=True)
        self.settings_file = config_dir / "ui_settings.json"
        
        # Initialize without loading any local training data
        # Each session starts fresh - decisions go directly to GitHub
        self.training_data = []
        self.load_settings()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Initialize GitHub uploader with configuration
        self.github_uploader = GitHubReportUploader()
        
        self.setup_ui()
        
        # Check network connectivity and update button states
        self.update_button_states()
        
        # Initialize with default folder and README
        self.initialize_with_readme()
        
        # Check if configuration is needed BEFORE showing the window
        # This prevents the main window from being visible during setup
        self._needs_initial_config = self.check_if_config_needed()
        
        # Use QTimer to handle first-time setup after event loop starts
        # If config is needed, window will stay hidden until config is complete
        QTimer.singleShot(100, self.handle_first_time_setup)
        
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('📁 File')
        
        # Configuration action
        config_action = file_menu.addAction('⚙️ Configuration...')
        config_action.triggered.connect(self.show_configuration)
        config_action.setStatusTip('Configure API keys and GitHub repository settings')
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = file_menu.addAction('❌ Exit')
        exit_action.triggered.connect(self.close)
        exit_action.setStatusTip('Exit DocMiner')
        
        # Help menu
        help_menu = menubar.addMenu('❓ Help')
        
        about_action = help_menu.addAction('📖 About DocMiner...')
        about_action.triggered.connect(self.show_about)
        about_action.setStatusTip('About DocMiner')
        
        help_menu.addSeparator()
        
        usage_action = help_menu.addAction('💡 Quick Help')
        usage_action.triggered.connect(self.show_quick_help)
        usage_action.setStatusTip('Quick help and FAQ')
        
    def check_if_config_needed(self):
        """Check if configuration is needed (returns True if config missing)"""
        from configuration_dialog import load_configuration
        
        config = load_configuration()
        
        # Check if critical settings are missing
        if not config.get("openai_api_key"):
            return True
        if not config.get("github_token"):
            return True
        if not (self.github_uploader.owner and self.github_uploader.repo):
            return True
            
        return False
    
    def handle_first_time_setup(self):
        """Handle first-time setup - shows config dialog and hides main window if needed"""
        if self._needs_initial_config:
            # Hide main window during initial configuration
            self.hide()
            
            from configuration_dialog import load_configuration
            config = load_configuration()
            
            missing_items = []
            if not config.get("openai_api_key"):
                missing_items.append("OpenAI API Key")
            if not config.get("github_token"):
                missing_items.append("GitHub Token")
            if not (self.github_uploader.owner and self.github_uploader.repo):
                missing_items.append("GitHub Repository")
            
            missing_text = ", ".join(missing_items)
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Configuration Required")
            msg.setText(f"⚙️ Configuration Setup Required\n\nMissing: {missing_text}")
            msg.setInformativeText(
                "DocMiner requires configuration before use.\n\n"
                "You'll need:\n"
                "• OpenAI API Key (for AI analysis)\n"
                "• GitHub Personal Access Token (for uploading reports)\n"
                "• GitHub Repository settings\n\n"
                "The configuration dialog will open now."
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            
            # Show configuration dialog - it's modal so it blocks
            self.show_configuration()
            
            # After configuration, show the main window
            self.show()
    
    def check_first_time_setup(self):
        """Deprecated - replaced by handle_first_time_setup"""
        pass
    
    def show_configuration(self):
        """Show the configuration dialog"""
        dialog = ConfigurationDialog(self)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            # Refresh GitHub uploader with new configuration
            self.github_uploader = GitHubReportUploader()
            
            # Update status indicators
            self.update_status_indicators()
            
            # Update button tooltips with new repository info
            self.update_button_states()
            
            # Update status bar with new repository info
            # Show upload destination in status bar if configured
            if hasattr(self.github_uploader, 'owner') and hasattr(self.github_uploader, 'repo'):
                if self.github_uploader.owner and self.github_uploader.repo:
                    repo_info = f"📦 Uploads to: {self.github_uploader.owner}/{self.github_uploader.repo}"
                else:
                    repo_info = "📦 Upload destination not configured"
            else:
                repo_info = "📦 Upload destination not configured"
            current_status = self.statusBar().currentMessage()
            if "📦 Uploads to:" in current_status:
                # Replace the repository part
                base_message = current_status.split("📦 Uploads to:")[0].strip()
                self.statusBar().showMessage(f"{base_message} {repo_info}")
            else:
                self.statusBar().showMessage(f"{current_status} {repo_info}")
        elif self._needs_initial_config:
            # User cancelled during initial setup - can't use app without config
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Configuration Required")
            msg.setText("⚠️ Configuration Required")
            msg.setInformativeText(
                "DocMiner cannot function without proper configuration.\n\n"
                "The application will now exit.\n\n"
                "Please run the application again and complete the configuration."
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            
            # Exit the application
            QApplication.quit()
    
    def show_quick_help(self):
        """Show quick help dialog answering common questions"""
        help_text = """
<h3>💡 Quick Help & FAQ</h3>

<p><b>Q: What does the AI analyze?</b><br>
A: The AI automatically reads and analyzes the <b>entire document</b> - every page, 
every paragraph. It doesn't just look at what you type in "Human Input".</p>

<p><b>Q: What should I put in "Human Input"?</b><br>
A: Use "Human Input" to record <b>your own manual findings</b> - specific quotes, 
page numbers, or observations you want to highlight. This is for YOUR evidence 
collection, separate from the AI's automatic analysis.</p>

<p><b>Q: Where can I find training data?</b><br>
A: Current folder: <b>{folder}</b><br>
The default training folder contains sample PDFs. Use "File → Configuration" to 
change the folder location. PDFs are located in the "ExtractorPDFs" folder.</p>

<p><b>Q: My PDF doesn't fit in the window properly</b><br>
A: Use the new <b>View mode</b> dropdown (Letter/A4/Full Width/Full Height) and 
<b>Zoom controls</b> (up to 200%) to adjust how the PDF displays. 
The "Selected Text" box below the PDF is collapsible - uncheck it to get more space.</p>

<p><b>Q: How do I collect evidence?</b><br>
1. Select text in the PDF viewer<br>
2. Text appears in "Selected Text" box (check the box if hidden)<br>
3. Click "Copy to Evidence →" button<br>
4. Evidence appears in "Human Input" tab</p>
        """.format(
            folder=Path(self.current_folder).name if hasattr(self, 'current_folder') else "Not loaded yet"
        )
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Quick Help")
        msg.setTextFormat(Qt.RichText)
        msg.setText(help_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setIcon(QMessageBox.Information)
        msg.exec()
    
    def toggle_layout_mode(self, mode):
        """Toggle between PDF-only, Split, and Analysis-only layouts (Overleaf-style)"""
        if mode == "pdf_only":
            # Show only PDF panel
            self.pdf_panel.setVisible(True)
            self.analysis_panel.setVisible(False)
            
        elif mode == "analysis_only":
            # Show only Analysis panel
            self.pdf_panel.setVisible(False)
            self.analysis_panel.setVisible(True)
            
        elif mode == "split":
            # Show both panels (default)
            self.pdf_panel.setVisible(True)
            self.analysis_panel.setVisible(True)
    

    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About DocMiner 6.1.0", 
                         "🎓 DocMiner 6.1.0\n\n"
                         "Professional Positionality Analysis Interface\n\n"
                         "Features:\n"
                         "• Paper state persistence\n"
                         "• Visual progress indicators\n"
                         "• Configurable GitHub uploads\n"
                         "• Professional positionality analysis\n"
                         "• PDF viewer with text selection\n"
                         "• AI-assisted and manual analysis modes\n\n"
                         "Built for Graduate Assistants and Research Teams\n\n"
                         "📦 GitHub Repository:\n"
                         "https://github.com/OhioMathTeacher/docminer\n\n"
                         "📜 License:\n"
                         "Creative Commons Attribution-NonCommercial 4.0\n"
                         "Academic and educational use freely permitted.\n"
                         "Contact copyright holder for commercial use.\n\n"
                         "© 2025 Michael Todd Edwards (OhioMathTeacher)\n"
                         "DocMiner Project")
        
    def setup_ui(self):
        """Create the enhanced training interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Header with progress
        header_layout = QHBoxLayout()
        
        # GA name input
        ga_label = QLabel("GA Name:")
        self.ga_name_input = QLineEdit()
        self.ga_name_input.setPlaceholderText("Enter your name for training reports")
        self.ga_name_input.setMaximumWidth(200)
        header_layout.addWidget(ga_label)
        header_layout.addWidget(self.ga_name_input)
        
        # Folder selection
        folder_btn = QPushButton("📁 Select PDF Folder")
        folder_btn.clicked.connect(self.select_folder)
        folder_btn.setStyleSheet("QPushButton { font-weight: bold; padding: 8px; }")
        header_layout.addWidget(folder_btn)
        
        # Spacer to push layout controls and Robbie to the right
        header_layout.addStretch()
        
        # Layout toggle buttons (Overleaf-style) - positioned left of Robbie
        layout_label = QLabel("Layout:")
        layout_label.setStyleSheet("QLabel { font-weight: bold; margin-right: 5px; }")
        header_layout.addWidget(layout_label)
        
        self.layout_btn_group = QButtonGroup()
        self.layout_btn_group.setExclusive(True)
        
        self.layout_pdf_only = QPushButton("📄 PDF")
        self.layout_pdf_only.setCheckable(True)
        self.layout_pdf_only.setToolTip("Show PDF viewer only - reading mode (Ctrl+1)")
        self.layout_pdf_only.setStyleSheet("QPushButton { padding: 6px 12px; } QPushButton:checked { background-color: #2196F3; color: white; font-weight: bold; }")
        self.layout_btn_group.addButton(self.layout_pdf_only, 1)
        header_layout.addWidget(self.layout_pdf_only)
        
        self.layout_split = QPushButton("🔀 Split")
        self.layout_split.setCheckable(True)
        self.layout_split.setChecked(True)  # Default
        self.layout_split.setToolTip("Show both PDF and Analysis panels - default mode (Ctrl+2)")
        self.layout_split.setStyleSheet("QPushButton { padding: 6px 12px; } QPushButton:checked { background-color: #2196F3; color: white; font-weight: bold; }")
        self.layout_btn_group.addButton(self.layout_split, 2)
        header_layout.addWidget(self.layout_split)
        
        self.layout_analysis_only = QPushButton("✏️ Analysis")
        self.layout_analysis_only.setCheckable(True)
        self.layout_analysis_only.setToolTip("Show Analysis panel only - writing mode (Ctrl+3)")
        self.layout_analysis_only.setStyleSheet("QPushButton { padding: 6px 12px; } QPushButton:checked { background-color: #2196F3; color: white; font-weight: bold; }")
        self.layout_btn_group.addButton(self.layout_analysis_only, 3)
        header_layout.addWidget(self.layout_analysis_only)
        
        # Connect layout toggle signals
        self.layout_pdf_only.clicked.connect(lambda: self.toggle_layout_mode("pdf_only"))
        self.layout_split.clicked.connect(lambda: self.toggle_layout_mode("split"))
        self.layout_analysis_only.clicked.connect(lambda: self.toggle_layout_mode("analysis_only"))
        
        header_layout.addWidget(QLabel("|"))  # Separator before Robbie
        
        # Animated Robbie processing indicator (animated GIF - always visible)
        self.processing_indicator = QLabel("")
        self.processing_indicator.setMinimumSize(60, 60)  # Reserve space
        self.processing_indicator.setMaximumSize(60, 60)  # Limit size
        self.processing_indicator.setScaledContents(True)  # Scale GIF to fit
        self.processing_indicator.setAlignment(Qt.AlignCenter)  # Center the GIF
        self.processing_indicator.setVisible(True)  # Always visible
        header_layout.addWidget(self.processing_indicator)
        
        # Load Robbie animated GIF
        from PySide6.QtGui import QMovie
        from PySide6.QtCore import QSize
        
        # Check if running as frozen exe (PyInstaller bundle)
        if getattr(sys, 'frozen', False):
            robbie_path = os.path.join(sys._MEIPASS, 'images', 'robbie_slow.gif')
        else:
            robbie_path = os.path.join(os.path.dirname(__file__), 'images', 'robbie_slow.gif')
        
        if os.path.exists(robbie_path):
            self.robbie_movie = QMovie(robbie_path)
            self.robbie_movie.setScaledSize(QSize(60, 60))  # Scale to fit
            self.processing_indicator.setMovie(self.robbie_movie)
            # DON'T start animation - will start when AI analysis begins
            print(f"DEBUG: Loaded animated Robbie GIF from {robbie_path}")
        else:
            print(f"Warning: Robbie GIF not found at {robbie_path}")
            self.robbie_movie = None
            self.processing_indicator.setText("🤖")  # Fallback emoji
        
        layout.addLayout(header_layout)
        
        # Main content area with fixed horizontal layout (NO splitter for stability)
        self.main_content = QHBoxLayout()
        self.main_content.setSpacing(4)
        self.main_content.setContentsMargins(0, 0, 0, 0)
        
        # Left panel: PDF Viewer - fixed width for coordinate stability
        self.pdf_panel = QGroupBox("PDF Document Viewer")
        self.pdf_panel.setFixedWidth(700)  # Fixed width for stable text selection coordinates
        pdf_layout = QVBoxLayout(self.pdf_panel)
        
        # Paper info + status dot
        paper_info_layout = QHBoxLayout()
        paper_info_layout.setContentsMargins(0, 0, 0, 0)
        paper_info_layout.setSpacing(8)

        self.paper_info = QLabel("No paper selected")
        self.paper_info.setFont(QFont("Courier New", 11, QFont.Bold))
        self.paper_info.setStyleSheet("QLabel { padding: 4px; background: white; border: 1px solid #666666; color: black; }")
        paper_info_layout.addWidget(self.paper_info, 1)

        # Small colored status dot: red/yellow/green depending on paper state
        self.pdf_status_dot = QLabel("")
        self.pdf_status_dot.setFixedSize(12, 12)
        self.pdf_status_dot.setStyleSheet("QLabel { background-color: #d32f2f; border-radius: 6px; border: 1px solid #aaa; }")
        self.pdf_status_dot.setToolTip("Paper status")
        paper_info_layout.addWidget(self.pdf_status_dot)

        pdf_layout.addLayout(paper_info_layout)
        
        # Note about PDF functionality
        pdf_note = QLabel("� PDF displays with zoom and text selection built-in")
        pdf_note.setStyleSheet("QLabel { color: #666; font-style: italic; padding: 5px; }")
        pdf_layout.addWidget(pdf_note)
        
        # PDF viewer - use embedded system viewer
        self.pdf_viewer = EmbeddedPDFViewer(parent_window=self)
        
        # Connect text selection signal from PDF viewer to main interface
        self.pdf_viewer.pdf_label.text_selected.connect(self.on_text_selected)
        
        pdf_layout.addWidget(self.pdf_viewer)
        
        # Simple tip about text selection workflow
        selection_tip = QLabel("💡 Select text in PDF → Automatically added to Human Input tab")
        selection_tip.setStyleSheet("QLabel { color: #666; font-size: 10px; font-style: italic; padding: 5px; background: #f0f8ff; border-radius: 3px; }")
        selection_tip.setWordWrap(True)
        pdf_layout.addWidget(selection_tip)
        
        # Add PDF panel to fixed layout
        self.main_content.addWidget(self.pdf_panel)
        
        # Right panel: Training interface - expands to fill remaining space
        self.analysis_panel = QGroupBox("Evidence")
        self.analysis_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout = QVBoxLayout(self.analysis_panel)
        right_layout.setContentsMargins(2, 2, 2, 2)  # Minimal margins
        right_layout.setSpacing(1)  # Very tight spacing
        
        # AI Pre-screening section
        prescreening_group = QGroupBox("AI Pre-screening Analysis")
        prescreening_layout = QVBoxLayout(prescreening_group)
        prescreening_layout.setContentsMargins(2, 2, 2, 2)  # Minimal margins
        prescreening_layout.setSpacing(1)  # Very tight spacing
        
        # Initial analysis button
        analysis_btn_layout = QHBoxLayout()
        self.initial_analysis_btn = QPushButton("🚀 Run AI Analysis")
        self.initial_analysis_btn.clicked.connect(self.run_initial_analysis)
        analysis_btn_layout.addWidget(self.initial_analysis_btn)
        analysis_btn_layout.addStretch()  # Make button wider by removing text and adding stretch
        prescreening_layout.addLayout(analysis_btn_layout)
        
        # Progress bar for AI analysis
        self.analysis_progress = QProgressBar()
        self.analysis_progress.setMaximum(100)
        self.analysis_progress.setVisible(False)  # Hidden by default
        self.analysis_progress.setTextVisible(True)
        prescreening_layout.addWidget(self.analysis_progress)
        
        right_layout.addWidget(prescreening_group)
        
        # Simplified location - integrated into other controls below to save space
        
        # Positionality judgment
        judgment_group = QGroupBox("Does this paper contain positionality statements?")
        judgment_layout = QVBoxLayout(judgment_group)
        judgment_layout.setContentsMargins(1, 1, 1, 1)  # Minimal margins
        judgment_layout.setSpacing(1)  # Very tight spacing
        
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
            btn.setStyleSheet("QRadioButton { font-size: 11px; padding: 4px; }")
            self.judgment_buttons[value] = btn
            self.judgment_group.addButton(btn)
            judgment_layout.addWidget(btn)
            
        right_layout.addWidget(judgment_group)
        
        # Evidence collection (simplified to two tabs)
        self.evidence_tabs = QTabWidget()
        # Fix tab label truncation - ensure tabs expand to fit text
        self.evidence_tabs.tabBar().setExpanding(True)
        self.evidence_tabs.setTabBarAutoHide(False)
        self.evidence_tabs.tabBar().setUsesScrollButtons(False)
        
        # Human Input tab (editable)
        human_tab = QWidget()
        human_layout = QVBoxLayout(human_tab)
        human_layout.setContentsMargins(2, 2, 2, 2)
        
        # Add helpful info label
        human_info = QLabel("📝 Manual Evidence Collection - Enter quotes/citations you manually identified:")
        human_info.setStyleSheet("QLabel { color: #1976D2; font-size: 10px; font-weight: bold; padding: 3px; background-color: #E3F2FD; border-radius: 3px; }")
        human_info.setWordWrap(True)
        human_info.setToolTip(
            "This field is for YOUR manual evidence collection.\n\n"
            "The AI analyzes the ENTIRE document automatically, not just what you put here.\n"
            "Use this field to record specific quotes, page numbers, or notes that you want to highlight."
        )
        human_layout.addWidget(human_info)
        
        self.human_input = QTextEdit()
        self.human_input.setMinimumHeight(200)
        self.human_input.setFont(QFont("Arial", 13))  # Increased from 12
        self.human_input.setPlaceholderText("Enter evidence quotes and analysis here...")
        self.human_input.setStyleSheet("QTextEdit { margin: 0px; padding: 2px; border: 1px solid #ddd; }")
        human_layout.addWidget(self.human_input)
        
        self.evidence_tabs.addTab(human_tab, "Human Input")
        
        # AI Input tab (editable)  
        ai_tab = QWidget()
        ai_layout = QVBoxLayout(ai_tab)
        ai_layout.setContentsMargins(2, 2, 2, 2)
        
        # Add helpful info label
        ai_info = QLabel("🤖 AI Automatic Analysis - The AI reads and analyzes the ENTIRE document:")
        ai_info.setStyleSheet("QLabel { color: #388E3C; font-size: 10px; font-weight: bold; padding: 3px; background-color: #E8F5E9; border-radius: 3px; }")
        ai_info.setWordWrap(True)
        ai_info.setToolTip(
            "The AI automatically processes the complete document text.\n\n"
            "This analysis is independent of what you enter in 'Human Input'.\n"
            "The AI scans the full paper to identify positionality statements, patterns, and context."
        )
        ai_layout.addWidget(ai_info)
        
        self.ai_input = QTextEdit()
        self.ai_input.setMinimumHeight(200)
        self.ai_input.setFont(QFont("Arial", 13))  # Increased from 11
        self.ai_input.setPlaceholderText("AI analysis results will appear here...")
        self.ai_input.setStyleSheet("QTextEdit { margin: 0px; padding: 2px; border: 1px solid #ddd; }")
        # Enable HTML rendering
        self.ai_input.setAcceptRichText(True)
        ai_layout.addWidget(self.ai_input)
        
        self.evidence_tabs.addTab(ai_tab, "AI Input")

        # Clear button for active evidence tab
        clear_evidence_btn = QPushButton("🗑️ Clear Current Tab")
        clear_evidence_btn.setStyleSheet("QPushButton { background-color: #607D8B; color: white; padding: 8px; font-weight: bold; font-size: 11px; } QPushButton:hover { background-color: #546E7A; }")
        clear_evidence_btn.clicked.connect(self.clear_current_evidence_tab)
        clear_evidence_btn.setToolTip("Clear all text from the currently active tab (Human Input or AI Input)")
        right_layout.addWidget(clear_evidence_btn)

        right_layout.addWidget(self.evidence_tabs)

        # Update paper status when human/AI input changes
        # (connect here because widgets have been created)
        try:
            self.human_input.textChanged.connect(self.update_current_paper_status)
            self.ai_input.textChanged.connect(self.update_current_paper_status)
        except Exception:
            pass
        
        # Add analysis panel to layout - it expands to fill remaining space
        self.main_content.addWidget(self.analysis_panel)
        
        # Add the fixed layout to main layout
        layout.addLayout(self.main_content)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        prev_btn = QPushButton("◀ Previous Paper")
        prev_btn.clicked.connect(self.previous_paper)
        button_layout.addWidget(prev_btn)
        
        skip_btn = QPushButton("⏭️ Next Paper")
        skip_btn.clicked.connect(self.next_paper)
        button_layout.addWidget(skip_btn)
        
        # Paper position counter (e.g., "3 of 12")
        self.paper_position = QLabel("")
        self.paper_position.setStyleSheet("QLabel { color: #333; font-weight: bold; margin-left: 10px; }")
        button_layout.addWidget(self.paper_position)
        
        button_layout.addStretch()
        
        # Progress info
        self.papers_completed = QLabel("0 papers labeled")
        self.papers_completed.setStyleSheet("QLabel { color: #666; font-style: italic; }")
        button_layout.addWidget(self.papers_completed)
        
        export_btn = QPushButton("� Export Evidence")
        export_btn.clicked.connect(self.export_evidence)
        button_layout.addWidget(export_btn)
        
        self.upload_btn = QPushButton("🚀 Upload Decision")
        self.upload_btn.clicked.connect(self.upload_decision)
        self.upload_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        button_layout.addWidget(self.upload_btn)
        
        layout.addLayout(button_layout)
        
        # Setup keyboard shortcuts for layout modes
        self.setup_keyboard_shortcuts()
        
        # Create permanent status bar widgets with clickable indicators
        self.create_status_bar_widgets()
        
        # Initial status message
        self.update_status_indicators()
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for quick layout switching"""
        from PySide6.QtGui import QShortcut, QKeySequence
        
        # Ctrl+1: PDF only mode
        shortcut_pdf = QShortcut(QKeySequence("Ctrl+1"), self)
        shortcut_pdf.activated.connect(lambda: [self.layout_pdf_only.setChecked(True), self.toggle_layout_mode("pdf_only")])
        
        # Ctrl+2: Split mode (default)
        shortcut_split = QShortcut(QKeySequence("Ctrl+2"), self)
        shortcut_split.activated.connect(lambda: [self.layout_split.setChecked(True), self.toggle_layout_mode("split")])
        
        # Ctrl+3: Analysis only mode
        shortcut_analysis = QShortcut(QKeySequence("Ctrl+3"), self)
        shortcut_analysis.activated.connect(lambda: [self.layout_analysis_only.setChecked(True), self.toggle_layout_mode("analysis_only")])
        
    def create_status_bar_widgets(self):
        """Create clickable status indicators in the status bar"""
        from PySide6.QtWidgets import QLabel
        from PySide6.QtCore import Qt
        
        # API Key Status (clickable)
        self.api_status_label = QLabel()
        self.api_status_label.setStyleSheet("QLabel { padding: 2px 8px; } QLabel:hover { background-color: #e0e0e0; cursor: pointer; }")
        self.api_status_label.mousePressEvent = lambda e: self.on_api_status_clicked()
        self.api_status_label.setToolTip("Click to configure API key")
        
        # GitHub Status (clickable)
        self.github_status_label = QLabel()
        self.github_status_label.setStyleSheet("QLabel { padding: 2px 8px; } QLabel:hover { background-color: #e0e0e0; cursor: pointer; }")
        self.github_status_label.mousePressEvent = lambda e: self.on_github_status_clicked()
        self.github_status_label.setToolTip("Click to configure GitHub")
        
        # Add to status bar (permanent widgets)
        self.statusBar().addPermanentWidget(self.api_status_label)
        self.statusBar().addPermanentWidget(self.github_status_label)
        
    def on_api_status_clicked(self):
        """Handle click on API status - open config if missing"""
        from configuration_dialog import load_configuration
        config = load_configuration()
        
        if not config.get("openai_api_key"):
            # Missing - show info and open config
            QMessageBox.information(self, "API Key Required", 
                                   "🔑 No API key configured.\n\n"
                                   "Opening configuration to set up your API key...")
            self.show_configuration()
        else:
            # Configured - just show details
            key_preview = config["openai_api_key"][:15] + "..."
            provider = "OpenRouter" if config["openai_api_key"].startswith("sk-or-") else "OpenAI"
            QMessageBox.information(self, "API Key Configured", 
                                   f"✅ {provider} API key is configured\n\n"
                                   f"Key: {key_preview}\n\n"
                                   "Click Configuration menu to change.")
    
    def on_github_status_clicked(self):
        """Handle click on GitHub status - open config if missing"""
        if not (self.github_uploader.owner and self.github_uploader.repo):
            # Missing - show info and open config
            QMessageBox.information(self, "GitHub Required", 
                                   "📦 GitHub not configured.\n\n"
                                   "Opening configuration to set up GitHub uploads...")
            self.show_configuration()
        else:
            # Configured - show details
            QMessageBox.information(self, "GitHub Configured", 
                                   f"✅ GitHub uploads configured\n\n"
                                   f"Owner: {self.github_uploader.owner}\n"
                                   f"Repo: {self.github_uploader.repo}\n\n"
                                   "Click Configuration menu to change.")
    
    def update_status_indicators(self):
        """Update the status bar indicators"""
        from configuration_dialog import load_configuration
        config = load_configuration()
        
        # API Key Status
        if config.get("openai_api_key"):
            provider = "OpenRouter" if config["openai_api_key"].startswith("sk-or-") else "OpenAI"
            self.api_status_label.setText(f"🔑 {provider} ✅")
            self.api_status_label.setStyleSheet("QLabel { color: #2e7d32; font-weight: bold; padding: 2px 8px; } QLabel:hover { background-color: #e0e0e0; cursor: pointer; }")
            self.api_status_label.setToolTip(f"{provider} API key configured - click for details")
        else:
            self.api_status_label.setText("🔑 API Key ❌")
            self.api_status_label.setStyleSheet("QLabel { color: #d32f2f; font-weight: bold; padding: 2px 8px; } QLabel:hover { background-color: #ffebee; cursor: pointer; }")
            self.api_status_label.setToolTip("⚠️ No API key - CLICK HERE to configure")
        
        # GitHub Status
        if self.github_uploader.owner and self.github_uploader.repo:
            self.github_status_label.setText(f"📦 GitHub ✅")
            self.github_status_label.setStyleSheet("QLabel { color: #2e7d32; font-weight: bold; padding: 2px 8px; } QLabel:hover { background-color: #e0e0e0; cursor: pointer; }")
            self.github_status_label.setToolTip(f"Uploads to {self.github_uploader.owner}/{self.github_uploader.repo} - click for details")
        else:
            self.github_status_label.setText("📦 GitHub ❌")
            self.github_status_label.setStyleSheet("QLabel { color: #d32f2f; font-weight: bold; padding: 2px 8px; } QLabel:hover { background-color: #ffebee; cursor: pointer; }")
            self.github_status_label.setToolTip("⚠️ GitHub not configured - CLICK HERE to set up")
        
        # Update main status message
        status_msg = "Ready to analyze papers"
        if self.papers_list:
            status_msg = f"Loaded {len(self.papers_list)} papers - Ready to analyze"
        self.statusBar().showMessage(status_msg)
        
    def select_folder(self):
        """Select folder containing PDFs to train on"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select PDF Folder", 
            str(self.default_pdf_folder)  # Start from default folder
        )
        if folder:
            self.pdf_folder = folder
            self.load_folder(folder)
            self.save_settings()  # Remember the new folder choice
            
    def load_folder(self, folder_path):
        """Load PDFs from specified folder"""
        try:
            self.papers_list = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
            self.papers_list.sort()  # Sort alphabetically for consistency
            self.current_paper_index = 0
            self.update_progress()
            if self.papers_list:
                self.load_current_paper()
                self.statusBar().showMessage(f"Loaded {len(self.papers_list)} papers from {Path(folder_path).name}")
            else:
                self.statusBar().showMessage(f"📁 No PDF files found in {Path(folder_path).name}")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading folder: {e}")
            
    def update_progress(self):
        """Update the processed papers counter at bottom of window"""
        if not self.papers_list:
            self.papers_completed.setText("0 papers labeled")
            return
            
        # Count processed papers
        processed_count = 0
        for filename in self.papers_list:
            if filename in self.paper_states and self.paper_states[filename].get('uploaded', False):
                processed_count += 1
        
        total = len(self.papers_list)
        self.papers_completed.setText(f"{processed_count} of {total} papers processed")
        # Also refresh the current paper status dot
        try:
            self.update_current_paper_status()
        except Exception:
            pass
        
    def update_processing_animation(self):
        """No-op: Robbie GIF animates itself automatically"""
        # The animated GIF plays continuously, no manual frame updates needed
        pass
        
    def open_pdf_externally(self):
        """Open the current PDF in the system's default PDF viewer"""
        if not self.papers_list or self.current_paper_index >= len(self.papers_list):
            QMessageBox.information(self, "No PDF", "No PDF is currently loaded.")
            return
            
        filename = self.papers_list[self.current_paper_index]
        filepath = os.path.join(self.pdf_folder, filename)
        
        if not os.path.exists(filepath):
            QMessageBox.critical(self, "File Not Found", f"PDF file not found: {filepath}")
            return
            
        success = open_pdf_with_system_viewer(filepath)
        if success:
            self.statusBar().showMessage(f"Opened {filename} in system PDF viewer", 3000)
        else:
            QMessageBox.critical(self, "Error", f"Could not open PDF with system viewer: {filename}")
        
    def load_current_paper(self):
        """Load and display the current paper"""
        if not self.papers_list or self.current_paper_index >= len(self.papers_list):
            return
            
        filename = self.papers_list[self.current_paper_index]
        filepath = os.path.join(self.pdf_folder, filename)
        
        # Update paper info (just filename, no counter)
        self.paper_info.setText(f"📄 {filename}")
        
        # Update position counter at bottom
        current_index = self.current_paper_index + 1  # 1-based for display
        total_papers = len(self.papers_list)
        self.paper_position.setText(f"{current_index} of {total_papers}")
        
        # Load PDF in embedded viewer
        success = self.pdf_viewer.load_pdf(filepath)
        if not success:
            return
        
        # NOTE: Removed automatic AI analysis here - it blocks the UI thread!
        # Users should click "Run AI Analysis" button to run analysis asynchronously
        
        # Clear previous inputs ONLY if no saved state exists
        # This preserves user's work when navigating back to a paper
        if filename not in self.paper_states or not any([
            self.paper_states[filename].get('human_text'),
            self.paper_states[filename].get('ai_text'),
            self.paper_states[filename].get('decision')
        ]):
            self.clear_inputs()
        
        # Load saved state for this paper (if it exists)
        self.load_current_paper_state()
        
        self.statusBar().showMessage(f"Loaded: {filename} ({current_index}/{total_papers}) - Text selection available in PDF viewer", 3000)
        # Update status dot for the newly loaded paper
        try:
            self.update_current_paper_status()
        except Exception:
            pass
        
    def clear_inputs(self):
        """Clear all input fields"""
        for btn in self.judgment_buttons.values():
            btn.setChecked(False)
        self.human_input.clear()
        self.ai_input.clear()
        
    def save_and_next(self):
        """Save current training data and move to next paper"""
        if self.save_current_training():
            self.next_paper()
        
    def save_current_training(self):
        """Save training data for current paper"""
        if not self.papers_list:
            return False
            
        filename = self.papers_list[self.current_paper_index]
        
        # Get judgment
        judgment = None
        for key, btn in self.judgment_buttons.items():
            if btn.isChecked():
                judgment = key
                break
                
        if not judgment:
            QMessageBox.warning(self, "Decision Required", "Please select a judgment option before making your decision.")
            return False
        
        # Create simplified training entry with available data
        entry = {
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
            "judgment": judgment,
            "evidence": self.human_input.toPlainText().strip(),
            "ai_analysis": self.ai_input.toPlainText().strip(),
            "pattern_types": [],  # Simplified - no pattern checkboxes in current interface
            "confidence": 3,  # Default confidence
            "explanation": "",  # No explanation field in current interface
            "pattern_suggestions": "",  # No pattern suggestions in current interface
        }
        
        # Remove existing entry for this file if present
        self.training_data = [d for d in self.training_data if d["filename"] != filename]
        
        # Add new entry to session data only (no local file persistence)
        self.training_data.append(entry)
        
        # Update progress display
        self.update_progress()
        
        self.statusBar().showMessage(f"Saved decision data for {Path(filename).name}")
        return True
        
    def next_paper(self):
        """Move to next paper"""
        # Save current paper state before moving
        self.save_current_paper_state()
        
        if self.current_paper_index < len(self.papers_list) - 1:
            self.current_paper_index += 1
            self.update_progress()
            self.load_current_paper()
            # Load saved state for new paper
            self.load_current_paper_state()
        else:
            QMessageBox.information(self, "🎉 Complete!", 
                                  f"All {len(self.papers_list)} papers have been reviewed!\n\n"
                                  f"Total decisions made: {len(self.training_data)} papers\n\n"
                                  f"Use 'Upload Decision' to upload your final analysis to GitHub.")
            
    def previous_paper(self):
        """Move to previous paper"""
        # Save current paper state before moving
        self.save_current_paper_state()
        
        if self.current_paper_index > 0:
            self.current_paper_index -= 1
            self.update_progress()
            self.load_current_paper()
            # Load saved state for new paper
            self.load_current_paper_state()
            
    # Note: Local training data persistence removed - decisions go directly to GitHub
    # This keeps the interface clean and prevents stale local data issues
    
    def check_network_connectivity(self):
        """Check if we have internet connectivity for GitHub upload"""
        import socket
        try:
            # Try to connect to GitHub
            socket.create_connection(("github.com", 443), timeout=3)
            return True
        except (socket.timeout, socket.error):
            return False
    
    def check_network_and_update_buttons(self):
        """Update button states and tooltips based on connectivity and configuration"""
        has_network = self.check_network_connectivity()
        has_token = bool(self.github_uploader.token)
        has_repo_config = bool(self.github_uploader.owner and self.github_uploader.repo)
        
        # Always keep upload button enabled so users can click for helpful feedback
        self.upload_btn.setEnabled(True)
        
        if has_network and has_token and has_repo_config:
            # Full functionality available
            repo_url = f"https://github.com/{self.github_uploader.owner}/{self.github_uploader.repo}"
            self.upload_btn.setToolTip(f"✅ Ready to upload your decision to:\n{repo_url}")
            self.upload_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        elif not has_token:
            # Missing GitHub token
            self.upload_btn.setToolTip("🔐 Click for GitHub token setup instructions")
            self.upload_btn.setStyleSheet("QPushButton { background-color: #FFA500; color: white; font-weight: bold; }")
        elif not has_network:
            # No internet connection
            self.upload_btn.setToolTip("🌐 No internet connection - click for more info")
            self.upload_btn.setStyleSheet("QPushButton { background-color: #888; color: #ccc; font-weight: bold; }")
        elif not has_repo_config:
            # Repository not configured
            self.upload_btn.setToolTip("📂 Repository not configured - click for setup info")
            self.upload_btn.setStyleSheet("QPushButton { background-color: #FF6B6B; color: white; font-weight: bold; }")
        else:
            # Default state
            self.upload_btn.setToolTip("Click to upload your decision")
            self.upload_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
            
    def check_ai_configuration_and_update_button(self):
        """Update AI analysis button based on API key configuration"""
        try:
            from configuration_dialog import load_configuration
            config = load_configuration()
            api_key = config.get('openai_api_key', '').strip()
            has_api_key = bool(api_key)
        except Exception:
            has_api_key = False
        
        if has_api_key:
            # API key configured - ready to use
            self.initial_analysis_btn.setToolTip("✅ Run AI analysis on current paper")
            self.initial_analysis_btn.setStyleSheet("QPushButton { background-color: #333333; color: white; font-weight: bold; padding: 6px; font-family: 'Courier New', monospace; }")
        else:
            # No API key - show helpful styling
            self.initial_analysis_btn.setToolTip("🔑 Click for OpenAI API key setup instructions")
            self.initial_analysis_btn.setStyleSheet("QPushButton { background-color: #FFA500; color: white; font-weight: bold; padding: 6px; font-family: 'Courier New', monospace; }")
    
    def update_button_states(self):
        """Update all button states based on current configuration"""
        self.check_network_and_update_buttons()
        self.check_ai_configuration_and_update_button()
            
    def export_evidence(self):
        """Export current evidence (AI + Human) to text file next to PDF"""
        if not hasattr(self, 'current_paper_index') or self.current_paper_index >= len(self.papers_list):
            QMessageBox.information(self, "No Paper", "No paper currently loaded to export evidence from.")
            return
            
        # Get current evidence
        human_evidence = self.human_input.toPlainText().strip()
        ai_evidence = self.ai_input.toPlainText().strip()
        
        if not human_evidence and not ai_evidence:
            QMessageBox.information(self, "No Evidence", "No evidence collected to export.")
            return
            
        # Get current PDF file path and create evidence file path
        current_pdf_path = Path(self.papers_list[self.current_paper_index])
        evidence_filename = current_pdf_path.stem + "_EVIDENCE.txt"
        evidence_path = current_pdf_path.parent / evidence_filename
        
        try:
            # Create evidence content
            content = f"EVIDENCE EXPORT\n"
            content += f"PDF File: {current_pdf_path.name}\n"
            content += f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += f"{'='*50}\n\n"
            
            if human_evidence:
                content += f"HUMAN EVIDENCE:\n"
                content += f"{'-'*20}\n"
                content += f"{human_evidence}\n\n"
            
            if ai_evidence:
                content += f"AI ANALYSIS:\n"
                content += f"{'-'*20}\n"
                content += f"{ai_evidence}\n\n"
            
            # Write to file
            with open(evidence_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            QMessageBox.information(self, "Export Successful", 
                                  f"Evidence exported successfully!\n\n"
                                  f"File: {evidence_filename}\n"
                                  f"Saved in same folder as PDF")
                                  
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Could not export evidence: {e}")

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
                QMessageBox.information(self, "Exported", 
                                      f"Training data exported to {filename}\n\n"
                                      f"Papers labeled: {len(self.training_data)}\n"
                                      f"Use training_analysis.py to analyze the results.")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Could not export: {e}")
                
    def upload_decision(self):
        """Upload final decision to GitHub (requires internet connection)"""
        
        # Check for GitHub token first and provide helpful feedback
        if not self.github_uploader.token:
            QMessageBox.information(self, "GitHub Setup Required", 
                                  "🔐 GitHub token not found!\n\n"
                                  "To upload decisions to GitHub, you need to:\n\n"
                                  "1. Create a GitHub Personal Access Token:\n"
                                  "   • Go to github.com → Settings → Developer settings → Personal access tokens\n"
                                  "   • Generate new token (classic) with 'repo' scope\n\n"
                                  "2. Set the environment variable:\n"
                                  "   export RESEARCH_BUDDY_GITHUB_TOKEN=\"your_token_here\"\n\n"
                                  "3. Restart the application\n\n"
                                  "💡 For now, use 'Export Evidence' to save your work locally!")
            return
        
        # Check network connectivity
        if not self.check_network_connectivity():
            QMessageBox.warning(self, "No Internet Connection", 
                              "🌐 No internet connection detected!\n\n"
                              "Upload to GitHub requires an internet connection.\n\n"
                              "💡 Use 'Export Evidence' to save your work locally until connection is restored.")
            return
        
        # Check GitHub repository configuration
        if not (self.github_uploader.owner and self.github_uploader.repo):
            QMessageBox.warning(self, "GitHub Repository Not Configured", 
                              "📂 GitHub repository not configured!\n\n"
                              "Please configure your GitHub repository settings:\n"
                              "• Owner: Your GitHub username\n"
                              "• Repository: Your repository name\n\n"
                              "💡 Use 'Export Evidence' to save locally for now.")
            return
        
        # First, try to save current state if there's an active paper
        if hasattr(self, 'current_paper_index') and self.current_paper_index < len(self.papers_list):
            current_filename = self.papers_list[self.current_paper_index]
            
            # Check if user has made any selections for current paper
            judgment_selected = any(btn.isChecked() for btn in self.judgment_buttons.values())
            evidence_text = self.human_input.toPlainText().strip()
            
            if judgment_selected or evidence_text:
                # Auto-save current paper's data
                saved = self.save_current_training()
                if not saved:
                    return  # User was warned about missing data, let them fix it
        
        # Now check if we have any training data at all
        if not self.training_data:
            # Check if there's at least some evidence in the interface
            evidence_text = self.human_input.toPlainText().strip()
            ai_analysis = self.ai_input.toPlainText().strip()
            
            if evidence_text or ai_analysis:
                QMessageBox.information(self, "Decision Required", 
                                      "Please select a judgment option (radio button) before uploading your decision.\n\nAlternatively, use 'Export Evidence' to save your work locally.")
                return
            else:
                QMessageBox.information(self, "No Decision", "No evidence collected to upload.\n\nCollect evidence first, then make a decision.")
                return
            
        ga_name = self.ga_name_input.text().strip()
        if not ga_name:
            QMessageBox.warning(self, "GA Name Required", "Please enter your name before recording your decision.")
            self.ga_name_input.setFocus()
            return
        
        print(f"DEBUG: GA Name from input field: '{ga_name}'")  # Debug logging
            
        try:
            # Process training session (save locally + upload to GitHub)
            result = self.github_uploader.process_training_session(self.training_data, ga_name)
            print(f"DEBUG: Uploader result: {result}")  # Debug logging
            
            if result['success']:
                # Mark current paper as uploaded
                if hasattr(self, 'current_paper_index') and self.current_paper_index < len(self.papers_list):
                    current_filename = self.papers_list[self.current_paper_index]
                    self.mark_paper_uploaded(current_filename)
                
                QMessageBox.information(self, "Decision Recorded", 
                                      f"Your decision has been successfully recorded and uploaded!\n\n"
                                      f"GA: {ga_name}\n"
                                      f"Session: {result['session_id']}\n"
                                      f"Papers analyzed: {len(self.training_data)}\n\n"
                                      f"Decision files created:\n"
                                      f"• {Path(result['json_file']).name}\n"
                                      f"• {Path(result['md_file']).name}\n\n"
                                      f"📦 Uploaded to Repository:\n"
                                      f"https://github.com/{self.github_uploader.owner}/{self.github_uploader.repo}\n\n"
                                      f"Your decision is now available on GitHub for review.")
            else:
                QMessageBox.warning(self, "Upload Failed", 
                                  f"Decision recorded locally but GitHub upload failed.\n\n"
                                  f"Error: {result['message']}\n\n"
                                  f"Decision files saved locally:\n"
                                  f"• {Path(result['json_file']).name}\n"
                                  f"• {Path(result['md_file']).name}")
                
        except Exception as e:
            QMessageBox.critical(self, "Decision Error", f"Could not record or upload decision: {e}")
                

        
    def initialize_with_readme(self):
        """Initialize with default ExtractorPDFs folder and show README first"""
        # Ensure default folder exists
        self.default_pdf_folder.mkdir(exist_ok=True)
        
        # Copy README PDF to default folder if it doesn't exist
        self.ensure_readme_exists()
        
        # Only use default folder if no folder was restored from settings
        if not self.pdf_folder or self.pdf_folder == str(self.default_pdf_folder):
            # Set default folder as current folder
            self.pdf_folder = str(self.default_pdf_folder)
            
            # Load PDFs from default folder (including README)
            self.load_folder(self.pdf_folder)
            
            # Find and display README first if available
            readme_index = self.find_readme_index()
            if readme_index >= 0:
                self.current_paper_index = readme_index
                self.load_current_paper()
                self.statusBar().showMessage("📖 Welcome! Reading the Getting Started guide. Add your PDFs to ExtractorPDFs folder.", 5000)
            else:
                # No README found, show first PDF or empty state
                if self.papers_list:
                    self.current_paper_index = 0
                    self.load_current_paper()
                    self.statusBar().showMessage(f"Loaded {len(self.papers_list)} PDFs from ExtractorPDFs folder", 3000)
                else:
                    self.statusBar().showMessage("📁 Add PDF files to your ~/ExtractorPDFs folder to begin training", 5000)
        else:
            # Folder was restored from settings - load it and restore position
            if os.path.exists(self.pdf_folder):
                self.load_folder(self.pdf_folder)
                # current_paper_index was already restored by load_settings
                if self.papers_list and self.current_paper_index < len(self.papers_list):
                    self.load_current_paper()
                    self.statusBar().showMessage(f"Restored session: {len(self.papers_list)} PDFs from {Path(self.pdf_folder).name}", 3000)
                else:
                    self.statusBar().showMessage(f"Restored folder: {Path(self.pdf_folder).name}", 3000)
            else:
                # Saved folder doesn't exist anymore - fall back to default
                self.pdf_folder = str(self.default_pdf_folder)
                self.load_folder(self.pdf_folder)
                self.statusBar().showMessage("Previous folder not found. Loaded default folder.", 3000)
    
    def ensure_readme_exists(self):
        """Ensure the README PDF exists in the default folder"""
        # Remove old about.pdf if it exists (legacy cleanup)
        old_readme = self.default_pdf_folder / "about.pdf"
        if old_readme.exists():
            try:
                old_readme.unlink()
                print(f"Removed legacy about.pdf")
            except:
                pass
        
        # Always copy fresh aboutDM.pdf from bundle to ensure latest version
        if not self.readme_pdf_path.exists():
            # Try to find bundled aboutDM.pdf in multiple locations
            possible_sources = [
                # PyInstaller .app bundle location
                Path(sys._MEIPASS) / "sample_pdfs" / "aboutDM.pdf" if getattr(sys, 'frozen', False) else None,
                # Development location
                Path(__file__).parent / "sample_pdfs" / "aboutDM.pdf",
            ]
            
            source_readme = None
            for source in possible_sources:
                if source and source.exists():
                    source_readme = source
                    break
            
            if source_readme:
                import shutil
                shutil.copy2(source_readme, self.readme_pdf_path)
                print(f"Copied DocMiner training guide to {self.readme_pdf_path}")
            else:
                # Create README if it doesn't exist
                try:
                    from utils.create_readme_pdf import create_readme_pdf
                    create_readme_pdf(self.readme_pdf_path)
                    print(f"Created README at {self.readme_pdf_path}")
                except:
                    print(f"Could not create README - aboutDM.pdf not found in bundle")
    
    def find_readme_index(self):
        """Find the index of the aboutDM.pdf file in papers list"""
        for i, paper in enumerate(self.papers_list):
            if "aboutdm.pdf" in paper.lower() or "about.pdf" in paper.lower():
                return i
        return -1
    
    def load_settings(self):
        """Load UI settings from file (window geometry, folder, progress)"""
        # Migration: Check for old config file
        old_config_path = Path.home() / ".research_buddy" / "interface_settings.json"
        if not self.settings_file.exists() and old_config_path.exists():
            try:
                with open(old_config_path, 'r') as f:
                    old_settings = json.load(f)
                    # Extract only UI settings (not credentials)
                    self.pdf_folder = old_settings.get("pdf_folder", str(self.default_pdf_folder))
                    # Restore window geometry and paper states if present
                    window_geometry = old_settings.get("window_geometry")
                    if window_geometry:
                        self.setGeometry(
                            window_geometry.get("x", 100),
                            window_geometry.get("y", 100),
                            window_geometry.get("width", 1200),
                            window_geometry.get("height", 800)
                        )
                    if "paper_states" in old_settings:
                        self.paper_states = old_settings["paper_states"]
                    if "current_paper_index" in old_settings:
                        self.current_paper_index = old_settings["current_paper_index"]
                print("Migrated UI settings from old config file")
                return
            except Exception as e:
                print(f"Error migrating UI settings: {e}")
        
        # Load from new UI settings file
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.pdf_folder = settings.get("pdf_folder", str(self.default_pdf_folder))
                    
                    # Restore window geometry
                    window_geometry = settings.get("window_geometry")
                    if window_geometry:
                        self.setGeometry(
                            window_geometry.get("x", 100),
                            window_geometry.get("y", 100),
                            window_geometry.get("width", 1200),
                            window_geometry.get("height", 800)
                        )
                    
                    # Restore paper states and current index
                    if "paper_states" in settings:
                        self.paper_states = settings["paper_states"]
                    if "current_paper_index" in settings:
                        self.current_paper_index = settings["current_paper_index"]
                    
                    # Note: PDF highlights no longer persisted - text capture is sufficient
        except Exception as e:
            print(f"Could not load settings: {e}")
            self.pdf_folder = str(self.default_pdf_folder)

    def save_settings(self):
        """Save UI settings to file (window geometry, folder, progress)"""
        try:
            # Get current window geometry
            geometry = self.geometry()
            
            settings = {
                "pdf_folder": self.pdf_folder,
                "window_geometry": {
                    "x": geometry.x(),
                    "y": geometry.y(),
                    "width": geometry.width(),
                    "height": geometry.height()
                },
                "current_paper_index": self.current_paper_index,
                "paper_states": self.paper_states,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            # Set file permissions to user-only (600)
            os.chmod(self.settings_file, 0o600)
        except Exception as e:
            print(f"Could not save settings: {e}")

    def on_text_selected(self, selected_text):
        """Handle text selection from PDF viewer - directly append to Human Input and add PDF highlight"""
        print(f"DEBUG - on_text_selected called with: '{selected_text[:100] if selected_text else 'EMPTY'}'")
        if selected_text.strip():
            # Add real PDF highlight annotation (if method exists and PDF is loaded)
            if hasattr(self.pdf_viewer, 'add_highlight_annotation') and self.pdf_viewer.pdf_document:
                self.pdf_viewer.add_highlight_annotation(selected_text)
            
            # Clean up the text
            text = clean_extracted_text(selected_text)
            
            # Prepend page number from PDF viewer's current page
            page_number = self.pdf_viewer.current_page + 1  # +1 for 1-based numbering
            text = f"[Page {page_number}]\n{text}"
            
            # Append to Human Input tab
            current_evidence = self.human_input.toPlainText().strip()
            if current_evidence:
                new_evidence = current_evidence + "\n\n" + text
            else:
                new_evidence = text
            self.human_input.setPlainText(new_evidence)
            
            # Automatically switch to Human Input tab so user sees the result
            self.evidence_tabs.setCurrentIndex(0)  # Human Input is index 0
            
            # Show confirmation
            self.statusBar().showMessage("✅ Text highlighted and added to Human Input", 2000)
            print(f"DEBUG - Text added to Human Input tab with highlight")
    
    def clear_current_evidence_tab(self):
        """Clear the currently active evidence tab (Human Input or AI Input)"""
        current_index = self.evidence_tabs.currentIndex()
        
        if current_index == 0:  # Human Input tab
            if self.human_input.toPlainText().strip():
                reply = QMessageBox.question(
                    self, 
                    "Clear Human Input",
                    "Are you sure you want to clear all Human Input text?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.human_input.clear()
                    self.statusBar().showMessage("✅ Human Input cleared", 2000)
        elif current_index == 1:  # AI Input tab
            if self.ai_input.toPlainText().strip():
                reply = QMessageBox.question(
                    self, 
                    "Clear AI Input",
                    "Are you sure you want to clear all AI Input text?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.ai_input.clear()
                    self.statusBar().showMessage("✅ AI Input cleared", 2000)
    
    def run_initial_analysis(self):
        """Run AI analysis on current paper and display findings asynchronously"""
        if not self.papers_list or self.current_paper_index >= len(self.papers_list):
            QMessageBox.information(self, "No Paper", "No paper selected for analysis.")
            return

        # Check for OpenAI API key first and provide helpful feedback
        try:
            from configuration_dialog import load_configuration
            config = load_configuration()
            api_key = config.get('openai_api_key', '').strip()

            if not api_key:
                QMessageBox.information(self, "OpenAI Setup Required", 
                                      "🔑 OpenAI API key not found!\n\n"
                                      "To use AI-powered analysis, you need to:\n\n"
                                      "1. Get an OpenAI API Key:\n"
                                      "   • Visit platform.openai.com/account/api-keys\n"
                                      "   • Create a new API key\n\n"
                                      "2. Configure in DocMiner:\n"
                                      "   • Use menu: Configuration → Settings\n"
                                      "   • Enter your API key\n\n"
                                      "💡 You can still analyze papers manually using the PDF viewer!\n"
                                      "Just select text and use the Human Input tab.")
                return
        except Exception as e:
            print(f"Could not check API key configuration: {e}")

        current_paper = self.papers_list[self.current_paper_index]
        pdf_path = Path(self.pdf_folder) / current_paper

        # Show progress bar and update status
        self.analysis_progress.setVisible(True)
        self.analysis_progress.setValue(0)
        
        # Start Robbie animation during processing
        if hasattr(self, 'robbie_movie') and self.robbie_movie:
            self.robbie_movie.start()
        
        self.statusBar().showMessage("🔄 Starting analysis...")
        self.initial_analysis_btn.setEnabled(False)
        QApplication.processEvents()  # Update UI

        # Run analysis in a background thread using QThread
        class AnalysisWorker(QThread):
            finished_signal = Signal(dict, str)
            error_signal = Signal(Exception)
            progress_signal = Signal(int, str)  # progress value, status message

            def __init__(self, pdf_path, paper_name):
                super().__init__()
                self.pdf_path = pdf_path
                self.paper_name = paper_name

            def run(self):
                try:
                    self.progress_signal.emit(10, "📄 Loading PDF file...")
                    
                    # Define progress callback
                    def progress_cb(pct, msg):
                        self.progress_signal.emit(pct, msg)
                    
                    # Call with progress callback
                    result = extract_positionality(str(self.pdf_path), progress_callback=progress_cb)
                    
                    self.progress_signal.emit(100, "✅ Analysis complete!")
                    self.finished_signal.emit(result, self.paper_name)
                except Exception as e:
                    self.error_signal.emit(e)

        def on_progress_update(value, message):
            self.analysis_progress.setValue(value)
            self.statusBar().showMessage(message)
            QApplication.processEvents()

        def on_analysis_finished(result, paper_name):
            # Stop Robbie animation
            if hasattr(self, 'robbie_movie') and self.robbie_movie:
                self.robbie_movie.stop()
                self.robbie_movie.jumpToFrame(0)  # Reset to first frame
            
            self.analysis_progress.setVisible(False)
            findings_text = self.format_ai_findings(result, paper_name)
            self.ai_input.setHtml(findings_text)
            self.evidence_tabs.setCurrentIndex(1)
            if result['positionality_score'] > 0.3:
                self.statusBar().showMessage(f"✅ Found {len(result['positionality_snippets'])} potential evidence excerpts", 5000)
                self.current_ai_findings = result
            else:
                self.statusBar().showMessage("✅ No strong positionality indicators found", 5000)
                self.current_ai_findings = None
            self.initial_analysis_btn.setEnabled(True)

        def on_analysis_error(e):
            # Stop Robbie animation
            if hasattr(self, 'robbie_movie') and self.robbie_movie:
                self.robbie_movie.stop()
                self.robbie_movie.jumpToFrame(0)  # Reset to first frame
            
            self.analysis_progress.setVisible(False)
            error_msg = str(e).lower()
            if ("401" in error_msg and "unauthorized" in error_msg) or \
               "invalid_api_key" in error_msg or \
               "authentication" in error_msg or \
               "incorrect api key" in error_msg:
                QMessageBox.warning(self, "API Key Error", 
                                  "🔑 OpenAI API Key Error!\n\n"
                                  "Your API key appears to be invalid or expired.\n\n"
                                  "Please check:\n"
                                  "• API key is correctly entered in Configuration → Settings\n"
                                  "• API key has sufficient credits\n"
                                  "• API key is not expired\n\n"
                                  "💡 You can still analyze papers manually!")
                self.statusBar().showMessage("AI analysis requires valid OpenAI API key - use Configuration menu")
                self.ai_input.setHtml("""
                <b><font color="#FF9800">🔑 AI Analysis Requires Setup</font></b><br><br>
                <p>To use AI-powered analysis, you need to configure an OpenAI API key:</p>
                <ol>
                <li><b>Get an API Key:</b> Visit <a href=\"https://platform.openai.com/account/api-keys\">platform.openai.com/account/api-keys</a></li>
                <li><b>Configure in DocMiner:</b> Use the menu: <b>Configuration → Settings</b></li>
                <li><b>Alternative:</b> You can still analyze papers manually using the PDF viewer and Human Input tab</li>
                </ol>
                <p><b>Manual Analysis:</b><br>
                • Read the PDF carefully<br>
                • Look for first-person statements about the author's background, position, or bias<br>
                • Select text in the PDF to copy quotes as evidence<br>
                • Make your judgment using the radio buttons</p>
                <p><i>DocMiner works great for manual analysis even without AI!</i></p>
                """)
            else:
                self.statusBar().showMessage(f"❌ Analysis failed: {str(e)}")
                self.ai_input.setPlainText(f"Error running analysis: {e}")
            self.initial_analysis_btn.setEnabled(True)

        # Create and start worker thread
        self.analysis_worker = AnalysisWorker(pdf_path, current_paper)
        self.analysis_worker.finished_signal.connect(on_analysis_finished)
        self.analysis_worker.error_signal.connect(on_analysis_error)
        self.analysis_worker.progress_signal.connect(on_progress_update)
        self.analysis_worker.start()
    
    def format_ai_findings(self, result, paper_name):
        """Format AI detection results as clean, professional plain text"""
        score = result['positionality_score']
        patterns = result['positionality_tests']
        snippets = result['positionality_snippets']
        
        # Determine confidence level and recommendation
        if score >= 0.7:
            confidence_level = "High"
            recommendation = "Explicit positionality detected"
        elif score >= 0.4:
            confidence_level = "Medium"
            recommendation = "Subtle/implicit positionality likely"
        elif score > 0:
            confidence_level = "Low"
            recommendation = "Minimal indicators found"
        else:
            confidence_level = "None"
            recommendation = "No positionality detected"
        
        # Create clean plain text with rich formatting
        text = f"""<b><font color="#2196F3">AI Analysis for {paper_name}</font></b><br><br>

<b>Confidence Level:</b> <font color="#FF9800">{confidence_level}</font> ({score:.3f})<br>
<b>Recommendation:</b> {recommendation}<br>
<b>Patterns Detected:</b> {', '.join(patterns).replace('_', ' ').title() if patterns else 'None'}<br><br><br>"""
        
        if snippets:
            text += "<b><font color=\"#4CAF50\">Evidence Excerpts Found:</font></b>\n\n"
            for i, (pattern, excerpt) in enumerate(snippets.items(), 1):
                # Clean up text: remove extra spaces, quotes, and format properly
                clean_text = clean_extracted_text(excerpt)
                
                # Intelligently truncate if too long
                if len(clean_text) > 300:
                    # Find a good breaking point (sentence end)
                    truncate_pos = clean_text.find('.', 250)
                    if truncate_pos == -1:
                        truncate_pos = 300
                    clean_text = clean_text[:truncate_pos + 1] + "..."
                
                # Estimate location based on content
                location = self.estimate_location_from_text(clean_text)
                
                # Display without redundant quotes (text is already clearly shown as a quote)
                text += f"""<b>#{i} - {pattern.replace('_', ' ').title()}</b><br>
<i>Likely Location: {location}</i><br>
{clean_text}<br><br><br>"""
        else:
            text += "<i><font color=\"#856404\">No specific evidence excerpts extracted. Consider manual review of the full paper.</font></i><br><br>"
        
        # Add AI recommendation summary
        text += "<br><b><font color=\"#2e7d32\">AI Recommendation:</font></b><br>"
        
        if score >= 0.7:
            text += "Strong evidence of explicit positionality statements. Recommend categorizing as Explicit."
        elif score >= 0.4:
            text += "Moderate evidence suggests subtle reflexivity. Recommend categorizing as Subtle/Implicit."
        elif score > 0:
            text += "Weak indicators found. Recommend manual review for thorough analysis."
        else:
            text += "No clear positionality detected. Recommend categorizing as No positionality statements."
            
        return text
    
    def estimate_location_from_text(self, text):
        """Estimate paper location based on text content"""
        text_lower = text.lower()
        
        # Location indicators
        if any(word in text_lower for word in ['introduction', 'background', 'this paper', 'this study']):
            return "Introduction/Background"
        elif any(word in text_lower for word in ['literature', 'previous research', 'scholars have']):
            return "Literature Review"
        elif any(word in text_lower for word in ['methodology', 'method', 'approach', 'data collection', 'participants']):
            return "Methodology"
        elif any(word in text_lower for word in ['findings', 'results', 'analysis revealed', 'data showed']):
            return "Results/Findings"
        elif any(word in text_lower for word in ['discussion', 'implications', 'these findings']):
            return "Discussion"
        elif any(word in text_lower for word in ['conclusion', 'in summary', 'to conclude']):
            return "Conclusion"
        else:
            return "Body/Content"
    
    def quick_accept_findings(self):
        """Quickly accept AI findings and populate form"""
        if not hasattr(self, 'current_ai_findings') or not self.current_ai_findings:
            return
            
        result = self.current_ai_findings
        
        # Let user make their own judgment decision - no auto-selection
        # AI results are shown in the AI Input tab for reference
        
        # Populate evidence from AI findings and determine locations
        evidence_parts = []
        locations_found = []
        
        for pattern, text in result['positionality_snippets'].items():
            clean_text = text.strip()
            evidence_parts.append(f"[{pattern.replace('_', ' ').title()}]: \"{clean_text}\"")
            
            # Estimate location for each piece of evidence
            location = self.estimate_location_from_text(clean_text)
            locations_found.append(location)
        
        self.evidence_text.setPlainText("\n\n".join(evidence_parts))
        
        # Auto-select location based on evidence analysis
        if locations_found:
            from collections import Counter
            location_counts = Counter(locations_found)
            
            # Determine primary location
            if len(set(locations_found)) > 2:
                primary_location = "Multiple Sections"
            elif len(set(locations_found)) == 2:
                primary_location = "Multiple Sections"
            else:
                primary_location = location_counts.most_common(1)[0][0]
                
            # Set the location dropdown
            location_index = self.location_dropdown.findText(primary_location)
            if location_index >= 0:
                self.location_dropdown.setCurrentIndex(location_index)
        
        # AI confidence and pattern information is now shown in AI Input tab
        # No separate confidence slider or pattern suggestions in simplified interface
        
        # Switch to AI Input tab to show the results
        self.evidence_tabs.setCurrentIndex(1)  # Switch to AI Input tab
        
        location_text = self.location_dropdown.currentText()
        self.statusBar().showMessage(f"AI findings accepted! Location: {location_text}", 3000)
        
    def quick_reject_findings(self):
        """Reject AI findings and proceed with manual review"""
        # Clear AI findings and reset for manual work
        self.ai_input.clear()
        self.statusBar().showMessage("Manual review mode")
        
        # Let user make their own judgment - no default selection
        
        self.statusBar().showMessage("Manual review mode - read the full paper carefully", 3000)
    
    def save_current_paper_state(self):
        """Save the current paper's content to paper_states"""
        if not self.papers_list or self.current_paper_index >= len(self.papers_list):
            return
            
        filename = self.papers_list[self.current_paper_index]
        
        # Get current content from UI
        human_text = self.human_input.toPlainText().strip()
        ai_text = self.ai_input.toPlainText().strip()
        
        # Get current decision from radio buttons (using actual judgment_buttons)
        decision = None
        for key, btn in self.judgment_buttons.items():
            if btn.isChecked():
                decision = key
                break
        
        # Save to paper_states (preserve uploaded flag if it exists)
        if filename not in self.paper_states:
            self.paper_states[filename] = {}
        
        # Preserve uploaded status when updating state
        uploaded_status = self.paper_states[filename].get('uploaded', False)
        
        self.paper_states[filename].update({
            'human_text': human_text,
            'ai_text': ai_text,
            'decision': decision,
            'uploaded': uploaded_status  # Preserve uploaded flag
        })
        
        # Persist to disk immediately for safety
        self.save_settings()
        
        # Refresh status dot when state is saved
        self.update_current_paper_status()
    
    def load_current_paper_state(self):
        """Load the saved state for current paper"""
        if not self.papers_list or self.current_paper_index >= len(self.papers_list):
            return
            
        filename = self.papers_list[self.current_paper_index]
        
        if filename in self.paper_states:
            state = self.paper_states[filename]
            
            # Restore text content
            self.human_input.setPlainText(state.get('human_text', ''))
            self.ai_input.setPlainText(state.get('ai_text', ''))
            
            # Restore decision radio buttons (using actual judgment_buttons)
            decision = state.get('decision')
            
            # Clear all buttons first
            for btn in self.judgment_buttons.values():
                btn.setChecked(False)
            
            # Set the correct button if decision exists
            if decision and decision in self.judgment_buttons:
                self.judgment_buttons[decision].setChecked(True)
        else:
            # Clear content for new paper
            self.human_input.clear()
            self.ai_input.clear()
            
            # Clear radio button selections
            for btn in self.judgment_buttons.values():
                btn.setChecked(False)
        
        # Update status dot to reflect loaded state
        self.update_current_paper_status()
    
    def mark_paper_uploaded(self, filename):
        """Mark a paper as uploaded/processed"""
        if filename not in self.paper_states:
            self.paper_states[filename] = {}
        
        self.paper_states[filename]['uploaded'] = True
        self.update_progress()  # Refresh the status indicators
        # Update the current paper status dot as it's been uploaded
        self.update_current_paper_status()

    def get_current_paper_status(self):
        """Compute current paper status: 'green' (submitted), 'yellow' (partial), 'red' (none)"""
        # Default to red (no analysis)
        status = 'red'

        if not self.papers_list or self.current_paper_index >= len(self.papers_list):
            return status

        filename = self.papers_list[self.current_paper_index]

        # If uploaded marker present -> green
        state = self.paper_states.get(filename, {})
        if state.get('uploaded'):
            return 'green'

        # Check for any human or AI evidence or judgment
        human = state.get('human_text', '') or self.human_input.toPlainText().strip()
        ai = state.get('ai_text', '') or self.ai_input.toPlainText().strip()

        # If there's evidence or partial data -> yellow
        if human or ai:
            return 'yellow'

        # Otherwise no data -> red
        return 'red'

    def update_current_paper_status(self):
        """Update the small colored dot reflecting current paper status"""
        try:
            color_map = {'green': '#2e7d32', 'yellow': '#f9a825', 'red': '#d32f2f'}
            status = self.get_current_paper_status()
            color = color_map.get(status, '#d32f2f')
            self.pdf_status_dot.setStyleSheet(f"QLabel {{ background-color: {color}; border-radius: 6px; border: 1px solid #aaa; }}")
            tip_map = {
                'green': 'Submitted — uploaded to GitHub',
                'yellow': 'Partial — evidence or AI analysis entered but not submitted',
                'red': 'No analysis yet — no human or AI evidence'
            }
            self.pdf_status_dot.setToolTip(tip_map.get(status, 'No analysis yet'))
        except Exception as e:
            print(f"Could not update paper status dot: {e}")
    
    def closeEvent(self, event):
        """Save settings when closing"""
        self.save_settings()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Force light theme with custom palette
    from PySide6.QtGui import QPalette, QColor
    palette = QPalette()
    
    # Window and base colors (light grey background)
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(0, 0, 255))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)
    
    window = EnhancedTrainingInterface()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()