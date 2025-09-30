#!/usr/bin/env python3
"""
Test Enhanced Patterns on Real Papers

This script tests our enhanced patterns against the real academic papers
to see what additional positionality statements we can detect.
"""

import sys
import os
sys.path.insert(0, '/home/todd/py-extractor')

import pdfplumber
import re
from enhanced_patterns import ENHANCED_PATTERNS

def test_enhanced_patterns_on_paper(pdf_path):
    """Test enhanced patterns against a real paper"""
    
    print(f"\n📄 TESTING ENHANCED PATTERNS: {os.path.basename(pdf_path)}")
    print("=" * 80)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
            
        print(f"📊 Paper length: {len(full_text)} characters, {len(pdf.pages)} pages")
        
        # Test each enhanced pattern
        matches_found = {}
        total_matches = 0
        
        for pattern_name, pattern in ENHANCED_PATTERNS.items():
            matches = list(pattern.finditer(full_text))
            if matches:
                matches_found[pattern_name] = []
                for match in matches[:3]:  # Show first 3 matches
                    start, end = match.span()
                    # Get context around match
                    context_start = max(0, start - 50)
                    context_end = min(len(full_text), end + 50)
                    context = full_text[context_start:context_end]
                    context = ' '.join(context.split())  # Clean whitespace
                    
                    matches_found[pattern_name].append({
                        'text': match.group(),
                        'context': context,
                        'position': (start, end)
                    })
                total_matches += len(matches)
        
        # Report results
        print(f"\n✅ ENHANCED PATTERN RESULTS:")
        print(f"   Total patterns matched: {len(matches_found)}/{len(ENHANCED_PATTERNS)}")
        print(f"   Total matches found: {total_matches}")
        
        if matches_found:
            print(f"\n💡 DETAILED MATCHES:")
            for pattern_name, matches in matches_found.items():
                print(f"\n   🎯 {pattern_name}: {len(matches)} matches")
                for i, match in enumerate(matches, 1):
                    print(f"      {i}. \"{match['text']}\"")
                    print(f"         Context: ...{match['context']}...")
        else:
            print(f"\n❌ No enhanced patterns matched.")
            print(f"   This could mean:")
            print(f"   - The paper discusses positionality theoretically rather than personally")
            print(f"   - Authors use different language patterns than our enhanced set")
            print(f"   - The paper may be about positionality but not contain author reflexivity")
        
        # Look for potential patterns we might have missed
        print(f"\n🔍 POTENTIAL MISSED PATTERNS:")
        first_person_patterns = [
            r'\bI\s+\w+',  # Any "I ..." patterns
            r'\bmy\s+\w+', # Any "my ..." patterns  
            r'\bwe\s+\w+', # Any "we ..." patterns
        ]
        
        for pattern_desc, pattern_str in [
            ("First person 'I'", r'\bI\s+\w+'),
            ("First person 'my'", r'\bmy\s+\w+'),
            ("Author voice 'we'", r'\bwe\s+\w+')
        ]:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            matches = pattern.findall(full_text)
            if matches:
                unique_matches = list(set(matches))[:5]  # First 5 unique
                print(f"   {pattern_desc}: {len(unique_matches)} unique patterns")
                print(f"      Examples: {', '.join(unique_matches[:3])}")
        
        return matches_found
        
    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")
        return {}

def main():
    papers = [
        'sample_pdfs/Knight-NeithernorThere-2016.pdf',
        'sample_pdfs/Moser-PersonalityNewPositionality-2008.pdf'
    ]
    
    all_results = {}
    
    for paper in papers:
        if os.path.exists(paper):
            results = test_enhanced_patterns_on_paper(paper)
            all_results[paper] = results
        else:
            print(f"❌ Paper not found: {paper}")
    
    # Summary comparison
    print(f"\n📋 SUMMARY COMPARISON")
    print("=" * 80)
    
    for paper, results in all_results.items():
        paper_name = os.path.basename(paper)
        pattern_count = len(results)
        total_matches = sum(len(matches) for matches in results.values())
        print(f"{paper_name:40} | {pattern_count:2d} patterns | {total_matches:2d} total matches")
    
    if any(all_results.values()):
        print(f"\n🎯 RECOMMENDATION: Enhanced patterns found additional positionality content!")
        print(f"   Consider integrating these patterns into the main detection system.")
    else:
        print(f"\n💭 OBSERVATION: These papers may discuss positionality conceptually")
        print(f"   rather than containing personal reflexive statements by authors.")

if __name__ == "__main__":
    main()