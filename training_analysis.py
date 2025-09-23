#!/usr/bin/env python3
"""
Training Data Analysis and Pattern Discovery

This script analyzes human-labeled training data to:
1. Discover new regex patterns from human examples
2. Evaluate current AI performance against human judgments
3. Generate improved detection rules
4. Create training reports for system improvement
"""

import json
import re
from collections import Counter, defaultdict
from metadata_extractor import extract_positionality

def load_training_data(filepath):
    """Load training data from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading training data: {e}")
        return []

def analyze_human_labels(training_data):
    """Analyze distribution of human judgments"""
    print("📊 HUMAN LABEL ANALYSIS")
    print("=" * 50)
    
    judgments = Counter(entry["judgment"] for entry in training_data)
    total = len(training_data)
    
    for judgment, count in judgments.most_common():
        pct = count / total * 100
        print(f"{judgment:20} {count:3d} ({pct:5.1f}%)")
    
    print(f"\nTotal papers labeled: {total}")
    return judgments

def extract_patterns_from_evidence(training_data):
    """Extract potential regex patterns from human evidence quotes"""
    print("\n🔍 PATTERN DISCOVERY FROM HUMAN EVIDENCE")
    print("=" * 50)
    
    positive_examples = []
    pattern_suggestions = []
    
    for entry in training_data:
        if entry["judgment"] in ["positive_explicit", "positive_subtle"]:
            evidence = entry.get("evidence", "").strip()
            if evidence:
                positive_examples.append({
                    "text": evidence,
                    "filename": entry["filename"],
                    "pattern_types": entry.get("pattern_types", []),
                    "suggestions": entry.get("pattern_suggestions", "")
                })
    
    print(f"Found {len(positive_examples)} positive examples with evidence")
    
    # Analyze common patterns
    print("\n📝 Human Evidence Examples:")
    for i, example in enumerate(positive_examples[:5], 1):
        print(f"\n{i}. {example['filename']}")
        print(f"   Types: {', '.join(example['pattern_types'])}")
        print(f"   Text: \"{example['text'][:100]}...\"")
        if example['suggestions']:
            print(f"   Suggestions: {example['suggestions']}")
    
    # Extract suggested patterns
    all_suggestions = []
    for entry in training_data:
        suggestions = entry.get("pattern_suggestions", "").strip()
        if suggestions:
            all_suggestions.extend(suggestions.split(','))
    
    if all_suggestions:
        print(f"\n💡 Human Pattern Suggestions ({len(all_suggestions)} total):")
        suggestion_counts = Counter(s.strip().lower() for s in all_suggestions if s.strip())
        for suggestion, count in suggestion_counts.most_common(10):
            print(f"   {count:2d}x \"{suggestion}\"")
    
    return positive_examples

def generate_regex_patterns(positive_examples):
    """Generate potential regex patterns from human examples"""
    print("\n⚙️  GENERATING NEW REGEX PATTERNS")
    print("=" * 50)
    
    # Common first-person reflexive patterns
    reflexive_phrases = []
    identity_phrases = []
    positioning_phrases = []
    
    for example in positive_examples:
        text = example["text"].lower()
        
        # Look for first-person patterns
        if re.search(r'\bi\s+(?:acknowledge|recognize|admit|must)', text):
            reflexive_phrases.append(text)
        
        # Look for identity disclosure
        if re.search(r'as\s+a\s+(?:black|white|latina|woman|man)', text):
            identity_phrases.append(text)
            
        # Look for positioning language
        if re.search(r'(?:positioned|situated|locate)', text):
            positioning_phrases.append(text)
    
    print(f"Reflexive patterns found: {len(reflexive_phrases)}")
    print(f"Identity patterns found: {len(identity_phrases)}")  
    print(f"Positioning patterns found: {len(positioning_phrases)}")
    
    # Suggest new regex patterns
    suggested_patterns = []
    
    if reflexive_phrases:
        suggested_patterns.append({
            "name": "enhanced_reflexive",
            "pattern": r"\bI\s+(?:must|should|cannot\s+help\s+but|am\s+forced\s+to)\s+(?:acknowledge|recognize|admit|note)",
            "rationale": "Stronger reflexive language from human examples"
        })
    
    if identity_phrases:
        suggested_patterns.append({
            "name": "expanded_identity",
            "pattern": r"\bAs\s+a\s+(?:Black|White|Latina?o?|Asian|Indigenous|queer|trans|disabled|working.class|first.generation)[^.]{0,80}(?:researcher|scholar|woman|man|person)",
            "rationale": "Extended identity categories from human examples"
        })
    
    print("\n💡 SUGGESTED NEW PATTERNS:")
    for i, pattern in enumerate(suggested_patterns, 1):
        print(f"{i}. {pattern['name']}")
        print(f"   Pattern: {pattern['pattern']}")
        print(f"   Rationale: {pattern['rationale']}\n")
    
    return suggested_patterns

def evaluate_ai_performance(training_data, pdf_folder):
    """Compare AI predictions with human judgments"""
    print("\n🤖 AI PERFORMANCE EVALUATION")
    print("=" * 50)
    
    correct = 0
    total = 0
    false_positives = []
    false_negatives = []
    
    for entry in training_data:
        filename = entry["filename"]
        human_judgment = entry["judgment"]
        
        # Convert human judgment to binary
        human_positive = human_judgment in ["positive_explicit", "positive_subtle"]
        
        try:
            # Get AI prediction
            pdf_path = f"{pdf_folder}/{filename}"
            ai_result = extract_positionality(pdf_path)
            ai_score = ai_result.get("positionality_score", 0.0)
            ai_positive = ai_score > 0.2  # Current threshold
            
            # Compare
            if human_positive == ai_positive:
                correct += 1
            elif human_positive and not ai_positive:
                false_negatives.append({
                    "filename": filename,
                    "human_judgment": human_judgment,
                    "ai_score": ai_score,
                    "evidence": entry.get("evidence", "")
                })
            elif not human_positive and ai_positive:
                false_positives.append({
                    "filename": filename,
                    "human_judgment": human_judgment,
                    "ai_score": ai_score
                })
                
            total += 1
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    if total > 0:
        accuracy = correct / total * 100
        print(f"Overall Accuracy: {correct}/{total} ({accuracy:.1f}%)")
        print(f"False Positives: {len(false_positives)}")
        print(f"False Negatives: {len(false_negatives)}")
        
        if false_negatives:
            print("\n❌ FALSE NEGATIVES (missed by AI):")
            for fn in false_negatives[:3]:
                print(f"   {fn['filename']} (score: {fn['ai_score']:.3f})")
                if fn['evidence']:
                    print(f"   Evidence: \"{fn['evidence'][:80]}...\"")
        
        if false_positives:
            print("\n⚠️  FALSE POSITIVES (incorrectly detected):")
            for fp in false_positives[:3]:
                print(f"   {fp['filename']} (score: {fp['ai_score']:.3f})")
    
    return {
        "accuracy": accuracy if total > 0 else 0,
        "false_positives": false_positives,
        "false_negatives": false_negatives
    }

def generate_training_report(training_data, pdf_folder=None):
    """Generate comprehensive training analysis report"""
    print("📋 TRAINING DATA ANALYSIS REPORT")
    print("=" * 80)
    
    # 1. Label distribution
    judgments = analyze_human_labels(training_data)
    
    # 2. Pattern discovery
    positive_examples = extract_patterns_from_evidence(training_data)
    
    # 3. Generate new patterns
    suggested_patterns = generate_regex_patterns(positive_examples)
    
    # 4. AI evaluation (if PDF folder provided)
    if pdf_folder:
        performance = evaluate_ai_performance(training_data, pdf_folder)
    else:
        print("\n⚠️  No PDF folder provided - skipping AI performance evaluation")
        performance = None
    
    # 5. Recommendations
    print("\n🎯 RECOMMENDATIONS FOR IMPROVEMENT")
    print("=" * 50)
    
    positive_rate = (judgments.get("positive_explicit", 0) + 
                    judgments.get("positive_subtle", 0)) / len(training_data) * 100
    
    print(f"1. Positive rate: {positive_rate:.1f}% - {'Good balance' if 20 <= positive_rate <= 80 else 'Consider more balanced dataset'}")
    
    if len(positive_examples) >= 3:
        print("2. Sufficient positive examples for pattern generation ✅")
    else:
        print("2. Need more positive examples with evidence quotes ⚠️")
    
    if performance and performance["accuracy"] > 70:
        print("3. AI performance is acceptable ✅")
    elif performance:
        print(f"3. AI performance needs improvement (current: {performance['accuracy']:.1f}%) ⚠️")
    
    print("4. Next steps:")
    print("   - Implement suggested regex patterns")
    print("   - Test on additional papers") 
    print("   - Collect more training examples if needed")
    print("   - Consider adjusting AI confidence thresholds")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze training data for positionality detection")
    parser.add_argument("training_file", help="Path to training data JSON file")
    parser.add_argument("--pdf-folder", help="Path to PDF folder for AI evaluation")
    
    args = parser.parse_args()
    
    # Load and analyze training data
    training_data = load_training_data(args.training_file)
    
    if not training_data:
        print("No training data found or file could not be loaded.")
        return
    
    generate_training_report(training_data, args.pdf_folder)

if __name__ == "__main__":
    main()