# 09 · Audience Activity (Follow, Like, Save)

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Artist Profiles (follow and public follower count), Mixes and Videos (like / save), Audience account area, Notifications, Analytics |
| **Source** | §3, §7, §10, §14, §18, §24 |

## Purpose

The private record of what each audience member does. Powers the personal library, drives notifications and produces the only public number: the aggregate follower count on an artist profile.

## Rules

- Follows, likes and saves are private to the user.
- Follower count is public as an aggregate; follower identities are never exposed.
- Admin visibility into this data is to be defined explicitly.
- Subject to NZ Privacy Act 2020 compliance.

## What it must provide (V1)

- Follow / unfollow artists.
- Like / unlike mixes and videos.
- Save / unsave mixes and videos.
- A private account area / library showing the user's follows, likes and saves.
- Aggregate follower count per artist.
- Like / save counts available to Analytics where useful.

## Data it owns

- Follow: user, artist, created at.
- Like: user, content (mix or video), created at.
- Save: user, content (mix or video), created at.

## Depends on

- Accounts & Permissions (must be logged in).
- CMS & Content Model (references to artists, mixes, videos).

## Build options

Lives in the Aesium database regardless of the auth provider: simple tables keyed by user and content.

## Later

- Activity feeds, playlists built from saves, account-linked playback preferences.

## Open questions

- Exact admin visibility into audience activity.
- Are like / save counts ever shown publicly? The requirements only make follower counts public.
