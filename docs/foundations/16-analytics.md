# 16 · Analytics

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Everything. Aesium-level reporting on audience, content, commerce and events. |
| **Source** | §3, §10, §18, §20, §21, §24 |

## Purpose

Understand how people use the platform and how content, the Shop and events perform. Data comes from several sources (website, audio provider, video provider, commerce, events). The requirement is to make those sources useful together rather than assuming one tool produces every metric.

## What it must provide (V1)

- Website traffic and audience behaviour.
- Mix plays and content performance.
- Video views.
- Follows, likes and saves where useful.
- Shop / event activity and revenue.
- Aesium-level reporting. Artist-facing reporting stays separate unless decided later.
- Optionally, genre filter / search activity as a new audience signal.

## Data it owns

- Activity events (plays, views, searches, cart actions) where Aesium collects them, or provider reports where the provider owns the data.

## Depends on

- Music Upload & Audio Hosting (play data).
- Video Upload & Hosting (view data).
- Commerce & Cart and Payments (revenue).
- Audience Activity (counts).
- Hosting & Infrastructure (web analytics tag).

## Build options

| Option | Meaning | Implication |
|---|---|---|
| Google Analytics or similar | Basic web analytics | Low cost; less control over data model and privacy |
| Plausible | Privacy-focused, simple | Lightweight; less depth |
| PostHog / Mixpanel | Product and behavioural analytics | More capability; potentially more cost and setup |

## Later

- Artist-facing metrics.
- Recommendations informed by behaviour.

## Open questions

- The minimum V1 analytics Aesium actually needs.
- Which artist metrics, if any, should be exposed.
- Should genre filtering / search activity be tracked?
