# 04 · Tagging & Classification

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Mixes (genre, V1), Search & Discovery, Artist Profiles (related artists derived from genre), Videos (Video Category), Products (Shop Category), Analytics (genre activity signal). Extendable to other content types later. |
| **Source** | §4, §7, §16, §18, §19, §24 |

## Purpose

A consistent, centrally managed way to categorise content so audiences can search and filter, and so related content can be surfaced.

## Two kinds of classification

1. **Genre tags** (new for V1). A managed list, multi-select, applied to mixes.
2. **Fixed classifications** that already exist and stay within their areas: Mix Type (In-House / Guest / Series), Artist / DJ, Series, Content Type, Video Category (Behind the Scenes / Live Sessions / Music Videos / Event Recordings), Shop Category.

## Rules

- Genre comes from a defined list managed by Aesium, never free text.
- A mix can have many genres; a genre is shared across many mixes.
- Artists nominate genres on submission; Aesium applies them against the approved list.
- Updating the genre list must not require editing every mix.

## What it must provide (V1)

- Genre list managed in the Admin / Back Office.
- Multi-select genre field on mix create / edit.
- Genre filtering wherever mixes are browsed.
- Genre included in Search.
- Dedicated genre pages, if the developer confirms they add no disproportionate complexity.
- Related-artist suggestions derived from the genres on an artist's linked mixes.

## Data it owns

- Genre: id, name, slug, optional description, ordering.
- Mix ↔ Genre junction.
- Fixed classifications as enumerations or small lookup tables per content type.

## Depends on

- CMS & Content Model.
- Admin / Back Office.
- Search & Discovery.

## Build options

- Aesium owns the structure and approved terminology.
- The chosen CMS may provide tagging and multi-select out of the box.
- Integration work connects genre to mixes, audience-facing filters and Search.

## Later

- Genre tagging on videos, editorial, events, products.
- Additional classification: mood, BPM, instrumentation, region.
- Genre-based recommendations.

## Open questions

- What genre list should Aesium use, and how granular?
- Manual staff entry or a structured submission for artist-nominated genres?
- Dedicated genre pages in V1, and the simplest way to structure them?
- Who has final control of the list?
