"""
agents.py — the two agents.

Agent 1 (Writer)  : drafts content on a topic. Knows nothing about the Editor.
Agent 2 (Editor)  : receives the draft, critiques it, and returns an improved
                    version PLUS a machine-readable list of what it changed.

The Editor returning structured JSON is the key design decision here: it means
"what did the Editor actually improve?" is data we can print and diff, not a
vibe we have to eyeball.
"""

import json
import re

from llm import call_llm

# --------------------------------------------------------------------------
# AGENT 1 — THE WRITER
# --------------------------------------------------------------------------

WRITER_SYSTEM = """You are WRITER, a technical content writer producing first drafts.

Your job: given a topic and an audience, write a complete, publishable-quality draft.

Rules:
- Write in Markdown. Start with an H1 title, then 3-5 short sections with H2 headings.
- Open with a concrete hook, not a definition. Never begin with "In today's world".
- Prefer specific examples, numbers and named tools over general claims.
- Short paragraphs (2-4 sentences). Plain English. No filler adjectives.
- Target the requested word count within ±15%.
- End with one clear takeaway the reader can act on.

You produce the draft only. Do not add notes, disclaimers, or commentary about
your own writing. Someone else will review it."""


def write_draft(topic: str, audience: str = "junior developers",
                words: int = 500) -> str:
    """Agent 1: produce the raw first draft."""
    user = (
        f"Topic: {topic}\n"
        f"Audience: {audience}\n"
        f"Target length: about {words} words\n\n"
        f"Write the draft now."
    )
    return call_llm(WRITER_SYSTEM, user, max_tokens=2000, temperature=0.8)


# --------------------------------------------------------------------------
# AGENT 2 — THE EDITOR / CRITIC
# --------------------------------------------------------------------------

EDITOR_SYSTEM = """You are EDITOR, a ruthless but fair senior editor and fact-checker.

You receive a draft written by another agent. You do NOT rewrite it from scratch
and you do NOT change the author's angle — you find real problems and fix them.

What you look for, in priority order:
1. ACCURACY   — claims that are wrong, outdated, or stated with false confidence.
2. EVIDENCE   — assertions that need a concrete example, number, or named tool.
3. STRUCTURE  — buried lede, sections in the wrong order, missing takeaway.
4. CLARITY    — jargon without explanation, bloated sentences, vague pronouns.
5. TONE       — hype, clichés, marketing voice, "In today's fast-paced world".

Rules:
- Every issue you raise must quote the exact text you object to.
- Do not invent statistics or sources to "strengthen" the draft. If a claim needs
  a source the author must supply, flag it instead of fabricating one.
- Keep the revised draft within ±20% of the original length. Tighten, don't pad.
- If a section is already good, leave it alone. Silence is a valid review.

Respond with ONE valid JSON object and nothing else — no prose, no code fences:

{
  "overall_verdict": "one sentence on the draft's biggest weakness",
  "issues_found": [
    {
      "type": "accuracy | evidence | structure | clarity | tone",
      "severity": "high | medium | low",
      "quote": "the exact text from the draft",
      "why": "what is wrong with it",
      "fix": "what you changed it to"
    }
  ],
  "changes_made": ["short bullet summary of each edit"],
  "revised_draft": "the full improved draft in Markdown"
}"""


def review_draft(topic: str, draft: str) -> dict:
    """Agent 2: critique + improve. Returns the parsed JSON review."""
    user = (
        f"The draft below was written on the topic: {topic}\n\n"
        f"--- BEGIN DRAFT ---\n{draft}\n--- END DRAFT ---\n\n"
        f"Review and improve it. Respond with the JSON object only."
    )
    raw = call_llm(EDITOR_SYSTEM, user, temperature=0.3, max_tokens=4000, json_mode=True)
    return _parse_json(raw, fallback_draft=draft)


# --------------------------------------------------------------------------
# OPTIONAL PATTERN B — Editor critiques, Writer does the rewrite
# --------------------------------------------------------------------------

def writer_revises(topic: str, draft: str, review: dict) -> str:
    """Send the Editor's notes back to the Writer so the author keeps the pen.

    Slower and costs a third call, but the voice stays consistent. Good thing to
    demo in the video as 'the same two agents, wired a different way'.
    """
    notes = "\n".join(f"- [{i['severity']}/{i['type']}] {i['quote']!r} — {i['why']}"
                      for i in review.get("issues_found", []))
    user = (
        f"Here is your draft on '{topic}':\n\n{draft}\n\n"
        f"An editor reviewed it and raised these issues:\n{notes}\n\n"
        f"Rewrite the draft addressing every issue. Keep your own voice and "
        f"angle. Output the revised Markdown draft only."
    )
    return call_llm(WRITER_SYSTEM, user, temperature=0.8, max_tokens=2000)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _parse_json(raw: str, fallback_draft: str) -> dict:
    """LLMs sometimes wrap JSON in prose or code fences. Dig it out safely."""
    text = raw.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Last resort: grab the outermost {...} block.
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    print("  [warn] Editor did not return valid JSON — keeping original draft.")
    return {
        "overall_verdict": "PARSE FAILED — see raw_response",
        "issues_found": [],
        "changes_made": [],
        "revised_draft": fallback_draft,
        "raw_response": raw,
    }
