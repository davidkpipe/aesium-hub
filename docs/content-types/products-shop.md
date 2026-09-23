# Products / Shop

| | |
|---|---|
| **Type** | Content type |
| **Foundations required (V1)** | Commerce & Cart, Payments, CMS & Content Model (artist attribution), Media Assets, Tagging (Shop Category), Admin, Analytics |
| **Foundations optional** | Accounts (account-linked cart), Search, Content Submission |
| **Source** | §12, §13, §15, §2 |

## What it is

Aesium-branded access to artist products, attributed to artists and surfaced through the Shop and Artist Profiles. Aesium never holds, packs or ships stock; fulfilment stays with the artist or a fulfilment party. Aesium takes a percentage of sales.

## Record

- Title, slug, description, images, price.
- Shop Category.
- Artist attribution.
- Source: Aesium-managed product, commerce-platform product id, or external artist store link.
- Publish / availability status.

## Relationships

- Artist (attribution).
- Series (shop content on a Series page).
- Cart items and order items (commission tracking per artist).

## V1 behaviours

- Product display, detail and purchase access.
- Add to cart, cart view, checkout hand-off (see [11 Commerce & Cart](../foundations/11-commerce-and-cart.md)).
- Sales tracking sufficient to calculate Aesium's percentage.

## Open questions

- Unified cart versus per-artist checkout.
- Commission calculation and collection.
- Who handles refunds, customer service and disputes.
