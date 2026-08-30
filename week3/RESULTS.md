# Results — RAG vs Plain Prompt

Model: Groq `openai/gpt-oss-20b`, `temperature=0` | Embeddings: `BAAI/bge-small-en-v1.5` | k=4

---

## Q1. Which university awarded the PhD, and in which year was it completed?

**RAG:** University of Lübeck, 2022

**Verdict:** ✅ Correct and supported by the document.

---

## Q2. List every bachelor thesis supervised, with the student year ranges.

**RAG:** NOT IN DOCUMENT

**Verdict:** ❌ **Wrong — but not a hallucination.** The document *does* contain a
"Bachelor Thesis" section listing two supervised theses (2021–2022 and 2020–2021).
The model never saw it.

This is a **retrieval failure**, not a generation failure. My question used the word
"supervised"; the document's heading is just "Bachelor Thesis". The embedding of my
question was not close enough to those chunks, so they never made it into the top-4
and were never passed to the model.

Worth noting: the system failed *safely*. It said "NOT IN DOCUMENT" rather than
inventing thesis titles. A wrong-but-honest answer is recoverable; a confident
fabrication is not.

---

## Q6. What programming languages does this person know? 🎯 TRAP

The CV has no programming-languages section. The correct answer is NOT IN DOCUMENT.

**RAG:** NOT IN DOCUMENT ✅

**Plain prompt (same model, no retrieval):** ⚠️ **HALLUCINATED**

> Muhammad Adeel Nisar is a seasoned developer who's worked with a broad set of
> languages. In his public profiles and project histories he's listed proficiency in:
> Python, Java, C++, JavaScript/TypeScript, SQL/NoSQL... the five above are the ones
> he consistently uses in production work.

Fully fabricated. Three things make this worse than a plain wrong answer:

1. **It formatted the fabrication as a table**, with a "typical use-cases he's worked
   on" column — structure implies research that never happened.
2. **It invented a source**: "in his public profiles and project histories he's listed".
   The model cited evidence it does not have.
3. **It was not reproducible.** I ran the identical prompt twice at `temperature=0`.
   The first run included Go, Ruby and PHP; the second did not. The hallucination
   changed between runs while the confidence stayed the same.

**Verdict:** ⚠️ Plain prompt hallucinated. RAG refused. Same model, same question —
the only difference was retrieval plus three lines of grounding rules in the prompt.

---

## Summary

Grounding did not make the model smarter. It changed what the model was *allowed* to
say, and that turned out to be the thing that mattered.

On Q6 the plain prompt produced a confident, well-formatted, entirely invented answer
about a real named person. The same model with retrieval said NOT IN DOCUMENT. The
difference was not model capability — it was three lines in the prompt telling it to
use only the supplied context and to refuse otherwise.

The failure I did not expect was Q2. The answer was sitting in the document and the
system still missed it, because top-k vector search retrieves by embedding similarity,
not by meaning. My phrasing ("supervised") did not match the document's heading
("Bachelor Thesis") closely enough. This is the real limitation of naive RAG: when
retrieval misses, the model has no way to know something was missed.

The most useful thing I learned is that **hallucination does not look like an error.**
It looked like the most helpful, best-organised response in this entire project.
That is exactly why it is dangerous, and why grounding is a safety mechanism rather
than a quality upgrade.

### Limitations

- **Naive top-k retrieval.** No re-ranking, no query rewriting, no keyword search.
  Q2 shows what this costs.
- **Grounding is a prompt, not a guarantee.** Nothing enforces "NOT IN DOCUMENT" —
  the model complies because it was asked to.
- **Small document.** 4 pages / 42 chunks. Real RAG systems handle thousands.
