# DocMiner Video Tutorial Script
## Character-Based Narration for ElevenLabs

**Duration:** ~8-10 minutes  
**Characters:**
- **Professor Todd** (Left) - Warm, experienced educator voice
- **DocMiner** (Center) - Friendly, helpful AI assistant voice  
- **Maya** (Right, GA) - Curious, enthusiastic graduate student voice

---

## Scene 1: Introduction (30 seconds)

**[Screen: Title card with three characters]**

**Professor Todd:**  
"Welcome to DocMiner! I'm Professor Todd, and I've been researching positionality statements in academic writing for years."

**DocMiner:**  
"And I'm DocMiner, your AI-powered assistant! I'm here to help you identify and analyze positionality statements efficiently."

**Maya:**  
"Hi! I'm Maya, a graduate assistant. I'll be learning alongside you today. Let's get started!"

---

## Scene 2: First-Time Configuration Dialog (2 minutes)

**[Screen: App launches, configuration dialog appears]**

**Maya:**  
"Oh! A configuration window popped up the first time I launched the app. What do I need to enter here?"

**Professor Todd:**  
"Great question, Maya! Let's go through each field. First, you'll need an OpenAI API key."

**DocMiner:**  
"The API key lets me access ChatGPT to help analyze text and identify positionality patterns. You can get one from platform.openai.com."

**Professor Todd:**  
"Next is the GitHub token. This is how we'll save and share your analysis work with the team."

**Maya:**  
"So the API key is for the AI analysis, and the GitHub token is for uploading our work. Got it!"

**DocMiner:**  
"Exactly! Now, let's talk about the GitHub username and repository fields."

**Professor Todd:**  
"Enter 'OhioMathTeacher' as the username - that's my GitHub account. And 'docminer' as the repository name."

**Maya:**  
"Why are we all using your repository, Professor?"

**Professor Todd:**  
"Good thinking! We're collecting everyone's analysis in one central location. This way, when all our graduate assistants analyze 5-10 articles each, we'll have a shared dataset."

**DocMiner:**  
"This shared data is crucial! Once we gather enough training examples, we'll use them to improve my pattern detection - aiming for 95% accuracy or better!"

**[Screen: User clicks 'Save Configuration' - single success dialog appears]**

**Maya:**  
"Perfect! Configuration saved. Now let's analyze some papers!"

---

## Scene 3: Getting Started - Entering Your Name & Loading PDFs (1 minute)

**[Screen: Main DocMiner interface]**

**DocMiner:**  
"First things first, Maya - enter your name in the 'Reviewer Name' field at the top."

**Maya:**  
"Why is that important?"

**Professor Todd:**  
"Your name becomes part of the saved filename. When we review all the analyses later, we'll know exactly who reviewed which paper and what their judgment was."

**[Screen: Click 'Load PDF' button]**

**Maya:**  
"Now I'll click 'Load PDF' and select an article to analyze. I'll start with this Armstrong paper on ethical engagement in anthropology."

**DocMiner:**  
"Great choice! The PDF is now displayed on the left side. You can navigate through pages using the controls at the bottom."

---

## Scene 4: Human Evidence - Highlighting Text (2 minutes)

**[Screen: Maya navigating through PDF pages]**

**Professor Todd:**  
"Now comes the important part - finding positionality statements. These are places where authors reflect on their own position, identity, or role in the research."

**Maya:**  
"Like when they say 'As a researcher...' or 'From my perspective as...'?"

**DocMiner:**  
"Exactly! When you find such a statement, simply click and drag to select the text in the PDF viewer."

**[Screen: Maya highlights text on page 3]**

**Maya:**  
"I found one! 'Though the courses originated independently, our respective focus on access and agency spurred exploration...'"

**DocMiner:**  
"Perfect! See how the selected text now appears in the 'Selected Text for Evidence' panel on the right? This is your human-identified evidence."

**Professor Todd:**  
"This is crucial, Maya. Your human judgment is training data. You're teaching DocMiner what a real positionality statement looks like."

**Maya:**  
"So I'm not just analyzing papers - I'm helping train the AI!"

**DocMiner:**  
"Precisely! Every piece of evidence you mark helps me get better at automatic detection."

---

## Scene 5: AI Pre-screening Analysis (1.5 minutes)

**[Screen: AI Pre-screening Analysis button]**

**Maya:**  
"What about this 'AI Pre-screening Analysis' button?"

**DocMiner:**  
"That's where I can help! Click that button, and I'll scan the entire document for potential positionality statements."

**[Screen: Maya clicks button, AI analysis appears]**

**Professor Todd:**  
"Think of this as a first pass. DocMiner will find likely candidates, but you still need to review them with your expert judgment."

**Maya:**  
"Oh, I see - it found several possible statements. Some look good, but a couple seem like they might be false positives."

**DocMiner:**  
"Exactly my current limitation! That's why we need your training data. Your corrections teach me to distinguish real positionality statements from similar-sounding text."

**Professor Todd:**  
"And notice - you can edit the text in both panels before submission. This lets you refine or add context to any evidence you've collected."

---

## Scene 6: Making Your Decision (1 minute)

**[Screen: Judgment radio buttons visible]**

**Maya:**  
"Now I need to make a decision. I see three options here..."

**DocMiner:**  
"Right! You can mark the paper as 'Positive' if it contains clear positionality statements, 'Negative' if it doesn't, or 'Needs Revision' if you're unsure."

**Professor Todd:**  
"This judgment becomes part of the filename when you save. For example, if you mark Armstrong's paper as positive, the file will be named something like 'Maya_Armstrong_positive_20251010_143022.json'"

**Maya:**  
"That's so much clearer than a cryptic filename! I can immediately see who reviewed it, which paper, and what the decision was."

---

## Scene 7: Uploading vs. Downloading (2 minutes)

**[Screen: Upload and Download buttons visible]**

**DocMiner:**  
"Now you have two options for saving your work: Upload to GitHub, or Download locally."

**Maya:**  
"What's the difference?"

**Professor Todd:**  
"Upload to GitHub is our primary method. It automatically saves your analysis to our shared repository where the whole team can access it."

**DocMiner:**  
"When you click 'Upload to GitHub', I'll save your work locally first in your home directory at ~/.research_buddy/training_reports/, then copy it to the repository and push it to GitHub."

**[Screen: Shows the upload process]**

**Maya:**  
"So it's saved in two places - my computer and the cloud?"

**Professor Todd:**  
"Exactly! The local copy is your backup. The GitHub copy is shared with the team."

**DocMiner:**  
"And here's the important part - your file goes into a single folder on GitHub called 'training_reports'. Everyone's analyses collect there."

**Maya:**  
"What if I'm working offline, or GitHub isn't available?"

**Professor Todd:**  
"Great question! That's why we added the Download option. Click it, and you'll get the JSON file saved to your downloads folder."

**DocMiner:**  
"You can manually upload it to GitHub later, or send it to Professor Todd via email. We wanted to make sure you never lose your work!"

---

## Scene 8: The Big Picture - Training Data & Goals (1.5 minutes)

**[Screen: Show example of multiple training reports in the folder]**

**Professor Todd:**  
"Let me show you the bigger picture. Every time you or another GA uploads an analysis, it goes into this shared training_reports folder."

**Maya:**  
"I can see files from different reviewers here - billy_Armstrong_positive, howard_Knight_negative... this is everyone's work!"

**DocMiner:**  
"This is my learning dataset! Once we collect analyses from all our graduate assistants on 5-10 articles each, we'll have dozens of training examples."

**Professor Todd:**  
"Then we'll analyze these patterns - what human experts identified as real positionality statements versus what they rejected."

**Maya:**  
"So you'll use our collective judgment to improve the AI detection?"

**DocMiner:**  
"Exactly! The goal is to train me to automatically detect positionality statements with 95% or better accuracy."

**Professor Todd:**  
"We're eliminating false negatives - real statements I might miss - and false positives - things that look like positionality but aren't."

**Maya:**  
"So eventually, the AI could do this automatically?"

**DocMiner:**  
"That's the goal! But we'll always need human verification. Your expert judgment is irreplaceable."

---

## Scene 9: Closing & Next Steps (30 seconds)

**[Screen: All three characters together]**

**Professor Todd:**  
"Excellent work today, Maya! You're now ready to start analyzing papers and contributing to our training dataset."

**Maya:**  
"I'm excited! This is real research - and I'm helping improve AI tools at the same time!"

**DocMiner:**  
"Remember: Every analysis you complete makes me smarter. Your careful attention to detail is training the next generation of research tools!"

**Professor Todd:**  
"If you have questions, check the documentation in the docs folder, or reach out to our team. Happy analyzing!"

**All Three:**  
"Thank you for joining us in the DocMiner project!"

**[Screen: Fade to credits/resources]**

---

## Post-Production Notes

### Visual Overlays to Include:
1. **Scene 2:** Highlight each configuration field as it's discussed
2. **Scene 4:** Arrow pointing to selected text and evidence panel
3. **Scene 5:** Circle the AI button, show analysis appearing
4. **Scene 6:** Zoom on radio buttons when discussed
7. **Scene 7:** Split screen showing local save + GitHub upload
8. **Scene 8:** File browser showing multiple training reports

### Character Images:
- Show character avatars in lower corner during their speaking parts
- Could animate simple expressions (happy, curious, explaining)

### Background Music:
- Soft, professional, non-distracting
- Slightly upbeat to match DocMiner's helpful tone

---

## ElevenLabs Voice Suggestions

**Professor Todd:**
- Voice: "Adam" or "Antoni" - warm, authoritative, mature
- Settings: Standard pace, slightly lower pitch

**DocMiner:**
- Voice: "Josh" or "Arnold" - friendly, clear, helpful
- Settings: Slightly faster pace, upbeat tone

**Maya:**
- Voice: "Elli" or "Rachel" - enthusiastic, curious, clear
- Settings: Standard pace, energetic delivery

---

## Estimated Timeline

- Script finalization: 30 minutes
- ElevenLabs voice generation: 1 hour
- Screen recording: 1 hour
- Video editing: 2-3 hours
- **Total:** ~5 hours

Would you like me to adjust anything in this script?
