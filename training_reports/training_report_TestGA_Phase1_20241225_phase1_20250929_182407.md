# Training Session Report

## Session Information
- **GA Name**: TestGA_Phase1
- **Session ID**: 20241225_phase1
- **Timestamp**: 2025-09-29T18:24:07.484881
- **Papers Analyzed**: 1

## Summary Statistics

### Judgment Distribution
- **positive_strong**: 1 papers (100.0%)

### Pattern Analysis
- **Total Evidence Quotes**: 1
- **Average Confidence**: 4.0/5

## Evidence Examples


### Example 1: test_paper.pdf
- **Confidence**: 4/5
- **Patterns**: authorial_positioning, research_context
- **Evidence**: "This paper demonstrates clear authorial positioning when the authors state "we position our work within...""

## Pattern Suggestions

No pattern suggestions provided.

## Next Steps for Analysis

1. **Pattern Discovery**: Analyze evidence quotes for new regex patterns
2. **False Negative Review**: Check papers marked negative for missed statements  
3. **Validation Testing**: Test discovered patterns on validation set
4. **System Integration**: Add successful patterns to detection engine

## Raw Data

```json
[
  {
    "filename": "test_paper.pdf",
    "judgment": "positive_strong",
    "evidence": "This paper demonstrates clear authorial positioning when the authors state \"we position our work within...\"",
    "confidence": 4,
    "pattern_types": [
      "authorial_positioning",
      "research_context"
    ]
  }
]
```
