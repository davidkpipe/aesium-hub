# 15 · Search & Discovery

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Artist Profiles, Mixes, Series, Editorial, Videos, Events, Products; Tagging (genre filters) |
| **Source** | §4, §19, §24 |

## Purpose

Let people find artists, mixes and other content. Much discovery already happens through the homepage, Artists, Series, Experiences, Events, Shop, genre browsing and follow / notifications. Search complements these.

## What it must provide (V1)

- Keyword search across artists and content, including mix genre.
- Useful results from the existing content model. No separate search platform is required for V1.
- Genre filtering within mix browsing; dedicated genre pages if confirmed low-complexity.
- Room for better relevance / ranking later.

## Data it owns

- None of its own in V1; it reads content records. A search index only if a dedicated engine is adopted later.

## Depends on

- CMS & Content Model.
- Tagging & Classification.
- Publishing Workflow (only published content is searchable).

## Build options

| Option | Meaning | Implication |
|---|---|---|
| Database / CMS search | Built-in or database full-text search | Lowest complexity; likely suitable for V1 |
| Dedicated search engine (Algolia, Typesense, Meilisearch) | Separate search service | More control over behaviour; additional service and maintenance |

## Later

- Ranking, typo tolerance, recommendations, richer genre-based discovery.

## Open questions

- Exactly what must be searchable in V1?
- Which filters and genre-based browsing routes, including dedicated genre pages?
