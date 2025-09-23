#!/usr/bin/env python3
"""
Analyze false negative papers to understand missed positionality patterns.
This will help us improve the regex detection system.
"""

import os
import re
import pdfplumber
from collections import Counter

def extract_sample_text(pdf_path, sections=["header", "middle", "conclusion"]):
    """Extract text samples from different sections of the PDF"""
    samples = {}
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            # Header: first page
            if "header" in sections and total_pages > 0:
                samples["header"] = pdf.pages[0].extract_text() or ""
            
            # Middle: around page 1/3 through
            if "middle" in sections and total_pages > 2:
                mid_page = total_pages // 3
                samples["middle"] = pdf.pages[mid_page].extract_text() or ""
            
            # Conclusion: last 2 pages
            if "conclusion" in sections and total_pages > 1:
                conclusion_text = ""
                for page in pdf.pages[-2:]:
                    conclusion_text += page.extract_text() or ""
                samples["conclusion"] = conclusion_text
                
    except Exception as e:
        print(f"Error extracting from {pdf_path}: {e}")
        
    return samples

def find_potential_positionality(text, context_name=""):
    """Find potential positionality statements using broader patterns"""
    
    # More comprehensive patterns to catch academic positionality language
    patterns = {
        # Current patterns (for comparison)
        "current_explicit": r"\b(?:My|Our) positionality\b",
        "current_reflexivity": r"\bI\s+(?:reflect|acknowledge|consider|recognize)\b",
        "current_researcher": r"\bI,?\s*as a researcher,",
        
        # Enhanced patterns for academic writing
        "identity_disclosure": r"\bAs a (?:woman|man|Black|White|Latina?|Asian|Indigenous|queer|trans|disabled|working.class)[^.]{0,50}(?:researcher|scholar|I)\b",
        "background_statement": r"\b(?:My|Our) (?:background|experience|identity|perspective) as [^.]{10,80}",
        "reflexive_awareness": r"\b(?:acknowledge|recognize|aware|conscious) (?:that )?(?:my|our) [^.]{10,60}(?:influence|affect|shape|bias)",
        "positioned_researcher": r"\b(?:positioned|situated) as [^.]{10,60}(?:researcher|scholar)",
        "disclosure_statement": r"\b(?:I|We) (?:bring|carry|hold) [^.]{10,60}(?:perspective|lens|experience)",
        "reflexive_I": r"\bI (?:must |should |cannot |can )?(?:acknowledge|note|recognize|admit|confess) [^.]{10,100}(?:bias|position|perspective|influence)",
        "methodological_reflexivity": r"\b(?:reflexiv|positional)[^.]{0,30}(?:methodology|approach|stance)",
        "insider_outsider": r"\b(?:insider|outsider) (?:perspective|position|status)[^.]{0,50}",
        "social_location": r"\bsocial location[^.]{0,50}",
        "standpoint_theory": r"\b(?:standpoint|situated knowledge)[^.]{0,30}",
    }
    
    findings = []
    
    for pattern_name, pattern in patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            # Get context around the match
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            context = text[start:end].strip()
            
            findings.append({
                "pattern": pattern_name,
                "match": match.group(0),
                "context": context,
                "section": context_name,
                "position": match.start()
            })
    
    return findings

def analyze_paper(pdf_path):
    """Comprehensive analysis of a single paper"""
    filename = os.path.basename(pdf_path)
    print(f"\n📄 ANALYZING: {filename}")
    print("=" * 60)
    
    # Extract text samples
    samples = extract_sample_text(pdf_path)
    
    all_findings = []
    
    for section_name, text in samples.items():
        if not text.strip():
            continue
            
        print(f"\n📍 {section_name.upper()} SECTION ({len(text)} chars)")
        print("-" * 30)
        
        findings = find_potential_positionality(text, section_name)
        
        if findings:
            for finding in findings:
                print(f"🔍 Pattern: {finding['pattern']}")
                print(f"   Match: '{finding['match']}'")
                print(f"   Context: ...{finding['context']}...")
                print()
                all_findings.append(finding)
        else:
            print("   No positionality patterns detected")
    
    # Summary
    if all_findings:
        pattern_counts = Counter(f["pattern"] for f in all_findings)
        print(f"\n📊 SUMMARY: {len(all_findings)} potential matches found")
        for pattern, count in pattern_counts.most_common():
            print(f"   {pattern}: {count}")
    else:
        print(f"\n📊 SUMMARY: No positionality language detected")
        print("   This may explain why it's a false negative!")
    
    return all_findings

def main():
    # Papers that should be POSITIVE but are currently NEGATIVE
    false_negative_papers = [
        "Dean-ReflexivityLimitsStudy-2021.pdf",
        "Parks-ObstaclesAddressingRace-2012.pdf", 
        "Vries-Transgenderpeoplecolor-2015.pdf"
    ]
    
    PDF_DIR = "/Users/todd/pdfs"
    
    print("🔍 ANALYZING FALSE NEGATIVE PAPERS")
    print("=" * 80)
    print("Looking for missed positionality patterns in papers that should be detected...")
    
    all_patterns_found = []
    
    for filename in false_negative_papers:
        pdf_path = os.path.join(PDF_DIR, filename)
        
        if not os.path.exists(pdf_path):
            print(f"⚠️  File not found: {filename}")
            continue
            
        try:
            findings = analyze_paper(pdf_path)
            all_patterns_found.extend(findings)
        except Exception as e:
            print(f"❌ Error analyzing {filename}: {e}")
    
    # Overall analysis
    print("\n" + "=" * 80)
    print("🎯 OVERALL PATTERN ANALYSIS")
    print("=" * 80)
    
    if all_patterns_found:
        pattern_summary = Counter(f["pattern"] for f in all_patterns_found)
        print(f"Total potential matches found: {len(all_patterns_found)}")
        print("\nMost common missed patterns:")
        for pattern, count in pattern_summary.most_common(10):
            print(f"  {count:2d}x {pattern}")
            
        print("\n💡 RECOMMENDATIONS:")
        print("1. Add the most frequent patterns to regex detection")
        print("2. Focus on 'identity_disclosure' and 'reflexive_awareness' patterns")
        print("3. Consider academic writing style variations")
        
    else:
        print("No positionality language found in any false negative papers!")
        print("This suggests either:")
        print("1. The papers don't actually contain positionality statements")
        print("2. The language is too subtle for pattern matching")
        print("3. Positionality statements are in unexpected locations")

if __name__ == "__main__":
    main()