# Week 5 — No-Code AI Automation: Support Ticket Triage

An automation that turns raw customer complaints into categorized, prioritized tickets with a drafted reply — without writing a backend.

**Stack:** Google Forms → Google Sheets → Make.com → Groq API (`openai/gpt-oss-120b`) → Gmail

---

## The workflow

```
Google Form submitted
        ↓
Google Sheets  (Watch New Rows)     ← trigger
        ↓
HTTP Module    (Groq Chat Completions)   ← AI step
        ↓
Gmail          (Send an Email)      ← action
```

| # | Module | Role |
|---|--------|------|
| 1 | Google Sheets — Watch New Rows | Fires on every new form response |
| 2 | HTTP — Make a request | Sends name + issue to Groq, gets structured JSON back |
| 3 | Gmail — Send an email | Delivers the AI-drafted reply to the customer |

---

## The AI step

The model is constrained to return **only JSON** with four keys — no prose, no markdown fences:

```json
{
  "category": "Billing | Technical | Course Content | General",
  "urgency":  "High | Medium | Low",
  "summary":  "one short sentence",
  "reply":    "3-4 sentence professional email reply"
}
```

`temperature` is set to `0.3` and `response_format` to `json_object` so the output stays consistent enough to be parsed by downstream steps.

---

## Test results

Two real form submissions, two very different tickets:

**Test 1 — billing complaint**

> *"I paid for the Python course last week but it is still not showing in my dashboard. I have the payment receipt. Please fix this urgently, my classes start tomorrow."*

```json
{
  "category": "Billing",
  "urgency": "High",
  "summary": "Paid Python course not appearing on dashboard",
  "reply": "Dear Ali, Thank you for contacting us about your Python course purchase..."
}
```

**Test 2 — praise + general question**

> *"I just wanted to say the new instructor for the JavaScript module explains things really well. Also, can you tell me when the next batch starts?"*

```json
{
  "category": "General",
  "urgency": "Low",
  "summary": "Positive feedback and asks about next batch start date.",
  "reply": "Dear Bilal Ahmed, thank you for your kind words about our new JavaScript instructor..."
}
```

Different category, different urgency, different tone in the reply. The classification is doing real work, not returning a fixed answer.

---

## Files

| File | What it is |
|------|-----------|
| `make_blueprint.json` | Full Make.com scenario — import it to recreate the workflow |
| `ai_prompt.md` | The system prompt and request body sent to Groq |
| `screenshots/` | Scenario run, AI output, delivered email |

---

## Reproducing this

1. Create a Google Form with three fields: Name, Email, Issue description
2. Link it to a Google Sheet, then add three empty columns: `Category`, `Urgency`, `AI Summary`
3. In Make.com: **Create scenario → ⋮ → Import Blueprint** and select `make_blueprint.json`
4. Reconnect Google Sheets and Gmail (connections don't transfer)
5. In the HTTP module, replace `YOUR_GROQ_API_KEY` in the Authorization header with your own key from [console.groq.com](https://console.groq.com)
6. Submit the form, hit **Run once**

---

## Notes from building it

**Zapier's free tier can't do this.** It allows two-step Zaps only — one trigger, one action. This workflow needs three steps. Make's free tier (1,000 credits/month, 2 active scenarios) handles it comfortably.

**Groq deprecates models.** `llama-3.3-70b-versatile` was retired in June 2026 and returns a `model_not_found` error. `openai/gpt-oss-120b` is the current replacement.

**The 15-minute polling delay is a problem when testing.** Make's free plan checks for new rows every 15 minutes. The **Run once** button bypasses this entirely — submit the form, click Run once, see the result immediately.

**A trigger only fires on genuinely new rows.** Re-running against a row Make has already read returns nothing and the scenario stops at step one. Each test needs a fresh form submission.

**Never commit an exported blueprint as-is.** Make embeds the API key in plain text inside the HTTP module's headers. The key in this repo has been replaced with a placeholder.

---

*Muhammad Ramzan — Generative AI & Prompt Engineering Internship, NeuroFive Solutions*
