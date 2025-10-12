"""
Text cleaning utilities for PDF extraction
Removes excessive whitespace and improves formatting
"""

import re

def clean_pdf_text(text):
    """
    Clean up PDF-extracted text for better readability.
    
    Fixes:
    - Multiple consecutive spaces → single space
    - Spaces before punctuation
    - Preserves paragraph breaks
    
    Args:
        text: Raw text extracted from PDF
        
    Returns:
        Cleaned text with proper formatting
    """
    if not text:
        return text
    
    # Replace multiple spaces with single space
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove spaces before punctuation
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    
    # Remove spaces after opening brackets/quotes
    text = re.sub(r'([(\["])\s+', r'\1', text)
    
    # Remove spaces before closing brackets/quotes
    text = re.sub(r'\s+([])\]"])', r'\1', text)
    
    # Normalize line breaks - preserve paragraph structure
    lines = text.split('\n')
    
    # Group into paragraphs (blank line = paragraph break)
    paragraphs = []
    current_para = []
    
    for line in lines:
        line = line.strip()
        if not line:
            # Blank line - end current paragraph
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
        else:
            current_para.append(line)
    
    # Don't forget last paragraph
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    # Join paragraphs with double newline for readability
    return '\n\n'.join(paragraphs)


def clean_selection_text(text):
    """
    Quick clean for selected text (less aggressive than full clean).
    Use this for "Copy to Evidence" functionality.
    """
    if not text:
        return text
    
    # Just normalize spaces and line breaks
    text = re.sub(r' {2,}', ' ', text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return ' '.join(lines)
