# Run B — Persona + Chain-of-Thought

## Prompt

You are a senior management accountant. Think step-by-step before answering. Work through revenue, variable cost, fixed cost, and opportunity cost separately, state explicitly whether the deposit is relevant to this decision, then give your final figure.

A bakery is offered a 6-month contract: 200 cakes per month at PKR 1,200 each. Ingredients cost PKR 700 per cake. It must lease a special oven at PKR 90,000 per month, and has already paid a non-refundable PKR 150,000 deposit on it. Taking the contract means its existing staff stop making cookies, which currently earn PKR 40,000 per month in contribution. Should the bakery take the contract, and what is the 6-month impact?

## Output

> **Revenue:** PKR 1,440,000 (200 x 1,200 x 6)
> **Variable cost:** PKR 840,000 (200 x 700 x 6)
> **Incremental fixed cost:** PKR 540,000 (90,000 x 6)
> **Opportunity cost:** PKR 240,000 (40,000 x 6)
> **Deposit:** The PKR 150,000 is irrelevant because it is non-refundable and already paid (sunk cost).
>
> **6-month impact:** 1,440,000 - 840,000 - 540,000 - 240,000 = **PKR (180,000) loss.**
>
> **Decision:** Do not take the contract; it would reduce profit by PKR 180,000 over 6 months.

## Evaluation

**CORRECT.**

Every cost category is broken out and independently checkable. The deposit is
explicitly named as a sunk cost and excluded with a stated reason. Most
importantly, the decision now matches the figure: a loss leads to a
recommendation against the contract.

## Side-by-Side

| | Run A | Run B |
|---|---|---|
| Final figure | -180,000 | -180,000 |
| Decision | Take the contract | Do not take the contract |
| Correct? | No (contradicts its own figure) | Yes |
| Cost categories shown | None | All four |
| Deposit treatment | Unstated | Named as sunk cost, excluded |
| Auditable | No | Yes |
