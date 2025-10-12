import os
from openai import OpenAI, AuthenticationError, APIError

# Initialize global client variable (will be configured on first use)
_openai_client = None

def get_openai_client():
    """Get configured OpenAI client with correct API endpoint."""
    global _openai_client
    
    # Always reload from environment in case config changed
    api_key = (os.getenv("RESEARCH_BUDDY_OPENAI_API_KEY") or 
              os.getenv("OPENAI_API_KEY") or "")
    
    if not api_key:
        print(" No OpenAI API key found. AI analysis will be disabled.")
        return None
    
    # Auto-detect API provider based on key prefix
    if api_key.startswith("sk-or-"):
        # OpenRouter key detected
        base_url = "https://openrouter.ai/api/v1"
        provider = "OpenRouter"
    elif api_key.startswith("sk-proj-"):
        # OpenAI project key
        base_url = "https://api.openai.com/v1"
        provider = "OpenAI (project key)"
    elif api_key.startswith("sk-"):
        # Standard OpenAI key
        base_url = "https://api.openai.com/v1"
        provider = "OpenAI"
    else:
        # Unknown key format - default to OpenAI
        base_url = "https://api.openai.com/v1"
        provider = f"Unknown (defaulting to OpenAI)"
    
    # Create new client with correct endpoint
    _openai_client = OpenAI(api_key=api_key, base_url=base_url)
    print(f"Configured OpenAI client for {provider} - endpoint: {base_url}")
    
    return _openai_client

import fitz  # PyMuPDF
import re
import pdfplumber
import requests
from PyPDF2 import PdfReader

def extract_metadata_pymupdf(pdf_path):
    """
    Extract embedded metadata using PyMuPDF (fitz).
    Returns dict: title, author, subject, keywords, creation_date, producer.
    """
    meta = {"title": None, "author": None, "subject": None, "keywords": None, "creation_date": None, "producer": None}
    try:
        doc = fitz.open(pdf_path)
        raw = doc.metadata
        meta.update({
            "title": raw.get("title"),
            "author": raw.get("author"),
            "subject": raw.get("subject"),
            "keywords": raw.get("keywords"),
            "creation_date": raw.get("creationDate"),
            "producer": raw.get("producer"),
        })
    except Exception as e:
        print(f"PyMuPDF metadata extraction failed for {pdf_path}: {e}")
    return meta


def extract_metadata_pdfplumber(pdf_path):
    """
    Extract text-based metadata using pdfplumber by scanning the first two pages.
    Returns dict: title, author, journal, volume, issue, pages, doi.
    """
    meta = {"title": None, "author": None, "journal": None, "volume": None, "issue": None, "pages": None, "doi": None}
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "".join(page.extract_text() or "" for page in pdf.pages[:2])
        match = re.search(r"^Title:\s*(.*)$", text, re.MULTILINE)
        if match: meta["title"] = match.group(1).strip()
        match = re.search(r"^Author[s]?:\s*(.*)$", text, re.MULTILINE)
        if match: meta["author"] = match.group(1).strip()
        match = re.search(r"doi:\s*(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", text, re.IGNORECASE)
        if match: meta["doi"] = match.group(1)
    except Exception as e:
        print(f"PdfPlumber metadata extraction failed for {pdf_path}: {e}")
    return meta


def extract_doi(pdf_path):
    """
    Scan the first two pages for a DOI using PyPDF2.
    """
    try:
        reader = PdfReader(pdf_path)
        text = "".join(page.extract_text() or "" for page in reader.pages[:2])
        match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.IGNORECASE)
        if match: return match.group(0)
    except Exception as e:
        print(f"PyPDF2 DOI extraction failed for {pdf_path}: {e}")
    return None


def crossref_lookup(doi_or_title):
    """
    Lookup metadata from Crossref using DOI or title.
    Returns dict: journal, volume, issue, author, title.
    """
    headers = {"User-Agent": "py-extractor/0.3 (mailto:youremail@example.com)"}
    if isinstance(doi_or_title, str) and doi_or_title.startswith("10."):
        url = f"https://api.crossref.org/works/{doi_or_title}"
    else:
        url = "https://api.crossref.org/works?query.title=" + requests.utils.quote(doi_or_title or "")
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            #print(f"Crossref lookup returned status {resp.status_code} for {doi_or_title}")
            return {}
        data = resp.json()
        item = data["message"]["items"][0] if not doi_or_title.startswith("10.") else data["message"]
        return {
            "journal": item.get("container-title", [None])[0],
            "volume": item.get("volume"),
            "issue": item.get("issue"),
            "author": ", ".join(f"{a.get('given')} {a.get('family')}" for a in item.get("author", [])) if item.get("author") else None,
            "title": item.get("title", [None])[0],
        }
    except requests.RequestException as e:
        print(f"Crossref lookup network error for {doi_or_title}: {e}")
    except ValueError:
        #print(f"Crossref lookup returned invalid JSON for {doi_or_title}")
        return {}


def datacite_lookup(doi):
    """
    Lookup metadata from DataCite using DOI.
    Returns dict: journal, volume, issue, author, title.
    """
    url = f"https://api.datacite.org/works/{doi}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print(f"DataCite lookup returned status {resp.status_code} for {doi}")
            return {}
        data = resp.json()
        attrs = data.get("data", {}).get("attributes", {})
        creators = attrs.get("creator", [])
        authors = ", ".join(f"{c.get('givenName','')} {c.get('familyName','')}".strip() for c in creators)
        return {
            "journal": attrs.get("container-title"),
            "volume": attrs.get("volume"),
            "issue": attrs.get("issue"),
            "author": authors or None,
            "title": attrs.get("title"),
        }
    except requests.RequestException as e:
        print(f"DataCite lookup network error for {doi}: {e}")
    except ValueError:
        print(f"DataCite lookup returned invalid JSON for {doi}")
    return {}

def extract_positionality(pdf_path, progress_callback=None):
    """
    Deep contextual AI analysis of positionality in academic papers.
    Uses multi-pass semantic analysis for thorough understanding.
    Returns dict with keys: positionality_tests (list), positionality_snippets (dict), positionality_score (float).
    
    This analysis is designed to take 30-60 seconds for thorough semantic understanding
    that goes beyond simple pattern matching. It provides value students can't easily replicate.
    
    Args:
        pdf_path: Path to the PDF file
        progress_callback: Optional callable(progress_pct, message) for progress updates
    """
    
    def report_progress(pct, msg):
        if progress_callback:
            progress_callback(pct, msg)
    
    # Get configured OpenAI client (will reload from environment)
    report_progress(5, "Initializing AI analysis system...")
    client = get_openai_client()
    
    if not client:
        # Fallback to basic regex if no AI available
        return _fallback_regex_analysis(pdf_path, report_progress)
    
    matched = []
    snippets = {}
    score = 0.0
    
    # Extract full PDF text for comprehensive analysis
    report_progress(10, "Reading entire document...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Get text from all pages with section markers
            sections = {}
            full_text = []
            
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                full_text.append(page_text)
                
                # Identify key sections
                if i == 0:
                    sections['introduction'] = page_text[:2000]
                elif i < 3:
                    if not sections.get('introduction'):
                        sections['introduction'] = sections.get('introduction', '') + '\n' + page_text
                
                # Look for methodology/methods section
                if re.search(r'\b(Methods?|Methodology)\b', page_text, re.IGNORECASE):
                    sections['methods'] = page_text[:2000]
                
            # Get conclusion (last 2 pages)
            if len(pdf.pages) >= 2:
                sections['conclusion'] = '\n'.join(p.extract_text() or "" for p in pdf.pages[-2:])
            
            full_text_str = '\n'.join(full_text)
            total_words = len(full_text_str.split())
            
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return {'positionality_tests': [], 'positionality_snippets': {}, 'positionality_score': 0.0}
    
    # PASS 1: Explicit positionality detection (15-30%)
    report_progress(15, "Pass 1/4: Scanning for explicit positionality statements...")
    explicit_result = _analyze_explicit_positionality(client, sections.get('introduction', ''), 
                                                       sections.get('methods', ''))
    if explicit_result['found']:
        matched.append('explicit_positionality')
        snippets['explicit'] = explicit_result['evidence']
        score = max(score, 0.9)
        report_progress(30, "Found explicit positionality statement!")
    
    # PASS 2: Reflexive awareness detection (30-45%)
    report_progress(30, "Pass 2/4: Analyzing for reflexive awareness and researcher positioning...")
    reflexive_result = _analyze_reflexive_awareness(client, sections.get('methods', ''), 
                                                     sections.get('conclusion', ''))
    if reflexive_result['found']:
        matched.append('reflexive_awareness')
        snippets['reflexive'] = reflexive_result['evidence']
        score = max(score, 0.7)
        report_progress(45, "Found reflexive awareness!")
    
    # PASS 3: Subtle/implicit positionality (45-65%)
    if score < 0.5:  # Only do deep scan if we haven't found strong signals yet
        report_progress(45, "Pass 3/4: Deep contextual analysis for subtle positionality...")
        subtle_result = _analyze_subtle_positionality(client, full_text_str, total_words)
        if subtle_result['found']:
            matched.append('subtle_positionality')
            snippets['subtle'] = subtle_result['evidence']
            score = max(score, 0.5)
            report_progress(65, "Found subtle positionality indicators!")
    else:
        report_progress(65, "Skipping subtle analysis - strong evidence already found")
    
    # PASS 4: Final comprehensive assessment (65-90%)
    report_progress(70, "Pass 4/4: Comprehensive semantic assessment...")
    assessment = _final_comprehensive_assessment(client, sections, matched, snippets)
    
    # Combine all findings
    final_snippets = {**snippets, **assessment.get('additional_evidence', {})}
    final_score = assessment.get('confidence_score', score)
    final_tests = matched + assessment.get('additional_patterns', [])
    
    report_progress(95, "Generating detailed analysis report...")
    
    # Generate human-readable explanation
    explanation = _generate_explanation(final_tests, final_snippets, final_score)
    final_snippets['ai_explanation'] = explanation
    
    report_progress(100, "Deep analysis complete!")
    
    return {
        "positionality_tests": final_tests,
        "positionality_snippets": final_snippets,
        "positionality_score": final_score
    }


def _fallback_regex_analysis(pdf_path, report_progress):
    """Fallback regex-based analysis when AI is not available"""
    report_progress(20, "AI unavailable - using pattern matching...")
    
    # Quick regex scan as fallback
    matched = []
    snippets = {}
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0].extract_text() or ""
            
            patterns = {
                "positionality_term": r"\bpositionalit\w*\b",
                "first_person_reflexivity": r"\bI\s+(?:acknowledge|recognize|reflect)",
            }
            
            for name, pattern in patterns.items():
                if re.search(pattern, first_page, re.IGNORECASE):
                    matched.append(name)
                    snippets[name] = "Pattern match found (AI analysis unavailable for details)"
                    break
    except Exception:
        pass
    
    report_progress(100, "Basic analysis complete")
    return {
        'positionality_tests': matched,
        'positionality_snippets': snippets,
        'positionality_score': 0.3 if matched else 0.0
    }


def _analyze_explicit_positionality(client, intro_text, methods_text):
    """Pass 1: Look for explicit positionality statements"""
    try:
        combined_text = (intro_text or '')[:3000] + '\n\n' + (methods_text or '')[:3000]
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert in qualitative research methodology and reflexivity in academic writing.

Your task: Identify EXPLICIT positionality statements where the author directly discusses their own identity, 
background, or position in relation to their research.

Look for statements like:
- "As a [identity] researcher..."
- "My positionality as..."
- "I acknowledge my position as..."
- "Coming from a [background]..."

Return ONLY 'NO' if no explicit statements exist.
If found, return 'YES' followed by the EXACT quote(s) on new lines."""
                },
                {
                    "role": "user",
                    "content": f"Analyze this text for explicit positionality statements:\n\n{combined_text}"
                }
            ],
            temperature=0,
            max_tokens=400,
            timeout=20.0
        )
        
        answer = resp.choices[0].message.content.strip()
        if answer.upper().startswith("YES"):
            evidence = '\n'.join(answer.split('\n')[1:]) if '\n' in answer else answer
            return {'found': True, 'evidence': evidence}
        
    except Exception as e:
        print(f"Explicit analysis failed: {e}")
    
    return {'found': False, 'evidence': ''}


def _analyze_reflexive_awareness(client, methods_text, conclusion_text):
    """Pass 2: Look for reflexive awareness and researcher self-awareness"""
    try:
        combined_text = (methods_text or '')[:3000] + '\n\n' + (conclusion_text or '')[:3000]
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert in reflexive research practices.

Your task: Identify instances where the researcher demonstrates reflexive awareness - acknowledging 
how their background, assumptions, or position may influence the research.

Look for:
- Acknowledgment of potential bias or influence
- Discussion of researcher role in the study
- Recognition of power dynamics
- Statements about assumptions or limitations due to researcher background

Return 'NO' if not found.
If found, return 'YES' followed by the most relevant quote(s)."""
                },
                {
                    "role": "user",
                    "content": f"Analyze for reflexive awareness:\n\n{combined_text}"
                }
            ],
            temperature=0,
            max_tokens=400,
            timeout=25.0
        )
        
        answer = resp.choices[0].message.content.strip()
        if answer.upper().startswith("YES"):
            evidence = '\n'.join(answer.split('\n')[1:]) if '\n' in answer else answer
            return {'found': True, 'evidence': evidence}
        
    except Exception as e:
        print(f"Reflexive analysis failed: {e}")
    
    return {'found': False, 'evidence': ''}


def _analyze_subtle_positionality(client, full_text, total_words):
    """Pass 3: Deep analysis for subtle/implicit positionality markers"""
    try:
        # Analyze in chunks for thoroughness
        chunk_size = 3000
        words = full_text.split()[:chunk_size * 3]  # First ~9000 words
        chunk = ' '.join(words)
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert at identifying subtle positionality markers in academic writing.

Your task: Look for SUBTLE or IMPLICIT indicators that the author is reflecting on their position, 
even if not explicitly stated as "positionality."

This includes:
- Descriptions of the author's relationship to the research site/participants
- Mention of shared identity or difference with research subjects
- Discussion of insider/outsider status
- Personal experiences that motivated the research
- Acknowledgment of privilege, access, or particular perspectives

Return 'NO' if nothing found.
If found, return 'YES' followed by the relevant passages and WHY they suggest positionality awareness."""
                },
                {
                    "role": "user",
                    "content": f"Analyze this text for subtle positionality indicators:\n\n{chunk}"
                }
            ],
            temperature=0.1,  # Slightly higher for nuanced interpretation
            max_tokens=500,
            timeout=35.0
        )
        
        answer = resp.choices[0].message.content.strip()
        if answer.upper().startswith("YES"):
            evidence = '\n'.join(answer.split('\n')[1:]) if '\n' in answer else answer
            return {'found': True, 'evidence': evidence}
        
    except Exception as e:
        print(f"Subtle analysis failed: {e}")
    
    return {'found': False, 'evidence': ''}


def _final_comprehensive_assessment(client, sections, matched_patterns, snippets):
    """Pass 4: Final comprehensive assessment and confidence scoring"""
    try:
        # Summarize what we found so far
        findings_summary = f"Patterns found: {', '.join(matched_patterns) if matched_patterns else 'None'}\n"
        findings_summary += "Evidence collected:\n"
        for key, value in snippets.items():
            findings_summary += f"- {key}: {value[:200]}...\n"
        
        intro_sample = sections.get('introduction', '')[:1500]
        methods_sample = sections.get('methods', '')[:1500]
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a senior qualitative research methodologist providing final assessment.

Given preliminary findings, provide a comprehensive assessment:

1. Confirm or refine the analysis
2. Assign a confidence score (0.0-1.0) for positionality presence
3. Identify any missed indicators
4. Explain the significance of what was (or wasn't) found

Format your response as:
CONFIDENCE: [0.0-1.0]
ASSESSMENT: [Your detailed assessment]
ADDITIONAL_EVIDENCE: [Any new quotes found, or "None"]"""
                },
                {
                    "role": "user",
                    "content": f"Preliminary findings:\n{findings_summary}\n\nIntroduction sample:\n{intro_sample}\n\nMethods sample:\n{methods_sample}\n\nProvide final assessment:"
                }
            ],
            temperature=0.2,
            max_tokens=600,
            timeout=30.0
        )
        
        answer = resp.choices[0].message.content.strip()
        
        # Parse response
        confidence_match = re.search(r'CONFIDENCE:\s*([0-9.]+)', answer)
        confidence = float(confidence_match.group(1)) if confidence_match else 0.5
        
        assessment_match = re.search(r'ASSESSMENT:\s*(.+?)(?=ADDITIONAL_EVIDENCE:|$)', answer, re.DOTALL)
        assessment_text = assessment_match.group(1).strip() if assessment_match else answer
        
        additional_match = re.search(r'ADDITIONAL_EVIDENCE:\s*(.+)', answer, re.DOTALL)
        additional_evidence = additional_match.group(1).strip() if additional_match else "None"
        
        result = {
            'confidence_score': confidence,
            'assessment': assessment_text,
            'additional_evidence': {'final_assessment': assessment_text},
            'additional_patterns': []
        }
        
        if additional_evidence and additional_evidence.lower() != "none":
            result['additional_evidence']['supplemental'] = additional_evidence
            result['additional_patterns'].append('comprehensive_review')
        
        return result
        
    except Exception as e:
        print(f"Final assessment failed: {e}")
        return {'confidence_score': 0.5, 'additional_evidence': {}, 'additional_patterns': []}


def _generate_explanation(patterns, snippets, score):
    """Generate human-readable explanation of findings"""
    if score >= 0.7:
        level = "STRONG positionality detected"
        emoji = ""
    elif score >= 0.4:
        level = "MODERATE positionality indicators found"
        emoji = ""
    else:
        level = "MINIMAL or NO positionality detected"
        emoji = ""
    
    explanation = f"{level} (Confidence: {score:.2f})\n\n"
    
    if patterns:
        explanation += f"Patterns identified: {', '.join(patterns)}\n\n"
        explanation += "Key evidence:\n"
        for key, value in list(snippets.items())[:5]:  # Show top 5
            if key != 'ai_explanation':
                explanation += f"• {key}: {value[:150]}...\n"
    else:
        explanation += "No clear positionality statements were identified in this paper.\n"
        explanation += "The author does not explicitly discuss their position, background, or potential biases.\n"
    
    return explanation


def extract_metadata(pdf_path):
    meta = {}
    meta.update(extract_metadata_pymupdf(pdf_path))
    text_meta = extract_metadata_pdfplumber(pdf_path)
    meta.update(text_meta)

    if meta.get("doi"): meta["doi"] = meta["doi"].strip().rstrip('.;,')
    if not meta.get("doi"):
        doi = extract_doi(pdf_path)
        if doi: meta["doi"] = doi.strip().rstrip('.;,')

    if meta.get("doi"):
        cr = crossref_lookup(meta["doi"]) or datacite_lookup(meta["doi"])
        for k, v in cr.items():
            if not meta.get(k) and v: meta[k] = v

    title_for_lookup = text_meta.get("title")
    if title_for_lookup:
        cr2 = crossref_lookup(title_for_lookup)
        for k in ("journal","volume","issue","author"):
            if not meta.get(k) and cr2.get(k): meta[k] = cr2[k]

    if not meta.get("author"):
        base = os.path.basename(pdf_path)
        nm = os.path.splitext(base)[0]
        m = re.match(r"^([A-Za-z]+)(?:-et-al)?(?:-\d{4}.*)?$", nm)
        if m:
            lead = m.group(1).replace("-"," ").title()
            auth = f"{lead} et al." if "-et-al" in nm else lead
            meta["author"] = auth
            meta["author_from_filename"] = auth

    pos = extract_positionality(pdf_path)
    meta["positionality_tests"]   = pos.get("positionality_tests", [])
    meta["positionality_snippets"] = pos.get("positionality_snippets", {})
    meta["positionality_score"]    = pos.get("positionality_score", 0.0)
    sc = meta.get("positionality_score", 0.0) or 0.0
    meta["positionality_confidence"] = "high" if sc>=0.75 else "medium" if sc>=0.2 else "low"
    return meta


