# PDF Text Selection Improvements - Implementation Plan

## Issues Identified

### 1. Selection Offset from Actual Text
**Problem**: Highlighted selection doesn't align with actual PDF text
**Cause**: PDF coordinate system vs. Qt widget coordinate system mismatch
**Severity**: Medium - affects usability but doesn't break functionality

### 2. Extra Spaces When Pasting
**Problem**: Pasted text has excessive whitespace
**Cause**: PDF extraction preserves layout spaces/formatting
**Severity**: Low - cosmetic issue

### 3. Two-Column Layout Selection
**Problem**: Selection highlights full width instead of single column
**Cause**: PDF doesn't encode column structure, just character positions
**Severity**: Medium - makes precise selection difficult

## Proposed Solutions

### Fix 1: Improve Selection-to-Text Mapping
**Approach**: Use pdfplumber's character bounding boxes

```python
def get_precise_text_from_selection(pdf_page, x1, y1, x2, y2):
    """
    Get text with precise character-level matching
    """
    chars = pdf_page.chars
    selected_chars = [
        char for char in chars
        if (x1 <= char['x0'] <= x2 and 
            y1 <= char['top'] <= y2)
    ]
    # Sort by reading order (top-to-bottom, left-to-right)
    selected_chars.sort(key=lambda c: (c['top'], c['x0']))
    return ''.join(c['text'] for c in selected_chars)
```

**Effort**: ~2-3 hours
**Files**: `enhanced_training_interface.py` (PDF viewer section)

### Fix 2: Clean Up Extracted Text
**Approach**: Post-process extracted text to remove excessive whitespace

```python
def clean_extracted_text(text):
    """
    Clean up PDF-extracted text for better readability
    """
    import re
    
    # Replace multiple spaces with single space
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove spaces before punctuation
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    
    # Normalize line breaks - keep paragraph structure
    lines = text.split('\n')
    
    # Group into paragraphs (blank line = paragraph break)
    paragraphs = []
    current_para = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
        else:
            current_para.append(line)
    
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    # Join paragraphs with double newline
    return '\n\n'.join(paragraphs)
```

**Effort**: ~1 hour
**Files**: `enhanced_training_interface.py` or new `utils/text_cleaner.py`

### Fix 3: Column-Aware Text Selection
**Approach**: Detect columns and constrain selection

```python
def detect_columns(pdf_page):
    """
    Detect column boundaries in PDF
    """
    from pdfplumber.utils import extract_text_with_layout
    
    # Get all text bounding boxes
    chars = pdf_page.chars
    
    # Cluster by X position to find columns
    x_positions = [c['x0'] for c in chars]
    
    # Simple approach: If significant gap in X, it's a column boundary
    # More sophisticated: Use clustering algorithm (DBSCAN)
    
    # For now, use simple heuristic:
    # If text has two distinct X-clusters, it's two-column
    
    page_width = pdf_page.width
    left_third = page_width / 3
    right_third = 2 * page_width / 3
    
    left_chars = [c for c in chars if c['x0'] < left_third]
    right_chars = [c for c in chars if c['x0'] > right_third]
    
    if len(left_chars) > 100 and len(right_chars) > 100:
        # Two-column layout detected
        column_boundary = (left_third + right_third) / 2
        return [
            (0, column_boundary),           # Left column
            (column_boundary, page_width)    # Right column
        ]
    
    return [(0, page_width)]  # Single column
```

**Effort**: ~4-5 hours (more complex)
**Files**: `enhanced_training_interface.py` (requires refactoring PDF viewer)

## Implementation Priority

### Phase 1: Quick Wins (Do Now)
1. ✅ Fix GitHub upload (Bearer token) - **DONE**
2. ⚙️ Add text cleaning function - **Easy, high impact**

### Phase 2: Medium Improvements (Next Sprint)
3. Improve selection coordinate mapping
4. Add "Clean Text" button to evidence panel

### Phase 3: Advanced Features (Future)
5. Column detection and smart selection
6. Visual column boundaries in PDF viewer
7. OCR fallback for scanned PDFs

## Estimated Timeline

- **Phase 1**: 2-3 hours total
- **Phase 2**: 1 week part-time
- **Phase 3**: 2-3 weeks part-time

## Recommendation

**For DocMiner 6.0 rebrand:**
- ✅ Include GitHub upload fix (critical)
- ✅ Include text cleaning (easy win)
- 📋 Plan Phase 2 for v6.1
- 📋 Plan Phase 3 for v6.2+

The two-column issue is complex and affects many academic papers. It's worth doing right, but doesn't need to block the rebrand.

## Alternative: Third-Party Library

**Consider**: `pypdf` has better column detection
```python
from pypdf import PdfReader
reader = PdfReader("paper.pdf")
text = reader.pages[0].extract_text(extraction_mode="layout")
```

This preserves column structure better but requires switching PDF libraries.

**Trade-off**: Better column handling vs. rewriting PDF extraction code

## Questions for User

1. Is text cleaning (removing extra spaces) enough for v5.2.1?
2. Should column detection wait for v6.1?
3. Try pypdf library or improve current pdfplumber approach?
