# 03 · Publishing Workflow

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Mixes, Series, Editorial, Videos, Events, Artist Profiles, Products (where Aesium manages product records), Homepage / featured content |
| **Source** | §3, §9, §10, §11, §16, §21 |

## Purpose

Every piece of content moves through the same lifecycle. Staff decide when something becomes visible, can schedule it for later, and can take it down without deleting it.

## States

| State | Meaning |
|---|---|
| Draft | Being worked on. Not visible to the audience. |
| Scheduled | Complete, with a future publish time. Becomes Published automatically. |
| Published | Visible in all its relevant platform locations. |
| Unpublished | Removed from public presentation, still available to staff. |

## Operating flow (§21)

Submit / Upload → Edit → Connect (artist / Series / event / product) → Schedule → Publish → Unpublish.

## What it must provide (V1)

- Draft, scheduled, published and unpublished states on every content type.
- A scheduler that publishes at the chosen time.
- Featured / homepage placement controls (homepage mix cards, featured products, "Next Up" event).
- Events derive Upcoming / Past from their dates rather than a manual status.
- Unpublish removes content from public pages but keeps it for management.
- Publishing rules: which fields are required before a record can go live.
- Publish events available as triggers for Notifications.

## Data it owns

- Per record: status, scheduled_at, published_at, unpublished_at.
- Featured placements: which record, which slot / location, order, optional start and end.

## Depends on

- CMS & Content Model.
- Admin / Back Office (the UI for these actions).
- Accounts & Permissions (who may publish).

## Build options

Most headless CMS platforms provide draft / publish and scheduling out of the box. Featured placement usually needs light custom configuration.

## Later

- Editorial calendar views.
- Versioning / revision history.

## Open questions

- Required fields per content type before publishing.
- Which placements are curated manually versus derived (for example "latest").
