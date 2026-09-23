# 14 · Content Submission & Intake

| | |
|---|---|
| **Type** | Shared foundation (workflow) |
| **Used by** | Mixes, Videos, Editorial, Artist Profiles (profile changes), Events, Products: anything an artist or content producer supplies |
| **Source** | §4, §7, §16, §21, §23, §24 |

## Purpose

The path from an artist or content producer to a published record. Artists do not log in. They provide media and information through an agreed simple process; Aesium reviews and confirms it, then connects, schedules and publishes.

## Operating flow

1. **Submit / upload.** The artist provides media, information and nominated genres.
2. **Review.** An Aesium team member checks and confirms.
3. **Populate.** Relevant admin fields are filled, automatically where practical.
4. **Connect.** Content is linked to the artist, Series, event or product.
5. **Schedule or publish.**

## What it must provide (V1)

One of two approaches, to be decided with the developer:

- **Manual staff entry** from whatever the artist sends.
- **A simple structured submission form** that can populate admin fields.

In both cases:

- Capture of nominated genre against the approved list.
- A review / approval step before anything is public.

## Data it owns (if structured)

- Submission: submitter, content type, files / links, proposed metadata and genres, status (received / reviewed / approved / rejected), reviewer, resulting content record.

## Depends on

- Admin / Back Office.
- Tagging & Classification.
- Media Assets, Music Upload, Video Upload (where files are delivered).

## Build options

| Option | Implication |
|---|---|
| Manual | No build; more staff time per item |
| Structured form | Light build; less re-keying; consistent data |

## Later

- Artist self-service accounts.

## Open questions

- Manual or structured submission?
- What information is submitted, and what can populate the admin system automatically?
