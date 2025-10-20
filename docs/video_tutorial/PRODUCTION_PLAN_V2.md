# DocMiner Video Tutorial - Production Plan v2.0
## Updated October 2025

---

## 🎯 Overview

Creating a comprehensive video tutorial for DocMiner v6.1.0 that serves both as:
1. **Quick Start Guide** (5 min) - Get up and running fast
2. **Deep Dive Tutorial** (15-20 min) - Complete workflow with best practices

---

## 📹 Video Types

### Option A: Two Separate Videos (Recommended)

**Quick Start (5 minutes)**
- Download & installation
- Basic configuration
- Load PDF and analyze one paper
- Export results
- Target: New users who want to try it immediately

**Complete Tutorial (15-20 minutes)**
- Everything from Quick Start PLUS:
- AI vs Manual analysis comparison
- Advanced configuration options
- Batch processing tips
- Common pitfalls and solutions
- Exporting for different use cases
- Target: GAs and regular users

### Option B: One Video with Chapters (Alternative)
- Single 15-20 minute video with YouTube chapters
- Users can skip to relevant sections
- Easier to maintain (one video to update)

---

## 🎬 Production Approach

### Character-Based vs. Screencast

**Option 1: Character-Based (Current Script)**
- Pros: Engaging, personality, memorable
- Cons: More production time, requires voice actors/ElevenLabs
- Best for: Academic/institutional audience

**Option 2: Simple Screencast with Narration**
- Pros: Faster to produce, easier to update
- Cons: Less engaging, more "standard tutorial"
- Best for: Technical users who want facts fast

**Option 3: Hybrid (Recommended)**
- Quick Start: Simple screencast with your voice
- Deep Dive: Character-based with ElevenLabs voices
- Best of both: Fast production + engaging content

---

## 🛠️ Technical Setup

### Recording Software (Linux)

**Screen Recording:**
- **OBS Studio** (Recommended)
  - Free, open source
  - High quality capture
  - Can record specific windows or full screen
  - Installation: `sudo apt install obs-studio`

- **SimpleScreenRecorder** (Alternative)
  - Lighter weight
  - Easier for beginners
  - Installation: `sudo apt install simplescreenrecorder`

**Video Editing:**
- **DaVinci Resolve** (Professional, free version available)
  - Download: https://www.blackmagicdesign.com/products/davinciresolve
  - Professional color grading, effects
  
- **Kdenlive** (Free, open source)
  - Installation: `sudo apt install kdenlive`
  - Easier learning curve
  
- **OpenShot** (Simplest option)
  - Installation: `sudo apt install openshot-qt`
  - Good for basic cuts and transitions

### Audio Setup

**Recording Your Voice:**
- Use a decent USB microphone (Blue Yeti, Audio-Technica ATR2100)
- Quiet room with soft furnishings (reduces echo)
- Audacity for audio cleanup: `sudo apt install audacity`

**ElevenLabs (for character voices):**
- https://elevenlabs.io
- Pay-per-use pricing
- High quality AI voices
- Can generate all character dialogue

---

## 📝 Updated Script Structure

### Quick Start Video (5 minutes)

**0:00-0:30 Introduction**
- What is DocMiner?
- What problem does it solve?

**0:30-1:30 Download & Install**
- Go to GitHub releases
- Download for your platform
- Installation steps
- First launch

**1:30-3:00 Configuration**
- API key (optional but recommended)
- Basic settings
- Save and close

**3:00-4:30 First Analysis**
- Load a sample PDF
- Highlight text evidence
- Make a decision
- Export results

**4:30-5:00 Next Steps**
- Where to get help
- Documentation links
- What to learn next

### Deep Dive Video (15-20 minutes)

Use existing VIDEO_TUTORIAL_SCRIPT.md as base, updated for v6.1.0 features:
- Progress tracking status dots (🟢🟡🔴)
- Position counter ("X of Y")
- Session persistence
- Folder memory
- Both AI-assisted and manual workflows

---

## 🎨 Visual Style Guide

### Branding Elements

**Colors:**
- Primary: Professional blues/grays
- Accent: Highlight color for important UI elements
- Keep it clean and academic

**On-Screen Text:**
- Font: Clear, sans-serif (Arial, Helvetica, or Open Sans)
- Size: Large enough to read on mobile
- Position: Lower third for captions
- Duration: Long enough to read 2x

**Callouts & Arrows:**
- Use sparingly
- Highlight UI elements being discussed
- Remove when no longer relevant

---

## 👕 DocMiner Merchandise Plan

### T-Shirt Design Ideas

**Concept 1: Minimalist Logo**
```
DocMiner
[Simple pickaxe + document icon]
```

**Concept 2: Retro Computing**
```
> MINING DOCUMENTS...
> LOADING...
> █████████████ 95% ACCURACY
```

**Concept 3: Academic Humor**
```
I MINE DOCUMENTS
(So You Don't Have To)
```

**Concept 4: Data Mining Visual**
```
[Mining helmet icon]
DOCMINER
Extracting Insights from Academic Literature
```

### Design Specifications

**For RedBubble/Print-on-Demand:**
- File format: PNG with transparent background
- Resolution: 4500 x 5400 pixels minimum (300 DPI)
- Color mode: RGB
- Keep text readable at small sizes

**Mockup Process:**
1. Create design in vector format (Inkscape - free on Linux)
2. Export as high-res PNG
3. Upload to RedBubble
4. Test on various products (t-shirts, mugs, stickers)

### Product Options

**RedBubble Store Items:**
- T-shirts (classic, fitted, V-neck)
- Hoodies
- Stickers
- Mugs
- Laptop sleeves
- Tote bags
- Notebooks

**Pricing Strategy:**
- Set artist margin to 20-30%
- Keep shirts affordable (~$20-25 retail)
- Offer discounts for bulk orders (research teams)

---

## 📅 Production Timeline

### Phase 1: Quick Start Video (Week 1)
- **Day 1-2:** Write final script
- **Day 3:** Record screen demos
- **Day 4:** Record narration
- **Day 5:** Edit and add callouts
- **Day 6-7:** Review, polish, export

### Phase 2: Deep Dive Video (Week 2-3)
- **Week 2:** Generate ElevenLabs audio, record demos
- **Week 3:** Edit, add effects, finalize

### Phase 3: Merchandise (Parallel)
- **Week 1:** Design concepts and mockups
- **Week 2:** Get feedback, refine
- **Week 3:** Set up RedBubble store

---

## 📊 Success Metrics

### Video Performance
- Views in first month
- Watch time (aim for >50% completion rate)
- Comments/questions (engage with viewers)
- Downloads after watching

### Merchandise
- Track which designs are popular
- Use feedback to iterate designs
- Consider limited editions for milestones

---

## 🔗 Resources & Links

### Tutorial Resources
- Existing script: `/docs/VIDEO_TUTORIAL_SCRIPT.md`
- Checklist: `/docs/VIDEO_TUTORIAL_CHECKLIST.md`
- Sample PDFs: `/sample_pdfs/`

### Design Resources
- Inkscape (vector graphics): https://inkscape.org/
- GIMP (image editing): https://www.gimp.org/
- Font resources: Google Fonts, DaFont
- Icon resources: The Noun Project, FontAwesome

### Merchandise Platforms
- RedBubble: https://www.redbubble.com/
- TeePublic: https://www.teepublic.com/
- Printful: https://www.printful.com/ (integrates with Shopify)
- CustomInk: https://www.customink.com/ (bulk orders)

---

## 🎯 Next Steps

1. **Decide on video format** (Quick Start only? Both? Character-based or screencast?)
2. **Write updated script** for v6.1.0 features
3. **Set up recording equipment** and test audio quality
4. **Create 2-3 t-shirt design concepts** for feedback
5. **Schedule production time** (when is the meeting over?)

---

## 💡 Tips from Experience

### Video Production
- **Script everything** - Even "casual" videos benefit from a script
- **Record in segments** - Easier to fix mistakes
- **Use a teleprompter** - Free apps available for tablets
- **Show, don't just tell** - Demonstrate every feature
- **Add captions** - Accessibility + SEO benefits
- **Thumbnail matters** - Design a custom thumbnail for YouTube

### Merchandise
- **Start simple** - One good design is better than five mediocre ones
- **Test print quality** - Order samples before promoting
- **Ask for feedback** - Show designs to your research team first
- **Link from README** - "Support the project" section
- **Consider donations** - Merch profits could fund development/hosting

---

## ✅ Checklist for Recording Day

- [ ] Quiet recording space
- [ ] Microphone tested and working
- [ ] Screen recording software configured
- [ ] DocMiner v6.1.0 installed and ready
- [ ] Sample PDFs loaded
- [ ] Script printed or on teleprompter
- [ ] Water nearby (for voice)
- [ ] Phone on silent
- [ ] Test recording (30 seconds) to check quality
- [ ] Backup recording location set

---

**Ready to create something great! 🎬🎨**
