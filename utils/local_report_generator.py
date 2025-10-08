#!/usr/bin/env python3
"""
Local Report Generator - Works without GitHub token
"""

import json
import os
from datetime import datetime
from pathlib import Path

def create_local_training_report(training_data, ga_name="TestUser"):
    """Create a local training report without requiring GitHub upload"""
    
    # Create reports directory in user's home directory (writable location)
    reports_dir = Path.home() / ".research_buddy" / "training_reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    session_id = datetime.now().strftime("%Y%m%d_%H%M")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Count judgments
    judgments = {}
    for entry in training_data:
        judgment = entry.get("judgment", "unknown")
        judgments[judgment] = judgments.get(judgment, 0) + 1
    
    # Generate markdown report
    report_content = f"""# Training Session Report

## Session Information
- **GA Name**: {ga_name}
- **Session ID**: {session_id}
- **Timestamp**: {datetime.now().isoformat()}
- **Papers Analyzed**: {len(training_data)}

## Summary Statistics

### Judgment Distribution
"""
    
    for judgment, count in judgments.items():
        percentage = (count / len(training_data)) * 100 if training_data else 0
        report_content += f"- **{judgment}**: {count} papers ({percentage:.1f}%)\n"
    
    # Extract evidence examples
    positive_examples = []
    for entry in training_data:
        if entry.get("judgment", "").startswith("positive") and entry.get("evidence"):
            positive_examples.append({
                "filename": entry["filename"],
                "evidence": entry["evidence"][:200] + ("..." if len(entry["evidence"]) > 200 else ""),
                "patterns": entry.get("pattern_types", []),
                "confidence": entry.get("confidence", 0)
            })
    
    report_content += f"""
### Pattern Analysis
- **Total Evidence Quotes**: {len(positive_examples)}
"""
    
    if positive_examples:
        avg_confidence = sum(e['confidence'] for e in positive_examples) / len(positive_examples)
        report_content += f"- **Average Confidence**: {avg_confidence:.1f}/5\n\n"
        report_content += "## Evidence Examples\n\n"
        
        for i, example in enumerate(positive_examples[:5], 1):
            report_content += f"""
### Example {i}: {example['filename']}
- **Confidence**: {example['confidence']}/5
- **Patterns**: {', '.join(example['patterns']) if example['patterns'] else 'None specified'}
- **Evidence**: "{example['evidence']}"

"""
    
    report_content += f"""
## Raw Data

```json
{json.dumps(training_data, indent=2)}
```
"""
    
    # Save files
    json_filename = f"training_session_{ga_name}_{session_id}_{timestamp}.json"
    md_filename = f"training_report_{ga_name}_{session_id}_{timestamp}.md"
    
    json_path = reports_dir / json_filename
    md_path = reports_dir / md_filename
    
    with open(json_path, 'w') as f:
        json.dump(training_data, f, indent=2)
    
    with open(md_path, 'w') as f:
        f.write(report_content)
    
    return {
        'success': True,
        'message': f'Reports saved locally:\n- {md_path}\n- {json_path}',
        'json_file': str(json_path),
        'md_file': str(md_path),
        'session_id': session_id
    }

if __name__ == "__main__":
    # Test with sample data
    sample_data = [
        {
            "filename": "test.pdf",
            "judgment": "positive_explicit",
            "evidence": "Sample evidence text",
            "confidence": 4
        }
    ]
    
    result = create_local_training_report(sample_data, "TestGA")
    print(f"Result: {result}")