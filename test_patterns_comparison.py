#!/usr/bin/env python3
"""
Test Current vs Enhanced Patterns on Real Statements

Test the actual reflexive statements we found against both current and enhanced patterns.
"""

import sys
import os
sys.path.insert(0, '/home/todd/py-extractor')

import re
from enhanced_patterns import ENHANCED_PATTERNS

# Current patterns from metadata_extractor.py
CURRENT_PATTERNS = {
    "explicit_positionality": re.compile(r"\b(?:My|Our) positionality\b", re.IGNORECASE),
    "positionality_term": re.compile(r"\bpositionalit\w*\b", re.IGNORECASE),
    "first_person_reflexivity": re.compile(r"\bI\s+(?:reflect|acknowledge|consider|recognize|admit|confess|must acknowledge|should note)\b", re.IGNORECASE),
    "researcher_positioning": re.compile(r"\bI,?\s*as (?:a |the )?(?:researcher|scholar|author),", re.IGNORECASE),
    "identity_disclosure": re.compile(r"\bAs a (?:woman|man|Black|White|Latina?|Asian|Indigenous|queer|trans|disabled|working.class)[^.]{0,50}(?:researcher|scholar|I)\b", re.IGNORECASE),
    "reflexive_awareness": re.compile(r"\b(?:acknowledge|recognize|aware|conscious) (?:that )?(?:my|our) [^.]{10,60}(?:influence|affect|shape|bias|perspective|position)", re.IGNORECASE),
    "background_influence": re.compile(r"\b(?:My|Our) (?:background|experience|identity|perspective) [^.]{10,80}(?:influence|shape|inform|affect)", re.IGNORECASE),
    "positioned_researcher": re.compile(r"\b(?:positioned|situated) as [^.]{10,60}(?:researcher|scholar)", re.IGNORECASE),
    "disclosure_statement": re.compile(r"\b(?:I|We) (?:bring|carry|hold) [^.]{10,60}(?:perspective|lens|experience|bias)", re.IGNORECASE),
}

def test_patterns_on_statements():
    """Test both current and enhanced patterns on real statements from the papers"""
    
    # Real statements found in the papers
    real_statements = [
        # From Knight paper
        "In order to be consistent with the subject of this article, it is important that we articulate our own cultural locations and positionalities as authors",
        "Delineating our positionalities supports the notion that our positions may influence curriculum and research",
        "It is from this context that we position ourselves as authors of this critical essay",
        "As individuals, we make assumptions based on our positionality",
        "Our position is a political point of departure",
        
        # From Moser paper  
        "Through discussion of my fieldwork experiences in Indonesia, I will illustrate some of the limitations of how positionality has been discussed",
        "This paper has developed out of my experiences conducting fieldwork in Indonesia",
        "However, as I got to know us, I observed that the ways in which we were treated and talked about by the locals",
        "I became aware that my position in the field was determined as much by how I conducted myself",
        "While it was clear to me that the vastly different social interactions with our research subjects must be important",
    ]
    
    print("🔬 TESTING PATTERNS ON REAL REFLEXIVE STATEMENTS")
    print("=" * 80)
    
    for i, statement in enumerate(real_statements, 1):
        print(f"\n📝 Statement {i}:")
        print(f"   \"{statement[:100]}{'...' if len(statement) > 100 else ''}\"")
        
        # Test current patterns
        current_matches = []
        for name, pattern in CURRENT_PATTERNS.items():
            if pattern.search(statement):
                current_matches.append(name)
        
        # Test enhanced patterns
        enhanced_matches = []
        for name, pattern in ENHANCED_PATTERNS.items():
            if pattern.search(statement):
                enhanced_matches.append(name)
        
        print(f"   📊 Current patterns: {len(current_matches)} matches")
        if current_matches:
            print(f"      ✅ {', '.join(current_matches)}")
        else:
            print(f"      ❌ No matches")
            
        print(f"   📈 Enhanced patterns: {len(enhanced_matches)} matches")
        if enhanced_matches:
            print(f"      ✅ {', '.join(enhanced_matches)}")
        else:
            print(f"      ❌ No matches")
        
        # Improvement indicator
        if enhanced_matches and not current_matches:
            print(f"      🎯 IMPROVEMENT: Enhanced patterns caught this statement!")
        elif len(enhanced_matches) > len(current_matches):
            print(f"      📈 IMPROVEMENT: Enhanced patterns found more matches!")
    
    # Summary
    total_statements = len(real_statements)
    current_caught = sum(1 for stmt in real_statements 
                        if any(pattern.search(stmt) for pattern in CURRENT_PATTERNS.values()))
    enhanced_caught = sum(1 for stmt in real_statements 
                         if any(pattern.search(stmt) for pattern in ENHANCED_PATTERNS.values()))
    
    print(f"\n📊 SUMMARY COMPARISON")
    print("=" * 40)
    print(f"Total reflexive statements: {total_statements}")
    print(f"Current system catches: {current_caught}/{total_statements} ({current_caught/total_statements*100:.1f}%)")
    print(f"Enhanced system catches: {enhanced_caught}/{total_statements} ({enhanced_caught/total_statements*100:.1f}%)")
    
    if enhanced_caught > current_caught:
        improvement = enhanced_caught - current_caught
        print(f"🎯 IMPROVEMENT: +{improvement} statements ({improvement/total_statements*100:.1f}% better)")
    
    return current_caught, enhanced_caught

if __name__ == "__main__":
    test_patterns_on_statements()