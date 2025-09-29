#!/usr/bin/env python3
"""
Manual First-Person Statement Finder

Look for actual first-person reflexive statements that our patterns might be missing.
"""

import sys
import os
sys.path.insert(0, '/home/todd/py-extractor')

import pdfplumber
import re

def find_first_person_statements(pdf_path):
    """Find potential first-person reflexive statements"""
    
    print(f"\n📄 SEARCHING FOR FIRST-PERSON STATEMENTS: {os.path.basename(pdf_path)}")
    print("=" * 80)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
        
        # Look for sentences with first-person reflexive language
        sentences = re.split(r'[.!?]+', full_text)
        
        potential_statements = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:  # Skip very short fragments
                continue
                
            # Look for first-person reflexive patterns
            if re.search(r'\b(I|my|we|our)\b', sentence, re.IGNORECASE):
                # Check for reflexive/positioning keywords
                reflexive_keywords = [
                    'acknowledge', 'recognize', 'realize', 'understand', 'admit',
                    'position', 'perspective', 'experience', 'background', 
                    'identity', 'culture', 'privilege', 'bias', 'assumption',
                    'reflexiv', 'reflect', 'situated', 'locate', 'outsider', 'insider'
                ]
                
                for keyword in reflexive_keywords:
                    if re.search(rf'\b{keyword}', sentence, re.IGNORECASE):
                        potential_statements.append({
                            'sentence': sentence[:200] + ('...' if len(sentence) > 200 else ''),
                            'keyword': keyword,
                            'first_person': True
                        })
                        break
        
        # Remove duplicates and clean up
        seen = set()
        unique_statements = []
        for stmt in potential_statements:
            key = stmt['sentence'][:100]  # Use first 100 chars as key
            if key not in seen:
                seen.add(key)
                unique_statements.append(stmt)
        
        print(f"🔍 Found {len(unique_statements)} potential first-person reflexive statements:")
        
        if unique_statements:
            for i, stmt in enumerate(unique_statements[:8], 1):  # Show first 8
                print(f"\n{i}. Keyword: '{stmt['keyword']}'")
                print(f"   Text: \"{stmt['sentence']}\"")
        else:
            print("   ❌ No clear first-person reflexive statements found.")
            print("   This suggests the paper discusses positionality theoretically")
            print("   rather than the authors reflecting on their own positions.")
        
        return unique_statements
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    papers = [
        'sample_pdfs/Knight-NeithernorThere-2016.pdf',
        'sample_pdfs/Moser-PersonalityNewPositionality-2008.pdf'
    ]
    
    for paper in papers:
        if os.path.exists(paper):
            find_first_person_statements(paper)
        else:
            print(f"❌ Paper not found: {paper}")

if __name__ == "__main__":
    main()