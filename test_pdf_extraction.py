#!/usr/bin/env python3
"""
Simple test script to verify PDF text extraction is working correctly
"""

import fitz
import sys
import os

def test_pdf_text_extraction(pdf_path):
    """Test text extraction from a PDF file"""
    print(f"Testing PDF text extraction: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return
    
    try:
        doc = fitz.open(pdf_path)
        print(f"✅ PDF opened successfully, {len(doc)} pages")
        
        # Test first page
        page = doc[0]
        print(f"\n📄 Page 1 analysis:")
        
        # Method 1: Simple text extraction
        simple_text = page.get_text()
        print(f"Simple text length: {len(simple_text)} characters")
        if simple_text:
            print(f"First 100 chars: '{simple_text[:100]}...'")
        
        # Method 2: Structured text extraction
        text_dict = page.get_text("dict")
        print(f"\n📊 Structured text analysis:")
        
        text_blocks = []
        for block in text_dict["blocks"]:
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        span_text = span.get("text", "").strip()
                        if span_text:
                            bbox = span["bbox"]
                            text_blocks.append({
                                "text": span_text,
                                "bbox": bbox
                            })
        
        print(f"Text blocks found: {len(text_blocks)}")
        if text_blocks:
            print("Sample text blocks:")
            for i, block in enumerate(text_blocks[:5]):
                print(f"  {i+1}. '{block['text'][:50]}...' at {block['bbox']}")
        
        # Test zoom transformation
        zoom = 1.5
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        print(f"\n🔍 Zoom test (150%): Rendered {pix.width}x{pix.height} pixels")
        
        doc.close()
        return text_blocks
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # Test with a known PDF if available
        test_files = [
            "/Users/todd/pdfs/cycyk-et-al-2022-moving-through-the-pipeline-ethnic-and-linguistic-disparities-in-special-education-from-birth-through.pdf",
            "test.pdf",
            "sample.pdf"
        ]
        
        pdf_path = None
        for test_file in test_files:
            if os.path.exists(test_file):
                pdf_path = test_file
                break
        
        if not pdf_path:
            print("❌ No test PDF found. Usage: python test_pdf_extraction.py <pdf_path>")
            return
    
    test_pdf_text_extraction(pdf_path)

if __name__ == "__main__":
    main()