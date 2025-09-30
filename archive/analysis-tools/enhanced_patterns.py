#!/usr/bin/env python3
"""
Enhanced Positionality Detection Patterns

This file contains improved patterns based on analysis of academic literature
and common positionality statement structures. These can be added to 
metadata_extractor.py to improve detection accuracy.
"""

import re

# Enhanced patterns for better positionality detection
ENHANCED_PATTERNS = {
    
    # 1. STRONGER REFLEXIVE LANGUAGE
    "enhanced_reflexive": re.compile(
        r"\bI\s+(?:must|should|cannot\s+help\s+but|am\s+forced\s+to|need\s+to)\s+"
        r"(?:acknowledge|recognize|admit|note|reflect\s+on|consider|confess)", 
        re.IGNORECASE
    ),
    
    # 2. EXPANDED IDENTITY CATEGORIES
    "expanded_identity": re.compile(
        r"\bAs\s+a\s+(?:Black|White|Latina?o?|Hispanic|Asian|Indigenous|Native|"
        r"queer|trans|LGBTQ|disabled|working.class|first.generation|immigrant|"
        r"veteran|single\s+mother|non.traditional)[^.]{0,80}"
        r"(?:researcher|scholar|woman|man|person|student|academic)", 
        re.IGNORECASE
    ),
    
    # 3. INSTITUTIONAL POSITIONING
    "institutional_position": re.compile(
        r"\b(?:My|Our)\s+(?:position|role|status)\s+as\s+[^.]{10,60}"
        r"(?:shapes?|influences?|affects?|informs?)", 
        re.IGNORECASE
    ),
    
    # 4. METHODOLOGICAL REFLEXIVITY
    "methodological_reflexivity": re.compile(
        r"\b(?:reflexiv|self.reflexiv|auto.ethnograph)[^.]{0,50}"
        r"(?:approach|methodology|method|practice|stance)", 
        re.IGNORECASE
    ),
    
    # 5. PRIVILEGE/POWER ACKNOWLEDGMENT
    "privilege_awareness": re.compile(
        r"\b(?:acknowledge|recognize|aware\s+of)\s+(?:my|our)\s+"
        r"(?:privilege|power|advantages?|position\s+of\s+privilege)", 
        re.IGNORECASE
    ),
    
    # 6. INSIDER/OUTSIDER STATUS
    "insider_outsider": re.compile(
        r"\b(?:insider|outsider)\s+(?:status|position|perspective|knowledge|"
        r"to\s+the\s+community|researcher)", 
        re.IGNORECASE
    ),
    
    # 7. LIVED EXPERIENCE REFERENCES
    "lived_experience": re.compile(
        r"\b(?:my|our)\s+(?:lived\s+experience|personal\s+experience|"
        r"own\s+experience)[^.]{10,80}(?:informs?|shapes?|influences?)", 
        re.IGNORECASE
    ),
    
    # 8. DISCLOSURE OF BACKGROUND
    "background_disclosure": re.compile(
        r"\bI\s+(?:come\s+from|grew\s+up|was\s+raised|identify\s+as)[^.]{10,80}"
        r"(?:which|this|that)[^.]{10,40}(?:influence|shape|affect)", 
        re.IGNORECASE
    ),
    
    # 9. SUBJECTIVITY ACKNOWLEDGMENT
    "subjectivity_explicit": re.compile(
        r"\b(?:subjective|partial|biased|limited)\s+(?:nature\s+of|"
        r"lens|perspective|viewpoint|interpretation)", 
        re.IGNORECASE
    ),
    
    # 10. POWER DYNAMICS AWARENESS
    "power_dynamics": re.compile(
        r"\bpower\s+(?:dynamic|relation|structure|differential)[^.]{0,50}"
        r"(?:between|with|in\s+the)", 
        re.IGNORECASE
    ),
    
    # 11. CULTURAL POSITIONING
    "cultural_positioning": re.compile(
        r"\b(?:cultural|ethnic|racial)\s+(?:background|identity|heritage)[^.]{10,60}"
        r"(?:inform|shape|influence|affect)", 
        re.IGNORECASE
    ),
    
    # 12. REFLEXIVE RESEARCH PRACTICE
    "reflexive_practice": re.compile(
        r"\breflexive\s+(?:research|practice|inquiry|approach|engagement)", 
        re.IGNORECASE
    )
}

def test_enhanced_patterns(text_sample):
    """Test enhanced patterns against a text sample"""
    results = {}
    for name, pattern in ENHANCED_PATTERNS.items():
        matches = pattern.findall(text_sample)
        if matches:
            results[name] = matches
    return results

# Example usage and testing
if __name__ == "__main__":
    # Test examples that current system might miss
    test_cases = [
        "I must acknowledge my privilege as a White researcher working in communities of color.",
        "My cultural background as a first-generation immigrant shapes my understanding of educational barriers.",
        "I cannot help but recognize that my position as an insider to this community affects my interpretation.",
        "The reflexive research approach requires constant examination of power dynamics.",
        "I come from a working-class background, which influences how I approach questions of social mobility.",
        "My lived experience as a disabled researcher informs my methodological choices.",
        "I recognize the partial nature of my perspective as an outsider to this community."
    ]
    
    print("Testing Enhanced Positionality Patterns")
    print("=" * 50)
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_text}")
        results = test_enhanced_patterns(test_text)
        if results:
            for pattern_name, matches in results.items():
                print(f"  ✅ {pattern_name}: {matches}")
        else:
            print("  ❌ No matches")