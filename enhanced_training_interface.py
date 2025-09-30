#!/usr/bin/env python3
"""
Enhanced Training Interface with PDF Viewer

This version includes a proper PDF renderer that displays pages as images,
making it much easier to read and annotate papers for training data collection.
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
from PySide6.QtCore import Qt, QTimer, Signal, QRect, QPoint, QUrl
from PySide6.QtGui import QFont, QTextCursor, QPixmap, QPainter, QPen, QColor, QBrush, QAction, QClipboard
from PySide6.QtWebEngineWidgets import QWebEngineView

import fitz  # PyMuPDF for PDF rendering
from metadata_extractor import extract_positionality
from github_report_uploader import GitHubReportUploader
from configuration_dialog import ConfigurationDialog
from first_run_setup import FirstRunSetupDialog, check_first_run

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
    text_selected = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.text_blocks = []
        self.text_lines = []  # Text organized by lines for proper selection
        self.selected_text = ""
        self.selection_start = None
        self.selection_end = None
        self.selection_rect = None
        self.selecting = False
        self.highlighted_lines = []  # Lines that should be highlighted
        
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
        """Start text selection with line-based behavior"""
        if event.button() == Qt.LeftButton:
            self.selection_start = event.position().toPoint()
            self.selecting = True
            self.selected_text = ""
            self.highlighted_lines = []
            print(f"DEBUG - Selection started at {self.selection_start}")
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """Update selection with real-time line highlighting"""
        if self.selecting and self.selection_start:
            self.selection_end = event.position().toPoint()
            self.update_line_selection()
            self.update()  # Trigger immediate repaint for visual feedback
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """Finish selection and emit selected text"""
        if event.button() == Qt.LeftButton and self.selecting:
            self.selection_end = event.position().toPoint()
            self.selecting = False
            self.update_line_selection()
            
            # Emit the final selected text
            if self.selected_text.strip():
                self.text_selected.emit(self.selected_text.strip())
                print(f"DEBUG - Final selection: '{self.selected_text[:100]}...'")
            else:
                self.text_selected.emit("")
                
        super().mouseReleaseEvent(event)
        
    def update_line_selection(self):
        """Update selection using line-based text editor behavior"""
        if not self.selection_start or not self.selection_end or not self.text_lines:
            self.selected_text = ""
            self.highlighted_lines = []
            return
            
        # Create selection rectangle
        self.selection_rect = QRect(self.selection_start, self.selection_end).normalized()
        
        # Find lines that intersect with selection rectangle
        selected_lines = []
        self.highlighted_lines = []
        
        for i, line in enumerate(self.text_lines):
            line_bbox = line['bbox']
            line_rect = QRect(
                int(line_bbox[0]), int(line_bbox[1]),
                int(line_bbox[2] - line_bbox[0]), 
                int(line_bbox[3] - line_bbox[1])
            )
            
            # Check if selection intersects with this line
            if self.selection_rect.intersects(line_rect):
                # Determine selection type within the line
                start_y = self.selection_rect.top()
                end_y = self.selection_rect.bottom()
                line_center_y = (line_bbox[1] + line_bbox[3]) / 2
                
                # If selection spans multiple lines or covers significant portion of line,
                # select entire line for text editor behavior
                selection_height = abs(self.selection_rect.height())
                line_height = line_bbox[3] - line_bbox[1]
                
                if (selection_height > line_height * 1.5 or  # Multi-line selection
                    self.selection_rect.width() > (line_bbox[2] - line_bbox[0]) * 0.8):  # Wide selection
                    
                    # Select entire line
                    selected_lines.append(line['text'])
                    self.highlighted_lines.append({
                        'rect': QRect(
                            int(line_bbox[0]),  # Start at actual text position
                            int(line_bbox[1]),
                            int(line_bbox[2] - line_bbox[0]),  # Width of actual text
                            int(line_bbox[3] - line_bbox[1])
                        ),
                        'line_index': i
                    })
                else:
                    # Partial line selection - select words within the selection area
                    selected_words = []
                    for block in line['blocks']:
                        block_bbox = block['bbox']
                        block_rect = QRect(
                            int(block_bbox[0]), int(block_bbox[1]),
                            int(block_bbox[2] - block_bbox[0]),
                            int(block_bbox[3] - block_bbox[1])
                        )
                        
                        if self.selection_rect.intersects(block_rect):
                            selected_words.append(block['text'])
                    
                    if selected_words:
                        partial_text = ' '.join(selected_words)
                        selected_lines.append(partial_text)
                        
                        # Highlight only the selected portion
                        self.highlighted_lines.append({
                            'rect': self.selection_rect.intersected(line_rect),
                            'line_index': i
                        })
        
        # Join selected text from all lines
        self.selected_text = '\n'.join(selected_lines) if selected_lines else ""
        
        # Debug output (less verbose during dragging)
        if not self.selecting:  # Only detailed debug when selection is complete
            print(f"DEBUG - Line selection complete: {len(selected_lines)} lines selected")
            print(f"DEBUG - Selected text: '{self.selected_text[:100]}...'")
            print(f"DEBUG - Highlighted {len(self.highlighted_lines)} line regions")
        
    def paintEvent(self, event):
        """Custom paint to show line-based selection highlighting"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        
        # Draw selection highlights for completed selections
        if self.highlighted_lines:
            painter.setBrush(QBrush(QColor(49, 106, 197, 100)))  # Text editor blue highlight
            painter.setPen(QPen(QColor(49, 106, 197, 150), 1))
            
            for highlight in self.highlighted_lines:
                painter.drawRect(highlight['rect'])
        
        # Draw real-time selection rectangle while dragging
        if self.selecting and self.selection_start and self.selection_end:
            painter.setBrush(QBrush(QColor(49, 106, 197, 60)))  # Lighter during selection
            painter.setPen(QPen(QColor(49, 106, 197), 2, Qt.DashLine))
            
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
    
    def __init__(self):
        super().__init__()
        self.current_pdf_path = None
        self.pdf_width = 612  # Standard letter width
        self.pdf_height = 792  # Standard letter height
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        
        # Controls - make them smaller
        controls = QHBoxLayout()
        
        self.pdf_info = QLabel("No PDF loaded")
        self.pdf_info.setAlignment(Qt.AlignCenter)
        self.pdf_info.setStyleSheet("QLabel { font-weight: bold; font-size: 10px; }")
        self.pdf_info.setMaximumHeight(20)
        controls.addWidget(self.pdf_info)
        
        # Add zoom control
        zoom_label = QLabel("Zoom:")
        zoom_label.setStyleSheet("QLabel { font-size: 9px; }")
        controls.addWidget(zoom_label)
        
        self.zoom_combo = QComboBox()
        self.zoom_combo.addItems([
            "Fit Width", "Fit Page", "100%", "125%", "150%", "80%", "65%", "50%"
        ])
        self.zoom_combo.setCurrentText("Fit Width")
        self.zoom_combo.setMaximumWidth(100)
        self.zoom_combo.setStyleSheet("QComboBox { font-size: 9px; padding: 2px; }")
        self.zoom_combo.currentTextChanged.connect(self.change_zoom)
        controls.addWidget(self.zoom_combo)
        
        controls.addStretch()
        
        layout.addLayout(controls)
        
        # Always use PyMuPDF for reliable aspect ratio control
        self.setup_pdf_viewer(layout)
        
    def setup_pdf_viewer(self, layout):
        """Setup PDF viewer using PyMuPDF with proper aspect ratio"""
        # Scrollable area with better space utilization
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.scroll_area.setStyleSheet("QScrollArea { border: 1px solid #ccc; background-color: #f0f0f0; }")
        
        # Remove restrictive width/height constraints - let it use available space
        self.scroll_area.setMinimumWidth(400)   # Just minimum for readability
        # No maximum width - use what's available
        self.scroll_area.setMinimumHeight(500)  # Reasonable minimum height
        
        # Use SelectablePDFLabel instead of regular QLabel for text selection
        self.pdf_label = SelectablePDFLabel()
        self.pdf_label.setAlignment(Qt.AlignCenter)
        self.pdf_label.setStyleSheet("QLabel { background-color: white; border: 1px solid #ddd; margin: 5px; }")
        self.pdf_label.setScaledContents(False)  # Don't auto-scale - we'll control this
        
        self.scroll_area.setWidget(self.pdf_label)
        layout.addWidget(self.scroll_area)
        
    def change_zoom(self, zoom_text):
        """Handle zoom level changes"""
        if self.current_pdf_path:
            self.load_pdf(self.current_pdf_path)
    
    def calculate_zoom_scale(self, zoom_text):
        """Calculate scale factor based on zoom selection and actual container size"""
        # Get actual available space in the PDF container
        available_width = self.scroll_area.width() - 40  # Account for scrollbars/margins
        available_height = self.scroll_area.height() - 40
        
        if zoom_text == "Fit Width":
            return available_width / self.pdf_width
        elif zoom_text == "Fit Page":
            # Fit to both width and height constraints
            width_scale = available_width / self.pdf_width
            height_scale = available_height / self.pdf_height
            return min(width_scale, height_scale)  # Use smaller scale to fit both dimensions
        elif zoom_text.endswith("%"):
            # Parse percentage
            percentage = int(zoom_text.replace("%", ""))
            return percentage / 100.0
        else:
            return 1.0  # Default to 100%
        
    def load_pdf(self, pdf_path):
        """Load PDF with proper aspect ratio calculation"""
        self.current_pdf_path = pdf_path
        filename = Path(pdf_path).name
        self.pdf_info.setText(f"📄 {filename}")
        
        try:
            import fitz
            doc = fitz.open(pdf_path)
            page = doc[0]
            
            # Get actual PDF dimensions
            rect = page.rect
            self.pdf_width = rect.width
            self.pdf_height = rect.height
            
            print(f"DEBUG: PDF dimensions: {self.pdf_width} x {self.pdf_height}")
            print(f"DEBUG: PDF aspect ratio: {self.pdf_width/self.pdf_height:.2f}")
            print(f"DEBUG: Is portrait: {self.pdf_height > self.pdf_width}")
            
            # Use zoom control to determine scale
            zoom_text = self.zoom_combo.currentText()
            scale = self.calculate_zoom_scale(zoom_text)
            
            # Apply minimum/maximum constraints for usability
            min_scale = 0.3
            max_scale = 3.0
            scale = max(min_scale, min(scale, max_scale))
                
            display_width = int(self.pdf_width * scale)
            display_height = int(self.pdf_height * scale)
            
            print(f"DEBUG: Calculated display size: {display_width} x {display_height} (scale: {scale:.2f})")
            
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
            
            # Extract text blocks for selection (before closing document)
            self.extract_text_blocks(page, scale)
            
            doc.close()
            print("DEBUG: PDF loaded with proper aspect ratio")
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
            
        except Exception as e:
            print(f"DEBUG: Text extraction failed: {e}")
            self.pdf_label.set_text_blocks([])

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
        self.setWindowTitle("Research Buddy 3.1 - Professional Positionality Analysis Interface")
        # Set reasonable default size but allow user to resize
        self.resize(1200, 800)  # Default size - user can resize as needed
        
        # Training data storage
        self.training_data = []
        self.current_paper_index = 0
        self.papers_list = []
        self.pdf_folder = ""
        
        # Paper state persistence - stores content for each paper
        self.paper_states = {}  # filename -> {human_text, ai_text, decision, uploaded}
        
        # Default folder in user's home directory
        self.default_pdf_folder = Path.home() / "ExtractorPDFs" 
        self.readme_pdf_path = self.default_pdf_folder / "about.pdf"
        
        # Settings file to remember state
        self.settings_file = Path(__file__).parent / "interface_settings.json"
        
        # Check for first run and show setup dialog
        if check_first_run():
            setup_dialog = FirstRunSetupDialog(self)
            if setup_dialog.exec() == QDialog.DialogCode.Rejected:
                # User skipped setup, show a gentle reminder
                QMessageBox.information(
                    self,
                    "Welcome to Research Buddy!",
                    "🎉 Welcome to Research Buddy 3.1!\n\n"
                    "You can configure API keys and GitHub settings anytime through:\n"
                    "Configuration → Settings\n\n"
                    "Research Buddy works great even without configuration!"
                )
        
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
        self.check_network_and_update_buttons()
        
        # Initialize with default folder and README
        self.initialize_with_readme()
        
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
        exit_action.setStatusTip('Exit Research Buddy')
        
        # Help menu
        help_menu = menubar.addMenu('❓ Help')
        
        about_action = help_menu.addAction('📖 About Research Buddy...')
        about_action.triggered.connect(self.show_about)
        about_action.setStatusTip('About Research Buddy')
        
    def show_configuration(self):
        """Show the configuration dialog"""
        dialog = ConfigurationDialog(self)
        if dialog.exec() == QDialog.Accepted:
            # Refresh GitHub uploader with new configuration
            self.github_uploader = GitHubReportUploader()
            
            # Update button tooltips with new repository info
            self.check_network_and_update_buttons()
            
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
            
            repo_url = f"https://github.com/{self.github_uploader.repo_owner}/{self.github_uploader.repo_name}"
            QMessageBox.information(self, "Configuration Updated", 
                                  f"Configuration has been updated successfully!\n\n"
                                  f"📦 Upload Destination:\n{repo_url}\n\n"
                                  f"New settings will be used for future uploads.")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Research Buddy 3.1", 
                         "🎓 Research Buddy 3.1\n\n"
                         "Enhanced State Management Interface\n\n"
                         "Features:\n"
                         "• Paper state persistence\n"
                         "• Visual progress indicators\n"
                         "• Configurable GitHub uploads\n"
                         "• Professional positionality analysis\n\n"
                         "Built for Graduate Assistants and Research Teams\n\n"
                         "© 2025 Research Buddy Project")
        
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
        
        # Progress tracking
        self.progress_label = QLabel("No papers loaded")
        self.progress_label.setFont(QFont("Courier New", 10, QFont.Bold))
        self.progress_bar = QProgressBar()
        header_layout.addWidget(self.progress_label)
        header_layout.addWidget(self.progress_bar)
        
        layout.addLayout(header_layout)
        
        # Main content area with splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)  # Thin separator line
        splitter.setChildrenCollapsible(False)  # Prevent collapsing
        
        # Left panel: PDF Viewer - prioritize PDF display
        pdf_panel = QGroupBox("PDF Document Viewer")
        pdf_panel.setMinimumWidth(600)   # Wider for better PDF viewing
        # Remove maximum width to let it expand naturally
        pdf_layout = QVBoxLayout(pdf_panel)
        
        # Paper info
        self.paper_info = QLabel("No paper selected")
        self.paper_info.setFont(QFont("Courier New", 11, QFont.Bold))
        self.paper_info.setStyleSheet("QLabel { padding: 4px; background: white; border: 1px solid #666666; color: black; }")
        pdf_layout.addWidget(self.paper_info)
        
        # Note about PDF functionality
        pdf_note = QLabel("� PDF displays with zoom and text selection built-in")
        pdf_note.setStyleSheet("QLabel { color: #666; font-style: italic; padding: 5px; }")
        pdf_layout.addWidget(pdf_note)
        
        # PDF viewer - use embedded system viewer
        self.pdf_viewer = EmbeddedPDFViewer()
        
        # Connect text selection signal from PDF viewer to main interface
        self.pdf_viewer.pdf_label.text_selected.connect(self.on_text_selected)
        
        pdf_layout.addWidget(self.pdf_viewer)
        

        
        # Quick text extraction area
        text_extract_group = QGroupBox("📝 Selected Text (for Evidence)")
        text_extract_layout = QVBoxLayout(text_extract_group)
        text_extract_layout.setContentsMargins(2, 2, 2, 2)  # Minimal margins
        text_extract_layout.setSpacing(1)  # Very tight spacing
        
        self.extracted_text = QPlainTextEdit()
        self.extracted_text.setReadOnly(False)  # Allow manual typing
        self.extracted_text.setFont(QFont("Courier New", 12))  # Larger, more readable font
        self.extracted_text.setStyleSheet("QPlainTextEdit { margin: 0px; padding: 1px; border: 1px solid #ddd; }")
        self.extracted_text.setPlaceholderText("Select text in PDF above or type quotes for evidence...")
        self.extracted_text.setMinimumHeight(180)  # Expanded to use space from removed AI Detection section
        text_extract_layout.addWidget(self.extracted_text)
        
        # Quick action buttons
        text_actions = QHBoxLayout()
        
        copy_to_evidence_btn = QPushButton("📋 Copy to Evidence")
        copy_to_evidence_btn.clicked.connect(self.copy_to_evidence)
        copy_to_evidence_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }")
        text_actions.addWidget(copy_to_evidence_btn)
        
        clear_text_btn = QPushButton("🗑️ Clear")
        clear_text_btn.clicked.connect(lambda: self.extracted_text.clear())
        text_actions.addWidget(clear_text_btn)
        
        text_actions.addStretch()
        text_extract_layout.addLayout(text_actions)
        
        pdf_layout.addWidget(text_extract_group)
        
        # Set PDF panel to prefer smaller size
        pdf_panel.setMaximumWidth(500)  # Limit PDF panel width
        pdf_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        splitter.addWidget(pdf_panel)
        
        # Right panel: Training interface - make it larger
        training_panel = QGroupBox("Evidence")
        training_panel.setMinimumWidth(400)  # Adequate minimum for usability
        # No maximum width - let it expand as needed
        # Remove maximum width constraint to let it use full available space
        training_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout = QVBoxLayout(training_panel)
        right_layout.setContentsMargins(2, 2, 2, 2)  # Minimal margins
        right_layout.setSpacing(1)  # Very tight spacing
        
        # AI Pre-screening section
        prescreening_group = QGroupBox("🔍 AI Analysis")
        prescreening_layout = QVBoxLayout(prescreening_group)
        prescreening_layout.setContentsMargins(2, 2, 2, 2)  # Minimal margins
        prescreening_layout.setSpacing(1)  # Very tight spacing
        
        # Initial analysis button
        analysis_btn_layout = QHBoxLayout()
        self.initial_analysis_btn = QPushButton("🚀 Run AI Analysis")
        self.initial_analysis_btn.clicked.connect(self.run_initial_analysis)
        self.initial_analysis_btn.setStyleSheet("QPushButton { background-color: #333333; color: white; font-weight: bold; padding: 6px; font-family: 'Courier New', monospace; }")
        analysis_btn_layout.addWidget(self.initial_analysis_btn)
        analysis_btn_layout.addStretch()  # Make button wider by removing text and adding stretch
        prescreening_layout.addLayout(analysis_btn_layout)
        
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
        
        # Human Input tab (editable)
        human_tab = QWidget()
        human_layout = QVBoxLayout(human_tab)
        human_layout.setContentsMargins(2, 2, 2, 2)
        
        human_layout.addWidget(QLabel("Human Evidence:"))
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
        
        ai_layout.addWidget(QLabel("AI Analysis:"))
        self.ai_input = QTextEdit()
        self.ai_input.setMinimumHeight(200)
        self.ai_input.setFont(QFont("Arial", 13))  # Increased from 11
        self.ai_input.setPlaceholderText("AI analysis results will appear here...")
        self.ai_input.setStyleSheet("QTextEdit { margin: 0px; padding: 2px; border: 1px solid #ddd; }")
        # Enable HTML rendering
        self.ai_input.setAcceptRichText(True)
        ai_layout.addWidget(self.ai_input)
        
        self.evidence_tabs.addTab(ai_tab, "AI Input")

        right_layout.addWidget(self.evidence_tabs)
        
        splitter.addWidget(training_panel)
        
        # Set stretch factors for better proportions
        splitter.setStretchFactor(0, 1)  # PDF panel gets 1 part  
        splitter.setStretchFactor(1, 1)  # Analysis panel gets 1 part (equal space)
        
        layout.addWidget(splitter)
        
        # Set more balanced default proportions
        splitter.setSizes([500, 700])  # Give more space to the right panel
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        prev_btn = QPushButton("◀ Previous Paper")
        prev_btn.clicked.connect(self.previous_paper)
        button_layout.addWidget(prev_btn)
        
        skip_btn = QPushButton("⏭️ Next Paper")
        skip_btn.clicked.connect(self.next_paper)
        button_layout.addWidget(skip_btn)
        
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
        
        # Status bar
        repo_info = f"📦 Uploads to: {self.github_uploader.repo_owner}/{self.github_uploader.repo_name}"
        self.statusBar().showMessage(f"Ready to analyze papers and make decisions. Select a PDF folder to begin. {repo_info}")
        
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
        """Update progress indicators"""
        if not self.papers_list:
            self.progress_label.setText("No papers loaded")
            self.progress_bar.setValue(0)
            self.papers_completed.setText("0 papers labeled")
            return
            
        current = self.current_paper_index + 1
        total = len(self.papers_list)
        
        # Count processed papers with status indicators
        processed_count = 0
        current_filename = self.papers_list[self.current_paper_index] if self.papers_list else ""
        status_indicator = "🔴"  # Red dot for unprocessed
        
        for filename in self.papers_list:
            if filename in self.paper_states and self.paper_states[filename].get('uploaded', False):
                processed_count += 1
        
        # Determine current paper status
        if current_filename in self.paper_states:
            if self.paper_states[current_filename].get('uploaded', False):
                status_indicator = "🟢"  # Green dot for uploaded/completed
            elif (self.paper_states[current_filename].get('human_text') or 
                  self.paper_states[current_filename].get('ai_text') or
                  self.paper_states[current_filename].get('decision')):
                status_indicator = "🟡"  # Yellow dot for in progress
        
        self.progress_label.setText(f"{status_indicator} Paper {current} of {total} | Processed: {processed_count}")
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.papers_completed.setText(f"{processed_count} papers processed")
        
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
        
        # Update paper info
        self.paper_info.setText(f"📄 {filename}")
        
        # Load PDF in embedded viewer
        success = self.pdf_viewer.load_pdf(filepath)
        if not success:
            return
        
        # Run AI detection for the analysis panel
        try:
            ai_result = extract_positionality(filepath)
            score = ai_result.get("positionality_score", 0.0)
            tests = ai_result.get("positionality_tests", [])
            
            ai_summary = f"🤖 AI Analysis:\n"
            ai_summary += f"Score: {score:.3f} | "
            ai_summary += f"Prediction: {'POSITIVE' if score > 0.2 else 'NEGATIVE'}\n"
            ai_summary += f"Patterns: {', '.join(tests) if tests else 'None detected'}"
            
            # AI results are now shown in the AI Input tab instead
            
        except Exception as e:
            # AI detection error handling - no longer showing in separate widget
            pass
        
        # Clear previous inputs
        self.clear_inputs()
        
        # Always start fresh - no loading of previous decisions
        # Each session focuses on current analysis only
        
        self.statusBar().showMessage(f"Loaded: {filename} - Text selection available in PDF viewer", 3000)
        
    def clear_inputs(self):
        """Clear all input fields"""
        for btn in self.judgment_buttons.values():
            btn.setChecked(False)
        self.human_input.clear()
        self.ai_input.clear()
        self.extracted_text.clear()
        
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
            "evidence": self.extracted_text.toPlainText().strip(),
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
        """Update button states based on network connectivity"""
        has_network = self.check_network_connectivity()
        
        if has_network:
            self.upload_btn.setEnabled(True)
            # Set upload button tooltip with repository info
            if hasattr(self.github_uploader, 'owner') and hasattr(self.github_uploader, 'repo'):
                if self.github_uploader.owner and self.github_uploader.repo:
                    repo_url = f"https://github.com/{self.github_uploader.owner}/{self.github_uploader.repo}"
                    self.upload_btn.setToolTip(f"Upload your decision to:\n{repo_url}")
                else:
                    self.upload_btn.setToolTip("Upload destination not configured - use Configuration menu")
            else:
                self.upload_btn.setToolTip("Upload destination not configured - use Configuration menu")
        else:
            self.upload_btn.setEnabled(False)
            self.upload_btn.setToolTip("No internet connection - use 'Export Evidence' to save your work locally")
            self.upload_btn.setStyleSheet("QPushButton { background-color: #888; color: #ccc; font-weight: bold; }")
            
    def export_evidence(self):
        """Export current evidence (AI + Human) to text file next to PDF"""
        if not hasattr(self, 'current_paper_index') or self.current_paper_index >= len(self.papers_list):
            QMessageBox.information(self, "No Paper", "No paper currently loaded to export evidence from.")
            return
            
        # Get current evidence
        human_evidence = self.extracted_text.toPlainText().strip()
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
        
        # First, try to save current state if there's an active paper
        if hasattr(self, 'current_paper_index') and self.current_paper_index < len(self.papers_list):
            current_filename = self.papers_list[self.current_paper_index]
            
            # Check if user has made any selections for current paper
            judgment_selected = any(btn.isChecked() for btn in self.judgment_buttons.values())
            evidence_text = self.extracted_text.toPlainText().strip()
            
            if judgment_selected or evidence_text:
                # Auto-save current paper's data
                saved = self.save_current_training()
                if not saved:
                    return  # User was warned about missing data, let them fix it
        
        # Now check if we have any training data at all
        if not self.training_data:
            # Check if there's at least some evidence in the interface
            evidence_text = self.extracted_text.toPlainText().strip()
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
            
        try:
            # Process training session (save locally + upload to GitHub)
            result = self.github_uploader.process_training_session(self.training_data, ga_name)
            
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
                                      f"https://github.com/{self.github_uploader.repo_owner}/{self.github_uploader.repo_name}\n\n"
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
                
    def connect_pdf_selection(self):
        """Connect PDF text selection to the extraction area"""
        # Connect mouse release to update extracted text
        original_mouse_release = self.pdf_viewer.pdf_label.mouseReleaseEvent
        
        def enhanced_mouse_release(event):
            original_mouse_release(event)
            # Update extracted text area when selection is made
            if self.pdf_viewer.pdf_label.selected_text:
                self.extracted_text.setPlainText(self.pdf_viewer.pdf_label.selected_text)
                
        self.pdf_viewer.pdf_label.mouseReleaseEvent = enhanced_mouse_release
        
        # Also override the copy method to update extraction area
        original_copy = self.pdf_viewer.pdf_label.copy_selected_text
        
        def enhanced_copy():
            original_copy()
            if self.pdf_viewer.pdf_label.selected_text:
                current_text = self.extracted_text.toPlainText()
                if current_text and current_text != self.pdf_viewer.pdf_label.selected_text:
                    new_text = current_text + "\n\n" + self.pdf_viewer.pdf_label.selected_text
                else:
                    new_text = self.pdf_viewer.pdf_label.selected_text
                self.extracted_text.setPlainText(new_text)
                
        self.pdf_viewer.pdf_label.copy_selected_text = enhanced_copy
        
    def initialize_with_readme(self):
        """Initialize with default ExtractorPDFs folder and show README first"""
        # Ensure default folder exists
        self.default_pdf_folder.mkdir(exist_ok=True)
        
        # Copy README PDF to default folder if it doesn't exist
        self.ensure_readme_exists()
        
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
                self.statusBar().showMessage("� Add PDF files to your ~/ExtractorPDFs folder to begin training", 5000)
    
    def ensure_readme_exists(self):
        """Ensure the README PDF exists in the default folder"""
        if not self.readme_pdf_path.exists():
            # Copy from app directory
            source_readme = Path(__file__).parent / "about.pdf"
            if source_readme.exists():
                import shutil
                shutil.copy2(source_readme, self.readme_pdf_path)
                print(f"Copied professional training guide to {self.readme_pdf_path}")
            else:
                # Create README if it doesn't exist
                from create_readme_pdf import create_readme_pdf
                create_readme_pdf(self.readme_pdf_path)
                print(f"Created README at {self.readme_pdf_path}")
    
    def find_readme_index(self):
        """Find the index of the README PDF in papers list"""
        for i, paper in enumerate(self.papers_list):
            if "README" in paper or "readme" in paper.lower():
                return i
        return -1
    
    def load_settings(self):
        """Load interface settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.pdf_folder = settings.get("pdf_folder", str(self.default_pdf_folder))
                    
                    # Load window geometry if saved
                    window_geometry = settings.get("window_geometry")
                    if window_geometry:
                        self.setGeometry(
                            window_geometry.get("x", 100),
                            window_geometry.get("y", 100),
                            window_geometry.get("width", 1400),
                            window_geometry.get("height", 1000)
                        )
        except Exception as e:
            print(f"Could not load settings: {e}")
            self.pdf_folder = str(self.default_pdf_folder)
    
    def save_settings(self):
        """Save interface settings to file"""
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
                "last_updated": datetime.now().isoformat()
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Could not save settings: {e}")
    
    def on_text_selected(self, selected_text):
        """Handle text selection from PDF viewer"""
        print(f"DEBUG - on_text_selected called with: '{selected_text[:100] if selected_text else 'EMPTY'}'")
        if selected_text.strip():
            self.extracted_text.setPlainText(selected_text)
            self.statusBar().showMessage("Text selected from PDF", 2000)
            print(f"DEBUG - Text set in extracted_text widget")
        else:
            self.extracted_text.clear()
            print(f"DEBUG - Cleared extracted_text widget")
            
    def copy_to_evidence(self):
        """Copy extracted text to Human Input tab and switch focus"""
        text = self.extracted_text.toPlainText().strip()
        if text:
            current_evidence = self.human_input.toPlainText().strip()
            if current_evidence:
                new_evidence = current_evidence + "\n\n" + text
            else:
                new_evidence = text
            self.human_input.setPlainText(new_evidence)
            
            # Switch to Human Input tab
            self.evidence_tabs.setCurrentIndex(0)  # Human Input is index 0
            
            # Show confirmation
            self.statusBar().showMessage("Text copied to Human Input", 2000)
    
    def run_initial_analysis(self):
        """Run AI analysis on current paper and display findings"""
        if not self.papers_list or self.current_paper_index >= len(self.papers_list):
            QMessageBox.information(self, "No Paper", "No paper selected for analysis.")
            return
        
        current_paper = self.papers_list[self.current_paper_index]
        pdf_path = Path(self.pdf_folder) / current_paper
        
        self.statusBar().showMessage("🔄 Analyzing...")
        self.initial_analysis_btn.setEnabled(False)
        QApplication.processEvents()  # Update UI
        
        try:
            # Run our enhanced detection
            result = extract_positionality(str(pdf_path))
            
            # Format findings for display
            findings_text = self.format_ai_findings(result, current_paper)
            self.ai_input.setHtml(findings_text)
            
            # Switch to AI Input tab
            self.evidence_tabs.setCurrentIndex(1)  # AI Input is index 1
            
            # Update status 
            if result['positionality_score'] > 0.3:
                self.statusBar().showMessage(f"Found {len(result['positionality_snippets'])} potential evidence excerpts")
                # Store findings for reference
                self.current_ai_findings = result
            else:
                self.statusBar().showMessage("No strong positionality indicators found")
                self.current_ai_findings = None
                
        except Exception as e:
            self.statusBar().showMessage(f"Analysis failed: {str(e)}")
            self.ai_input.setPlainText(f"Error running analysis: {e}")
            
        finally:
            self.initial_analysis_btn.setEnabled(True)
    
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
                # Clean up and intelligently truncate text
                clean_text = excerpt.strip()
                if len(clean_text) > 300:
                    # Find a good breaking point (sentence end)
                    truncate_pos = clean_text.find('.', 250)
                    if truncate_pos == -1:
                        truncate_pos = 300
                    clean_text = clean_text[:truncate_pos + 1] + "..."
                
                # Estimate location based on content
                location = self.estimate_location_from_text(clean_text)
                
                text += f"""<b>#{i} - {pattern.replace('_', ' ').title()}</b><br>
<i>Likely Location: {location}</i><br>
"{clean_text}"<br><br><br>"""
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
        
        # Get current decision from radio buttons
        decision = None
        if hasattr(self, 'evidence_strong_radio') and self.evidence_strong_radio.isChecked():
            decision = 'strong'
        elif hasattr(self, 'evidence_moderate_radio') and self.evidence_moderate_radio.isChecked():
            decision = 'moderate'
        elif hasattr(self, 'evidence_minimal_radio') and self.evidence_minimal_radio.isChecked():
            decision = 'minimal'
        elif hasattr(self, 'evidence_none_radio') and self.evidence_none_radio.isChecked():
            decision = 'none'
        
        # Save to paper_states
        if filename not in self.paper_states:
            self.paper_states[filename] = {}
        
        self.paper_states[filename].update({
            'human_text': human_text,
            'ai_text': ai_text,
            'decision': decision
        })
    
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
            
            # Restore decision radio buttons
            decision = state.get('decision')
            if hasattr(self, 'evidence_strong_radio'):
                self.evidence_strong_radio.setChecked(decision == 'strong')
            if hasattr(self, 'evidence_moderate_radio'):
                self.evidence_moderate_radio.setChecked(decision == 'moderate')
            if hasattr(self, 'evidence_minimal_radio'):
                self.evidence_minimal_radio.setChecked(decision == 'minimal')
            if hasattr(self, 'evidence_none_radio'):
                self.evidence_none_radio.setChecked(decision == 'none')
        else:
            # Clear content for new paper
            self.human_input.clear()
            self.ai_input.clear()
            
            # Clear radio button selections
            if hasattr(self, 'evidence_strong_radio'):
                self.evidence_strong_radio.setChecked(False)
            if hasattr(self, 'evidence_moderate_radio'):
                self.evidence_moderate_radio.setChecked(False)
            if hasattr(self, 'evidence_minimal_radio'):
                self.evidence_minimal_radio.setChecked(False)
            if hasattr(self, 'evidence_none_radio'):
                self.evidence_none_radio.setChecked(False)
    
    def mark_paper_uploaded(self, filename):
        """Mark a paper as uploaded/processed"""
        if filename not in self.paper_states:
            self.paper_states[filename] = {}
        
        self.paper_states[filename]['uploaded'] = True
        self.update_progress()  # Refresh the status indicators
    
    def closeEvent(self, event):
        """Save settings when closing"""
        self.save_settings()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = EnhancedTrainingInterface()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()