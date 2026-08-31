# AI Prompt — Support Ticket Triage

The exact request body sent from Make.com's HTTP module to the Groq Chat Completions endpoint.

**Endpoint:** `https://api.groq.com/openai/v1/chat/completions`
**Method:** `POST`

**Headers**

```
Authorization: Bearer YOUR_GROQ_API_KEY
Content-Type: application/json
```

**Body**

```json
{
  "model": "openai/gpt-oss-120b",
  "temperature": 0.3,
  "response_format": { "type": "json_object" },
  "messages": [
    {
      "role": "system",
      "content": "You are a support ticket triage assistant for MRS Platform, an online course platform. Analyze the customer's issue and respond ONLY with a valid JSON object. No markdown, no code fences, no extra text. The JSON must have exactly these four keys: category (one of: Billing, Technical, Course Content, General), urgency (one of: High, Medium, Low), summary (one short sentence, max 15 words), reply (a polite professional email reply to the customer, 3 to 4 sentences, addressing them by name, acknowledging their issue and stating the next step)."
    },
    {
      "role": "user",
      "content": "Customer name: {{2.`Your Name: (B)`}}\nIssue: {{2.`Describe your issue: (D)`}}"
    }
  ]
}
```

The `{{2.…}}` placeholders are Make.com mappings pulling live values from the Google Sheets trigger module.

---

## Why the prompt is written this way

**Enums instead of open-ended labels.** Asking for "a category" produces a different label every run — *Payment*, *Billing Issue*, *Finance*. Listing the four allowed values means the output can be filtered, counted, and routed.

**"No markdown, no code fences" is not redundant.** Models habitually wrap JSON in triple backticks. That wrapper breaks any parser downstream, so it's ruled out explicitly.

**`response_format: json_object` is the real guarantee.** The instruction handles intent; this parameter enforces it at the API level. Both together are more reliable than either alone.

**`temperature: 0.3`.** Classification needs consistency, not creativity. The same ticket should land in the same category every time.

**The reply is specified, not left open.** Length, tone, name usage, and the requirement to state a next step are all defined. Without those constraints the model produces replies that vary wildly in length and usefulness.

---

## Sample output

```json
{
  "category": "Billing",
  "urgency": "High",
  "summary": "Paid Python course not appearing on dashboard",
  "reply": "Dear Ali, Thank you for contacting us about your Python course purchase. We're sorry the course is not yet visible on your dashboard. Our billing team will verify your receipt and restore access before your class starts tomorrow. We will update you shortly."
}
```
