# ElevenLabs Setup Guide for Research Buddy Tutorial

## Quick Start Guide

### Step 1: Create ElevenLabs Account
1. Go to https://elevenlabs.io/
2. Sign up for a free account
3. Free tier includes: 10,000 characters/month (plenty for this tutorial)

### Step 2: Choose Voices for Each Character

**Recommended Voice Assignments:**

1. **Professor Todd** (Experienced educator)
   - Voice: "Adam" or "Antoni"
   - Age: Mature
   - Tone: Warm, authoritative, professorial
   - Accent: American (neutral)

2. **Research Buddy** (AI Assistant)
   - Voice: "Josh" or "Arnold"  
   - Age: Young adult
   - Tone: Friendly, helpful, enthusiastic
   - Accent: American (neutral)

3. **Maya** (Graduate Assistant)
   - Voice: "Elli" or "Rachel"
   - Age: Young adult
   - Tone: Curious, engaged, enthusiastic
   - Accent: American (neutral)

### Step 3: Generate Audio for Each Scene

**Process:**
1. Copy one character's lines from a scene
2. Paste into ElevenLabs text box
3. Select the voice
4. Click "Generate"
5. Download the MP3 file
6. Name it: `scene1_professor.mp3`, `scene1_maya.mp3`, etc.

### Step 4: Organize Your Files

```
research-buddy/
  docs/
    video_tutorial/
      audio/
        scene1_professor_intro.mp3
        scene1_buddy_intro.mp3
        scene1_maya_intro.mp3
        scene2_professor_config.mp3
        scene2_buddy_apikey.mp3
        scene2_maya_question.mp3
        ... etc
      script/
        VIDEO_TUTORIAL_SCRIPT.md
        recording_notes.txt
```

## Character Line Count (for planning)

**Total script:** ~3,500 words = ~28,000 characters

**Breakdown by character:**
- Professor Todd: ~1,200 words (~9,600 characters)
- Research Buddy: ~1,100 words (~8,800 characters)
- Maya: ~1,200 words (~9,600 characters)

**Free tier limit:** 10,000 characters/month

**Solution:** You'll need to either:
1. Upgrade to paid tier ($5/month for 30,000 chars) **RECOMMENDED**
2. Split across 3 months (generate one character per month)
3. Use multiple free accounts

**Pro tip:** The $5/month "Starter" plan is worth it for video production!

## Advanced: Voice Settings for Each Character

### Professor Todd - Authoritative but Warm
```
Voice: Adam
Stability: 60%
Clarity: 75%
Style Exaggeration: 30%
Speaker Boost: ON
```

### Research Buddy - Friendly & Helpful
```
Voice: Josh
Stability: 50%
Clarity: 80%
Style Exaggeration: 40%
Speaker Boost: ON
```

### Maya - Curious & Enthusiastic
```
Voice: Rachel
Stability: 55%
Clarity: 75%
Style Exaggeration: 45%
Speaker Boost: ON
```

## Tips for Best Results

1. **Add pauses** with commas and periods in the script
2. **Use SSML tags** for emphasis (if needed):
   - `<break time="0.5s"/>` for pauses
   - `<emphasis level="strong">important word</emphasis>` for stress
   
3. **Generate in sections** - Don't try to do whole scenes at once
   - Easier to edit
   - Can re-generate individual lines if needed

4. **Listen before downloading** - ElevenLabs lets you preview
   - Adjust settings if voice doesn't sound right
   - Regenerate until it's perfect

## Alternative: Voice Cloning (Advanced)

If you want truly custom voices:
1. Record 1-2 minutes of your own voice reading the script
2. Upload to ElevenLabs Professional Voice Cloning
3. Generate all dialogue in your cloned voice
4. Pitch-shift in post-production for different characters

## Next Steps After Audio Generation

1. **Import audio into video editor** (DaVinci Resolve, Adobe Premiere, iMovie)
2. **Sync with screen recording** of Research Buddy
3. **Add character images** as overlays in corner
4. **Add visual callouts** (arrows, circles, text highlights)
5. **Export final video**

## Cost Estimate

**Recommended Setup:**
- ElevenLabs Starter: $5/month (cancel after first month)
- Total characters needed: ~28,000
- Starter plan: 30,000 characters ✓

**ROI:** One month subscription produces:
- This Research Buddy tutorial
- Multiple Mathemagical History Tour episodes
- Any other narrated content

## Sample Test Generation

Want to test before committing? Try this short sample:

**Test Text (Professor Todd):**
```
Welcome to Research Buddy! I'm Professor Todd, and I've been researching 
positionality statements in academic writing for years. Today, I'll show you 
how our AI-powered tool can help identify these important elements in scholarly work.
```

Generate this in 2-3 different voices to find the one you like best!

## Questions?

Check:
- ElevenLabs Documentation: https://elevenlabs.io/docs
- ElevenLabs Discord: Community support
- Video tutorials on YouTube: Search "ElevenLabs tutorial"

---

**Ready to get started?** Sign up at https://elevenlabs.io/ and let's create some amazing narration! 🎙️
