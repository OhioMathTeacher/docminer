#!/usr/bin/env python3
"""
Enhanced positionality detection with improved patterns and fallbacks.
This module provides better detection when AI is unavailable.
"""

import re
import pdfplumber
from typing import Dict, List, Tuple

def enhanced_positionality_detection(pdf_path: str) -> Dict:
    """
    Enhanced positionality detection with comprehensive regex patterns
    and smart fallback mechanisms when AI is unavailable.
    """
    
    # Enhanced pattern library for academic positionality language
    POSITIONALITY_PATTERNS = {
        # Explicit positionality statements
        "explicit_positionality": r"\b(?:My|Our) positionality\b",
        "positionality_term": r"\bpositionalit\w*\b",
        
        # Identity and background disclosure
        "identity_disclosure": r"\bAs a (?:woman|man|Black|White|Latina?o?|Asian|Indigenous|queer|trans|disabled|working.class|first.generation)[^.]{0,80}(?:researcher|scholar|I)\b",
        "background_statement": r"\b(?:My|Our) (?:background|experience|identity|perspective) as [^.]{10,100}",
        "social_identity": r"\b(?:identify|identities) as (?:a |an )?(?:woman|man|Black|White|Latina?o?|Asian|Indigenous|queer|trans|disabled)[^.]{0,50}",
        
        # Reflexive awareness and acknowledgment
        "reflexive_awareness": r"\b(?:acknowledge|recognize|aware|conscious) (?:that )?(?:my|our) [^.]{5,80}(?:influence|affect|shape|bias|perspective|position|lens)",
        "bias_acknowledgment": r"\b(?:acknowledge|recognize|admit) (?:my|our) (?:own )?(?:bias|biases|assumptions|preconceptions|limitations)",
        "subjective_awareness": r"\b(?:my|our) (?:subjective|partial|limited) (?:perspective|view|understanding|lens)",
        
        # Researcher positioning
        "researcher_positioning": r"\bI,?\s*as (?:a |the )?(?:researcher|scholar|author|investigator),",
        "positioned_researcher": r"\b(?:positioned|situated) as (?:a |an )?(?:researcher|scholar|outsider|insider)",
        "researcher_role": r"\b(?:my|our) role as (?:a |the )?(?:researcher|scholar|investigator)",
        
        # First-person reflexive statements
        "first_person_reflexivity": r"\bI\s+(?:reflect|acknowledge|consider|recognize|admit|confess|must acknowledge|should note|cannot ignore)",
        "reflexive_questioning": r"\bI (?:wonder|question|ask myself|consider) [^.]{10,80}(?:position|perspective|bias|influence)",
        "self_examination": r"\bI (?:examine|explore|investigate) (?:my )?(?:own )?(?:assumptions|biases|position|perspective)",
        
        # Methodological reflexivity
        "methodological_reflexivity": r"\b(?:reflexiv|positional)[^.]{0,50}(?:methodology|approach|stance|analysis)",
        "reflexive_methodology": r"\breflexive (?:methodology|approach|analysis|practice)",
        "standpoint_theory": r"\b(?:standpoint theory|situated knowledge|feminist standpoint)",
        
        # Disclosure and transparency
        "disclosure_statement": r"\b(?:I|We) (?:bring|carry|hold) [^.]{10,80}(?:perspective|lens|experience|bias|assumptions)",
        "transparency_statement": r"\b(?:transparent|transparency) about (?:my|our) [^.]{10,60}(?:position|bias|perspective)",
        "position_statement": r"\b(?:position|stance) (?:myself|ourselves) as [^.]{10,60}",
        
        # Power and privilege awareness
        "privilege_acknowledgment": r"\b(?:acknowledge|recognize) (?:my|our) [^.]{5,50}(?:privilege|advantages|power)",
        "power_dynamics": r"\b(?:power dynamics|power relations) [^.]{5,50}(?:research|study|investigation)",
        "insider_outsider": r"\b(?:insider|outsider) (?:perspective|position|status|researcher)",
        
        # Limitations and boundaries
        "limitation_acknowledgment": r"\b(?:limitations? of|bounded by) (?:my|our) [^.]{10,60}(?:perspective|position|experience)",
        "boundary_awareness": r"\b(?:boundaries|limits) of (?:my|our) [^.]{10,50}(?:understanding|knowledge|perspective)",
    }
    
    results = {
        "positionality_tests": [],
        "positionality_snippets": {},
        "positionality_score": 0.0,
        "detection_method": "enhanced_regex"
    }
    
    try:
        # Extract text from different sections
        text_sections = extract_text_sections(pdf_path)
        
        # Apply pattern matching across all sections
        all_matches = []
        
        for section_name, text in text_sections.items():
            if not text.strip():
                continue
                
            section_matches = find_patterns_in_text(text, POSITIONALITY_PATTERNS, section_name)
            all_matches.extend(section_matches)
        
        # Process matches and calculate score
        if all_matches:
            results["positionality_tests"] = list(set(match["pattern"] for match in all_matches))
            
            # Store best snippets for each pattern
            for match in all_matches:
                pattern = match["pattern"]
                if pattern not in results["positionality_snippets"]:
                    results["positionality_snippets"][pattern] = match["context"]
            
            # Calculate confidence score based on matches
            results["positionality_score"] = calculate_confidence_score(all_matches)
        
        return results
        
    except Exception as e:
        print(f"Enhanced positionality detection failed for {pdf_path}: {e}")
        return results

def extract_text_sections(pdf_path: str) -> Dict[str, str]:
    """Extract text from different sections of the PDF"""
    sections = {}
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            # Introduction/Header (first 2 pages)
            if total_pages > 0:
                intro_text = ""
                for i in range(min(2, total_pages)):
                    intro_text += pdf.pages[i].extract_text() or ""
                sections["introduction"] = intro_text
            
            # Methods section (around 1/3 through)
            if total_pages > 3:
                methods_page = total_pages // 3
                sections["methods"] = pdf.pages[methods_page].extract_text() or ""
            
            # Discussion/Conclusion (last 2-3 pages)
            if total_pages > 2:
                conclusion_text = ""
                start_page = max(0, total_pages - 3)
                for i in range(start_page, total_pages):
                    conclusion_text += pdf.pages[i].extract_text() or ""
                sections["conclusion"] = conclusion_text
                
    except Exception as e:
        print(f"Error extracting text sections: {e}")
    
    return sections

def find_patterns_in_text(text: str, patterns: Dict[str, str], section: str) -> List[Dict]:
    """Find positionality patterns in text"""
    matches = []
    
    for pattern_name, pattern_regex in patterns.items():
        try:
            regex = re.compile(pattern_regex, re.IGNORECASE | re.MULTILINE)
            for match in regex.finditer(text):
                # Get context around match
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                matches.append({
                    "pattern": pattern_name,
                    "match_text": match.group(0),
                    "context": context,
                    "section": section,
                    "start_pos": match.start(),
                    "confidence": get_pattern_confidence(pattern_name, context)
                })
                
        except re.error as e:
            print(f"Regex error in pattern {pattern_name}: {e}")
            continue
    
    return matches

def get_pattern_confidence(pattern_name: str, context: str) -> float:
    """Assign confidence scores to different pattern types"""
    
    # High confidence patterns (explicit positionality language)
    high_confidence = [
        "explicit_positionality", "positionality_term", "identity_disclosure",
        "bias_acknowledgment", "reflexive_awareness"
    ]
    
    # Medium confidence patterns (researcher positioning)
    medium_confidence = [
        "researcher_positioning", "positioned_researcher", "first_person_reflexivity",
        "methodological_reflexivity", "disclosure_statement"
    ]
    
    # Lower confidence patterns (might be academic language)
    lower_confidence = [
        "standpoint_theory", "insider_outsider", "power_dynamics"
    ]
    
    if pattern_name in high_confidence:
        return 0.9
    elif pattern_name in medium_confidence:
        return 0.7
    elif pattern_name in lower_confidence:
        return 0.4
    else:
        return 0.5

def calculate_confidence_score(matches: List[Dict]) -> float:
    """Calculate overall confidence score based on matches"""
    if not matches:
        return 0.0
    
    # Weight by pattern confidence and frequency
    total_confidence = 0.0
    pattern_counts = {}
    
    for match in matches:
        pattern = match["pattern"] 
        confidence = match["confidence"]
        
        # Count pattern frequency (diminishing returns)
        count = pattern_counts.get(pattern, 0) + 1
        pattern_counts[pattern] = count
        
        # Apply frequency discount
        frequency_factor = min(1.0, 1.0 / count)
        weighted_confidence = confidence * frequency_factor
        total_confidence += weighted_confidence
    
    # Normalize by number of unique patterns found
    unique_patterns = len(pattern_counts)
    normalized_score = min(1.0, total_confidence / max(1, unique_patterns))
    
    return normalized_score

if __name__ == "__main__":
    # Test the enhanced detection
    import sys
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        result = enhanced_positionality_detection(pdf_path)
        print(f"Enhanced detection results for {pdf_path}:")
        print(f"Score: {result['positionality_score']:.3f}")
        print(f"Tests: {result['positionality_tests']}")
        for pattern, snippet in result['positionality_snippets'].items():
            print(f"{pattern}: {snippet[:100]}...")
    else:
        print("Usage: python enhanced_detection.py <pdf_path>")