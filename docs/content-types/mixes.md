# Mixes (DJ / Mix)

| | |
|---|---|
| **Type** | Content type |
| **Foundations required (V1)** | CMS & Content Model, Publishing Workflow, Tagging (genre), Media Assets, Music Upload & Audio Hosting, Audio Player, Audience Activity (like / save), Accounts, Admin, Search, Analytics |
| **Foundations optional** | Series (episode), Content Submission, Notifications |
| **Source** | §3, §4, §5, §6 |

## What it is

Aesium's core audio content. A mix belongs to an artist, may sit in a Series with an episode number, carries one or more genres from the managed list, and can be liked and saved privately.

## Record

- Title, slug, description, artwork.
- Mix Type: In-House / Guest / Series.
- Audio reference (provider id or file), duration.
- Genres (multi-select from the managed list).
- Publish status, scheduled / published dates, featured / homepage placement.

## Relationships

- Artist(s).
- Series plus episode order (optional). The mix stays an ordinary mix with an added relationship.
- Genres (many-to-many).
- Likes and saves (private).
- Play events (analytics).

## V1 behaviours

- Create / edit records; upload or connect audio; playable through the persistent player.
- Draft, scheduled, published.
- Homepage / featured placement.
- Genre filtering and search.
- Like and save.

## Later

- Queue / playlist, resume across visits, genre recommendations.

## Open questions

- Audio provider and what its API allows; OneMusic NZ licensing position.
