# Week 2 — Task 2: Chain-of-Thought & Persona Prompting

**NeuroFive Solutions — Generative AI & Prompt Engineering Internship**
Submitted by: Muhammad Ramzan

---

## Objective

Demonstrate, with a controlled before/after comparison, that Chain-of-Thought
(CoT) instruction combined with a domain persona measurably improves the
correctness and clarity of an LLM's answer to a reasoning problem.

---

## The Problem

A bakery is offered a 6-month contract: 200 cakes per month at PKR 1,200 each.
Ingredients cost PKR 700 per cake. It must lease a special oven at PKR 90,000
per month, and has already paid a non-refundable PKR 150,000 deposit on it.
Taking the contract means its existing staff stop making cookies, which
currently earn PKR 40,000 per month in contribution.

**Should the bakery take the contract, and what is the 6-month impact?**

The problem was chosen because it contains two independent traps: an
**opportunity cost** that is easy to omit, and a **sunk cost** (the deposit)
that is easy to wrongly include.

### Ground truth

| Line item | Per month | 6 months |
|---|---|---|
| Revenue (200 x 1,200) | 240,000 | 1,440,000 |
| Variable cost (200 x 700) | (140,000) | (840,000) |
| Oven lease | (90,000) | (540,000) |
| Cookie opportunity cost | (40,000) | (240,000) |
| **Net impact** | **(30,000)** | **(180,000)** |

The PKR 150,000 deposit is a sunk cost and is excluded.
**Correct decision: do not take the contract.**

---

## Results

| | Run A (plain) | Run B (CoT + persona) |
|---|---|---|
| Final figure | -180,000 | -180,000 |
| Decision | **Take the contract** | **Do not take the contract** |
| Correct? | No | Yes |
| Cost categories shown | None | All four |
| Deposit treatment | Unstated | Named as sunk cost, excluded |
| Auditable | No | Yes |

Full prompts and raw outputs: [`run-a-plain.md`](run-a-plain.md) ·
[`run-b-cot-persona.md`](run-b-cot-persona.md) · [`prompts.md`](prompts.md)

---

## Analysis — Why CoT + Persona Changed the Result

The plain prompt produced a self-contradictory answer: it reported a PKR 180,000
loss and then recommended taking the contract in the same sentence. Because no
intermediate reasoning was required, the model never had to reconcile the figure
it computed with the decision it announced, so the contradiction survived into
the output unchecked. Adding "think step-by-step" forced each cost category into
the visible response, which meant the sign of the final total had to be
confronted before a recommendation could be attached to it. The management
accountant persona supplied the domain frame that made two specific items
salient — the foregone cookie contribution as an opportunity cost, and the
non-refundable deposit as a sunk cost to be explicitly excluded — turning an
unverifiable one-liner into a costed analysis a reviewer can audit line by line.

---

## Key Finding

The most interesting failure was not an arithmetic error. Run A got the number
right and the **decision** wrong. This suggests CoT's value here is not
primarily computational — it is that externalising the reasoning forces the
model to keep its conclusion consistent with its own intermediate results.

---

## Method Notes

- **Model:** ChatGPT (standard
