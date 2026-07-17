```markdown
# NeuroFive Solutions — GenAI Internship

Internee: Muhammad Ramzan
Track: Generative AI & Prompt Engineering
Cohort: July 2026

---

# Week 1

## Task 1: Zero-Shot vs Few-Shot Showdown

### Problem
Classify 10 customer support messages as "Complaint", "Question", or "Praise".

### Messages
1. My order arrived broken and no one has responded to my emails in 3 days.
2. How do I reset my password? I can't find the link.
3. Your support team fixed my issue in 5 minutes, amazing service!
4. This is the second time you've charged me twice for one order.
5. Does this plan include international shipping?
6. I just want to say thank you, the new update fixed everything.
7. Why is my refund still not showing in my account after a week?
8. Can I upgrade my subscription mid-cycle?
9. The app keeps crashing every time I try to upload a photo.
10. Loved how fast the delivery was this time, keep it up!

### Zero-Shot Prompt
```
Classify each of the following customer support messages as
"Complaint", "Question", or "Praise". Just give the label for each.

1. My order arrived broken and no one has responded to my emails in 3 days.
2. How do I reset my password? I can't find the link.
3. Your support team fixed my issue in 5 minutes, amazing service!
4. This is the second time you've charged me twice for one order.
5. Does this plan include international shipping?
6. I just want to say thank you, the new update fixed everything.
7. Why is my refund still not showing in my account after a week?
8. Can I upgrade my subscription mid-cycle?
9. The app keeps crashing every time I try to upload a photo.
10. Loved how fast the delivery was this time, keep it up!
```

### Few-Shot Prompt
```
Classify customer support messages as "Complaint", "Question", or "Praise".

Examples:
"My package never arrived and it's been two weeks." → Complaint
"What time does customer support open?" → Question
"You guys are the best, fixed my issue instantly!" → Praise

Now classify these:
1. My order arrived broken and no one has responded to my emails in 3 days.
2. How do I reset my password? I can't find the link.
3. Your support team fixed my issue in 5 minutes, amazing service!
4. This is the second time you've charged me twice for one order.
5. Does this plan include international shipping?
6. I just want to say thank you, the new update fixed everything.
7. Why is my refund still not showing in my account after a week?
8. Can I upgrade my subscription mid-cycle?
9. The app keeps crashing every time I try to upload a photo.
10. Loved how fast the delivery was this time, keep it up!
```

### Results Table

| Tool | Zero-shot Accuracy | Few-shot Accuracy |
|------|--------------------|--------------------|
| Claude | 10/10 (100%) | 10/10 (100%) |
| ChatGPT | 10/10 (100%) | 10/10 (100%) |
| Gemini | 10/10 (100%) | 10/10 (100%) |

### Takeaway
Zero-shot aur few-shot dono prompts ne teeno tools mein 10/10 accuracy di. Iski wajah ye hai ke test messages kaafi clear aur unambiguous the, is liye AI ko example dekhne ki zaroorat nahi pari sahi answer dene ke liye. Ye is baat ko confirm karta hai ke few-shot prompting ka real fayda tab zyada nazar aata hai jab messages ambiguous ya mixed-tone hon (jaise message #7 jo "why" se shuru hota hai lekin asal mein complaint hai). Overall, simple aur clear-cut tasks mein zero-shot bhi utna hi reliable hota hai jitna few-shot, lekin complex cases mein few-shot ziyada consistency deta hai.

### Video
LinkedIn post: [paste your LinkedIn video post link here]
```
