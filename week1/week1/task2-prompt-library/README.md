# Task 2: Build Your First Reusable Prompt Library

## Use Case: Study / Exam Notes

## Reusable Template

ROLE: You are an expert academic tutor and note-making specialist for [SUBJECT].

CONTEXT: A student is preparing for [EXAM/TEST TYPE] and needs to understand 
the topic "[TOPIC]" at a [DIFFICULTY LEVEL] level.

TASK: Create clear, structured study notes on this topic that help the 
student memorize and understand key concepts quickly.

FORMAT: Use headings, bullet points, and bold key terms. Include a short 
summary at the end (3-4 lines).

CONSTRAINTS: Keep it under [WORD LIMIT] words. Avoid unnecessary jargon. 
Use simple examples where possible.

---

## Prompt 1 — Computer Science
ROLE: You are an expert academic tutor and note-making specialist for Computer Science.
CONTEXT: A student is preparing for a university mid-term and needs to understand the topic "Time Complexity & Big-O Notation" at an undergraduate level.
TASK: Create clear, structured study notes on this topic.
FORMAT: Use headings, bullet points, bold key terms, and a 3-4 line summary at the end.
CONSTRAINTS: Keep it under 300 words. Avoid unnecessary jargon. Use simple examples.

### Output 1
Big-O Notation describes how an algorithm's runtime or memory usage grows as input size increases.
- **O(1)** – Constant time (e.g., accessing an array element by index)
- **O(n)** – Linear time (e.g., looping through a list once)
- **O(n²)** – Quadratic time (e.g., nested loops)
- **O(log n)** – Logarithmic time (e.g., binary search)

**Summary:** Big-O helps compare algorithm efficiency independent of hardware. Lower complexity means better scalability for large inputs.

---

## Prompt 2 — Machine Learning
ROLE: You are an expert academic tutor and note-making specialist for Machine Learning.
CONTEXT: A student is preparing for an M.Phil entrance test and needs to understand the topic "Overfitting vs Underfitting" at a graduate level.
TASK: Create clear, structured study notes on this topic.
FORMAT: Use headings, bullet points, bold key terms, and a 3-4 line summary at the end.
CONSTRAINTS: Keep it under 300 words. Avoid unnecessary jargon. Use simple examples.

### Output 2
- **Overfitting:** Model learns training data too well, including noise → poor performance on new/unseen data.
- **Underfitting:** Model is too simple → fails to capture patterns even in training data.
- **Fix for overfitting:** regularization, more training data, dropout
- **Fix for underfitting:** more complex model, better features

**Summary:** Good models balance bias and variance — neither memorizing noise nor oversimplifying the pattern.

---

## Prompt 3 — English Language
ROLE: You are an expert academic tutor and note-making specialist for English Language.
CONTEXT: A student is preparing for an IELTS exam and needs to understand the topic "Active vs Passive Voice" at an intermediate level.
TASK: Create clear, structured study notes on this topic.
FORMAT: Use headings, bullet points, bold key terms, and a 3-4 line summary at the end.
CONSTRAINTS: Keep it under 250 words. Avoid unnecessary jargon. Use simple examples.

### Output 3
- **Active voice:** Subject performs the action → "The cat chased the mouse."
- **Passive voice:** Subject receives the action → "The mouse was chased by the cat."
- Passive voice uses **"to be" + past participle**.

**Summary:** Active voice is direct and commonly preferred in writing; passive voice is used when the doer is unknown or unimportant.

---

## Prompt 4 — Statistics
ROLE: You are an expert academic tutor and note-making specialist for Statistics.
CONTEXT: A student is preparing for a semester final exam and needs to understand the topic "Mean, Median, and Mode" at a beginner level.
TASK: Create clear, structured study notes on this topic.
FORMAT: Use headings, bullet points, bold key terms, and a 3-4 line summary at the end.
CONSTRAINTS: Keep it under 250 words. Avoid unnecessary jargon. Use simple examples.

### Output 4
- **Mean:** Average of all values (sum ÷ count)
- **Median:** Middle value when data is sorted
- **Mode:** Most frequently occurring value

**Summary:** These are measures of central tendency. Mean is sensitive to outliers; median and mode are not.

---

## Prompt 5 — Pakistan Studies
ROLE: You are an expert academic tutor and note-making specialist for Pakistan Studies.
CONTEXT: A student is preparing for an HEC/CSS-level exam and needs to understand the topic "Objectives Resolution 1949" at an advanced level.
TASK: Create clear, structured study notes on this topic.
FORMAT: Use headings, bullet points, bold key terms, and a 3-4 line summary at the end.
CONSTRAINTS: Keep it under 300 words. Avoid unnecessary jargon. Use simple examples.

### Output 5
- Passed by Pakistan's Constituent Assembly, moved by **Liaquat Ali Khan**
- Declared sovereignty belongs to Allah, exercised by the people through elected representatives
- Laid the ideological foundation for Pakistan's future constitutions

**Summary:** Considered a "grundnorm" of Pakistan's constitutional history, blending Islamic principles with democratic governance.

---

## Video
LinkedIn post: [paste your LinkedIn video post link here]
