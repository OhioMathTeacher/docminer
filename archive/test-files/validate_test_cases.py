#!/usr/bin/env python3
"""
Test Case Validation for Search Buddy Positionality Detector

This script runs the 6 test cases and compares actual vs expected results.
Documents the specific test scenarios and validates detection accuracy.
"""

import os
import sys
from metadata_extractor import extract_positionality

# Test case definitions with expected results and rationale
TEST_CASES = {
    "Dean-ReflexivityLimitsStudy-2021.pdf": {
        "expected": "NEGATIVE",  # Updated based on analysis
        "rationale": "Bibliography/references section about reflexivity - no personal positioning",
        "focus": "Academic references on reflexivity methodology (not personal statements)"
    },
    "Parks-ObstaclesAddressingRace-2012.pdf": {
        "expected": "NEGATIVE",  # Updated based on analysis
        "rationale": "Literature review about field obstacles - analyzes others' work, not personal position", 
        "focus": "Meta-analysis of mathematics education field (not personal positioning)"
    },
    "Vries-Transgenderpeoplecolor-2015.pdf": {
        "expected": "UNCERTAIN",  # Needs deeper analysis
        "rationale": "Theoretical modeling paper with 'I theorize' - may contain subtle positioning",
        "focus": "Intersectional theoretical framework development"
    },
    "cycyk-et-al-2022-moving-through-the-pipeline-ethnic-and-linguistic-disparities-in-special-education-from-birth-through.pdf": {
        "expected": "NEGATIVE",
        "rationale": "Multi-author quantitative pipeline study - unlikely individual positionality",
        "focus": "Large-scale statistical analysis of educational pathways"
    },
    "datnow-et-al-2022-bridging-educational-change-and-social-justice-a-call-to-the-field.pdf": {
        "expected": "NEGATIVE",
        "rationale": "Multi-author policy/systems research with institutional focus",
        "focus": "Field-wide call to action rather than personal positioning"
    },
    "henrekson-et-al-2025-the-purposes-of-education-a-citizen-perspective-beyond-political-elites.pdf": {
        "expected": "NEGATIVE", 
        "rationale": "Theoretical/philosophical research less likely to include personal positioning",
        "focus": "Abstract analysis of educational purposes and citizen perspectives"
    }
}

def analyze_detection_accuracy(results):
    """Analyze overall detection performance"""
    correct = 0
    total = len(results)
    
    print("\n" + "="*80)
    print("📊 DETECTION ACCURACY ANALYSIS")
    print("="*80)
    
    for filename, result in results.items():
        expected = TEST_CASES[filename]["expected"]
        actual = result["detected"]
        is_correct = expected == actual
        
        if is_correct:
            correct += 1
            status = "✅ CORRECT"
        else:
            status = "❌ INCORRECT"
            
        print(f"{status}: {filename}")
        print(f"   Expected: {expected}, Got: {actual}")
        print(f"   Score: {result['score']:.3f}, Tests: {result['tests']}")
        print()
    
    accuracy = correct / total * 100
    print(f"🎯 Overall Accuracy: {correct}/{total} ({accuracy:.1f}%)")
    
    # Analyze false positives/negatives
    false_pos = sum(1 for f, r in results.items() 
                   if TEST_CASES[f]["expected"] == "NEGATIVE" and r["detected"] == "POSITIVE")
    false_neg = sum(1 for f, r in results.items() 
                   if TEST_CASES[f]["expected"] == "POSITIVE" and r["detected"] == "NEGATIVE")
    
    print(f"🚫 False Positives: {false_pos}")
    print(f"🔍 False Negatives: {false_neg}")
    
    return accuracy, false_pos, false_neg

def main():
    PDF_DIR = "/Users/todd/pdfs"
    
    if not os.path.isdir(PDF_DIR):
        print(f"❌ Test directory not found: {PDF_DIR}")
        print("Please update PDF_DIR path in this script.")
        sys.exit(1)
    
    print("🧪 SEARCH BUDDY TEST CASE VALIDATION")
    print("="*80)
    print(f"Test Directory: {PDF_DIR}")
    print(f"Test Cases: {len(TEST_CASES)}")
    print()
    
    results = {}
    
    # Process each test case
    for filename, test_info in TEST_CASES.items():
        pdf_path = os.path.join(PDF_DIR, filename)
        
        if not os.path.exists(pdf_path):
            print(f"⚠️  File not found: {filename}")
            continue
            
        print(f"📄 Testing: {filename}")
        print(f"   Expected: {test_info['expected']}")
        print(f"   Focus: {test_info['focus']}")
        
        try:
            # Run positionality detection
            pos_result = extract_positionality(pdf_path)
            
            score = pos_result.get("positionality_score", 0.0) or 0.0
            tests = pos_result.get("positionality_tests", [])
            
            # Determine detection result based on current algorithm
            regex_keys = {
                "explicit_positionality", "first_person_reflexivity", "researcher_self",
                "author_self", "as_a_role", "I_position", "I_situated", 
                "positionality", "self_reflexivity"
            }
            
            has_regex = any(t in regex_keys for t in tests)
            has_gpt = "gpt_full_text" in tests and score >= 0.6
            detected = "POSITIVE" if (has_regex or has_gpt) else "NEGATIVE"
            
            results[filename] = {
                "detected": detected,
                "score": score,
                "tests": tests,
                "expected": test_info["expected"]
            }
            
            print(f"   Result: {detected} (score: {score:.3f})")
            print(f"   Tests triggered: {', '.join(tests) if tests else 'None'}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results[filename] = {
                "detected": "ERROR", 
                "score": 0.0, 
                "tests": [], 
                "expected": test_info["expected"]
            }
        
        print("-" * 60)
    
    # Analyze results
    if results:
        analyze_detection_accuracy(results)
        
        # Suggestions for improvement
        print("\n💡 IMPROVEMENT SUGGESTIONS:")
        print("- Review false negatives for missed positionality patterns")
        print("- Validate regex patterns against actual academic writing")
        print("- Consider expanding AI analysis scope")
        print("- Test with valid OpenAI API key for full functionality")

if __name__ == "__main__":
    main()