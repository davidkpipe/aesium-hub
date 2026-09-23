# 08 · Video Upload & Hosting

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Videos, Artist Profiles (Experiences), Series, Events (recordings), Analytics (views) |
| **Source** | §10, §11, §24 |

## Purpose

Host and play video reliably while the CMS keeps the video record, metadata, relationships and publishing state. Video rights (music sync, footage, likeness) are separate from the DJ mix audio-licensing question and are not resolved by it.

## What it must provide (V1)

- Upload, or connect, a video to a video record.
- Playback on the site inside Artist Profile Experiences and other confirmed placements.
- Thumbnail / artwork handling.
- Publish / schedule / unpublish respected.
- Viewing analytics received from the provider.

## Data it owns

- Video reference: provider, provider video id / embed URL, duration, processing status.
- View events, or a provider analytics sync.

## Depends on

- Hosting & Infrastructure.
- Media Assets (thumbnails).
- Rights clearance for footage, music sync and likeness, plus attendee permissions for filmed events. A cleared physical event does not automatically clear its recording for on-demand publishing.

## Build options

| Option | Meaning | Implication |
|---|---|---|
| YouTube embed | External platform hosts and delivers | Lowest infrastructure cost; less control over the branded experience |
| Vimeo | Specialist hosting with an established player | Simpler branded experience; subscription and usage limits |
| Video infrastructure (Cloudflare Stream, Mux, Bunny) | Aesium's own branded player, provider handles delivery | More control; more integration and usage-based cost |

## Later

- Playlists or continuous play if ever required.

## Open questions

- Required video quality, upload limits and expected viewing volume.
- Audiovisual rights and attendee permissions for filmed events.
