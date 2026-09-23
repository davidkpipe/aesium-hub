# 17 · Hosting & Infrastructure

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Everything |
| **Source** | §1, §5, §17, §20, §24 |

## Purpose

Reliable hosting for the website / application, database, images and assets, integrations, backups and monitoring, alongside the chosen media, auth and payment services. The stack depends heavily on the CMS, auth, audio, video, commerce and events choices, so it is confirmed last.

## What it must provide (V1)

- Host the website / application, with client-side navigation so playback persists across pages.
- Store platform data (database).
- Store general images / assets with CDN delivery.
- Backups and recovery.
- Monitoring and basic operational alerts.
- Integrations and API connections to external services.
- Capacity to grow with audience and media usage.

## Data it owns

- Environments, configuration, secrets, backups, logs.

## Depends on

Decisions in: CMS, Accounts, Music Upload, Video Upload, Commerce, Payments.

## Build options

| Option | Meaning | Implication |
|---|---|---|
| Managed / cloud | Managed hosting and infrastructure services | Lowest operational burden; usage costs grow with the platform |
| Bundled platform | One provider combining several services | Simpler setup; greater lock-in |
| Self-managed / custom | Developer manages more of the infrastructure directly | More control; substantially more operational responsibility |

Current state: the Aesium Hub static site in this repository deploys to Cloudflare Pages with no build step. The platform build will need a stack that can run an application, database and integrations.

## Later

- Staging environments, scaling media delivery.

## Open questions

- Hosting stack once CMS / database / auth decisions are clearer.
- Backup, monitoring and recovery expectations.
- Does the chosen framework support navigation without full page reloads?
