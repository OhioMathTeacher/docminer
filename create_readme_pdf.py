#!/usr/bin/env python3
"""
Create a README PDF for the training interface using PyMuPDF
"""

import fitz  # PyMuPDF
from pathlib import Path

def create_readme_pdf(output_path):
    """Create a README PDF using PyMuPDF"""
    
    # Create a new PDF document
    doc = fitz.open()
    page = doc.new_page()
    
    # Set up fonts and colors
    font_title = "helv"  # Helvetica
    font_body = "helv"
    
    # Page dimensions
    width = page.rect.width
    height = page.rect.height
    margin = 50
    y_pos = height - margin
    
    # Title
    title_text = "🎓 Search Buddy Training Interface"
    title_rect = fitz.Rect(margin, y_pos - 30, width - margin, y_pos)
    page.insert_text(title_rect.tl, title_text, fontsize=20, fontname=font_title, color=(0, 0, 1))
    y_pos -= 50
    
    # Subtitle
    subtitle_text = "Enhanced PDF Viewer & Positionality Detection Training"
    subtitle_rect = fitz.Rect(margin, y_pos - 15, width - margin, y_pos)
    page.insert_text(subtitle_rect.tl, subtitle_text, fontsize=14, fontname=font_body)
    y_pos -= 40
    
    # Content sections
    sections = [
        {
            "title": "🚀 Welcome!",
            "content": [
                "This is your training interface for improving the positionality detection system.",
                "You're currently viewing this README in the integrated PDF viewer - the same viewer",
                "you'll use to analyze academic papers for positionality statements."
            ]
        },
        {
            "title": "📋 Getting Started",
            "content": [
                "1. Add PDFs: Copy your academic papers to the ExtractorPDFs folder",
                "2. Select Text: Click and drag to highlight positionality statements", 
                "3. Make Judgments: Mark as positive/negative examples",
                "4. Add Evidence: Selected text automatically populates evidence fields",
                "5. Export Data: Save training data to improve the AI system"
            ]
        },
        {
            "title": "✨ Text Selection Features",
            "content": [
                "The PDF viewer includes professional text selection capabilities:",
                "• Line-based selection: Drag vertically to select entire lines",
                "• Word precision: Small selections target specific words", 
                "• Real-time highlighting: See selection as you drag",
                "• Automatic scrolling: Scroll through long documents",
                "• Instant text extraction: Selected text appears immediately below"
            ]
        },
        {
            "title": "🎯 What is Positionality?",
            "content": [
                "Positionality refers to statements where researchers reveal their identity,",
                "background, perspective, or relationship to their research topic. Look for:",
                "• Authors describing their personal background or identity",
                "• Statements about the researcher's relationship to the topic", 
                "• Acknowledgments of perspective or potential bias",
                "• References to the author's professional or personal experience"
            ]
        },
        {
            "title": "📝 Example Positionality Statements",
            "content": [
                '"As a former special education teacher, I bring firsthand experience..."',
                '"The author identifies as a Latino/Hispanic researcher studying Latino communities..."',
                '"My position as an outsider to this community required careful consideration..."'
            ]
        },
        {
            "title": "📁 Folder Management", 
            "content": [
                "Your PDFs are stored in the ExtractorPDFs folder in your home directory.",
                "The system remembers which PDFs you've loaded and will restore them on startup.",
                "You can change the default folder using the 'Select PDF Folder' button."
            ]
        },
        {
            "title": "💡 Training Tips",
            "content": [
                "• Include context around positionality statements for better training",
                "• Mark both clear positive AND negative examples", 
                "• Use pattern checkboxes to categorize different types",
                "• Save your work regularly to preserve training data"
            ]
        }
    ]
    
    # Add sections
    for section in sections:
        # Check if we need a new page
        if y_pos < 150:
            page = doc.new_page()
            y_pos = height - margin
            
        # Section title
        title_rect = fitz.Rect(margin, y_pos - 18, width - margin, y_pos)
        page.insert_text(title_rect.tl, section["title"], fontsize=16, fontname=font_title, color=(0, 0, 1))
        y_pos -= 25
        
        # Section content
        for line in section["content"]:
            if y_pos < 100:
                page = doc.new_page()
                y_pos = height - margin
                
            line_rect = fitz.Rect(margin, y_pos - 12, width - margin, y_pos)
            page.insert_text(line_rect.tl, line, fontsize=11, fontname=font_body)
            y_pos -= 16
            
        y_pos -= 10  # Extra space between sections
    
    # Footer
    if y_pos < 100:
        page = doc.new_page()
        y_pos = height - margin
    
    y_pos -= 30
    footer_text = "Ready to begin? Add some PDF files to your ExtractorPDFs folder and start training!"
    footer_rect = fitz.Rect(margin, y_pos - 15, width - margin, y_pos)
    page.insert_text(footer_rect.tl, footer_text, fontsize=12, fontname=font_body, color=(0.5, 0.5, 0.5))
    
    # Save the PDF
    doc.save(str(output_path))
    doc.close()
    return True

if __name__ == "__main__":
    output = Path("README_Training_Guide.pdf")
    create_readme_pdf(output)
    print(f"Created {output}")