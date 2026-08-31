"""
run_pipeline.py — the orchestrator.

    topic ──> [Agent 1: WRITER] ──draft──> [Agent 2: EDITOR] ──> final + change log

Everything from a run is written to runs/<topic-slug>/ so you have receipts:
the raw draft, the editor's structured review, the final output, and a diff
summary. That folder is what you screen-share in the video.

Usage:
    python run_pipeline.py                          # runs the 2 default topics
    python run_pipeline.py --topic "your topic"     # one custom topic
    python run_pipeline.py --pattern writer-revises # editor critiques, writer rewrites
"""

import argparse
import json
import re
import time
from pathlib import Path

from agents import review_draft, write_draft, writer_revises

DEFAULT_TOPICS = [
    "Why RAG beats fine-tuning for most startup use cases",
    "Prompt injection: the security bug every AI app ships with",
]

RUNS_DIR = Path("runs")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50]


def wc(text: str) -> int:
    return len(text.split())


def run_topic(topic: str, pattern: str = "editor-rewrites",
              audience: str = "junior developers", words: int = 500) -> dict:
    """Run the full two-agent pipeline on one topic."""
    out_dir = RUNS_DIR / slugify(topic)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 70}\nTOPIC: {topic}\n{'=' * 70}")

    # ---- Agent 1 -----------------------------------------------------
    print("[1/2] WRITER  drafting...", end=" ", flush=True)
    t0 = time.time()
    draft = write_draft(topic, audience=audience, words=words)
    print(f"done ({wc(draft)} words, {time.time() - t0:.1f}s)")
    (out_dir / "01_writer_draft.md").write_text(draft, encoding="utf-8")

    # ---- Agent 2 -----------------------------------------------------
    print("[2/2] EDITOR  reviewing...", end=" ", flush=True)
    t0 = time.time()
    review = review_draft(topic, draft)
    print(f"done ({len(review.get('issues_found', []))} issues, "
          f"{time.time() - t0:.1f}s)")
    (out_dir / "02_editor_review.json").write_text(
        json.dumps(review, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- Which agent holds the pen? ----------------------------------
    if pattern == "writer-revises":
        print("[3/3] WRITER  applying editor's notes...", end=" ", flush=True)
        final = writer_revises(topic, draft, review)
        print("done")
    else:
        final = review.get("revised_draft", draft)

    (out_dir / "03_final_output.md").write_text(final, encoding="utf-8")

    result = {
        "topic": topic,
        "pattern": pattern,
        "draft_words": wc(draft),
        "final_words": wc(final),
        "verdict": review.get("overall_verdict", ""),
        "issues": review.get("issues_found", []),
        "changes": review.get("changes_made", []),
        "dir": str(out_dir),
    }
    (out_dir / "comparison.md").write_text(_topic_report(result), encoding="utf-8")

    print(f"\n  Editor's verdict: {result['verdict']}")
    for issue in result["issues"]:
        print(f"    · [{issue.get('severity', '?')}/{issue.get('type', '?')}] "
              f"{issue.get('why', '')}")
    print(f"  Artifacts: {out_dir}/")
    return result


def _topic_report(r: dict) -> str:
    by_type: dict[str, int] = {}
    for issue in r["issues"]:
        by_type[issue.get("type", "other")] = by_type.get(issue.get("type", "other"), 0) + 1

    lines = [
        f"# Comparison — {r['topic']}",
        "",
        f"**Pattern:** `{r['pattern']}`  ",
        f"**Length:** {r['draft_words']} words (draft) → {r['final_words']} words (final) "
        f"({r['final_words'] - r['draft_words']:+d})  ",
        f"**Issues found by Editor:** {len(r['issues'])} "
        f"({', '.join(f'{k}: {v}' for k, v in by_type.items()) or 'none'})",
        "",
        "## Editor's verdict",
        "",
        f"> {r['verdict']}",
        "",
        "## What the Editor actually changed",
        "",
    ]
    for issue in r["issues"]:
        lines += [
            f"### {issue.get('type', '?').title()} "
            f"({issue.get('severity', '?')} severity)",
            "",
            f"- **Original:** {issue.get('quote', '')}",
            f"- **Problem:** {issue.get('why', '')}",
            f"- **Fix:** {issue.get('fix', '')}",
            "",
        ]
    if r["changes"]:
        lines += ["## Change log", ""] + [f"- {c}" for c in r["changes"]] + [""]
    lines += [
        "## Files",
        "",
        "| File | What it is |",
        "|---|---|",
        "| `01_writer_draft.md` | Raw Agent 1 output — no editor involved |",
        "| `02_editor_review.json` | Agent 2's structured critique |",
        "| `03_final_output.md` | Post-editor final |",
        "",
    ]
    return "\n".join(lines)


def _summary_report(results: list[dict]) -> str:
    lines = [
        "# Run summary — all topics",
        "",
        "| Topic | Draft words | Final words | Issues found |",
        "|---|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {r['topic']} | {r['draft_words']} | {r['final_words']} "
                     f"| {len(r['issues'])} |")
    lines += ["", "## Per-topic detail", ""]
    for r in results:
        lines.append(f"- [{r['topic']}]({slugify(r['topic'])}/comparison.md) — "
                     f"_{r['verdict']}_")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Two-agent Writer/Editor pipeline")
    ap.add_argument("--topic", action="append", help="topic (repeatable)")
    ap.add_argument("--pattern", default="editor-rewrites",
                    choices=["editor-rewrites", "writer-revises"])
    ap.add_argument("--audience", default="junior developers")
    ap.add_argument("--words", type=int, default=500)
    args = ap.parse_args()

    topics = args.topic or DEFAULT_TOPICS
    results = [run_topic(t, args.pattern, args.audience, args.words) for t in topics]

    RUNS_DIR.mkdir(exist_ok=True)
    (RUNS_DIR / "SUMMARY.md").write_text(_summary_report(results), encoding="utf-8")
    print(f"\n{'=' * 70}\nAll done. Summary written to runs/SUMMARY.md\n{'=' * 70}")


if __name__ == "__main__":
    main()
