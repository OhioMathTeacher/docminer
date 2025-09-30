#!/usr/bin/env python3
"""
Test script to demonstrate PDF dimension extraction functionality.
This shows how to get exact PDF page dimensions for proper viewer sizing.
"""

import os
from enhanced_training_interface import get_pdf_page_info

def test_pdf_dimensions():
    """Test PDF dimension extraction on available PDFs"""
    
    # Look for PDF files in common locations
    pdf_paths = []
    
    # Check sample_pdfs directory
    sample_dir = "sample_pdfs"
    if os.path.exists(sample_dir):
        for file in os.listdir(sample_dir):
            if file.lower().endswith('.pdf'):
                pdf_paths.append(os.path.join(sample_dir, file))
    
    # Check root directory
    for file in os.listdir('.'):
        if file.lower().endswith('.pdf'):
            pdf_paths.append(file)
    
    if not pdf_paths:
        print("No PDF files found to test!")
        return
    
    print("=== PDF Dimension Analysis ===\n")
    
    for pdf_path in pdf_paths[:3]:  # Test first 3 PDFs found
        print(f"📄 Analyzing: {pdf_path}")
        
        info = get_pdf_page_info(pdf_path, 0)  # First page
        
        if info:
            dims = info['dimensions']
            print(f"   📏 Page 1 of {info['total_pages']}")
            print(f"   📐 Dimensions: {dims['points']['width']:.1f} × {dims['points']['height']:.1f} points")
            print(f"   📏 In inches: {dims['inches']['width']:.1f} × {dims['inches']['height']:.1f}")
            print(f"   🖥️  At 72 DPI: {dims['pixels_72dpi']['width']} × {dims['pixels_72dpi']['height']} pixels")
            print(f"   🖥️  At 150 DPI: {dims['pixels_150dpi']['width']} × {dims['pixels_150dpi']['height']} pixels")
            print(f"   📊 Aspect ratio: {info['aspect_ratio']:.3f}")
            print(f"   🔄 Orientation: {info['orientation']}")
            
            # Show how to calculate proper viewer size
            width_150dpi = dims['pixels_150dpi']['width']
            height_150dpi = dims['pixels_150dpi']['height']
            margin = 40  # 20px margin on each side
            
            print(f"   🎯 Recommended viewer size: {width_150dpi + margin} × {height_150dpi + margin} pixels (with margins)")
            
        else:
            print(f"   ❌ Could not read PDF dimensions")
        
        print()

if __name__ == "__main__":
    test_pdf_dimensions()