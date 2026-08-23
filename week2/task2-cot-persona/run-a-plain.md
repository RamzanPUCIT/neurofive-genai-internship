# Run A — Plain Prompt (no CoT, no persona)

## Prompt

Answer in one line with only the final figure and decision. Do not show any working or steps.

A bakery is offered a 6-month contract: 200 cakes per month at PKR 1,200 each. Ingredients cost PKR 700 per cake. It must lease a special oven at PKR 90,000 per month, and has already paid a non-refundable PKR 150,000 deposit on it. Taking the contract means its existing staff stop making cookies, which currently earn PKR 40,000 per month in contribution. Should the bakery take the contract, and what is the 6-month impact?

## Output

> Take the contract: 6-month loss = PKR 180,000.

## Evaluation

**INCORRECT — self-contradictory.**

The arithmetic landed on the right magnitude (-180,000), but the recommendation
is the exact opposite of what that figure implies. The model states a loss and
then advises taking the contract in the same sentence. With no reasoning step,
it never had to reconcile the number with the decision, so the contradiction
went undetected. No cost categories are visible, and the sunk-cost treatment of
the deposit is unstated — there is no way to audit how the figure was reached.
