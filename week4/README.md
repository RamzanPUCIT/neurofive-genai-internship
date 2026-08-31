# Two-Agent Writer → Editor Pipeline

Week 4 · Generative AI & Prompt Engineering · NeuroFive Solutions

A minimal multi-agent system: one agent writes, a second agent reviews and improves the first agent's work. Every run saves the raw draft, the editor's structured critique, and the final output side by side — so the improvement is measurable, not assumed.

Built on Groq (`openai/gpt-oss-120b`) with two chained API calls.

---

## Architecture

```
   topic
     │
     ▼
┌─────────────────┐   draft (markdown)   ┌─────────────────┐
│    AGENT 1      │ ───────────────────► │    AGENT 2      │
│    WRITER       │                      │  EDITOR/CRITIC  │
│                 │                      │                 │
│ persona:        │                      │ persona:        │
│ content writer  │                      │ senior editor + │
│ hook, examples, │                      │ fact-checker    │
│ takeaway        │                      │                 │
│ temp 0.8        │                      │ temp 0.3        │
└─────────────────┘                      └────────┬────────┘
                                                  │ JSON
                                                  ▼
                                    ┌──────────────────────────┐
                                    │ issues_found[]           │
                                    │ changes_made[]           │
                                    │ revised_draft  ← final   │
                                    └──────────────────────────┘
```

**Why the Editor returns JSON:** "what did the second agent actually improve?" is the question this task is really asking. If the Editor returned prose, the answer would be a guess. Structured output (via Groq's `response_format={"type": "json_object"}`) turns the critique into data the orchestrator can count, print, and write into a comparison report automatically.

| | Agent 1 — Writer | Agent 2 — Editor |
|---|---|---|
| Job | Draft from scratch | Critique + improve someone else's draft |
| Sees | Topic, audience, length | Topic + full draft (not the writer's prompt) |
| Temperature | 0.8 — wants range | 0.3 — wants consistency |
| Output | Markdown | JSON (critique + revised draft) |
| Explicitly told **not** to | Comment on its own work | Rewrite from scratch, or invent sources |

The Writer doesn't know an editor exists. That isolation is deliberate — if the Writer knew it was being reviewed, it would hedge, and the editing pass would have less to catch.

---

## Setup

```bash
python -m venv venv && venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Create a `.env` file:

```
GROQ_API_KEY=gsk_your_key_here
MODEL=openai/gpt-oss-120b
```

## Run

```bash
python run_pipeline.py                              # both default topics
python run_pipeline.py --topic "your topic here"    # a custom topic
python run_pipeline.py --pattern writer-revises     # alternate wiring
```

Output lands in `runs/<topic-slug>/`:

| File | Contents |
|---|---|
| `01_writer_draft.md` | Raw Agent 1 output, untouched |
| `02_editor_review.json` | Agent 2's full structured critique |
| `03_final_output.md` | Post-editor final |
| `comparison.md` | Auto-generated: word delta, issue counts, every change |

---

## Results

Two topics, one run, `editor-rewrites` pattern.

| Topic | Draft words | Final words | Issues found |
|---|---|---|---|
| Why RAG beats fine-tuning for most startup use cases | 451 | 492 (+41) | 4 |
| Prompt injection: the security bug every AI app ships with | 588 | 601 (+13) | 6 |

Ten issues across both runs, by category:

| Category | Count |
|---|---|
| Evidence — claim with no source | 3 |
| Accuracy — technically wrong | 3 |
| Clarity | 2 |
| Structure | 2 |

### What the Editor actually improved

**1. It caught a fabricated statistic — without fabricating a replacement.**

The Writer produced a confident, specific number that does not exist:

> *Draft:* A 2023 study measured a **73% success rate** for simple "ignore previous" attacks on GPT-3.5 when the prompt was not sandboxed.
>
> *Final:* A 2023 study reported a high success rate for simple "ignore previous" attacks on GPT-3.5 when prompts were not sandboxed **(source needed)**.

This is the most useful thing in the whole run. The Editor's system prompt says: *"Do not invent statistics or sources to 'strengthen' the draft. If a claim needs a source the author must supply, flag it instead of fabricating one."* It followed that exactly — softened the claim and marked it, rather than inventing a plausible-looking citation. An editor agent that patches hallucinations with new hallucinations is worse than no editor at all.

**2. It caught a technical error the draft stated with total confidence.**

> *Draft:* Prompt injection exploits the fact that language models treat every token as a command.
>
> *Editor:* Models treat tokens as text, not as executable commands; the attack works because the model follows instructions embedded in the prompt.
>
> *Final:* Prompt injection exploits the fact that language models follow any instruction that appears in the prompt, regardless of its source.

**3. It caught actively bad security advice.**

The Writer recommended setting `temperature=0` as a defence against prompt injection. The Editor flagged that lowering temperature reduces randomness but does nothing to stop injection, and rewrote the point to say so. A junior developer following the unedited draft would have shipped a false sense of security.

**4. Both drafts got longer, not shorter.**

Editing is usually subtraction, but not here — every structural fix (add a definition, add an intro paragraph, break the takeaway into its own section) *adds* text. The Editor cut hype in places, but structural additions outweighed the cuts in both runs. Worth knowing when budgeting output tokens for a pipeline like this.

### Where the Editor didn't help

The more interesting half. In the same prompt-injection run, the final output **still contains** two fabricated details the Editor let through:

- an unsourced "last month, a startup using `gpt-3.5-turbo`…" anecdote
- a "$5,000 bug bounty" story with no reference

It caught the invented 73% statistic but missed two invented incidents in the same document. That is the core limitation: **both agents run on the same base model, so they share blind spots.** This is a quality pass, not an independent fact-check. Anything that actually matters still needs a human or a genuinely different verifier.

Two other limits:

- On an already-tight draft, the Editor sometimes edits for the sake of editing.
- It can only flag missing sources, never supply them.

---

## Two orchestration patterns

Same two agents, different wiring — the first real design decision in multi-agent work.

**A. `editor-rewrites` (default, 2 calls)** — the Editor produces the final text. Fast and cheap, but output drifts toward the Editor's voice.

**B. `writer-revises` (3 calls)** — the Editor only critiques; its notes go back to the Writer, who rewrites. Costs one more call, but authorship stays with Agent 1 and the voice stays consistent. Closer to how real editorial teams work.

---

## Files

```
llm.py             one call_llm() function — the only file that touches the API
agents.py          both system prompts + the two agent functions
run_pipeline.py    orchestrator, artifacts, comparison reports
runs/              evidence from each run
```

---

**Author:** Muhammad Ramzan
