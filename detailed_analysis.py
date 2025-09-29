#!/usr/bin/env python3
"""
Detailed Positionality Analysis

This script provides more detailed output showing exactly what patterns matched
and where, plus suggestions for improvement.
"""

import sys
import os
sys.path.insert(0, '/home/todd/py-extractor')

from metadata_extractor import extract_metadata, extract_positionality
import pdfplumber
import re

def analyze_paper_detailed(pdf_path):
    """Provide detailed analysis of positionality detection"""
    
    print(f"\n📄 ANALYZING: {os.path.basename(pdf_path)}")
    print("=" * 80)
    
    # 1. Extract full metadata
    metadata = extract_metadata(pdf_path)
    
    print(f"📝 Basic Info:")
    print(f"   Title: {metadata.get('title', 'Not found')}")
    print(f"   Author: {metadata.get('author', 'Not found')}")
    print(f"   DOI: {metadata.get('doi', 'Not found')}")
    
    # 2. Show positionality results
    pos_score = metadata.get('positionality_score', 0.0)
    pos_tests = metadata.get('positionality_tests', [])
    pos_snippets = metadata.get('positionality_snippets', {})
    
    print(f"\n🎯 Current Detection:")
    print(f"   Score: {pos_score:.3f}")
    print(f"   Confidence: {metadata.get('positionality_confidence', 'unknown')}")
    print(f"   Patterns matched: {', '.join(pos_tests) if pos_tests else 'None'}")
    
    # 3. Show actual matched text
    if pos_snippets:
        print(f"\n💬 Matched Text:")
        for pattern, snippet in pos_snippets.items():
            print(f"   {pattern}: \"{snippet}\"")
    
    # 4. Extract some sample text for manual review
    print(f"\n📖 Text Samples for Manual Review:")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # First page
            page1_text = pdf.pages[0].extract_text() or ""
            print(f"\n   🔍 First page (first 500 chars):")
            print(f"   {page1_text[:500]}...")
            
            # Look for potential positionality keywords
            keywords = ['positionality', 'position', 'reflexiv', 'I acknowledge', 
                       'my perspective', 'as a researcher', 'my background',
                       'privilege', 'identity', 'insider', 'outsider']
            
            full_text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
            
            print(f"\n   🔍 Keyword Context Search:")
            for keyword in keywords:
                pattern = re.compile(rf'.{{0,50}}{re.escape(keyword)}.{{0,50}}', re.IGNORECASE)
                matches = pattern.findall(full_text)
                if matches:
                    print(f"      '{keyword}': {len(matches)} matches")
                    for i, match in enumerate(matches[:2], 1):  # Show first 2 matches
                        clean_match = ' '.join(match.split())
                        print(f"         {i}. \"{clean_match}\"")
                        
    except Exception as e:
        print(f"   Error extracting text: {e}")
    
    return metadata

def main():
    if len(sys.argv) != 2:
        print("Usage: python detailed_analysis.py <pdf_file>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    analyze_paper_detailed(pdf_path)

if __name__ == "__main__":
    main()