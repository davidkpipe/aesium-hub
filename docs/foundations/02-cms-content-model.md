# 02 · CMS & Content Model

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Every content type, Admin / Back Office, Search, Homepage |
| **Source** | §1, §2, §7, §8, §16, §23 |

## Purpose

The single place where content records live and, more importantly, where the relationships between them are stored. The requirements describe one connected content system: a mix belongs to an artist, sits in a Series, appears on the Homepage and can be liked or saved. A video links to an artist, a Series and an event. A product is attributed to an artist and surfaced through the Shop and the profile.

## Core principle

Build the content model generically from the start. Artist Profiles and Series should share the same underlying page / content structure, and the tagging model should be able to extend to other content types. Deciding this early avoids an expensive retrofit.

## What it must provide (V1)

- A record for each content type with its own identity, metadata, artwork and publishing state.
- Relationships staff can manage without editing technical data:
  - Artist ↔ Mix, Video, Article, Event, Release, Product
  - Series ↔ Mix (with episode order), Video, Article, Product, external links, Event
  - Event ↔ Artist, Series, Video (event recordings)
  - Mix ↔ Genre (many-to-many)
- Shared fields on every record: title, slug, description, artwork, publish status, scheduled / published dates, featured flag.
- Existing classifications kept in their areas: Mix Type (In-House / Guest / Series), Content Type, Video Category, Shop Category.
- A "hub page" pattern shared by Artist Profiles and Series: identity, description, artwork, and connected content shown through the Experiences grid and filters.
- A hard separation between public content data and private audience activity data.

## Data it owns

All content records and their relationship (junction) tables. See the [entity diagram](../entity-diagram.md).

## Depends on

- Hosting & Infrastructure (database, asset storage).
- Publishing Workflow (states applied to every record).
- Tagging & Classification.
- Media Assets (artwork).

## Build options

| Option | Meaning | Implication |
|---|---|---|
| Headless CMS / admin platform (Directus, Strapi, Payload) | Configure a CMS | Lower custom build; vendor dependency |
| Custom | Build the content system for Aesium | Maximum control; more build and maintenance |
| Hybrid | CMS foundation plus custom Aesium admin experience | Balances flexibility and effort |

## Later

- Generic tagging across all content types.
- Recommendations built on the relationship graph.
- Revision history if required.

## Open questions

- Validate the data structure and how relationships should work (developer validation item, §23).
- Which fields are mandatory before an artist profile or Series can be published?
