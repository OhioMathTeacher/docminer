# DocMiner v6.1.1 - Visual Feature Guide
## Quick Reference for Tomorrow's Demo

---

## 🎨 New Layout Toggle (Overleaf-Style)

### Header Layout
```
┌─────────────────────────────────────────────────────────────────────────┐
│  GA Name: [Becca      ]  [📁 Select PDF Folder]                        │
│                                                                          │
│  Layout: [📄 PDF] [🔀 Split] [✏️ Analysis]  |  [🤖 Robbie animating]    │
└─────────────────────────────────────────────────────────────────────────┘
                    ↑
              Click to toggle!
              Ctrl+1 / Ctrl+2 / Ctrl+3
```

---

## Mode 1: 📄 PDF Only (Ctrl+1)

```
┌───────────────────────────────────────────────────────────────┐
│ 📄 PDF Document Viewer                                        │
├───────────────────────────────────────────────────────────────┤
│ ◀ Page 1 of 5 ▶  |  View: [Letter ▼]  |  Zoom: [150% ▼]      │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│                                                               │
│                                                               │
│              [FULL-SCREEN PDF DISPLAY]                        │
│                                                               │
│              Read, zoom, select text                          │
│                                                               │
│                                                               │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│ ☐ Selected Text  ← Collapsed by default                      │
├───────────────────────────────────────────────────────────────┤
│ 💡 Tip: Select text → Check box → Copy to Evidence           │
└───────────────────────────────────────────────────────────────┘

✅ Maximum reading space
✅ No distractions
✅ Perfect for small screens
```

---

## Mode 2: 🔀 Split View (Ctrl+2) - Default

```
┌─────────────────────────────────┬───────────────────────────────┐
│ 📄 PDF Document Viewer          │ Evidence & Analysis           │
├─────────────────────────────────┼───────────────────────────────┤
│ ◀ 1 of 5 ▶  View: [Letter ▼]   │ 🚀 Run AI Analysis            │
│ Zoom: [Auto ▼]                  │                               │
├─────────────────────────────────┤ Does paper contain           │
│                                 │ positionality?                │
│   [PDF content with text        │ ⚪ ✅ Yes - Explicit          │
│    selection enabled]           │ ⚪ 🔍 Yes - Subtle            │
│                                 │ ⚪ ❌ No                       │
│   Highlight text → appears      │ ⚪ ❓ Uncertain                │
│   in "Selected Text" below      │                               │
│                                 │ ┌─ Human Input ─────────────┐ │
│                                 │ │ 📝 Manual Evidence        │ │
│                                 │ │ [Your notes here]         │ │
├─────────────────────────────────┤ └───────────────────────────┘ │
│ ☐ Selected Text                 │                               │
│                                 │ ┌─ AI Input ───────────────┐ │
│              ◄═ DRAG ME! ═►     │ │ 🤖 AI Analysis            │ │
│                                 │ │ [AI findings here]        │ │
│     (Adjust proportions)        │ └───────────────────────────┘ │
├─────────────────────────────────┼───────────────────────────────┤
│ 💡 Tip: Select text...          │ [Save & Next] [Upload]        │
└─────────────────────────────────┴───────────────────────────────┘

✅ See both panels simultaneously
✅ Drag splitter to adjust
✅ Standard workflow mode
```

---

## Mode 3: ✏️ Analysis Only (Ctrl+3)

```
┌─────────────────────────────────────────────────────────────────┐
│ Evidence & Analysis                                             │
├─────────────────────────────────────────────────────────────────┤
│ 🚀 Run AI Analysis                                              │
│                                                                 │
│ Does this paper contain positionality statements?               │
│ ⚪ ✅ Yes - Explicit positionality statements                   │
│ ⚪ 🔍 Yes - Subtle/implicit positionality                       │
│ ⚪ ❌ No positionality statements                               │
│ ⚪ ❓ Uncertain/borderline case                                 │
│                                                                 │
│ ┌─ Human Input Tab ──────────────────────────────────────────┐ │
│ │ 📝 Manual Evidence Collection - Enter quotes/citations     │ │
│ │                                                            │ │
│ │ ┌────────────────────────────────────────────────────────┐ │ │
│ │ │ [Large text editing area]                              │ │ │
│ │ │                                                        │ │ │
│ │ │ Type evidence, quotes, page numbers, analysis...       │ │ │
│ │ │                                                        │ │ │
│ │ │                                                        │ │ │
│ │ └────────────────────────────────────────────────────────┘ │ │
│ └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─ AI Input Tab ────────────────────────────────────────────┐  │
│ │ 🤖 AI Automatic Analysis - Full document processed        │  │
│ │                                                           │  │
│ │ ┌───────────────────────────────────────────────────────┐ │  │
│ │ │ [AI findings displayed here]                          │ │  │
│ │ │                                                       │ │  │
│ │ │ • Identity disclosure found on p. 3                   │ │  │
│ │ │ • Methodological reflexivity on p. 12                 │ │  │
│ │ └───────────────────────────────────────────────────────┘ │  │
│ └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│ [◀ Previous Paper]  [Next Paper ⏭️]  [💾 Export]  [🚀 Upload]  │
└─────────────────────────────────────────────────────────────────┘

✅ Full screen for writing
✅ No PDF distraction
✅ Focus on analysis
```

---

## 🔧 New PDF Viewer Features

### View Mode Dropdown
```
View: [ Letter      ▼ ]
      │ Letter          ← Optimized for 8.5×11" (US)
      │ A4             ← Optimized for 210×297mm
      │ Full Width     ← Fill width, scroll vertically
      │ Full Height    ← Fill height, scroll horizontally
      └ Custom         ← Use actual PDF dimensions
```

### Extended Zoom Range
```
Zoom: [ Auto    ▼ ]
      │ Auto          ← Intelligent fit based on View mode
      │ 50%           ← See whole page at once
      │ 65%
      │ 80%
      │ 100%          ← Actual size
      │ 125%
      │ 150%
      │ 175%
      │ 200%          ← NEW! Perfect for small screens
      └─────────────
```

### Collapsible Selected Text Panel
```
┌─────────────────────────────────────────────┐
│ ☐ Selected Text    ← Click to expand/hide  │
└─────────────────────────────────────────────┘
                ↓ (when checked)
┌─────────────────────────────────────────────┐
│ ☑ Selected Text    ← Click to collapse     │
├─────────────────────────────────────────────┤
│ [Text you selected appears here]            │
│                                             │
│ [Copy to Evidence →] [Clear]                │
└─────────────────────────────────────────────┘
```

---

## 💡 New Help Features

### Quick Help Menu
```
Menu: Help → 💡 Quick Help

┌────────────────────────────────────────┐
│  💡 Quick Help & FAQ                   │
├────────────────────────────────────────┤
│                                        │
│  Q: What does the AI analyze?          │
│  A: The ENTIRE document automatically  │
│                                        │
│  Q: What goes in "Human Input"?        │
│  A: YOUR manual evidence collection    │
│                                        │
│  Q: Where is training data?            │
│  A: Current folder: 2001               │
│                                        │
│  Q: PDF doesn't fit?                   │
│  A: Use View modes + Zoom controls     │
│                                        │
│  Q: How to collect evidence?          │
│  A: Select → Check box → Copy          │
│                                        │
│              [ OK ]                    │
└────────────────────────────────────────┘
```

### Info Labels on Input Tabs
```
┌─ Human Input Tab ────────────────────────────┐
│ 📝 Manual Evidence Collection               │
│    Enter quotes/citations you identified    │
│    ℹ️ (Hover for more info)                 │
├─────────────────────────────────────────────┤
│ [Your evidence text here]                   │
└─────────────────────────────────────────────┘

┌─ AI Input Tab ──────────────────────────────┐
│ 🤖 AI Automatic Analysis                    │
│    The AI reads and analyzes ENTIRE doc     │
│    ℹ️ (Hover for more info)                 │
├─────────────────────────────────────────────┤
│ [AI findings displayed here]                │
└─────────────────────────────────────────────┘
```

---

## ⌨️ Keyboard Shortcuts Reference Card

```
╔═══════════════════════════════════════════════╗
║         DOCMINER KEYBOARD SHORTCUTS           ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  LAYOUT MODES                                 ║
║  ───────────────────────────────────────────  ║
║  Ctrl + 1    📄 PDF Only (reading mode)       ║
║  Ctrl + 2    🔀 Split View (default)          ║
║  Ctrl + 3    ✏️ Analysis Only (writing mode)  ║
║                                               ║
║  WINDOW CONTROLS                              ║
║  ───────────────────────────────────────────  ║
║  Drag corner/edge    Resize window            ║
║  Drag splitter       Adjust panel sizes       ║
║  (in Split mode)                              ║
║                                               ║
╚═══════════════════════════════════════════════╝

Print this and tape it next to your monitor!
```

---

## 🪟 Window Resizing

### Before: Fixed/Constrained
```
┌─────────────────────────────┐
│  1200 × 800 pixels          │
│  (fixed size)               │
│                             │
│  ❌ Can't resize freely     │
│  ❌ No minimum enforced     │
│  ❌ Doesn't adapt to screen │
└─────────────────────────────┘
```

### After: Fully Resizable
```
        ↖ Drag any corner
┌─────────────────────────────┐ ← Drag top edge
│  Any size you want!         │
│                             │
│  ✅ Drag corners            │
│  ✅ Drag edges              │ ← Drag side edge
│  ✅ Maximize/minimize       │
│  ✅ Min: 900×600            │
│  ✅ Adapts to any screen    │
└─────────────────────────────┘
         Drag bottom edge ↓
```

---

## 📊 Before/After Comparison

### Viewing Space
```
BEFORE:
┌────────────┐
│ PDF: 50%   │ } Fixed split
│ Analysis:  │
│    50%     │
└────────────┘

AFTER:
┌────────────┐     ┌────────────┐     ┌────────────┐
│ PDF: 100%  │  or │ PDF: 40%   │  or │ Analysis:  │
│            │     │ Analysis:  │     │   100%     │
│            │     │   60%      │     │            │
└────────────┘     └────────────┘     └────────────┘
  PDF Only           Split (drag)       Analysis Only
   (Ctrl+1)           (Ctrl+2)           (Ctrl+3)
```

### Zoom Range
```
BEFORE: 50% ─────────── 150%
                        ↑ Max zoom

AFTER:  50% ─────────── 200%
                        ↑ NEW! Much better for small screens
```

### Help
```
BEFORE:
❌ No in-app help
❌ Unclear AI behavior
❌ Unknown folder location

AFTER:
✅ Help → Quick Help menu
✅ Info labels on tabs
✅ Tooltips everywhere
✅ Current folder shown
```

---

## 🎯 Demo Script for Tomorrow

### 1. Show PDF Improvements (2 min)
"Becca mentioned her screen was too small. Let's see the fixes..."
- Load a PDF from 2001 folder
- **Point out**: "Selected Text" box is collapsed by default
- **Show**: View dropdown - "Letter optimizes for standard papers"
- **Demo**: Zoom to 200% - "Much more readable now!"
- **Compare**: 50% vs 200% side-by-side

### 2. Show Layout Toggle (3 min)
"We added Overleaf-style layouts for different workflows..."
- **Point to buttons**: "Three modes next to Robbie"
- **Click PDF Only** (Ctrl+1) - "Focus on reading"
- **Click Split** (Ctrl+2) - "See both, drag the divider"
- **Drag splitter** - "Adjust proportions as you work"
- **Click Analysis** (Ctrl+3) - "Focus on writing"
- **Demo shortcut**: Press Ctrl+1 - "Instant switching!"

### 3. Show Help Features (2 min)
"You asked what the AI analyzes. Let's see the new help..."
- **Open**: Help → Quick Help
- **Read**: "AI analyzes ENTIRE document automatically"
- **Show**: "Human Input is YOUR manual collection"
- **Point out**: Current folder name
- **Switch to Human Input tab** - "See the info label?"
- **Hover** - "Tooltip explains in detail"

### 4. Show Window Resize (1 min)
"The window is now fully resizable..."
- **Drag corner** - "Resize to any size"
- **Maximize** - "Full screen on large monitors"
- **Minimize** - "Works on small laptops too"

### 5. Get Feedback (2 min)
"Becca, can you try it on your laptop?"
- Load PDF from 2001 folder
- Try different View modes
- Test 200% zoom
- Try layout toggle
- Drag splitter
- Check if questions are answered

---

## ✅ Success Criteria

After demo, Becca should be able to answer:

- [ ] "Can you see the full PDF now?" → **Yes!**
- [ ] "Is the text readable at 200%?" → **Yes!**
- [ ] "What does the AI analyze?" → **Entire document!**
- [ ] "What goes in Human Input?" → **My manual notes!**
- [ ] "Can you focus on just reading?" → **Yes, PDF Only mode!**
- [ ] "Can you focus on just writing?" → **Yes, Analysis Only mode!**
- [ ] "Can you adjust the split?" → **Yes, drag the divider!**

---

**Ready to demo!** 🎉
