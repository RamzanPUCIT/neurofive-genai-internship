# AI Resume Feedback Tool

Capstone project — Week 6, Generative AI & Prompt Engineering Internship at NeuroFive Solutions.

A mini web app that reviews a resume against a target job role and returns structured, recruiter-style feedback — a match score, strengths, missing skills, rewritten bullet points, and red flags.

---

## The Problem

Most students send the same resume to every job and never find out why they get rejected. Professional resume reviews are expensive, and generic AI chat replies are long, unstructured, and often invent experience the candidate never had.

This tool gives instant, role-specific feedback in a fixed structure — so it is fast to read and impossible to misread.

---

## Approach

**Core flow:**

```
Resume (PDF upload or pasted text) + Target job role
            ↓
   Groq API  ·  recruiter persona prompt  ·  JSON schema enforced
            ↓
   Structured JSON  →  rendered as a clean Streamlit UI
```

**Advanced element used (Weeks 4–5):** structured JSON output.
The model is forced into `response_format={"type": "json_object"}` with an exact schema defined in the system prompt, so every response is machine-readable and the UI never has to parse free text.

**Prompt design (built on Weeks 1–5):**
- Persona framing — "senior technical recruiter with 10 years of experience"
- Exact JSON schema written into the system prompt
- Anti-hallucination rules — every point must come from the resume text; never invent experience
- Edge-case rule — if the input is not a readable resume, return score 0 and explain
- `temperature=0.3` so feedback stays consistent across runs

---

## Tech Stack

| Layer | Choice |
|---|---|
| Front end | Streamlit |
| LLM provider | Groq |
| Model | `openai/gpt-oss-120b` |
| PDF parsing | pypdf |
| Secrets | python-dotenv (`.env`, git-ignored) |
| Language | Python 3 |

---

## Project Structure

```
Week6/
├── app.py             # Streamlit UI
├── analyzer.py        # Groq API call + JSON parsing
├── prompt.py          # System prompt with JSON schema
├── check_models.py    # Lists live Groq models
├── test_run.py        # CLI test of the core logic
├── requirements.txt
├── .env               # not committed
└── .gitignore
```

---

## Setup

```bash
python -m venv venv
venv\Scripts\Activate          # Windows
pip install -r requirements.txt
```

Create a `.env` file:

```
GROQ_API_KEY=your_key_here
```

Run:

```bash
streamlit run app.py
```

---

## Testing

Tested with 5 realistic inputs:

| # | Input | Expected | Result |
|---|---|---|---|
| 1 | Real ML resume → Junior Machine Learning role | High score | **78/100** ✅ |
| 2 | Same resume → mismatched role | Score drops | **30/100** ✅ |
| 3 | One-line vague resume → Junior AI Engineer | Very low score | **10/100** ✅ |
| 4 | Non-resume text (weather report) → Data Scientist | Score 0, no invented strengths | **0/100, strengths empty** ✅ |
| 5 | `hello` (5 characters) | Blocked before the API call | Validation warning ✅ |

Test 4 is the key one: the model returned an empty strengths list instead of inventing qualifications — the anti-hallucination rule in the prompt held.

---

## Problems Faced & Fixes

**1. Model 404s.** Hard-coded model names have failed before, so `check_models.py` queries the live Groq model list first. `openai/gpt-oss-120b` was picked from that list, not from memory.

**2. `400 — 'messages' must contain the word 'json'`.** Groq requires the literal word "json" somewhere in the prompt when JSON mode is on. Fixed by writing the schema into the system prompt.

**3. `400 — json_validate_failed` with empty output.** `max_tokens` was set to 50. Reasoning models spend tokens thinking before they write, so the budget ran out before any JSON was produced. Raised to 3000.

---

## What I'd Improve With More Time

- **Job description input** — compare against a pasted JD instead of just a role title, for far more precise gap analysis
- **RAG layer** — retrieve real job postings so missing-skills feedback reflects the current market, not model priors
- **PDF export** — download the feedback as a formatted report
- **Before/after diff view** — show original vs improved bullets side by side with changes highlighted
- **Batch mode** — score one resume against several roles at once to find the best fit
- **Scanned-PDF support** — add OCR, since pypdf returns nothing for image-based PDFs

---

## Author

**Muhammad Ramzan** — Computer Science undergraduate, PUCIT
Generative AI & Prompt Engineering Intern at NeuroFive Solutions
