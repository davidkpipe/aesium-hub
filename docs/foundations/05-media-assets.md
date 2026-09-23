# 05 · Media Assets (Images & Artwork)

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Every content type: artwork, thumbnails, profile photos, article images, product images |
| **Source** | §7, §9, §10, §16, §17 |

## Purpose

Every record on the platform carries artwork. Images need to be uploaded once, stored reliably, served fast at the right sizes and reused across records. Audio and video have their own foundations because they involve specialist providers and licensing.

## What it must provide (V1)

- Upload from the Admin / Back Office.
- Storage in general asset storage (cloud object storage) behind a CDN.
- Automatic resizing / responsive variants for cards, hero images and thumbnails.
- Alt text and basic metadata.
- Reuse of one asset across records (an artist photo on the profile and on an event card).
- Backups as part of infrastructure.

## Data it owns

- Media asset: id, kind, storage key / URL, filename, dimensions, size, alt text, uploaded by, uploaded at.

## Depends on

- Hosting & Infrastructure (object storage, CDN).
- CMS & Content Model (artwork fields reference assets).
- Admin / Back Office (upload UI).

## Build options

Most headless CMS platforms include an asset library and image transformation. Otherwise pair object storage (S3, R2 or similar) with an image service.

## Later

- Focal-point cropping.
- Rights / credit metadata per image.

## Open questions

- Required image sizes and treatments per placement (article layout, profile, cards).
