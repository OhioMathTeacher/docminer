import os
import openai

# Try multiple environment variable names for API key
api_key = (os.getenv("RESEARCH_BUDDY_OPENAI_API_KEY") or 
          os.getenv("OPENAI_API_KEY") or "")

if api_key:
    openai.api_key = api_key
else:
    print("⚠️  No OpenAI API key found. AI analysis will be disabled.")
    openai.api_key = None
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

import re
import pdfplumber
import openai  # make sure your key is configured

def extract_positionality(pdf_path):
    """
    Extract positionality/reflexivity statements via enhanced regex + AI fallbacks.
    Uses comprehensive pattern matching with AI enhancement when available.
    Returns dict with keys: positionality_tests (list), positionality_snippets (dict), positionality_score (float).
    """
    
    # Refresh API key in case it was set by configuration dialog
    api_key = (os.getenv("RESEARCH_BUDDY_OPENAI_API_KEY") or 
              os.getenv("OPENAI_API_KEY") or "")
    
    if api_key and api_key != openai.api_key:
        openai.api_key = api_key
        print(f"✅ Updated OpenAI API key from environment")
    
    matched = []
    snippets = {}
    score = 0.0

    # 1) Header regex tests (first page)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = pdf.pages
            header_text = pages[0].extract_text() or ""
    except Exception:
        header_text = ""

    tests = {
        # Core positionality patterns
        "explicit_positionality":   re.compile(r"\b(?:My|Our) positionality\b", re.IGNORECASE),
        "positionality_term":       re.compile(r"\bpositionalit\w*\b", re.IGNORECASE),
        
        # First-person reflexive statements
        "first_person_reflexivity": re.compile(r"\bI\s+(?:reflect|acknowledge|consider|recognize|admit|confess|must acknowledge|should note)\b", re.IGNORECASE),
        "researcher_positioning":   re.compile(r"\bI,?\s*as (?:a |the )?(?:researcher|scholar|author),", re.IGNORECASE),
        "identity_disclosure":      re.compile(r"\bAs a (?:woman|man|Black|White|Latina?|Asian|Indigenous|queer|trans|disabled|working.class)[^.]{0,50}(?:researcher|scholar|I)\b", re.IGNORECASE),
        
        # Reflexive awareness patterns  
        "reflexive_awareness":      re.compile(r"\b(?:acknowledge|recognize|aware|conscious) (?:that )?(?:my|our) [^.]{10,60}(?:influence|affect|shape|bias|perspective|position)", re.IGNORECASE),
        "background_influence":     re.compile(r"\b(?:My|Our) (?:background|experience|identity|perspective) [^.]{10,80}(?:influence|shape|inform|affect)", re.IGNORECASE),
        
        # Positioning language
        "positioned_researcher":    re.compile(r"\b(?:positioned|situated) as [^.]{10,60}(?:researcher|scholar)", re.IGNORECASE),
        "social_location":          re.compile(r"\bsocial location[^.]{0,50}", re.IGNORECASE),
        "standpoint_perspective":   re.compile(r"\b(?:standpoint|situated knowledge|insider perspective|outsider status)[^.]{0,30}", re.IGNORECASE),
        
        # Methodological reflexivity
        "methodological_reflexivity": re.compile(r"\b(?:reflexiv|positional)[^.]{0,30}(?:methodology|approach|stance)", re.IGNORECASE),
        "disclosure_statement":     re.compile(r"\b(?:I|We) (?:bring|carry|hold) [^.]{10,60}(?:perspective|lens|experience|bias)", re.IGNORECASE),
        
        # Bias acknowledgment
        "bias_acknowledgment":      re.compile(r"\b(?:my|our) (?:own )?(?:bias|biases|assumptions|preconceptions)[^.]{0,50}", re.IGNORECASE),
        "subjective_awareness":     re.compile(r"\b(?:subjective|partial|limited) (?:perspective|view|understanding)[^.]{0,30}", re.IGNORECASE),

        # Enhanced academic reflexivity patterns (Research Buddy 2.0)
        "authorial_positioning":    re.compile(r"\b(?:we|I)\s+(?:articulate|position|locate|situate)\s+(?:our|my)\s+(?:own\s+)?(?:cultural\s+)?(?:location|position|positionality|perspective)", re.IGNORECASE),
        "research_context":         re.compile(r"\b(?:this\s+paper|this\s+research|my\s+fieldwork|our\s+study)\s+(?:has\s+)?(?:developed|emerged|stems|arises)\s+(?:out\s+of|from)\s+(?:my|our)\s+(?:experiences?|background|work)", re.IGNORECASE),
        "positional_influence":     re.compile(r"\b(?:our|my)\s+(?:position|positionality|background|experience)\s+(?:may\s+|might\s+|could\s+|will\s+)?(?:influence|affect|shape|inform)\s+(?:curriculum|research|interpretation|analysis)", re.IGNORECASE),
        "fieldwork_reflexivity":    re.compile(r"\b(?:I|we)\s+(?:became\s+aware|observed|recognized|realized)\s+that\s+(?:my|our)\s+(?:position|presence|background|identity)", re.IGNORECASE),
        "assumption_acknowledgment": re.compile(r"\b(?:we|I)\s+(?:make|hold|carry|bring)\s+(?:assumptions|presuppositions|biases)\s+(?:based\s+on|about|regarding)\s+(?:our|my)\s+(?:position|background|experience)", re.IGNORECASE),
        "contextual_positioning":   re.compile(r"\b(?:it\s+is\s+)?from\s+this\s+(?:context|position|perspective|standpoint)\s+that\s+(?:we|I)\s+(?:position|approach|understand|view)", re.IGNORECASE),
        "political_positioning":    re.compile(r"\b(?:our|my)\s+position\s+is\s+(?:a\s+)?(?:political|critical|theoretical)\s+(?:point\s+of\s+departure|stance|perspective)", re.IGNORECASE),
        "experiential_grounding":   re.compile(r"\bthrough\s+(?:discussion\s+of\s+)?(?:my|our)\s+(?:fieldwork\s+|research\s+|personal\s+)?experiences?\s+(?:in|with|conducting|as)", re.IGNORECASE),
        "reflexive_observation":    re.compile(r"\b(?:as\s+I|while\s+I|when\s+I|however,?\s+I)\s+(?:got\s+to\s+know|spent\s+time|interacted|worked)\s+.{0,30}\s+(?:I\s+observed|I\s+became\s+aware|I\s+realized)", re.IGNORECASE),
        "researcher_identity":      re.compile(r"\b(?:as\s+individuals|as\s+researchers|as\s+authors),?\s+(?:we|I)\s+(?:make|hold|carry|bring|acknowledge)", re.IGNORECASE),

    }

    for name, pat in tests.items():
        m = pat.search(header_text)
        if m:
            matched.append(name)
            snippets[name] = m.group(0).strip()
            break

    # 2) GPT-fallback on header if no regex hit
    if not matched and header_text and openai.api_key:
        try:
            snippet = header_text[:500]
            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a specialist in academic research methods. "
                            "Find sentences where the author explicitly uses first‑person language "
                            "to reflect on their own positionality or biases. "
                            "If none exists in the passage, reply 'NONE'."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            "Passage:\n\n" + header_text[:500]
                        )
                    }
                ],
                temperature=0.0
            )

            answer = resp.choices[0].message.content.strip()
            if answer.upper() != "NONE":
                matched.append("gpt_header")
                snippets["gpt_header"] = answer
        except (openai.AuthenticationError, openai.APIError) as e:
            print(f"OpenAI API error (header analysis): {e}")
            # Continue without GPT analysis

    # 3) Tail-end regex scan (last 2 pages)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            tail_text = "\n".join(p.extract_text() or "" for p in pdf.pages[-2:])
    except Exception:
        tail_text = ""

    tail_hits = [name for name, pat in tests.items() if pat.search(tail_text)]
    if tail_hits:
        for name in tail_hits:
            if name not in matched:
                matched.append(name)
            snippets.setdefault("tail_"+name, tail_text[:200] + "...")
        score = max(score, 0.5)

    # 4) Baseline score
    if score == 0.0:
        score = len(matched) / (len(tests) + 2)

    # 5) Conditional full-text GPT-4 pass
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = "\n".join(p.extract_text() or "" for p in pdf.pages)
            page_count = len(pdf.pages)
    except Exception:
        full_text = ""
        page_count = 0

    # after computing `score` and loading full_text…

    # only invoke full‐text GPT if:
    # 1) there was some regex/tail signal (score ≥ 0.1)
    # 2) and the PDF actually has a Discussion/Implications/Conclusion heading
    needs_ai = (
        score >= 0.1
        and bool(re.search(r"\b(Discussion|Implications|Conclusion)\b",
                           full_text,
                           re.IGNORECASE))
    )

    if needs_ai:
        m = re.search(r"(Discussion|Implications|Conclusion)", full_text, re.IGNORECASE)
        tail = full_text[m.start():] if m else full_text
        words = tail.split()
        chunk_size = 500
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a specialist in academic research methods. "
                            "Identify any first‑person (‘I’ or ‘we’) statements in this passage "
                            "where the author Reflects on their own positionality or standpoint. "
                            "If none exists, reply 'NO'."
                        )
                    },
                    {
                        "role": "user",
                        "content": "Passage:\n\n" + chunk
                    }
                ],
                temperature=0
            )
            answer = resp.choices[0].message.content.strip()
            if answer.upper().startswith("YES"):
                matched.append("gpt_full_text")
                snippet = answer.splitlines()[1] if "\n" in answer else answer
                snippets["gpt_full_text"] = snippet
                score = 1.0
                break

    return {
        "positionality_tests": matched,
        "positionality_snippets": snippets,
        "positionality_score": score
    }


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


