# 13 · Admin / Back Office

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Every content type and every staff task |
| **Source** | §1, §16, §20, §21, §22, §24 |

## Purpose

One place where Aesium staff operate the platform: create and manage content, artists, Series, events, products, publishing, tags, featured content and the relationships between records, without editing technical data directly.

## What it must provide (V1)

- Create / edit / publish content of every type.
- Manage artists and their connected content.
- Manage Series and episode ordering.
- Manage events and event connections.
- Manage product attribution and commerce information.
- Manage the genre list, categories and artwork.
- Draft, schedule, publish, unpublish; manage featured content.
- Receive structured submissions, if that process is chosen.
- View appropriate audience / account information (scope to be defined).
- Basic dashboard / operational views.
- Staff permissions per role.

The Now Playing bar, volume control and cart create no significant new day-to-day admin work. Cart orders sit within existing Shop administration.

## Data it owns

- Staff users and roles (shared with Accounts & Permissions).
- Operational settings: genre list, featured slots, homepage configuration.

## Depends on

- CMS & Content Model (the admin sits on top of it).
- Accounts & Permissions.
- Connections to audio, video, commerce, events, accounts and analytics services.

## Build options

| Option | Meaning | Implication |
|---|---|---|
| Headless CMS / admin platform (Directus, Strapi, Payload) | Configure rather than build | Lower custom build; vendor / platform dependency |
| Custom admin | Built specifically for Aesium | Maximum control; more upfront build and maintenance |
| Hybrid | CMS foundation plus custom Aesium admin screens | Balances flexibility and build effort |

## Later

- Automation of repetitive tasks.
- Artist self-service.

## Open questions

- How many staff will use the system?
- One admin role or separated access in V1?
- Which tasks should be automated?
