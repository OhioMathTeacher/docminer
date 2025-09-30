#!/usr/bin/env python3
"""
Deep dive into paper content to manually inspect for positionality language
"""

import pdfplumber
import os

def extract_full_text_sample(pdf_path, max_chars=2000):
    """Extract a readable sample of text from the paper"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for i, page in enumerate(pdf.pages[:3]):  # First 3 pages
                page_text = page.extract_text() or ""
                full_text += f"\n--- PAGE {i+1} ---\n{page_text}"
                if len(full_text) > max_chars:
                    break
            return full_text[:max_chars] + "..." if len(full_text) > max_chars else full_text
    except Exception as e:
        return f"Error reading PDF: {e}"

def manual_inspection(pdf_path):
    """Manual inspection of paper content"""
    filename = os.path.basename(pdf_path)
    print(f"\n📖 MANUAL INSPECTION: {filename}")
    print("=" * 80)
    
    text_sample = extract_full_text_sample(pdf_path, 3000)
    print("FIRST 3000 CHARACTERS:")
    print("-" * 40)
    print(text_sample)
    
    print("\n" + "="*80)
    print("MANUAL ANALYSIS QUESTIONS:")
    print("1. Does this paper actually contain positionality statements?")
    print("2. Are there subtle first-person reflective statements?")
    print("3. Does the author discuss their background/identity?")
    print("4. Is there any reflexivity about research position?")
    print("="*80)

def main():
    papers_to_inspect = [
        "Parks-ObstaclesAddressingRace-2012.pdf",
        "Vries-Transgenderpeoplecolor-2015.pdf"
    ]
    
    PDF_DIR = "/Users/todd/pdfs"
    
    for filename in papers_to_inspect:
        pdf_path = os.path.join(PDF_DIR, filename)
        if os.path.exists(pdf_path):
            manual_inspection(pdf_path)
        else:
            print(f"File not found: {filename}")

if __name__ == "__main__":
    main()