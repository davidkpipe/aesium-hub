# 07 · Audio Player (Persistent Now Playing & Volume)

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Mixes, Series, Artist Profiles, Homepage: anywhere a mix can be played. Biggest cross-platform impact because it dictates how site navigation is built. |
| **Source** | §5, §6, §17, §20, §23, §24 |

## Purpose

Playback continues uninterrupted as the user moves between pages. A site-wide Now Playing bar shows the current mix and controls; a dedicated full-view player page gives a richer listening view.

## What it must provide (V1)

- Persistent bar: current mix title and artist, progress, play / pause.
- Dedicated full-view player page / view.
- Playback continues across page navigation. The site must change pages without a full browser reload, which is a front-end architecture decision affecting the whole site.
- Selecting a different mix while one is playing switches immediately.
- Volume control and mute / unmute inside the same player. Desktop: full slider. Mobile: mute / unmute where device limits apply.
- Volume and playback state stay consistent while navigating (held in the browser for the session).
- Connected to whichever audio backend is chosen.

## Data it owns

- Client-side session state only: current mix, position, play / pause, volume, mute. No server data needed in V1.

## Depends on

- Music Upload & Audio Hosting (the backend must allow custom player control).
- Hosting & Infrastructure / front-end framework (client-side navigation).
- Analytics (existing play tracking; no separate system needed).

## Build options

| Option | Implication for the player |
|---|---|
| Self-hosted audio | Direct access to the file; fully custom player; greatest control |
| SoundCloud | Playback API supports custom experiences in principle; confirm the level of control before committing |
| Mixcloud | Built around its own player and streaming model; a fully custom persistent bar is an open technical question |

Volume is not a separate build-versus-buy decision. It is part of the player; the variable is how much control the provider allows over appearance and behaviour.

## Later

- Queue / playlist / autoplay next mix.
- Resume where you left off across separate visits.
- Remember volume across visits (browser preference or account-linked setting).

## Open questions

- Does the preferred backend support the required player control?
- Should the last volume / mute setting be remembered on a future visit?
- Is mute / unmute sufficient on mobile for V1, with a full slider where technically possible?
