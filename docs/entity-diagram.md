# Aesium Entity Diagram

A first-pass data model drawn from the requirements document, for the developer to validate (§23). It is deliberately concrete so there is something to argue with. Section numbers (§) refer to *Aesium Platform Requirements & Build Options*.

GitHub renders the diagrams below. The [foundation docs](README.md) describe what each area must do.

## Reading the notation

Crow's-foot cardinality, read from the far entity's point of view:

| Symbol | Meaning |
|---|---|
| `\|\|` | exactly one |
| `\|o` | zero or one |
| `}\|` | one or more |
| `}o` | zero or more |

`Artist }|--o{ Mix` reads: each Mix has one or more Artists; each Artist has zero or more Mixes.

## Overview

The core graph without attributes. Content records on the left connect to each other; audience and commerce records hang off them.

```mermaid
erDiagram
    Artist }|--o{ Mix : "credited on"
    Artist }o--o{ Video : "features in"
    Artist }o--o{ Article : "subject of"
    Artist }o--o{ Event : "plays at"
    Artist ||--o{ Product : "attributed"
    Mix }o--o{ Genre : "tagged"
    Series |o--o{ Mix : "numbered episodes"
    Series }o--o{ Video : "collects"
    Series }o--o{ Article : "collects"
    Series }o--o{ Product : "collects"
    Series }o--o{ Event : "associated"
    Event |o--o{ Video : "recorded as"
    AudienceUser }o--o{ Artist : "follows"
    AudienceUser }o--o{ Mix : "likes, saves"
    AudienceUser }o--o{ Video : "likes, saves"
    AudienceUser |o--o{ Order : "places, or guest"
    Order }o--|{ Product : "contains"
    Order ||--o{ Payment : "settled by"
    StaffUser ||--o{ ContentSubmission : "reviews"
    ContentSubmission }o--o| Artist : "on behalf of"
```

## 1. Content graph

Everything Aesium publishes, and how the records connect. Artist Profiles and Series are both "hub" pages over the same content (§8).

```mermaid
erDiagram
    Artist }|--o{ Mix : "credited on"
    Artist }o--o{ Video : "features in"
    Artist }o--o{ Article : "subject of"
    Artist }o--o{ Event : "plays at"
    Artist }|--o{ Release : "released"
    Artist ||--o{ Product : "attributed to"
    Artist }o--o{ ArtistGroup : "member of"
    Artist }o--o{ Artist : "related, curated"
    Mix }o--o{ Genre : "tagged with"
    Series ||--o{ SeriesEpisode : "orders"
    Mix ||--o| SeriesEpisode : "appears as"
    Series }o--o{ Video : "collects"
    Series }o--o{ Article : "collects"
    Series }o--o{ Product : "collects"
    Series ||--o{ ExternalLink : "links out"
    Series }o--o{ Event : "associated with"
    Event |o--o{ Video : "recorded as"

    Artist {
        string id PK
        string name
        string slug UK
        enum status "resident | guest"
        string location
        text bio
        string artwork_id FK "MediaAsset"
        string spotify_url "defined fields in V1"
        string bandcamp_url
        json social_links
        enum publish_status
        int follower_count "derived aggregate, never identities"
    }
    Mix {
        string id PK
        string title
        string slug UK
        text description
        string artwork_id FK "MediaAsset"
        enum mix_type "in_house | guest | series"
        string audio_provider "self-hosted | Mixcloud | SoundCloud"
        string audio_ref "provider track id or file key"
        int duration_sec
        enum publish_status "draft | scheduled | published | unpublished"
        datetime scheduled_at
        datetime published_at
        bool featured "homepage placement"
    }
    Genre {
        string id PK
        string name UK
        string slug UK
        int sort_order
    }
    Series {
        string id PK
        string title
        string slug UK
        text description
        string artwork_id FK "MediaAsset"
        enum publish_status
    }
    SeriesEpisode {
        string series_id FK
        string mix_id FK
        int episode_number
        int sort_order
    }
    Article {
        string id PK
        string title
        string slug UK
        text body "rich text"
        text pull_quote "In Their Words"
        string hero_image_id FK "MediaAsset"
        enum publish_status
        datetime scheduled_at
        datetime published_at
    }
    Video {
        string id PK
        string title
        string slug UK
        text description
        enum category "bts | live_session | music_video | event_recording"
        string video_provider "YouTube | Vimeo | Stream | Mux"
        string video_ref "provider video id"
        string thumbnail_id FK "MediaAsset"
        int duration_sec
        enum publish_status
        datetime scheduled_at
        datetime published_at
    }
    Event {
        string id PK
        string title
        string slug UK
        text description
        datetime starts_at "upcoming or past is derived"
        datetime ends_at
        string venue
        string artwork_id FK "MediaAsset"
        enum action_type "external_ticket | rsvp | aesium_checkout"
        string action_url
        bool next_up "featured event"
        enum publish_status
    }
    Product {
        string id PK
        string title
        string slug UK
        text description
        decimal price
        string shop_category
        string artist_id FK "attribution"
        enum source "aesium | commerce_platform | artist_store"
        string external_ref "platform product id or store URL"
        enum publish_status
    }
    Release {
        string id PK
        string title
        date released_on
        string artwork_id FK "MediaAsset"
        string listen_url
    }
    ArtistGroup {
        string id PK
        string name
        enum kind "collective | discovery_group"
    }
    ExternalLink {
        string id PK
        string series_id FK
        string label
        string url
    }
```

Modelling notes:

- Artist ↔ Mix is many-to-many so back-to-back sets and collaborations work. Most mixes will have one artist. A `primary_artist_id` on Mix plus a credits table is an equivalent shape if the developer prefers it.
- `SeriesEpisode` is a junction that carries data (episode number, order), so a mix stays an ordinary mix with an added Series relationship (§8).
- Product → Artist is a single attribution in V1 (§12). Turn it into a junction if co-branded products appear.
- Related artists are derived at read time from shared genres across an artist's mixes (§7). The curated self-link is optional context for collectives.
- `ArtistGroup` covers both an established collective and the shared discovery presentation for artists with limited content (§7).
- Artist external links are defined fields in V1 (§7), not a link table. Series external links are a list.
- Every content entity carries the same publishing fields (§3). Event upcoming / past is derived from `starts_at`, never stored (§11).
- Artwork fields reference `MediaAsset` (see Operations).

## 2. Audience & activity

Free accounts and their private activity. Only `follower_count` on Artist is ever public (§7, §14).

```mermaid
erDiagram
    AudienceUser ||--o{ Follow : "follows via"
    Artist ||--o{ Follow : "followed via"
    AudienceUser ||--o{ Like : "makes"
    AudienceUser ||--o{ Save : "makes"
    Mix |o--o{ Like : "target"
    Video |o--o{ Like : "target"
    Mix |o--o{ Save : "target"
    Video |o--o{ Save : "target"
    AudienceUser ||--o{ NotificationPreference : "sets"
    AudienceUser ||--o{ Notification : "receives"

    AudienceUser {
        string id PK
        string email UK
        string display_name
        string auth_provider_ref "Auth0, Clerk or Supabase id"
        datetime created_at
    }
    Follow {
        string user_id FK
        string artist_id FK
        datetime created_at
    }
    Like {
        string user_id FK
        enum content_type "mix | video"
        string content_id FK
        datetime created_at
    }
    Save {
        string user_id FK
        enum content_type "mix | video"
        string content_id FK
        datetime created_at
    }
    NotificationPreference {
        string user_id FK
        enum channel "email | browser"
        enum topic "new_mix | new_video | new_article | event"
        bool enabled
    }
    Notification {
        string id PK
        string user_id FK
        string topic
        string content_ref
        datetime sent_at
        datetime read_at
    }
```

Modelling notes:

- Like and Save point at exactly one of Mix or Video: a `content_type` + `content_id` pair, or two nullable foreign keys.
- `follower_count` is an aggregate over Follow. Follower identities are never exposed; admin visibility is still to be defined (§14).
- Notifications are produced by Follow + publish events, filtered by preferences (§14).
- With a managed auth provider, `AudienceUser` holds only the provider reference plus profile fields; passwords never live in Aesium's database.

## 3. Commerce & payments

Which of these tables exist on Aesium's side depends entirely on the commerce architecture (§12, §13, §15).

```mermaid
erDiagram
    AudienceUser |o--o{ Cart : "owns, optional"
    Cart ||--o{ CartItem : "holds"
    Product ||--o{ CartItem : "added as"
    Cart ||--o| Order : "checks out into"
    AudienceUser |o--o{ Order : "places, guest allowed"
    Order ||--|{ OrderItem : "contains"
    Product ||--o{ OrderItem : "sold as"
    Artist ||--o{ OrderItem : "earns from"
    Order ||--o{ Payment : "settled by"
    ArtistPayout |o--|{ OrderItem : "aggregates"
    Artist ||--o{ ArtistPayout : "receives"
    Event |o--o{ Order : "ticket order, if Aesium checkout"
    Event ||--o{ EventRSVP : "collects"
    AudienceUser |o--o{ EventRSVP : "responds"

    Cart {
        string id PK
        string session_id "guests"
        string user_id FK "null for guests"
        datetime updated_at
    }
    CartItem {
        string cart_id FK
        string product_id FK
        int quantity
    }
    Order {
        string id PK
        string user_id FK "null for guest"
        string email
        enum status "pending | paid | fulfilled | refunded"
        decimal subtotal
        decimal total
        string commerce_platform_ref "e.g. Shopify order id"
        datetime created_at
    }
    OrderItem {
        string order_id FK
        string product_id FK
        string artist_id FK "for commission"
        int quantity
        decimal unit_price
        decimal aesium_commission
        decimal artist_share
    }
    Payment {
        string id PK
        string order_id FK
        string provider "Stripe"
        string provider_ref
        decimal amount
        decimal provider_fee
        enum status "authorised | captured | refunded"
        datetime created_at
    }
    ArtistPayout {
        string id PK
        string artist_id FK
        date period_start
        date period_end
        decimal amount
        enum status "pending | paid"
        string provider_ref "Stripe Connect transfer"
    }
    EventRSVP {
        string id PK
        string event_id FK
        string user_id FK "or email for guests"
        string email
        enum status "going | cancelled"
        datetime created_at
    }
```

Modelling notes:

- With Aesium-owned or headless Shopify, Cart, Order and Payment live in Shopify and Stripe; Aesium keeps references for reporting (§12, §13).
- With artist-owned stores there may be no Cart or Order on Aesium's side at all, only outbound links. A unified cart across independent stores is not established as achievable (§13).
- `OrderItem` carries `artist_id` and the split so Aesium's percentage is calculable per line (§12, §15).
- `ArtistPayout` aggregates order items per period. Stripe Connect could replace it with automatic transfers (§15).
- `EventRSVP` exists only if Aesium hosts RSVP. Tickets sold through Aesium checkout would be Orders (§11).

## 4. Operations

Staff, intake, media, featured placement and activity data behind the Admin / Back Office.

```mermaid
erDiagram
    Role ||--o{ StaffUser : "assigned to"
    StaffUser ||--o{ ContentSubmission : "reviews"
    Artist |o--o{ ContentSubmission : "on behalf of"
    StaffUser ||--o{ MediaAsset : "uploads"
    StaffUser ||--o{ FeaturedPlacement : "curates"
    AudienceUser |o--o{ ActivityEvent : "attributed, when signed in"

    Role {
        string id PK
        string name "Administrator | Content-Editorial | Events | Commerce | Contributor"
        json permissions
    }
    StaffUser {
        string id PK
        string email UK
        string name
        string role_id FK
    }
    ContentSubmission {
        string id PK
        string artist_id FK "may not exist yet"
        string submitter_email
        enum content_type "mix | video | article | event | product | profile_change"
        json files_or_links
        json proposed_metadata
        json proposed_genres "checked against the Genre list"
        enum status "received | reviewed | approved | rejected"
        string reviewed_by FK "StaffUser"
        string result_type "record type created"
        string result_id "record created on approval"
        datetime submitted_at
    }
    FeaturedPlacement {
        string id PK
        enum slot "homepage_mix | homepage_hero | next_up_event | featured_product"
        string content_type
        string content_id "polymorphic"
        int sort_order
        datetime starts_at
        datetime ends_at
    }
    MediaAsset {
        string id PK
        string storage_key
        string url "CDN"
        string filename
        int width
        int height
        string alt_text
        string uploaded_by FK
        datetime uploaded_at
    }
    ActivityEvent {
        string id PK
        enum kind "play | view | search | genre_filter | add_to_cart"
        string content_type
        string content_id
        string user_id "null when anonymous"
        string session_id
        enum source "site | audio_provider | video_provider | commerce"
        datetime occurred_at
    }
```

Modelling notes:

- Roles follow §22 and may collapse to Administrator only in V1.
- `ContentSubmission` exists only if the structured submission route is chosen (§14, §21). On approval it produces the real content record.
- `FeaturedPlacement` is polymorphic (slot + content reference) so one mechanism covers homepage mixes, the Next Up event and featured products.
- `MediaAsset` is referenced by every artwork, thumbnail and hero-image field in the content graph.
- `ActivityEvent` may live in the analytics provider rather than the database (§18). Play and view data often arrives from the audio and video providers.

## Decisions that change this diagram

| Decision (§24) | What moves |
|---|---|
| Audio provider | `Mix.audio_*` fields; whether play events are collected or synced |
| Video provider | `Video.video_*` fields; whether view events are collected or synced |
| Commerce model | Whether Cart, Order, Payment, ArtistPayout exist locally or as references |
| Event checkout / RSVP | Whether `EventRSVP` exists; whether Orders can be ticket orders |
| Authentication provider | Shape of `AudienceUser`; possibly `StaffUser` |
| Submission approach | Whether `ContentSubmission` exists |
| Staff permissions | Number of `Role` rows |
| Genre list | `Genre` rows and granularity |
