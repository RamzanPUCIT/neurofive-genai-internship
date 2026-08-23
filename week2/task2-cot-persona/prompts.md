
# Week 2 — Task 2: Chain-of-Thought & Persona Prompting

## Problem Used

A bakery is offered a 6-month contract: 200 cakes per month at PKR 1,200 each.
Ingredients cost PKR 700 per cake. It must lease a special oven at PKR 90,000
per month, and has already paid a non-refundable PKR 150,000 deposit on it.
Taking the contract means its existing staff stop making cookies, which
currently earn PKR 40,000 per month in contribution.
Should the bakery take the contract, and what is the 6-month impact?

## Correct Answer (ground truth)

- Revenue: 200 x 1,200 = 240,000/month
- Variable cost: 200 x 700 = 140,000/month
- Contribution: 100,000/month
- Less oven lease: -90,000  ->  10,000/month
- Less cookie opportunity cost: -40,000  ->  **-30,000/month**
- 6-month impact: **-180,000. Do not take the contract.**
- The PKR 150,000 deposit is a **sunk cost** and is irrelevant to the decision.

## Run A — Plain Prompt (no reasoning instruction, no persona)

> Answer in one line with only the final figure and decision.
> Do not show any working or steps.
>
> [problem text above]

## Run B — Persona + Chain-of-Thought

> You are a senior management accountant. Think step-by-step before answering.
> Work through revenue, variable cost, fixed cost, and opportunity cost
> separately, state explicitly whether the deposit is relevant to this
> decision, then give your final figure.
>
> [problem text above]

## Method Notes

- Model used: ChatGPT (standard chat model, not a reasoning model).
- Each run was executed in a **fresh chat session** to prevent context bleed.
