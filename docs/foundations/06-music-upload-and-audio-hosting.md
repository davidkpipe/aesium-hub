# 06 · Music Upload & Audio Hosting

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Mixes, Audio Player, Series (episodes), Homepage (mix cards), Analytics (plays) |
| **Source** | §3, §5, §20, §23, §24 |

## Purpose

Get mix audio onto the platform and delivered to listeners. The CMS stores the mix record and its relationships; the audio itself can be self-hosted or delivered by a specialist provider. This decision gates the player design and the licensing position.

## What it must provide (V1)

- Upload audio, or connect an externally hosted track, to a mix record.
- Make the audio playable on the site through the Audio Player.
- Expose playback to a persistent, custom-controlled player (see [07 Audio Player](07-audio-player.md)).
- Provide or receive play analytics that can be combined with Aesium analytics.
- Respect publishing status: unpublished mixes are not playable.

## Data it owns

- Audio reference on the mix: provider, provider track id or file key, duration, stream / embed URL, processing status.
- Play events, or a sync from the provider's analytics.

## Depends on

- Hosting & Infrastructure (storage and streaming if self-hosted).
- Licensing. OneMusic NZ's position on on-demand DJ mixes must be confirmed before choosing self-hosting. This is a gating dependency, not a parallel task.

## Build options

| Option | Meaning | Implication |
|---|---|---|
| Aesium-owned / custom audio infrastructure | Aesium controls the player and delivery | More build and licensing responsibility |
| Mixcloud or similar | Provider handles delivery and its platform infrastructure | Less infrastructure; dependency on provider pricing / API; custom player control is an open question |
| SoundCloud or similar | Established platform with a playback API | Needs confirmation of API access and licensing; licensing position materially less established than Mixcloud's |

## Later

- Queue / playlist / autoplay next mix.
- Resume where you left off across visits.

## Open questions

- Preferred audio provider and what its API actually allows.
- OneMusic NZ position on on-demand DJ mixes.
- Does the backend support the level of custom player control required for the Now Playing bar?
- How are play analytics exposed and combined with Aesium analytics?
