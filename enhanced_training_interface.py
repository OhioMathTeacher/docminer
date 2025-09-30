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
    QTabWidget, QSlider, QMenu, QPlainTextEdit, QLineEdit, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, Signal, QRect, QPoint, QUrl
from PySide6.QtGui import QFont, QTextCursor, QPixmap, QPainter, QPen, QColor, QBrush, QAction, QClipboard
from PySide6.QtWebEngineWidgets import QWebEngineView

import fitz  # PyMuPDF for PDF rendering
from metadata_extractor import extract_positionality
from github_report_uploader import GitHubReportUploader

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
        
        self.pdf_label = QLabel()
        self.pdf_label.setAlignment(Qt.AlignCenter)
        self.pdf_label.setStyleSheet("QLabel { background-color: white; border: 1px solid #ddd; margin: 5px; }")
        self.pdf_label.setScaledContents(False)  # Don't auto-scale - we'll control this
        
        self.scroll_area.setWidget(self.pdf_label)
        layout.addWidget(self.scroll_area)
        
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
            
            # Calculate optimal display size for much narrower PDF pane
            container_width = 480  # Much narrower available width
            padding = 40  # Account for margins and scrollbars
            available_width = container_width - padding
            
            # Calculate scale to fit width while maintaining aspect ratio
            scale = available_width / self.pdf_width
            
            # For portrait documents, work with narrower space
            if self.pdf_height > self.pdf_width:  # Portrait
                # Ensure readable scale in narrow container
                min_scale = 0.6  # Lower minimum for narrow space
                max_scale = 0.8  # Keep it reasonable
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
            
            doc.close()
            print("DEBUG: PDF loaded with proper aspect ratio")
            return True
            
        except Exception as e:
            print(f"DEBUG: PDF loading failed: {e}")
            self.pdf_label.setText(f"Error loading PDF: {e}")
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
        self.setWindowTitle("Training Buddy - Professional Positionality Analysis Interface")
        # Set reasonable default size but allow user to resize
        self.resize(1200, 800)  # Default size - user can resize as needed
        
        # Training data storage
        self.training_data = []
        self.current_paper_index = 0
        self.papers_list = []
        self.pdf_folder = ""
        
        # Default folder in user's home directory
        self.default_pdf_folder = Path.home() / "ExtractorPDFs" 
        self.readme_pdf_path = self.default_pdf_folder / "about.pdf"
        
        # Settings file to remember state
        self.settings_file = Path(__file__).parent / "interface_settings.json"
        self.training_file = "training_data.json"
        
        # Load existing training data and settings
        self.load_training_data()
        self.load_settings()
        
        # Initialize GitHub uploader
        self.github_uploader = GitHubReportUploader()
        
        self.setup_ui()
        
        # Initialize with default folder and README
        self.initialize_with_readme()
        
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
        pdf_layout.addWidget(self.pdf_viewer)
        

        
        # Quick text extraction area
        text_extract_group = QGroupBox("📝 Selected Text (for Evidence)")
        text_extract_layout = QVBoxLayout(text_extract_group)
        text_extract_layout.setContentsMargins(2, 2, 2, 2)  # Minimal margins
        text_extract_layout.setSpacing(1)  # Very tight spacing
        text_extract_group.setMaximumHeight(100)  # Smaller
        
        self.extracted_text = QPlainTextEdit()
        self.extracted_text.setReadOnly(False)  # Allow manual typing
        self.extracted_text.setFont(QFont("Courier New", 12))  # Larger, more readable font
        self.extracted_text.setStyleSheet("QPlainTextEdit { margin: 0px; padding: 1px; border: 1px solid #ddd; }")
        self.extracted_text.setPlaceholderText("Select text in PDF above or type quotes for evidence...")
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
        
        # AI Detection Results (compact)
        ai_group = QGroupBox("🤖 Current AI Detection")
        ai_layout = QVBoxLayout(ai_group)
        ai_group.setMaximumHeight(100)  # More compact
        
        self.ai_results = QLabel("No detection results")
        self.ai_results.setWordWrap(True)
        self.ai_results.setFont(QFont("Courier New", 9))  # Smaller font
        self.ai_results.setStyleSheet("QLabel { background: white; padding: 3px; border: 1px solid #666666; color: black; }")
        ai_layout.addWidget(self.ai_results)
        
        pdf_layout.addWidget(ai_group)
        
        # Set PDF panel to prefer smaller size
        pdf_panel.setMaximumWidth(500)  # Limit PDF panel width
        pdf_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        splitter.addWidget(pdf_panel)
        
        # Right panel: Training interface - make it larger
        training_panel = QGroupBox("Human Expert Analysis and Labeling")
        training_panel.setMinimumWidth(400)  # Adequate minimum for usability
        # No maximum width - let it expand as needed
        # Remove maximum width constraint to let it use full available space
        training_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout = QVBoxLayout(training_panel)
        right_layout.setContentsMargins(2, 2, 2, 2)  # Minimal margins
        right_layout.setSpacing(1)  # Very tight spacing
        
        # AI Pre-screening section
        prescreening_group = QGroupBox("🔍 AI Pre-Screening (Speed Up Your Work!)")
        prescreening_layout = QVBoxLayout(prescreening_group)
        prescreening_layout.setContentsMargins(2, 2, 2, 2)  # Minimal margins
        prescreening_layout.setSpacing(1)  # Very tight spacing
        
        # Initial analysis button
        analysis_btn_layout = QHBoxLayout()
        self.initial_analysis_btn = QPushButton("🚀 Run Initial Analysis")
        self.initial_analysis_btn.clicked.connect(self.run_initial_analysis)
        self.initial_analysis_btn.setStyleSheet("QPushButton { background-color: #333333; color: white; font-weight: bold; padding: 6px; font-family: 'Courier New', monospace; }")
        analysis_btn_layout.addWidget(self.initial_analysis_btn)
        
        self.analysis_status = QLabel("Click to analyze this paper for positionality")
        self.analysis_status.setStyleSheet("QLabel { color: #666; font-style: italic; }")
        analysis_btn_layout.addWidget(self.analysis_status)
        analysis_btn_layout.addStretch()
        prescreening_layout.addLayout(analysis_btn_layout)
        
        # AI findings display with scroll
        self.ai_findings = QTextEdit()
        self.ai_findings.setMinimumHeight(150)  # Smaller
        self.ai_findings.setMaximumHeight(200)  # More compact
        self.ai_findings.setReadOnly(True)
        self.ai_findings.setPlaceholderText("AI analysis results will appear here...\n\nClick 'Run Initial Analysis' to see:\n• Overall confidence score\n• Detected patterns\n• Evidence excerpts with locations\n• Recommended judgment")
        self.ai_findings.setStyleSheet("QTextEdit { background: #f8f9fa; border: 1px solid #ddd; font-family: 'Segoe UI', Arial; margin: 0px; padding: 2px; }")
        self.ai_findings.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        prescreening_layout.addWidget(self.ai_findings)
        
        # Quick validation buttons
        quick_validate_layout = QHBoxLayout()
        self.quick_accept_btn = QPushButton("✅ Accept AI Findings")
        self.quick_accept_btn.clicked.connect(self.quick_accept_findings)
        self.quick_accept_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        self.quick_accept_btn.setEnabled(False)
        
        self.quick_reject_btn = QPushButton("❌ Reject - Manual Review")
        self.quick_reject_btn.clicked.connect(self.quick_reject_findings)
        self.quick_reject_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
        self.quick_reject_btn.setEnabled(False)
        
        quick_validate_layout.addWidget(self.quick_accept_btn)
        quick_validate_layout.addWidget(self.quick_reject_btn)
        quick_validate_layout.addStretch()
        prescreening_layout.addLayout(quick_validate_layout)
        
        right_layout.addWidget(prescreening_group)
        
        # Simplified location - integrated into other controls below to save space
        
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
            btn.setStyleSheet("QRadioButton { font-size: 11px; padding: 4px; }")
            self.judgment_buttons[value] = btn
            self.judgment_group.addButton(btn)
            judgment_layout.addWidget(btn)
            
        right_layout.addWidget(judgment_group)
        
        # Evidence collection (tabbed for space efficiency)
        evidence_tabs = QTabWidget()
        
        # Evidence tab
        evidence_tab = QWidget()
        evidence_layout = QVBoxLayout(evidence_tab)
        
        evidence_layout.addWidget(QLabel("Quote specific text:"))
        self.evidence_text = QTextEdit()
        self.evidence_text.setMaximumHeight(80)
        self.evidence_text.setFont(QFont("Arial", 12))
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
        
        evidence_tabs.addTab(evidence_tab, "📝 Evidence")
        
        # Patterns tab
        patterns_tab = QWidget()
        pattern_layout = QGridLayout(patterns_tab)
        
        self.pattern_checkboxes = {}
        patterns = [
            ("identity", "Identity disclosure"),
            ("researcher_pos", "Researcher positioning"),
            ("bias_ack", "Bias acknowledgment"),
            ("reflexive", "Reflexive awareness"),
            ("methodological", "Methodological reflexivity"),
            ("social_location", "Social location/standpoint")
        ]
        
        for i, (key, label) in enumerate(patterns):
            cb = QCheckBox(label)
            cb.setStyleSheet("QCheckBox { font-size: 10px; }")
            self.pattern_checkboxes[key] = cb
            pattern_layout.addWidget(cb, i // 2, i % 2)
            
        evidence_tabs.addTab(patterns_tab, "🏷️ Patterns")
        
        # Notes tab
        notes_tab = QWidget()
        notes_layout = QVBoxLayout(notes_tab)
        
        # Confidence rating
        confidence_layout = QHBoxLayout()
        confidence_layout.addWidget(QLabel("Confidence:"))
        self.confidence_spin = QSpinBox()
        self.confidence_spin.setRange(1, 5)
        self.confidence_spin.setValue(3)
        self.confidence_spin.setSuffix("/5")
        confidence_layout.addWidget(self.confidence_spin)
        confidence_layout.addStretch()
        notes_layout.addLayout(confidence_layout)
        
        # Explanation
        notes_layout.addWidget(QLabel("Explanation:"))
        self.explanation_text = QTextEdit()
        self.explanation_text.setMaximumHeight(60)
        self.explanation_text.setFont(QFont("Arial", 12))
        notes_layout.addWidget(self.explanation_text)
        
        # Pattern suggestions
        notes_layout.addWidget(QLabel("AI Pattern Suggestions:"))
        self.pattern_suggestions = QTextEdit()
        self.pattern_suggestions.setMaximumHeight(50)
        self.pattern_suggestions.setFont(QFont("Arial", 9))
        notes_layout.addWidget(self.pattern_suggestions)
        
        evidence_tabs.addTab(notes_tab, "📋 Notes")
        
        right_layout.addWidget(evidence_tabs)
        
        splitter.addWidget(training_panel)
        
        # Set stretch factors for reasonable proportions
        splitter.setStretchFactor(0, 2)  # PDF panel gets 2 parts  
        splitter.setStretchFactor(1, 1)  # Analysis panel gets 1 part
        
        layout.addWidget(splitter)
        
        # Set reasonable default proportions - user can adjust splitter
        splitter.setSizes([700, 500])  # Give Analysis Pane adequate space
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        prev_btn = QPushButton("◀ Previous Paper")
        prev_btn.clicked.connect(self.previous_paper)
        button_layout.addWidget(prev_btn)
        
        save_btn = QPushButton("💾 Save & Next Paper")
        save_btn.clicked.connect(self.save_and_next)
        save_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; }")
        button_layout.addWidget(save_btn)
        
        skip_btn = QPushButton("Skip Paper ▶")
        skip_btn.clicked.connect(self.next_paper)
        button_layout.addWidget(skip_btn)
        
        button_layout.addStretch()
        
        # Progress info
        self.papers_completed = QLabel("0 papers labeled")
        self.papers_completed.setStyleSheet("QLabel { color: #666; font-style: italic; }")
        button_layout.addWidget(self.papers_completed)
        
        export_btn = QPushButton("📤 Export Data")
        export_btn.clicked.connect(self.export_training_data)
        button_layout.addWidget(export_btn)
        
        upload_btn = QPushButton("🚀 Export & Upload")
        upload_btn.clicked.connect(self.export_and_upload)
        upload_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; }")
        button_layout.addWidget(upload_btn)
        
        layout.addLayout(button_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready to start training. Select a PDF folder to begin.")
        
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
        completed = len(self.training_data)
        
        self.progress_label.setText(f"Paper {current} of {total}")
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.papers_completed.setText(f"{completed} papers labeled")
        
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
            
            self.ai_results.setText(ai_summary)
            
        except Exception as e:
            self.ai_results.setText(f"AI detection failed: {e}")
        
        # Clear previous inputs
        self.clear_inputs()
        
        # Load existing training data for this paper if available
        self.load_existing_label(filename)
        
        self.statusBar().showMessage(f"Loaded: {filename} - Text selection available in PDF viewer", 3000)
        
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
                    
                self.statusBar().showMessage(f"Loaded existing label for {filename}")
                break
        
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
            QMessageBox.warning(self, "Missing Data", "Please select a judgment before saving.")
            return False
        
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
        self.update_progress()
        
        self.statusBar().showMessage(f"Saved training data for {filename}")
        return True
        
    def next_paper(self):
        """Move to next paper"""
        if self.current_paper_index < len(self.papers_list) - 1:
            self.current_paper_index += 1
            self.update_progress()
            self.load_current_paper()
        else:
            QMessageBox.information(self, "🎉 Complete!", 
                                  f"All {len(self.papers_list)} papers have been reviewed!\n\n"
                                  f"Total labeled: {len(self.training_data)} papers\n"
                                  f"Ready to export training data for analysis.")
            
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
                QMessageBox.information(self, "Exported", 
                                      f"Training data exported to {filename}\n\n"
                                      f"Papers labeled: {len(self.training_data)}\n"
                                      f"Use training_analysis.py to analyze the results.")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Could not export: {e}")
                
    def export_and_upload(self):
        """Export training data and upload to GitHub automatically"""
        if not self.training_data:
            QMessageBox.information(self, "No Data", "No training data to export and upload.")
            return
            
        ga_name = self.ga_name_input.text().strip()
        if not ga_name:
            QMessageBox.warning(self, "GA Name Required", "Please enter your name before uploading.")
            self.ga_name_input.setFocus()
            return
            
        try:
            # Process training session (save locally + upload to GitHub)
            result = self.github_uploader.process_training_session(self.training_data, ga_name)
            
            if result['success']:
                QMessageBox.information(self, "Upload Successful", 
                                      f"Training report uploaded successfully!\n\n"
                                      f"GA: {ga_name}\n"
                                      f"Session: {result['session_id']}\n"
                                      f"Papers labeled: {len(self.training_data)}\n\n"
                                      f"Files created:\n"
                                      f"• {Path(result['json_file']).name}\n"
                                      f"• {Path(result['md_file']).name}\n\n"
                                      f"Report available on GitHub.")
            else:
                QMessageBox.warning(self, "Upload Failed", 
                                  f"Report created locally but upload failed.\n\n"
                                  f"Error: {result['message']}\n\n"
                                  f"Files saved locally:\n"
                                  f"• {Path(result['json_file']).name}\n"
                                  f"• {Path(result['md_file']).name}")
                
        except Exception as e:
            QMessageBox.critical(self, "Upload Error", f"Could not create or upload report: {e}")
                
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
        if selected_text.strip():
            self.extracted_text.setPlainText(selected_text)
            self.statusBar().showMessage("Text selected from PDF", 2000)
        else:
            self.extracted_text.clear()
            
    def copy_to_evidence(self):
        """Copy extracted text to evidence field"""
        text = self.extracted_text.toPlainText().strip()
        if text:
            current_evidence = self.evidence_text.toPlainText().strip()
            if current_evidence:
                new_evidence = current_evidence + "\n\n" + text
            else:
                new_evidence = text
            self.evidence_text.setPlainText(new_evidence)
            
            # Show confirmation
            self.statusBar().showMessage("Text copied to evidence field", 2000)
    
    def run_initial_analysis(self):
        """Run AI analysis on current paper and display findings"""
        if not self.papers_list or self.current_paper_index >= len(self.papers_list):
            QMessageBox.information(self, "No Paper", "No paper selected for analysis.")
            return
        
        current_paper = self.papers_list[self.current_paper_index]
        pdf_path = Path(self.pdf_folder) / current_paper
        
        self.analysis_status.setText("🔄 Analyzing...")
        self.initial_analysis_btn.setEnabled(False)
        QApplication.processEvents()  # Update UI
        
        try:
            # Run our enhanced detection
            result = extract_positionality(str(pdf_path))
            
            # Format findings for display
            findings_text = self.format_ai_findings(result, current_paper)
            self.ai_findings.setHtml(findings_text)
            
            # Update status and enable buttons
            if result['positionality_score'] > 0.3:
                self.analysis_status.setText(f"Found {len(result['positionality_snippets'])} potential evidence excerpts")
                self.quick_accept_btn.setEnabled(True)
                self.quick_reject_btn.setEnabled(True)
                # Store findings for quick acceptance
                self.current_ai_findings = result
            else:
                self.analysis_status.setText("No strong positionality indicators found")
                self.quick_accept_btn.setEnabled(False)
                self.quick_reject_btn.setEnabled(True)
                self.current_ai_findings = None
                
        except Exception as e:
            self.analysis_status.setText(f"Analysis failed: {str(e)}")
            self.ai_findings.setPlainText(f"Error running analysis: {e}")
            
        finally:
            self.initial_analysis_btn.setEnabled(True)
    
    def format_ai_findings(self, result, paper_name):
        """Enhanced format AI detection results with detailed analysis"""
        score = result['positionality_score']
        patterns = result['positionality_tests']
        snippets = result['positionality_snippets']
        
        # Determine confidence level and recommendation
        if score >= 0.7:
            confidence_level = "High"
            recommendation = "Explicit positionality detected"
            confidence_color = "#4CAF50"
        elif score >= 0.4:
            confidence_level = "Medium"
            recommendation = "Subtle/implicit positionality likely"
            confidence_color = "#FF9800"
        elif score > 0:
            confidence_level = "Low"
            recommendation = "Minimal indicators found"
            confidence_color = "#FF5722"
        else:
            confidence_level = "None"
            recommendation = "No positionality detected"
            confidence_color = "#666"
        
        # Create comprehensive HTML display
        html = f"""
        <div style="font-family: 'Courier New', monospace;">
        <h3 style="color: #2196F3; margin-bottom: 10px;">AI Analysis for {paper_name}</h3>
        
        <div style="background: #f0f7ff; padding: 12px; border-radius: 6px; margin: 10px 0;">
        <p style="margin: 5px 0;"><b>Confidence Level:</b> <span style="color: {confidence_color}; font-weight: bold;">{confidence_level}</span> ({score:.3f})</p>
        <p style="margin: 5px 0;"><b>Recommendation:</b> {recommendation}</p>
        <p style="margin: 5px 0;"><b>Patterns Detected:</b> {', '.join(patterns).replace('_', ' ').title() if patterns else 'None'}</p>
        </div>
        """
        
        if snippets:
            html += "<h4 style='color: #4CAF50; margin-top: 15px;'>Evidence Excerpts Found:</h4>"
            for i, (pattern, text) in enumerate(snippets.items(), 1):
                # Clean up and intelligently truncate text
                clean_text = text.strip()
                if len(clean_text) > 300:
                    # Find a good breaking point (sentence end)
                    truncate_pos = clean_text.find('.', 250)
                    if truncate_pos == -1:
                        truncate_pos = 300
                    clean_text = clean_text[:truncate_pos + 1] + "..."
                
                # Estimate location based on content
                location = self.estimate_location_from_text(clean_text)
                
                html += f"""
                <div style="margin: 12px 0; padding: 10px; background: #f9f9f9; border-left: 4px solid #2196F3; border-radius: 4px;">
                <p style="margin: 0; font-weight: bold; color: #333;">#{i} - {pattern.replace('_', ' ').title()}</p>
                <p style="margin: 5px 0; font-style: italic; color: #666;">Likely Location: {location}</p>
                <p style="margin: 5px 0; line-height: 1.4;"><i>"{clean_text}"</i></p>
                </div>
                """
        else:
            html += """
            <div style="background: #fff3cd; padding: 10px; border-radius: 6px; margin: 10px 0;">
            <p style="color: #856404; margin: 0;"><i>No specific evidence excerpts extracted. Consider manual review of the full paper.</i></p>
            </div>
            """
        
        # Add AI recommendation summary
        html += f"""
        <div style="background: #e8f5e8; padding: 12px; border-radius: 6px; margin: 15px 0 5px 0;">
        <h4 style="color: #2e7d32; margin: 0 0 8px 0;">AI Recommendation:</h4>
        <p style="margin: 0; color: #2e7d32;">
        """
        
        if score >= 0.7:
            html += "Strong evidence of explicit positionality statements. Recommend <b>Accept AI Findings</b> → Explicit."
        elif score >= 0.4:
            html += "Moderate evidence suggests subtle reflexivity. Recommend <b>Accept AI Findings</b> → Subtle/Implicit."
        elif score > 0:
            html += "Weak indicators found. Recommend <b>Manual Review</b> for thorough analysis."
        else:
            html += "No clear positionality detected. Recommend <b>Reject</b> → No positionality statements."
            
        html += "</p></div></div>"
            
        return html
    
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
        
        # Set judgment based on AI confidence
        if result['positionality_score'] >= 0.7:
            self.judgment_buttons['positive_explicit'].setChecked(True)
        elif result['positionality_score'] >= 0.4:
            self.judgment_buttons['positive_subtle'].setChecked(True)
        else:
            self.judgment_buttons['uncertain'].setChecked(True)
            
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
        
        # Set confidence based on AI score (scale 1-5)
        ai_confidence = min(5, max(2, int(result['positionality_score'] * 5) + 1))
        self.confidence_slider.setValue(ai_confidence)
        
        # Add AI assistance note to pattern suggestions
        patterns = ', '.join(result['positionality_tests'])
        ai_note = f"AI-detected patterns: {patterns}"
        if locations_found:
            ai_note += f"\nLocations: {', '.join(set(locations_found))}"
        self.pattern_suggestions.setPlainText(ai_note)
        
        location_text = self.location_dropdown.currentText()
        self.statusBar().showMessage(f"AI findings accepted! Location: {location_text}", 3000)
        
    def quick_reject_findings(self):
        """Reject AI findings and proceed with manual review"""
        # Clear AI findings and reset for manual work
        self.ai_findings.clear()
        self.analysis_status.setText("Manual review mode")
        self.quick_accept_btn.setEnabled(False)
        self.quick_reject_btn.setEnabled(False)
        
        # Set default negative judgment for manual verification
        self.judgment_buttons['negative'].setChecked(True)
        self.confidence_slider.setValue(3)
        
        self.statusBar().showMessage("Manual review mode - read the full paper carefully", 3000)
    
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