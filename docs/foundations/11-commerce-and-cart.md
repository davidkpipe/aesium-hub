# 11 · Commerce & Shopping Cart

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Products / Shop, Artist Profiles (merchandise), Series (shop content), Events (if Aesium hosts ticket checkout), Payments |
| **Source** | §12, §13, §15, §20, §24 |

## Purpose

A branded way to access products associated with Aesium artists. Aesium does not hold, pack or ship stock and takes a percentage of sales. The cart sits inside whichever commerce architecture is chosen; the two decisions are linked and should be made together.

## What it must provide (V1)

- Display products with artist attribution; product detail and purchase access.
- Add to cart from featured products and product grids.
- Cart view (slide-out drawer or page) with quantity controls and item removal.
- Header cart icon with an accurate item-count badge.
- Cart available while browsing; hand-off into checkout.
- Guest checkout without an account; optional account-linked cart where the architecture supports it.
- Track sales sufficiently to calculate Aesium's percentage.
- Reporting / reconciliation.

## Data it owns (depends on architecture)

- Product: title, description, images, price, artist attribution, Shop Category, external store link or commerce-platform id.
- Cart and cart items (session or account).
- Orders and order items, with artist attribution per line for commission.
- Where a commerce platform is used, cart and order data may live there and be referenced rather than copied.

## Depends on

- Payments.
- CMS & Content Model (product records, artist links).
- Accounts & Permissions (optional account-linked cart; Commerce staff role).
- Admin / Back Office (product attribution, order visibility).

## Build options

| Option | Meaning | Implication |
|---|---|---|
| Aesium-owned / custom commerce | Aesium-owned Shopify or a custom backend; central operation | Unified experience and control; more commerce administration; fulfilment stays with artists or a third party; cart built from scratch if fully custom |
| Headless commerce | Shopify (or similar) backend with Aesium's own front-end | Branded experience with less to build; cart behaviour and persistence provided by the platform |
| Hosted checkout / embed | Hosted cart and checkout, light integration | Least build; less control over the pre-checkout experience |
| Artist-owned Shopify stores | Aesium is the discovery layer linking to artist stores | Lowest fulfilment burden; multiple checkouts; a single unified cart is not established as achievable and would need technical confirmation |

## Later

- Cart persistence across visits and devices.
- More advanced saved shopping behaviour; wish-lists.

## Open questions

- Can products be purchased through one unified cart, or is per-artist checkout acceptable?
- Drawer, page, or something else?
- Should the cart persist across visits, for guests as well as logged-in users?
- How is Aesium's percentage calculated and collected?
- Who handles refunds, customer service and disputes?
