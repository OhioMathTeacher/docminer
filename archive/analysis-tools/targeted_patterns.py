#!/usr/bin/env python3
"""
Targeted Patterns for Academic Reflexivity

Based on analysis of real academic papers, create patterns that match
the actual language academics use when discussing their positionality.
"""

import re

# New patterns based on actual academic reflexive statements
ACADEMIC_REFLEXIVITY_PATTERNS = {
    
    # 1. AUTHORIAL POSITIONING
    "authorial_positioning": re.compile(
        r"\b(?:we|I)\s+(?:articulate|position|locate|situate)\s+(?:our|my)\s+"
        r"(?:own\s+)?(?:cultural\s+)?(?:location|position|positionality|perspective)",
        re.IGNORECASE
    ),
    
    # 2. RESEARCH CONTEXT ACKNOWLEDGMENT  
    "research_context": re.compile(
        r"\b(?:this\s+paper|this\s+research|my\s+fieldwork|our\s+study)\s+"
        r"(?:has\s+)?(?:developed|emerged|stems|arises)\s+(?:out\s+of|from)\s+"
        r"(?:my|our)\s+(?:experiences?|background|work)",
        re.IGNORECASE
    ),
    
    # 3. POSITIONAL INFLUENCE ACKNOWLEDGMENT
    "positional_influence": re.compile(
        r"\b(?:our|my)\s+(?:position|positionality|background|experience)\s+"
        r"(?:may\s+|might\s+|could\s+|will\s+)?(?:influence|affect|shape|inform)\s+"
        r"(?:curriculum|research|interpretation|analysis)",
        re.IGNORECASE
    ),
    
    # 4. FIELDWORK REFLEXIVITY
    "fieldwork_reflexivity": re.compile(
        r"\b(?:I|we)\s+(?:became\s+aware|observed|recognized|realized)\s+that\s+"
        r"(?:my|our)\s+(?:position|presence|background|identity)",
        re.IGNORECASE
    ),
    
    # 5. ASSUMPTION ACKNOWLEDGMENT
    "assumption_acknowledgment": re.compile(
        r"\b(?:we|I)\s+(?:make|hold|carry|bring)\s+(?:assumptions|presuppositions|biases)\s+"
        r"(?:based\s+on|about|regarding)\s+(?:our|my)\s+(?:position|background|experience)",
        re.IGNORECASE
    ),
    
    # 6. CONTEXTUAL SELF-POSITIONING
    "contextual_positioning": re.compile(
        r"\b(?:it\s+is\s+)?from\s+this\s+(?:context|position|perspective|standpoint)\s+that\s+"
        r"(?:we|I)\s+(?:position|approach|understand|view)",
        re.IGNORECASE
    ),
    
    # 7. POLITICAL/CRITICAL POSITIONING
    "political_positioning": re.compile(
        r"\b(?:our|my)\s+position\s+is\s+(?:a\s+)?(?:political|critical|theoretical)\s+"
        r"(?:point\s+of\s+departure|stance|perspective)",
        re.IGNORECASE
    ),
    
    # 8. EXPERIENTIAL GROUNDING
    "experiential_grounding": re.compile(
        r"\bthrough\s+(?:discussion\s+of\s+)?(?:my|our)\s+"
        r"(?:fieldwork\s+|research\s+|personal\s+)?experiences?\s+"
        r"(?:in|with|conducting|as)",
        re.IGNORECASE
    ),
    
    # 9. REFLEXIVE OBSERVATION
    "reflexive_observation": re.compile(
        r"\b(?:as\s+I|while\s+I|when\s+I|however,?\s+I)\s+"
        r"(?:got\s+to\s+know|spent\s+time|interacted|worked)\s+.{0,30}\s+"
        r"(?:I\s+observed|I\s+became\s+aware|I\s+realized)",
        re.IGNORECASE
    ),
    
    # 10. RESEARCHER IDENTITY WORK
    "researcher_identity": re.compile(
        r"\b(?:as\s+individuals|as\s+researchers|as\s+authors),?\s+"
        r"(?:we|I)\s+(?:make|hold|carry|bring|acknowledge)",
        re.IGNORECASE
    )
}

def test_targeted_patterns():
    """Test the new targeted patterns on our real statements"""
    
    real_statements = [
        "In order to be consistent with the subject of this article, it is important that we articulate our own cultural locations and positionalities as authors",
        "Delineating our positionalities supports the notion that our positions may influence curriculum and research",
        "It is from this context that we position ourselves as authors of this critical essay",
        "As individuals, we make assumptions based on our positionality",
        "Our position is a political point of departure",
        "Through discussion of my fieldwork experiences in Indonesia, I will illustrate some of the limitations",
        "This paper has developed out of my experiences conducting fieldwork in Indonesia",
        "However, as I got to know us, I observed that the ways in which we were treated and talked about",
        "I became aware that my position in the field was determined as much by how I conducted myself",
        "While it was clear to me that the vastly different social interactions with our research subjects must be important",
    ]
    
    print("🎯 TESTING TARGETED ACADEMIC REFLEXIVITY PATTERNS")
    print("=" * 70)
    
    total_caught = 0
    
    for i, statement in enumerate(real_statements, 1):
        print(f"\n📝 Statement {i}:")
        print(f"   \"{statement[:80]}{'...' if len(statement) > 80 else ''}\"")
        
        matches = []
        for name, pattern in ACADEMIC_REFLEXIVITY_PATTERNS.items():
            if pattern.search(statement):
                matches.append(name)
        
        if matches:
            print(f"   ✅ MATCHED: {', '.join(matches)}")
            total_caught += 1
        else:
            print(f"   ❌ No matches")
    
    print(f"\n📊 RESULTS:")
    print(f"   Statements caught: {total_caught}/{len(real_statements)} ({total_caught/len(real_statements)*100:.1f}%)")
    
    return total_caught, len(real_statements)

if __name__ == "__main__":
    test_targeted_patterns()