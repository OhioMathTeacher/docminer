# Testing macOS Executable on M1 Mac Mini

## 🧪 Quick Test Guide

**Goal:** Verify the macOS executable works correctly before your GAs use it.

---

## 📥 Download and Extract

### Option 1: Download from GitHub Release (Recommended)
```bash
cd ~/Downloads
curl -L -o DocMiner-5.1.1-macos.tar.gz \
  "https://github.com/OhioMathTeacher/docminer/releases/download/v5.1.1/DocMiner-5.1.1-macos.tar.gz"
tar -xzf DocMiner-5.1.1-macos.tar.gz
cd DocMiner5.1.1
```

### Option 2: If You Already Built It Locally
```bash
cd ~/docminer/dist/DocMiner5.1.1
```

---

## ✅ Test Checklist

### 1. Basic Launch Test
```bash
./DocMiner5.1.1
```

**Expected:**
- ✅ Application window opens
- ✅ No immediate crash
- ✅ GUI appears with menu bar

**If it says "unidentified developer":**
```bash
# Right-click the app → Open → Open
# Or from terminal:
xattr -dr com.apple.quarantine DocMiner5.1.1
./DocMiner5.1.1
```

### 2. PDF Loading Test
1. Click **File → Load PDF** (or equivalent button)
2. Navigate to a sample PDF
3. Select and open it

**Expected:**
- ✅ PDF viewer displays the document
- ✅ Can scroll through pages
- ✅ Text is readable

### 3. Text Selection Test
1. Click and drag to select text in the PDF
2. Try to highlight a passage

**Expected:**
- ✅ Text selection works
- ✅ Selection highlights appear
- ✅ Selected text can be copied

### 4. AI Features Test (Optional - requires API key)
1. Go to **Configuration → Settings**
2. Enter a test OpenAI API key
3. Try AI-assisted analysis

**Expected:**
- ✅ Settings save correctly
- ✅ API connection works
- ✅ No crashes

### 5. Manual Mode Test (No API key needed)
1. Use the app WITHOUT entering API keys
2. Try manual analysis features
3. Save a report

**Expected:**
- ✅ Works in offline mode
- ✅ Can save annotations
- ✅ Can export results

---

## 🐛 Common Issues & Fixes

### Issue: "DocMiner5.1.1 is damaged and can't be opened"
**Fix:**
```bash
xattr -dr com.apple.quarantine DocMiner5.1.1
```

### Issue: Application crashes on startup
**Fix:** Run from terminal to see error:
```bash
./DocMiner5.1.1
# Look for error messages in terminal output
```

### Issue: Missing dependencies
**Fix:** This shouldn't happen (all bundled), but if it does:
```bash
# Check what's missing
otool -L DocMiner5.1.1
```

### Issue: PDF won't load
**Fix:** 
- Try a different PDF
- Check file permissions
- Ensure PDF is not corrupted

---

## 📝 Test Report Template

After testing, note:

```
✅/❌ Application launches
✅/❌ PDF loads correctly  
✅/❌ Text selection works
✅/❌ Runs without API keys (manual mode)
✅/❌ Settings save properly

macOS Version: _______________
Mac Model: M1 Mac Mini
File Size: ~212 MB
Executable Location: _______________
```

---

## 🎯 If All Tests Pass

**The executable is ready for your GAs!** They can:
1. Download from GitHub release
2. Extract the archive
3. Double-click to run
4. Start analyzing papers immediately

---

## 📤 If Issues Found

1. Note the exact error message
2. Check terminal output for details
3. Test on Intel Mac if available (compatibility check)
4. Report back for troubleshooting

---

**Good luck with testing!** 🚀
