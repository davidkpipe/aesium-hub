# Aesium Platform — Foundations

Working documents extracted from *Aesium Platform Requirements & Build Options* (`Documents/Aesium Platform/Aesium_Platform_Requirements_Build_Options_Updated_Final.docx`). Each file is deliberately short: a starting point to expand with the developer, not a finished spec. Section numbers (§) refer to the source document.

## How to read this

The requirements draw a line between two kinds of thing:

- **Foundations** are shared building blocks. Each is built once and used by several features (CMS, accounts, publishing, tagging, media, commerce, payments, admin, hosting, analytics, search).
- **Content types** are the features the audience sees (artist profiles, mixes, series, editorial, videos, events, products). Each is a record in the CMS that relies on the foundations rather than being its own system.

The [entity diagram](entity-diagram.md) shows how the records relate. The [statement of work](statement-of-work.md) prices the build, phases and hosting options.

## Foundations

| # | Foundation | One-liner |
|---|---|---|
| 01 | [Accounts & Permissions](foundations/01-accounts-and-permissions.md) | Free audience accounts, staff roles. Artists have no accounts in V1. |
| 02 | [CMS & Content Model](foundations/02-cms-content-model.md) | The records and, crucially, the relationships between them. Shared hub structure for Artist Profiles and Series. |
| 03 | [Publishing Workflow](foundations/03-publishing-workflow.md) | Draft, scheduled, published, unpublished. Featured and homepage placement. |
| 04 | [Tagging & Classification](foundations/04-tagging-and-classification.md) | Managed genre list (multi-select on mixes) plus existing fixed classifications. |
| 05 | [Media Assets](foundations/05-media-assets.md) | Images and artwork for every record. |
| 06 | [Music Upload & Audio Hosting](foundations/06-music-upload-and-audio-hosting.md) | Getting mix audio in and delivered. Gated by licensing and the provider decision. |
| 07 | [Audio Player](foundations/07-audio-player.md) | Persistent Now Playing bar, full-view player, volume. Shapes the whole site's navigation. |
| 08 | [Video Upload & Hosting](foundations/08-video-upload-and-hosting.md) | Video provider, playback, rights. |
| 09 | [Audience Activity](foundations/09-audience-activity.md) | Follow, like, save. Private, with public aggregate follower counts. |
| 10 | [Notifications](foundations/10-notifications.md) | Preference-driven updates from followed artists. |
| 11 | [Commerce & Cart](foundations/11-commerce-and-cart.md) | Products, cart, checkout model, commission tracking. |
| 12 | [Payments](foundations/12-payments.md) | Processing, refunds, reconciliation, artist payouts. |
| 13 | [Admin / Back Office](foundations/13-admin-back-office.md) | One place for staff to manage everything and the links between records. |
| 14 | [Content Submission](foundations/14-content-submission.md) | Artist → Aesium review → publish. Manual or structured form. |
| 15 | [Search & Discovery](foundations/15-search-and-discovery.md) | Keyword search and genre filtering over the existing content model. |
| 16 | [Analytics](foundations/16-analytics.md) | Web, plays, views, activity, commerce and events made useful together. |
| 17 | [Hosting & Infrastructure](foundations/17-hosting-and-infrastructure.md) | App, database, assets, backups, monitoring. Decided last. |

## Content types

| Content type | One-liner |
|---|---|
| [Artist Profiles](content-types/artist-profiles.md) | Hub page per artist. Aesium-managed. Follow and follower count. |
| [Mixes](content-types/mixes.md) | Core audio content. Artist, optional Series episode, genres, like/save. |
| [Series](content-types/series.md) | Theme-led hub collecting mixes (ordered episodes), video, editorial, shop content, links. |
| [Editorial / Articles](content-types/editorial-articles.md) | Interviews and articles linked to artists and/or Series. |
| [Videos](content-types/videos.md) | Behind the Scenes, Live Sessions, Music Videos, Event Recordings. |
| [Events](content-types/events.md) | Upcoming / past, Next Up, ticket or RSVP action, recordings. |
| [Products / Shop](content-types/products-shop.md) | Artist-attributed products, Aesium takes a percentage, no stock handling. |

## Dependency matrix

Which foundations each feature needs. ● required for V1 · ○ optional or later · – not used.

| Feature | Acc | CMS | Pub | Tag | Img | Aud | Ply | Vid | Act | Ntf | Com | Pay | Adm | Sub | Srch | Ana | Host |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Artist Profiles | ● | ● | ● | ● | ● | – | ○ | ○ | ● | ● | ○ | – | ● | ○ | ● | ● | ● |
| Mixes | ● | ● | ● | ● | ● | ● | ● | – | ● | ○ | – | – | ● | ○ | ● | ● | ● |
| Series | – | ● | ● | ○ | ● | ○ | ○ | ○ | – | ○ | ○ | – | ● | – | ● | ● | ● |
| Editorial | – | ● | ● | ○ | ● | – | – | – | – | ○ | – | – | ● | ○ | ● | ● | ● |
| Videos | ● | ● | ● | ● | ● | – | – | ● | ● | ○ | – | – | ● | ○ | ● | ● | ● |
| Events | ○ | ● | ● | ○ | ● | – | – | ○ | – | ○ | ○ | ○ | ● | ○ | ● | ● | ● |
| Products / Shop | ○ | ● | ● | ● | ● | – | – | – | – | – | ● | ● | ● | ○ | ○ | ● | ● |
| Homepage | – | ● | ● | ○ | ● | ● | ● | ○ | – | – | ○ | – | ● | – | – | ● | ● |
| Audience account area | ● | – | – | – | – | – | – | – | ● | ● | ○ | – | ● | – | – | ● | ● |

Column key: Acc Accounts & Permissions · CMS CMS & Content Model · Pub Publishing Workflow · Tag Tagging & Classification · Img Media Assets · Aud Music Upload & Audio Hosting · Ply Audio Player · Vid Video Upload & Hosting · Act Audience Activity · Ntf Notifications · Com Commerce & Cart · Pay Payments · Adm Admin / Back Office · Sub Content Submission · Srch Search & Discovery · Ana Analytics · Host Hosting & Infrastructure.

Notes on the matrix:

- Artist Profiles need Tagging because related artists are derived from the genres on an artist's mixes (§7).
- Videos and Products use their own fixed classifications (Video Category, Shop Category) rather than genre (§4).
- Events touch Commerce and Payments only if Aesium hosts ticket checkout (§11, §15).
- The Audio Player affects Hosting because playback must survive page navigation (§5, §17, §20).

## Decisions Aesium carries into the build discussion (§24)

| Decision | Where it is captured |
|---|---|
| Audio hosting / playback approach | [06 Music Upload](foundations/06-music-upload-and-audio-hosting.md), [07 Audio Player](foundations/07-audio-player.md) |
| Video hosting / playback approach | [08 Video Upload](foundations/08-video-upload-and-hosting.md) |
| Commerce model, including Aesium's percentage | [11 Commerce & Cart](foundations/11-commerce-and-cart.md), [12 Payments](foundations/12-payments.md) |
| Event checkout / RSVP approach | [Events](content-types/events.md), [12 Payments](foundations/12-payments.md) |
| Audience authentication provider | [01 Accounts](foundations/01-accounts-and-permissions.md) |
| CMS / admin approach | [02 CMS](foundations/02-cms-content-model.md), [13 Admin](foundations/13-admin-back-office.md) |
| Artist / content submission approach | [14 Content Submission](foundations/14-content-submission.md) |
| Payment relationship across Shop and Events | [12 Payments](foundations/12-payments.md) |
| Minimum V1 analytics | [16 Analytics](foundations/16-analytics.md) |
| Minimum V1 search | [15 Search](foundations/15-search-and-discovery.md) |
| Final staff permissions | [01 Accounts](foundations/01-accounts-and-permissions.md), [13 Admin](foundations/13-admin-back-office.md) |
| Licensing and legal (music, video, events, artist payments, NZ Privacy Act 2020) | 06, 08, Events, 12, 01 |
| Genre list structure, granularity and control | [04 Tagging](foundations/04-tagging-and-classification.md) |
| Now Playing experience (immediate switching, full-view player) | [07 Audio Player](foundations/07-audio-player.md) |
| Shopping Cart presentation and persistence, unified cart question | [11 Commerce & Cart](foundations/11-commerce-and-cart.md) |

## Out of scope for V1

- Membership / paywall. Audience accounts stay free (§1).
- Artist self-service accounts (§7).
- Cross-visit persistence for player position, volume and cart (§5, §6, §13).
- Queue / playlist / autoplay (§5).
- Tagging beyond genre on mixes; mood, BPM, region; recommendations (§4).
- Artist-facing analytics (§18).
