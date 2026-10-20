# SplitLedger Business Rules

## Currency

SplitLedger currently supports one currency: BAM (KM).

All monetary calculations are performed using integer cents.

Examples:

- 1.00 KM = 100 cents
- 10.50 KM = 1050 cents
- 100.00 KM = 10000 cents

Floating-point arithmetic must not be used for financial calculations.

## Amount validation

A valid expense amount must:

- be a valid decimal number
- be greater than 0
- contain no more than two decimal places
- not exceed 10,000,000.00 KM

## Equal splitting

Expenses are split equally between all members participating in the expense.

If an amount cannot be divided evenly, remainder cents are assigned deterministically by ascending member ID.

Example:

100.00 KM = 10000 cents

10000 / 3:

- Member 1: 3334 cents
- Member 2: 3333 cents
- Member 3: 3333 cents

The sum of all shares must always equal the original expense amount.

## Core financial invariants

1. The sum of expense shares must equal the expense amount.
2. The sum of all group balances must equal zero.
3. No expense share may be negative.
4. No settlement amount may be negative or zero.
5. Financial calculations must never create or destroy cents.