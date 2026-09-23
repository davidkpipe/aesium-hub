# 12 · Payments

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Commerce & Cart (Shop), Events (if Aesium hosts checkout). Audience accounts are free and never charge. |
| **Source** | §11, §12, §15, §24 |

## Purpose

The money layer. Connects payment processing to whichever commerce and event models are selected, records transactions, handles refunds and supports Aesium's commission and artist payouts.

## What it must provide (V1)

- Payment processing connected to the Shop checkout.
- Event payments if Aesium hosts event checkout.
- Refunds through the selected transaction flow.
- Transaction records and reconciliation.
- Artist payout / commission support. Assess Stripe Connect (or equivalent) for automatically splitting payments between Aesium and artist payees rather than manual periodic payouts.

## Data it owns

- Payment / transaction: order reference, provider, amount, fees, status, commission amount, artist payout amount, timestamps.
- Payout records per artist and period, if Aesium manages payouts.

## Depends on

- Commerce & Cart (what is being paid for).
- Accounts & Permissions (Commerce role for reporting).
- Legal / accounting confirmation of the artist money flow.

## Build options

| Option | Meaning | Implication |
|---|---|---|
| Shared Stripe-based payment layer | One payment relationship across applicable Aesium transactions | Consistent reporting and money flow; more integration if vendors would otherwise provide checkout |
| Best-of-breed per system | Each specialist platform handles its own transactions | Simpler individual integrations; fragmented reporting and reconciliation |
| Hybrid | Share payment infrastructure where useful, keep specialist commerce / ticketing systems | Middle ground |

## Later

- Automated payout schedules.
- Artist-facing sales reporting, only if explicitly decided.

## Open questions

- One payment relationship across Shop and Events?
- Artist money flow, confirmed with accountant and legal advisers.
- Is Stripe Connect appropriate?
