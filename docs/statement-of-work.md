# Aesium Platform Statement of Work

*Design, build and launch of Version 1 of the Aesium platform on .NET, SvelteKit and PostgreSQL, hosted on AWS with media on Cloudflare R2, with priced options for SoundCloud audio hosting, YouTube video and managed authentication, and a costed stretch package for physical goods.*

| | |
|---|---|
| **Client** | Aesium |
| **Supplier** | David Pipe |
| **Version** | 1.1, 26 September 2026 |
| **Basis** | *Aesium Platform Requirements & Build Options*, *Aesium Platform Operating Model*, and the derived working documents in `docs/` (foundations, content types, entity model) |
| **Currency** | Build pricing in NZD excluding GST. Hosting and service costs in USD unless stated. |

## 1. Overview

This Statement of Work covers the design, build, hosting set-up and launch of Version 1 of the Aesium platform: a New Zealand cultural platform for DJ mixes, artists, series, editorial, video, events and an artist shop.

It sets out scope, the technical approach, deliverables with hour estimates, the delivery plan and its lead-time dependencies, priced options for audio hosting, video hosting and authentication, a costed stretch package for physical goods, build pricing, monthly running costs, assumptions, and commercial terms including change control and maintenance.

The build is a custom platform rather than a configured content management product. Staff edit pages in place on the live templates; the database record is the source of truth and the page templates are code. This keeps the editing experience close to the audience experience and avoids a second administration system. Content entry is staff work: Aesium staff upload and connect every mix, video, article, event and product.

## 2. Objectives

- Launch a fast, branded platform where audiences discover artists, listen to mixes without interruption while browsing, and follow the artists they care about.
- Give Aesium staff one place to manage every record and the relationships between records, editing pages directly.
- Keep running costs low and predictable for a New Zealand audience.
- Leave a clean foundation for later phases (membership, artist self-service, recommendations, archive licensing) without a rebuild.

Success criteria at launch:

- Every V1 content type can be created, connected, scheduled, published and unpublished by staff without developer help.
- Playback continues across page navigation on desktop and mobile.
- Public pages reach a Lighthouse performance score of 90 or better on mobile, with Largest Contentful Paint under 2.0 seconds on a typical New Zealand 4G connection.
- Public pages meet WCAG 2.1 AA, and the video player carries caption tracks.
- Production runs across two availability zones, staging and production are reproducible from code, deploys are automated, and the database can be restored to any point in the previous 14 days, to within five minutes of the present.

## 3. Scope

### 3.1 In scope (Version 1)

Shared foundations, built once and used across every feature:

| # | Foundation | V1 scope |
|---|---|---|
| 01 | Accounts & permissions | Free audience accounts; staff sign-in with Administrator and Editor roles. Artists and contributors do not log in. |
| 02 | CMS & content model | Records, relationships and the shared hub-page pattern for artist profiles and series; edit-in-place editing; credits and rights metadata on every content item. |
| 03 | Publishing workflow | Draft, scheduled, published, unpublished; scheduler; featured and homepage placement. |
| 04 | Tagging & classification | Managed genre list with multi-select on mixes; fixed classifications kept per area. |
| 05 | Media assets | Image upload, storage, responsive variants, alt text, credit and rights fields, reuse across records. |
| 06 | Audio hosting | Upload or connect mix audio; stream it to the player; respect publishing state. |
| 07 | Audio player | Persistent Now Playing bar, full-view player, immediate switching, volume and mute. |
| 08 | Video hosting | Upload or connect video; branded playback with caption tracks; thumbnails; view counts. |
| 09 | Audience activity | Follow, like, save; private library; public aggregate follower counts. |
| 10 | Notifications | Preferences and email updates when a followed artist publishes. |
| 11 | Commerce & cart | Products with artist attribution; cart; guest checkout hand-off; commission rate per artist with per-product override. |
| 12 | Payments | Card processing, refunds, transaction records, automatic Aesium and artist split at the configured commission. |
| 13 | Admin back office | Dashboard, content lists, staff, settings, genre list, featured slots. |
| 14 | Content submission | Structured submission form with genre nomination and staff review. |
| 15 | Search & discovery | Keyword search across content including genre, macron-insensitive; genre filtering and genre pages. |
| 16 | Analytics & reporting | Web analytics, platform events, reporting views mapped to Aesium's measures, ticket and shop figures. |
| 17 | Hosting & infrastructure | AWS application and database across two availability zones, Cloudflare front end and media, point-in-time recovery, monitoring. |
| 18 | Ticketing integration | Event records in Aesium; ticket sales and RSVP on an external ticketing platform, integrated by API and embedded checkout. |

Content types and pages: Artist profiles, Mixes, Series, Editorial articles, Videos, Events, Products and Shop, Homepage with curated placements, audience account area, and static pages (About, Contact, Privacy, Terms).

Discovery and design: decision workshops for the open questions in Section 12.2, and wireframes and visual mock-ups for every screen the existing concept does not cover.

### 3.2 Out of scope

- Membership or paywall. Audience accounts stay free.
- Artist self-service accounts and artist-facing analytics. Priced as a later addition in Section 8.1.
- Contributor logins. Freelance writers, photographers and filmmakers send their work to the Editor by email or file transfer, and the Editor enters it.
- Queue, playlist and autoplay; resuming playback or cart across visits.
- Tagging beyond genre on mixes (mood, BPM, region) and recommendations.
- Aesium-hosted ticket sales and RSVP. Ticketing runs on an external platform integrated in work package 18.
- Physical goods handling: product variants, stock, shipping rates, fulfilment tracking and pre-orders, unless the stretch package in Section 5.2 is taken up.
- Native mobile apps.
- Content production and content entry: copywriting, photography, video production, audio mastering, artwork, and the uploading and connecting of records beyond the initial import in work package 22.
- Licensing of any kind: music, recordings, video, images, fonts, venue and event licences, and the negotiation and fees for them. See Section 8.4.
- Legal documents (privacy policy, terms of use, artist agreements) and accounting set-up.
- Migration of historical content beyond the initial import in work package 22.
- Ongoing support and maintenance after the warranty period. This is provided under the maintenance clause in Section 11 at the same hourly rate.

## 4. Technical approach

### 4.1 Stack

| Layer | Choice | Reason |
|---|---|---|
| Back end | .NET 10 (ASP.NET Core minimal APIs), Entity Framework Core | Long-term support release; strongly typed; runs well in a small container. |
| Database | PostgreSQL 17 on Amazon RDS, Multi-AZ, with point-in-time recovery | Relational model fits the content graph; JSONB for flexible fields; built-in full-text search covers V1; a standby in a second zone takes over on failure. |
| Front end | SvelteKit on Svelte 5 | Client-side navigation keeps the player alive between pages; server rendering for search engines and sharing; small bundles. |
| Front-end hosting | Cloudflare Pages | Edge delivery with New Zealand points of presence; generous free tier. |
| Application hosting | Amazon ECS on Fargate, two containers across two availability zones in ap-southeast-6 (Auckland) with ap-southeast-2 (Sydney) as fallback | Managed containers, nothing to patch, data stays in New Zealand where the region supports every service. |
| Media storage | Cloudflare R2 | No egress fees; S3-compatible API; served through Cloudflare's CDN on an Aesium domain. |
| Images | Cloudflare Image Transformations | Responsive variants generated on demand from the original. |
| Audio (base) | Self-hosted on R2 with a custom player | Full control over the listening experience. See Option A. |
| Video (base) | Cloudflare Stream | Branded player with caption tracks and adaptive streaming inside the same Cloudflare account. See Option B. |
| Editing | Edit-in-place on rendered templates; TipTap for rich text | The page is the editor. Templates are code; records are data. |
| Authentication (base) | ASP.NET Core Identity for staff and audience; email sign-in; two-factor for staff | No per-user fees; account data stays in Aesium's database; passwords can move to a managed provider later without a reset. See Option C. |
| Ticketing | External ticketing platform (Humanitix assumed, Eventbrite as the alternative) integrated by API and embedded checkout | Ticketing, payment and attendee handling stay with a specialist; Aesium keeps the event page and the numbers. Free events cost nothing on either platform. |
| Background jobs | Hangfire | Scheduled publishing, media processing, notification sending, provider syncs. |
| Payments | Stripe Checkout and Stripe Connect | Supported in New Zealand; automatic split between Aesium and artist accounts at a per-artist rate. |
| Email | Amazon SES with DKIM, DMARC, bounce and complaint handling | Transactional and notification email at very low cost, with deliverability set up from the start. |
| Analytics | Plausible for traffic; platform events in PostgreSQL for plays, follows, tickets and sales | Privacy-friendly and cookie-free traffic analytics; the platform counts its own activity. See Section 4.5. |
| Infrastructure as code | AWS CDK; GitHub Actions in Aesium's GitHub organisation | Staging and production defined in code; automated test and deploy on every change. |

### 4.2 Editing model

Staff sign in and switch any page into edit mode. Text, rich text, artwork slots, dates and classifications become editable where they sit on the page. Relationships (artist on a mix, episodes in a series, videos on an event, credits on an article) are set through pickers that search existing records. Changes save automatically as a draft; a publishing bar shows status and offers schedule, publish and unpublish. A back office covers what does not belong on a page: content lists with filters, the genre list, featured slots, staff, submissions, orders, reporting and settings.

Content entry is staff work. Artists, writers, photographers and filmmakers deliver material to Aesium by email, file transfer or the submission form; Aesium staff upload it, connect it and publish it. Neither artists nor contributors log in.

### 4.3 Player architecture

The audio player is written against a small provider interface (load, play, pause, seek, volume, progress events). The self-hosted provider and the SoundCloud provider both implement it, so the hosting decision in Option A changes the provider, not the site. The same pattern applies to video.

### 4.4 Environments and resilience

- Staging and production, each with its own database, buckets and secrets. Staging is password-protected and hidden from search engines.
- Preview deployments of the front end for every change under review.
- Production runs two application containers, one in each of two availability zones, behind the load balancer, so a container or a zone can fail without downtime. The containers sit in public subnets with public IP addresses, which is ECS Express Mode's default, and accept traffic only from the load balancer, so there is no NAT gateway to run or pay for.
- The production database is a Multi-AZ deployment with a synchronous standby in a second zone and automatic failover. Automated backups are kept for 14 days and transaction logs are shipped every five minutes, so the database can be restored to any point in that window to within five minutes of the present. A restore into staging is rehearsed at each phase release.
- Media buckets are versioned, so an overwritten or deleted file can be recovered.
- Uptime monitoring, error tracking and log retention of 30 days.

### 4.5 Analytics and reporting

Analytics come from three sources and are brought together in the back office so that staff read one set of views rather than four dashboards.

- **Traffic**, from Plausible: page views, visitors, referrers, countries, devices, and outbound clicks such as ticket links and artists' external links. Plausible is cookieless, so no consent banner is needed and it does not follow people across sites.
- **Platform events**, recorded by the platform itself in PostgreSQL: play start, thirty seconds played, play completed, follow, like, save, genre filter used, search term, cart, checkout started, order placed, submission received. Events attach to the account when the visitor is signed in and otherwise to an anonymous session that lasts for that visit only.
- **Provider figures**, pulled on a schedule: video views from Cloudflare Stream or YouTube; tickets sold and attendees from the ticketing platform; revenue, refunds and payouts from Stripe.

The reporting views are defined against the measures in the Operating Model:

| Measure in the Operating Model | Source | View in the back office |
|---|---|---|
| Programming: resident retention; guest mix cadence hit rate | Publishing records | Publishing calendar: mixes per artist per month against the planned cadence |
| Audience: returning listener rate; discovery-to-follow conversion | Platform events for signed-in listeners; Plausible for overall traffic | Audience view: listeners who return within 30 days; plays that lead to a follow in the same session |
| Artist pipeline: completed Guest Spot, Highlight and Feature projects | Content records per artist | Artist view: content by artist and type, first and latest publish dates |
| Archive: content pieces produced per quarter | Content records | Archive view: pieces published per quarter by type |
| Physical releases and tickets sold per event | Ticketing platform; shop orders | Events view: tickets sold and attended per event. Shop view: orders, revenue and commission by artist and product |
| Brand and commercial: press mentions; partner inbound | Outside the platform | Not measured by the platform |
| Retention: artists still engaged after 12 months | Content records | Artist view: months since each artist's last published item |

Each view takes a date range and exports to CSV, and a monthly summary of the same figures is emailed to staff. Two limits are worth knowing in advance. Returning visitors who are not signed in cannot be counted across days, because Plausible does not identify people; returning listener rate therefore comes from signed-in activity. Tickets for events sold anywhere other than the integrated ticketing platform are visible only as clicks on the link. Artist-facing reporting is excluded from V1, as the requirements ask.

## 5. Deliverables and hour estimates

Hours are estimates of the effort to deliver working, tested functionality. Each work package includes its own automated tests and short technical notes. A detailed breakdown is in Appendix A.

### 5.1 Work packages

| Work package | What it delivers | Hours | Phase |
|---|---|---|---|
| 1. Discovery, decisions & design mock-ups | Decision workshops and a decision log for the open questions in Section 12.2; wireframes and visual mock-ups for every screen the existing concept does not cover | 36 | 1, 2, 3 |
| 2. Platform foundations & infrastructure | Repositories in Aesium's GitHub organisation, CI/CD, staging and production on AWS via CDK across two availability zones, Cloudflare set-up, logging and alerts | 34 | 1 |
| 3. Accounts & permissions | Staff sign-in with Administrator and Editor roles and two-factor; audience registration, sign-in, recovery, profile, deletion and data export | 30 | 1, 2 |
| 4. Content model & edit-in-place | Data model for every record and relationship; inline editing framework on rendered pages; slugs and page metadata | 48 | 1 |
| 5. Credits & rights metadata | Collaborator records and roles on every content item; rights holder, licence terms and cleared uses per asset; credits on public pages; archive export | 12 | 1 |
| 6. Publishing workflow | Draft, scheduled, published, unpublished on every type; scheduler; preview links; publish hooks | 12 | 1 |
| 7. Tagging & classification | Managed genre list, multi-select, fixed classifications, filters, genre pages | 8 | 1 |
| 8. Media assets | Direct-to-R2 upload, responsive variants, alt text, media library, reuse, clean-up | 16 | 1 |
| 9. Audio hosting & delivery | Large-file upload, processing, waveform, streaming delivery, play counting (base: self-hosted on R2) | 20 | 1 |
| 10. Audio player | Persistent Now Playing bar, full-view player, immediate switching, volume and mute, lock-screen controls | 24 | 1 |
| 11. Video hosting & playback | Upload, processing, branded player with caption tracks, thumbnails, view counts (base: Cloudflare Stream) | 14 | 2 |
| 12. Content types & pages | Templates and behaviours for every content type, homepage placements, account area, static pages | 102 | 1, 2, 3 |
| 13. Search & discovery | Full-text search with macron-insensitive matching, results page, genre filtering, related content | 10 | 1 |
| 14. Design system & front-end build | Tokens, typography, components, responsive layouts, dark mode, accessibility | 28 | 1 |
| 15. Email deliverability & SEO | Sending domain, DKIM, DMARC, bounce and complaint handling, one-click unsubscribe; sitemap, robots, canonical URLs, structured data | 14 | 1 |
| 16. Analytics & reporting | Web analytics, platform events, reporting views mapped to the Operating Model's measures, CSV export, monthly summary | 16 | 1, 2, 3 |
| 17. Audience activity & notifications | Follow, like, save, private library, follower counts; preferences; publish-triggered email | 24 | 2 |
| 18. Ticketing integration | Ticketing platform linked to event records, embedded checkout on event pages, ticket and attendee counts synced | 16 | 2 |
| 19. Admin back office & submissions | Dashboard, content lists, staff, settings, audit log; submission form and review queue | 26 | 2 |
| 20. Commerce & payments | Cart, guest checkout, Stripe Checkout, Stripe Connect split at a per-artist commission with per-product override, refunds, orders, reporting | 40 | 3 |
| 21. Quality, security & performance | End-to-end tests, performance tuning, security and privacy review, load test | 28 | 1, 2, 3 |
| 22. Launch & handover | Content import, staff training, documentation, go-live, two weeks of hypercare | 16 | 1, 2, 3 |
| Subtotal, build | | 574 | |
| 23. Project management & communication | Planning, weekly reviews and demos, decision log, reporting | 48 | All |
| Total | | 622 | |

Content types and pages (work package 12) in detail:

| Page or content type | Included | Hours |
|---|---|---|
| Artist profiles | Hub page pattern, Experiences grid and filters, related artists from shared genres, follow button and follower count, external links, releases, grouped presentation for artists with little content | 18 |
| Mixes | Listing with genre filter, detail page, tracklist, credits, series episode display, like and save | 14 |
| Series | Hub page reuse, episode ordering, collected videos, articles, products and links | 12 |
| Editorial articles | Rich text layout, images, byline and credits, pull quote, "In Their Words" section on profiles | 12 |
| Videos | Listing, detail page, video categories, credits, artist, series and event links, like and save | 8 |
| Events | Upcoming and Past, Next Up, venue, ticket action from the ticketing platform, recordings | 10 |
| Products and Shop | Listing, detail page, shop categories, artist attribution, series placement | 12 |
| Homepage & featured placements | Curated slots with ordering and start and end dates, latest and featured content | 12 |
| Static pages, navigation and footer | About, Contact, Privacy, Terms; header, footer, cart icon | 4 |
| Total | | 102 |

### 5.2 Stretch package: physical goods commerce

Work package 20 sells products and splits the money. It does not handle what physical goods need once orders arrive in volume: variants, stock, shipping, and a way for artists to fulfil orders without logging in. The Operating Model also describes Aesium running its own vinyl and tape releases, merchandise drops and pre-orders, which need products sold by Aesium with no artist split. This package covers all of that and is priced separately, so Aesium can take it up in Phase 3, later, or not at all.

| Item | Included | Hours |
|---|---|---|
| Variants and stock | Size, colour and format variants; stock per variant; sold-out and low-stock states; stock adjustments in the back office | 10 |
| Shipping and tax | Shipping address capture at checkout; shipping rates by zone (New Zealand, Australia, rest of world) and by seller; GST-inclusive pricing and order tax lines | 8 |
| Fulfilment without logins | Order email to the artist with packing details; fulfilment status (new, packed, shipped with tracking number) set by staff or by the artist through a tokenised link; shipping notification to the customer | 10 |
| Aesium-sold products and drops | Products sold by Aesium with no artist split; pre-orders and limited drops with an availability window and a quantity cap | 8 |
| Reporting and tests | Stock and fulfilment reporting; automated tests across the above | 4 |
| Total | | 40 |

Price: NZD 6,000 excluding GST. Merchant of record, GST treatment and refund responsibility are specified with Aesium's accountant at the start of the store work, whether or not this package is taken up (Section 12.2).

## 6. Delivery plan

The build is delivered in three phases. Each phase ends with a working, deployable release that Aesium can put in front of real users.

| Phase | Focus | Build hours | PM hours | Total hours | Duration |
|---|---|---|---|---|---|
| 1. Foundation & listening | Discovery and mock-ups, infrastructure, staff accounts, content model and editing, credits and rights, publishing, genres, media, audio, player, artist profiles, mixes, series, editorial, homepage, static pages, search, email and SEO, analytics, design system | 374 | 32 | 406 | 13 to 14 weeks |
| 2. Audience, video & events | Audience accounts, follow, like and save, notifications, video, events with ticketing, admin dashboard, submissions | 134 | 11 | 145 | 5 weeks |
| 3. Shop & payments | Products, cart, checkout, Stripe Connect with per-artist commission, orders, refunds, reporting; the physical goods stretch package if taken up | 66 | 5 | 71 | 2 to 3 weeks |
| Total | | 574 | 48 | 622 | 20 to 22 weeks |

The phases follow the Operating Model's roadmap. Phase 1 delivers its V1: resident and guest programming, editorial and the web platform, so the first guest spots launch with their write-ups. Phase 2 delivers its V2: audience accounts, live sessions on video, and small venue events with ticketing. Phase 3 delivers the commerce that V3 and V4 need for physical releases and merchandise. Each phase is priced and can be committed separately, so Phase 3 can be scheduled when the shop is ready to open rather than at kick-off.

Milestones:

| Milestone | Week | Evidence |
|---|---|---|
| M0 Kick-off | 0 | Decisions in Section 12.1 confirmed; accounts, GitHub organisation and access in place |
| M1 Foundations | 4 | Staging live on AWS across two zones; staff sign-in; content model migrated; edit-in-place working on the artist template; Phase 1 mock-ups approved |
| M2 Phase 1 beta | 10 | Artists, mixes, series, articles, homepage, player and search working end to end on staging with real content |
| M3 Phase 1 launch | 14 | Production live; hypercare begins |
| M4 Phase 2 release | 19 | Audience accounts, follow, notifications, video, events with ticketing, submissions live |
| M5 Phase 3 release | 22 | Shop and payments live; reconciliation report available |
| M6 Handover | 22 | Documentation, training and warranty start |

Durations assume decisions and content arrive when needed and a delivery cadence of roughly 30 hours per week on the project.

Lead-time dependencies. The items below are outside the Supplier's control and can each move the timeline. Aesium's tasks run in parallel with the build; the build itself is sequential because one developer delivers it.

| Dependency | Who | Typical lead time | Needed by |
|---|---|---|---|
| GitHub organisation in Aesium's name with the Supplier as a member | Aesium | Same day | M0 |
| AWS account with billing set up and access to the Auckland region | Aesium | 1 to 2 days | M0 |
| Cloudflare account and moving the domain's DNS to it | Aesium | 1 to 3 days | M1 |
| Amazon SES production access; new accounts start in a sandbox that cannot email the public | Supplier requests it on Aesium's account | 1 to 2 business days | M1 |
| Genre list, profile fields and the other workshop decisions | Aesium, in the workshops | Weeks 1 to 2 | M1 |
| Content, artwork, audio and copy for the Phase 1 launch | Aesium | Ongoing from week 1 | M2 |
| Music licence confirmation for self-hosted streaming | Aesium, with APRA AMCOS and Recorded Music NZ | 2 to 8 weeks | M3, if audio is self-hosted |
| SoundCloud Artist Pro account and API credentials (Option A or the adapter) | Aesium | Days | M2 |
| Plausible account | Aesium | Same day | M2 |
| Privacy policy and terms of use | Aesium's lawyer | Weeks | M3 |
| Ticketing platform account and API key | Aesium | 1 to 3 days | Phase 2 start |
| YouTube channel in good standing (Option B) | Aesium | Same day | Phase 2 start |
| Stripe account and approval as a Connect platform | Aesium | Allow 1 to 2 weeks; Stripe reviews the platform profile before live payouts | Phase 3 start |
| Artist onboarding to Stripe Connect, one artist at a time | Aesium coordinates; each artist completes it | Days per artist | Before that artist's first product goes on sale |

## 7. Options

Four decisions shape the product, the build and the running cost: where mix audio lives, where video lives, who runs authentication, and what runs the shop. The base configuration keeps all four under Aesium's control. Each option below swaps a provider, describes what changes in the interface, lists the downsides, and prices the difference. Section 7.4 assesses Shopify against Aesium's two criteria for a commerce platform.

### 7.1 Audio: self-hosted on R2 (base) or SoundCloud (Option A)

| | Base: self-hosted on R2 | Option A: SoundCloud |
|---|---|---|
| Where audio lives | Aesium's R2 bucket, streamed on an Aesium domain through expiring URLs; no download | SoundCloud, on Aesium's account |
| How staff add a mix | Upload the file on the mix page; processing runs in the background | Upload to SoundCloud, then paste the track link on the mix page |
| Player | Fully custom bar and full-view player | Custom bar controlling a SoundCloud widget that must remain visible |
| Licensing | Aesium's responsibility and outside this Statement of Work. Online licences from APRA AMCOS and Recorded Music NZ are the usual route and must be in place before launch | SoundCloud's terms make the uploader responsible for the rights in every upload. SoundCloud's own agreements with labels and collecting societies cover some material, and its automated matching removes what they do not. This reduces Aesium's exposure but does not remove it, and SoundCloud's position on DJ mixes is less established than Mixcloud's |
| Play analytics | In Aesium's database and reports | On SoundCloud; Aesium records play starts only |
| Build hours | 20 (work package 9, audio hosting) + 24 (work package 10, audio player) | 14 (SoundCloud integration) + 30 (work package 10 with the widget adapter). Net change: 0 |
| Monthly cost | R2 storage about USD 1 to 3; music licences from about NZD 510 a year on the published small-service tariffs, otherwise quoted | Artist Pro plan USD 99 a year (NZD 135 when bought from New Zealand) on Aesium's account. Mixes cannot stay on artists' free accounts: a free SoundCloud account allows two hours of upload in total and the USD 39-a-year Artist plan three hours, so a library of mixes needs Artist Pro's unlimited uploads, either on Aesium's account or on each artist's |

Interface changes with Option A:

- The Now Playing bar carries a compact SoundCloud widget. SoundCloud's terms require its player and branding to stay visible and unobscured, so the bar shows a slim SoundCloud strip (track link, logo) alongside Aesium's own play, pause, progress and volume controls, which drive the widget through its API.
- Artwork, waveform and duration come from SoundCloud. The full-view player shows SoundCloud's waveform rather than a custom one.
- Mixes are added by pasting a SoundCloud link. There is no audio upload in Aesium's admin in V1. SoundCloud issues API credentials to Artist Pro subscribers, so upload from Aesium through SoundCloud's API can be added later (about 8 hours).
- On iOS Safari and some Android browsers, audio inside a third-party frame needs a tap inside that frame before it will start. "Play from any card" and "switch immediately" work on desktop but can require a second tap on mobile.
- Tracks that are deleted, made private, geo-blocked or have embedding turned off show a fallback state instead of playing. Staff get a warning in the admin when a linked track stops resolving.
- Volume works through the widget API, so the desktop slider and mobile mute both function.

Downsides of Option A:

- Loss of control. Availability, playback quality, branding and the terms of use are SoundCloud's. Tracks can be removed by automated rights matching without notice.
- Branding and leakage. The SoundCloud logo and link sit inside the listening experience, and each track links out to soundcloud.com.
- Advertising. SoundCloud is ad-supported for free listeners inside its own apps and site. It does not currently play ads inside embedded players, but its terms allow it to change that.
- Dependency for the core feature. A change to SoundCloud's widget, API or pricing affects every mix on the site.
- Analytics split. Listening data lives on SoundCloud; Aesium reports show play starts only.
- Future limits. Content on SoundCloud cannot be placed behind an Aesium membership later.
- Workflow. Every mix is uploaded twice: to SoundCloud, then linked in Aesium. Because free SoundCloud accounts cannot hold a library of mixes, the uploading falls to Aesium's own account.

Upsides of Option A:

- No storage, transcoding or delivery to run. Waveforms and encodes are provided.
- Part of the licensing exposure moves onto SoundCloud's agreements and its takedown process rather than sitting wholly with Aesium.
- Many artists already publish to SoundCloud, and their existing audiences and play counts carry over.
- Fast path to launch if Aesium's own licence position is unresolved.

Alternative considered: Mixcloud. It is built for DJ mixes and its licensing for mixes is the most established of the three. Its widget must also stay visible and, for free listeners, restricts seeking within a mix, which conflicts with the required player behaviour. Mixcloud Pro costs USD 11.25 a month on the annual plan (USD 15 monthly). It can be priced as a variant of Option A if Aesium prefers it.

### 7.2 Video: Cloudflare Stream (base) or YouTube (Option B)

| | Base: Cloudflare Stream | Option B: YouTube |
|---|---|---|
| Where video lives | Aesium's Cloudflare account | Aesium's YouTube channel, or the artist's own channel |
| How staff add a video | Upload on the video page; processing runs in the background | Upload in YouTube Studio, then paste the link on the video page |
| Player | Aesium-branded player, adaptive streaming | YouTube's player inside Aesium's page |
| Captions | Caption tracks uploaded in the admin as WebVTT files and shown in the player, as WCAG requires for prerecorded video. Stream generates English and eleven other languages' captions automatically at no extra cost, which staff can correct before publishing. The captions themselves are content that Aesium supplies | YouTube's captions, including its automatic ones, inside its player |
| Advertising | None | YouTube may show ads before or during videos |
| View analytics | In Aesium's database and reports | In YouTube Studio; Aesium records play starts, and can pull view counts |
| Build hours | 14 (work package 11, video hosting, including captions) | 8 (YouTube integration). Net change: minus 6 |
| Monthly cost | USD 5 per 1,000 minutes stored plus USD 1 per 1,000 minutes watched. About USD 45 at a modest starting library; scales with viewing | USD 0 |

Interface changes with Option B:

- Video pages show Aesium's own thumbnail and play button until the viewer clicks. The YouTube player loads only then, which keeps pages fast and on-brand until playback starts.
- Once playing, the player is YouTube's: YouTube logo, title overlay when paused, share button, "Watch on YouTube" link, and end-screen suggestions from the same channel. None of this can be restyled or removed.
- The player sits in a fixed 16:9 frame. Vertical or square videos show with letterboxing.
- Starting a video pauses the mix in the Now Playing bar, and starting a mix pauses the video. This is done through YouTube's player events.
- Videos are added by pasting a link. Title, duration and a fallback thumbnail are fetched automatically. There is no video upload in Aesium's admin.
- Embedding uses YouTube's privacy-enhanced domain and loads no Google scripts until the viewer chooses to play. This makes any ads non-personalised but does not remove them, and the privacy policy still needs to cover Google's processing once playback starts.
- Videos that are private, deleted, age-restricted, or have embedding disabled by their owner show a fallback state. Artist-owned videos are the usual source of this.

Downsides of Option B:

- Advertising. YouTube's terms give it the right to run ads on any video, including those from channels that are not in its Partner Program, and those ads appear in embedded players. Neither the channel owner nor the embedding site can switch ads off for embeds, Aesium cannot choose which brands appear, and Aesium earns nothing from them unless it joins the Partner Program.
- Rights matching. Live sets and mixes containing recorded music are routinely matched by Content ID. Outcomes include muted audio, blocking in some countries, or the claimant taking ad revenue. A strike can restrict the channel.
- Loss of control. Availability, player design, policy changes and removals are YouTube's decisions. A channel termination removes every video at once.
- Branding and leakage. The YouTube logo, title bar and end-screen suggestions pull viewers off Aesium.
- Analytics off-platform. Watch time and audience data live in YouTube Studio.
- Future limits. YouTube-hosted video cannot be placed behind an Aesium membership later.
- Account dependency. Aesium's video library lives in a Google account that must be secured and kept in good standing.

Upsides of Option B:

- No hosting or delivery cost at any scale.
- Adaptive streaming, captions, chapters and live streaming are included.
- YouTube search and recommendations bring an audience of their own.
- Artists often have their videos there already, so linking is immediate.

Alternative considered: Vimeo. It gives an ad-free, brandable player with uploaded and automatic captions, domain-restricted embedding and privacy controls for a fixed subscription (Starter USD 12 a month per seat on the annual plan with 2 TB of storage; Standard USD 25 with 4 TB), with no per-minute charge. Vimeo also caps uploads per seat per year on these plans (60 on Starter, 120 on Standard), which suits a small library. It sits between the two options on cost and control and can be substituted for Cloudflare Stream at no change to build hours.

### 7.3 Authentication: ASP.NET Core Identity (base) or Auth0 (Option C)

The requirements note that a managed authentication provider is the more established approach. The base configuration uses ASP.NET Core Identity, Microsoft's identity framework inside the application, because it has no per-user cost, keeps account data in Aesium's own database in New Zealand, and can be moved to a managed provider later without asking anyone to reset a password. The comparison below is with Auth0, the most widely used managed provider.

| | Base: ASP.NET Core Identity | Option C: Auth0 |
|---|---|---|
| What it is | Microsoft's identity framework inside the application. Accounts, password hashes and sessions live in Aesium's database | A managed identity service. Accounts live in an Auth0 tenant hosted in Australia, and the platform trusts Auth0's tokens |
| Build hours | 30 (work package 3) | 26: tenant configuration as code, hosted sign-in pages in Aesium's colours, token validation, profile sync, deletion and export through Auth0's API. Net change: minus 4 |
| Monthly cost at launch | 0 | 0 on the Free plan, which covers up to 25,000 monthly active users |
| Monthly cost as the audience grows | 0 | 0 while the Free plan's limits suit. The Essentials plan, needed for authenticator-app two-factor, sign-up and email customisation and five-day logs, is priced on every active user: USD 35 at 500, 70 at 1,000, 350 at 5,000 and 700 at 10,000 monthly active users |
| Two-factor for staff | Authenticator app, built in | Passkeys on the Free plan; authenticator-app codes need Essentials |
| Social and passwordless sign-in | Not included; about 4 hours per provider if wanted later | Included: Google, Apple and other social sign-ins, passkeys, and one-time codes by email or SMS |
| Sign-in pages | Aesium's own pages | Auth0's hosted pages on Aesium's domain with Aesium's logo and colours; full control of the layout needs a paid plan |
| Sign-in logs for investigating problems | Kept by the platform for 30 days | 1 day on the Free plan, 5 on Essentials, 10 on Professional |
| Where account data lives | Aesium's database in Auckland | Auth0's Australia region; the privacy policy must say that account data is held in Australia |
| Maintenance | Kept current with .NET releases under the maintenance clause | Auth0 maintains the service; Aesium holds the account, its bill and its configuration |
| Moving later | Password hashes are PBKDF2, which Auth0 imports after a format conversion, so a later move needs no password reset (24 hours, Section 8.1) | Auth0 does not export password hashes, so moving away later means every audience member resets their password |

Cost and benefit. The base configuration costs nothing beyond ordinary maintenance for the life of the platform. Auth0 also costs nothing until Aesium wants authenticator-app two-factor for staff, more than a day of sign-in logs, or an audience beyond the Free plan, after which the Essentials plan runs from USD 420 to 8,400 a year across the audience sizes above. What Auth0 buys is social and passwordless sign-in, which the requirements do not ask for, and one less security surface for the Supplier to maintain. Recommendation: the base configuration, with the 24-hour migration in Section 8.1 keeping the door to Auth0 open if social sign-in becomes a priority.

### 7.4 Commerce platform: custom on Stripe (base) or Shopify (considered)

Aesium set two criteria for any commerce platform: it must pay artists out automatically, and it must support a separate store for each artist. The base configuration meets both with Stripe Connect and per-artist product listings on Aesium's own front end.

Shopify was assessed against the same criteria. Three arrangements exist, and one meets both.

| Arrangement | Pays artists automatically | Separate store per artist | Assessment |
|---|---|---|---|
| Shopify Collective | Yes. Aesium's store sells products supplied by each artist's store. The cost price is debited from Aesium's Shopify Payments balance and transferred to the artist when the artist marks the order fulfilled, at no extra charge | Yes. Every artist runs their own Shopify store, which must be in New Zealand, priced in NZD and on Shopify Payments | Meets both criteria. Available to New Zealand merchants |
| Multi-vendor app on Aesium's store (Webkul MultiVendor Marketplace, Puppet Vendors) | Yes, through the app's Stripe Connect or PayPal payouts on commission rules | Partly. Each artist gets a vendor dashboard and listing page inside Aesium's store, not an independent store | Meets the first criterion and the second only loosely. Adds USD 15 to 60 a month for Webkul plus USD 10 for its Stripe Connect add-on, or USD 49 a month upwards for Puppet Vendors |
| Artists' own Shopify stores linked from Aesium | No. Sales happen in the artist's store and Aesium's commission would be invoiced by hand | Yes | Fails the first criterion |

How Shopify Collective would work for Aesium:

- Aesium's store on the Basic plan (USD 29 a month billed yearly, USD 39 monthly) is the retailer. Aesium's front end reads products and builds the cart through the Storefront API, which is free on every plan, and hands over to Shopify's hosted checkout, as the base configuration does with Stripe.
- Each artist's store is the supplier and needs its own Shopify plan, also from USD 29 a month, with Shopify Payments active. Artists who already sell on Shopify connect in minutes. Artists who do not would be paying for a store to sell a few items, or Aesium would pay it for them.
- Aesium's commission is the difference between the retail price and the artist's cost price, set per product, so it is dynamic by construction.
- Stripe is not offered as a gateway on Shopify in New Zealand, so payments run through Shopify Payments at 2.65% + NZD 0.30 on the Basic plan, close to Stripe's rate.
- Variants, stock, shipping rates, fulfilment and tracking are native to Shopify, so most of the physical goods stretch package in Section 5.2 would not be needed. Aesium's own releases and merchandise would sit in Aesium's store as ordinary products.
- Each artist manages their own store, which departs from the assumption that artists never log in to anything. Aesium keeps the customer relationship and the seller's consumer-law obligations, as in the base configuration.

Build effect: work package 20 becomes about 34 hours (Storefront API integration, cart, checkout hand-off, order webhooks into reporting, Collective set-up and artist onboarding notes) instead of 40. Running cost: Aesium's plan from USD 29 a month, plus a Shopify plan for every artist store. Section 7.5 shows this as Option D.

Recommendation: keep the base configuration unless most artists already run Shopify stores. Stripe Connect pays artists into their bank accounts with nothing for them to subscribe to, and Aesium's per-artist commission is one field. Revisit Shopify Collective if the shop grows into a catalogue that needs Shopify's stock and shipping tooling, because that is the point at which the stretch package would otherwise be built.

### 7.5 Option combinations

| Configuration | Build hours change | Monthly cost change | Notes |
|---|---|---|---|
| Base: R2 audio, Cloudflare Stream video, ASP.NET Core Identity | 0 | 0 | Full control; Aesium's music licences required before audio launch |
| Option A only: SoundCloud audio | 0 | plus USD 0 to 8; may reduce Aesium's own licence needs, which Aesium confirms | Player provider swap |
| Option B only: YouTube video | minus 6 | about minus USD 45 at launch volume, more as viewing grows | Provider swap |
| Option C only: Auth0 authentication | minus 4 | 0 at launch; rises with monthly active users (Section 7.3) | Identity provider swap |
| Option D only: Shopify Collective commerce | minus 6 | plus USD 29 for Aesium's store, plus a Shopify plan per artist store | Most of the physical goods stretch package becomes unnecessary (Section 7.4) |
| Options A and B | minus 6 | about minus USD 38 at launch | Lowest running cost, least control |
| Base plus SoundCloud adapter kept | plus 20 | 0 | Both audio providers available; mixes can be self-hosted or linked |
| Base plus YouTube adapter kept | plus 8 | 0 | Both video providers available |
| Physical goods stretch package | plus 40 | 0 | Any configuration |

Recommendation: keep the base configuration for audio, because the listening experience is the product, and build the SoundCloud adapter (plus 20 hours) so that individual mixes can be linked where licensing or an artist's preference requires it, and so the site can launch on linked audio if Aesium's licences are not yet in place. For video, launch with YouTube (Option B) and the click-to-play facade, since the video library is small at launch and advertising exposure is limited to the videos Aesium chooses to embed. Move to Cloudflare Stream when a branded, ad-free experience matters more than the per-minute cost; the provider interface makes that a 14-hour change. Keep ASP.NET Core Identity for authentication and revisit Auth0 only if social sign-in or passwordless login becomes a priority. Keep the custom shop on Stripe Connect unless most artists already run Shopify stores.

## 8. Pricing

### 8.1 Build

Rate: NZD 150 per hour, excluding GST. Every figure below is hours multiplied by this rate.

| Phase | Hours | Price (NZD, ex GST) |
|---|---|---|
| 1. Foundation & listening | 406 | 60,900 |
| 2. Audience, video & events | 145 | 21,750 |
| 3. Shop & payments | 71 | 10,650 |
| Total, base configuration | 622 | 93,300 |
| Contingency reserve (10%, drawn only through approved change requests) | 62 | 9,300 |

Option adjustments to the total:

| Option | Hours | Price (NZD, ex GST) |
|---|---|---|
| Option A: SoundCloud instead of self-hosted audio | 0 | 0 |
| Option B: YouTube instead of Cloudflare Stream | minus 6 | minus 900 |
| Option C: Auth0 instead of ASP.NET Core Identity | minus 4 | minus 600 |
| Option D: Shopify Collective instead of the custom shop on Stripe | minus 6 | minus 900 |
| SoundCloud adapter kept alongside self-hosting | plus 20 | plus 3,000 |
| YouTube adapter kept alongside Cloudflare Stream | plus 8 | plus 1,200 |
| Recommended configuration (base audio plus SoundCloud adapter, YouTube video, ASP.NET Core Identity) | 636 | 95,400 |

Stretch package, priced separately and taken up by change request:

| Package | Hours | Price (NZD, ex GST) |
|---|---|---|
| Physical goods commerce (Section 5.2) | 40 | 6,000 |

Later additions, not included in V1 and shown for planning only:

| Addition | Hours | Price (NZD, ex GST) |
|---|---|---|
| Move authentication to Auth0 after launch: password hashes converted to Auth0's import format, a rehearsal import, sign-in flows, tenant configuration | 24 | 3,600 |
| Artist self-service accounts: artist role, invitation, profile and content editing with staff approval before publishing | 40 | 6,000 |

### 8.2 Running costs

Estimated monthly costs at launch volume: about 10,000 page views a month, 300 mixes averaging 150 MB, 60 videos averaging 40 minutes, 2,000 video views a month, 20,000 emails a month, two application containers across two availability zones and a Multi-AZ database. Figures are in USD and drawn from the providers' published price lists on 23 September 2026, using the Auckland region (ap-southeast-6), which runs about 10% above Sydney. There is no extra charge for ECS Express Mode.

| Item | Base | Options A and B | Notes |
|---|---|---|---|
| AWS: two application containers (0.5 vCPU, 1 GB each, one per availability zone) | 48 | 48 | Survives the loss of a container or a zone |
| AWS: load balancer | 25 | 25 | Created by ECS Express Mode; billed hourly plus usage |
| AWS: PostgreSQL db.t4g.micro Multi-AZ, 20 GB storage, point-in-time recovery | 45 | 45 | Synchronous standby in a second zone; the Multi-AZ rate in Auckland is USD 0.0533 an hour, twice the Single-AZ rate, and storage is doubled too |
| AWS: secrets, container registry, logs, data transfer | 7 | 7 | No NAT gateway: the containers have public addresses and accept traffic only from the load balancer |
| Cloudflare: Workers Paid plan for server rendering | 5 | 5 | Free tier may be enough at launch |
| Cloudflare: R2 storage (about 50 GB) | 1 | 0 | No egress charges; first 10 GB free |
| Cloudflare: image transformations | 3 | 3 | First 5,000 unique transformations free |
| Cloudflare: Stream (2,400 minutes stored, 30,000 minutes watched) | 45 | 0 | Storage prepaid in 1,000-minute blocks; grows with library and viewing |
| SoundCloud Artist Pro (annual plan) | 0 | 8 | USD 99 a year on Aesium's account |
| YouTube | 0 | 0 | |
| Ticketing platform | 0 | 0 | Booking fees are charged per ticket and normally passed to the buyer (Section 8.3) |
| Auth0 | 0 | 0 | Base uses ASP.NET Core Identity; Option C is free at launch volume (Section 7.3) |
| Plausible Analytics, Starter plan (10,000 page views) | 9 | 9 | 19 at 100,000 page views; Growth plan 14 |
| Amazon SES (20,000 emails) | 2 | 2 | Sydney rate; SES pricing is not yet listed for Auckland |
| Error tracking and uptime monitoring | 0 | 0 | Free tiers at this scale |
| Domain and DNS | 2 | 2 | Annual registration averaged |
| Total per month | about 192 | about 154 | |
| Total per year | about 2,300 | about 1,850 | |

A single-zone configuration (one container and a Single-AZ database) would cost about USD 145 a month in the base configuration. The difference buys the ability to lose a container or an availability zone without an outage.

Not included above: music licences for self-hosted streaming (Section 8.4, base configuration only), Stripe processing fees and ticketing fees (Section 8.3), and any paid support plans.

Growth scenario, ten times the launch volume (100,000 page views, two larger containers, a larger Multi-AZ database, 30,000 minutes stored and 300,000 minutes watched):

| Configuration | Monthly (USD) | What drives it |
|---|---|---|
| Base | about 730 | Cloudflare Stream is about 60% of the total |
| Options A and B | about 280 | Compute and database; media delivery costs nothing |

### 8.3 Transaction and usage fees

| Fee | Amount | Applies to |
|---|---|---|
| Stripe card processing, New Zealand cards | 2.65% + NZD 0.30 per successful charge (Stripe's Connect page shows 2.7%; confirm at sign-up) | Every shop order |
| Stripe card processing, international cards | 3.5% + NZD 0.30, plus 2% where currency conversion is needed | Orders paid with non-NZ cards |
| Stripe Connect, Aesium sets its own pricing | NZD 2 per connected artist account in any month it is paid, plus 0.25% + NZD 0.25 per payout | Artist share of each order |
| Stripe disputes | NZD 25 per dispute, refunded if won | Chargebacks |
| Humanitix booking fee, New Zealand | Free events: nothing. Paid tickets: 5% + NZD 0.49 per ticket excluding GST (3% + NZD 0.30 for registered charities). Passed to the buyer by default; can be absorbed or split | Every ticket sold through the integrated platform |
| Eventbrite fees, New Zealand | Free events: nothing. Paid tickets: 3.7% + NZD 1.79 service fee per ticket plus 2.9% payment processing per order. Paid by the buyer by default | Alternative ticketing platform |
| Amazon SES | USD 0.10 per 1,000 emails | Notification and transactional email |
| Cloudflare R2 | USD 0.015 per GB-month; USD 4.50 per million writes; USD 0.36 per million reads | Media beyond the free tier |
| Cloudflare Stream | USD 5 per 1,000 minutes stored; USD 1 per 1,000 minutes watched | Base video configuration |

### 8.4 Costs outside this Statement of Work

Licensing of any kind is outside this Statement of Work. The Supplier does not advise on, obtain or pay for licences, and nothing in this document is licensing advice. The figures below are for orientation only. These costs are the Client's and are not included in the figures above:

- Music licences for on-demand streaming of mixes (base audio configuration). OneMusic NZ licenses premises, not websites; online use is licensed separately by APRA AMCOS (compositions) and Recorded Music NZ (recordings). APRA AMCOS publishes an Online Mini Licence at NZD 250 to 1,000 a year per category of use for services earning under NZD 12,000 a year; Recorded Music NZ publishes an Audio Webcast Licence at NZD 260 plus GST a year for non-interactive webcasts and quotes on-demand services case by case. Whether an on-demand mix player fits the fixed tariffs or needs a quoted licence, and whether the licences cover listeners outside New Zealand, is for Aesium to confirm with both bodies.
- Rights clearance for video: music synchronisation, footage, likeness, and attendee permissions for filmed events.
- Domain registration, business email, a GitHub organisation, and the Stripe, AWS, Cloudflare, ticketing platform, SoundCloud, YouTube, Auth0 (Option C) and Plausible accounts, which are opened in Aesium's name.
- Legal documents: privacy policy, terms of use, artist agreements, refund policy.
- Accounting and tax advice on the artist money flow, merchant of record, GST and Aesium's commission.
- Paid support plans on any third-party service.

## 9. Assumptions and dependencies

- The existing Aesium mockup and brand (typefaces, palette, layouts) is the design source for the screens it covers. Screens it does not cover are designed in work package 1 as wireframes and then visual mock-ups, with two review rounds each, before they are built.
- Two staff roles, Administrator and Editor, are enough for V1. Further roles are a change.
- Content entry is staff work. Artists, writers, photographers and filmmakers deliver material by email, file transfer or the submission form; staff upload it, connect it and publish it. Neither artists nor contributors log in.
- Notifications are email only in V1. Browser push is a later addition.
- The shop is Aesium-managed: products are records in Aesium, orders go through one unified cart and Stripe Checkout on Stripe's hosted page, and Stripe Connect splits each order between Aesium and the artist at that artist's commission rate, with a per-product override. Moving to Stripe's hosted page pauses the mix for the duration of checkout, which Aesium has accepted. Aesium handles customer service and refunds through Stripe. Fulfilment stays with artists.
- Ticket sales and RSVPs, including free events, run on the external ticketing platform. Aesium's event pages embed its checkout and show ticket and attendee counts from it; events sold elsewhere carry a plain link.
- Search uses PostgreSQL full-text search with accent-insensitive matching. A dedicated search engine is a later option.
- The application runs in ap-southeast-6 (Auckland) if ECS, RDS and the supporting services are available there at kick-off; otherwise in ap-southeast-2 (Sydney) with a documented migration path.
- Production runs across two availability zones from launch, as described in Section 4.4.
- Self-hosted audio does not go live until Aesium confirms it holds the licences described in Section 8.4. The build proceeds regardless; only public playback is gated. Licensing is outside this Statement of Work.
- Browser support: the current and previous major versions of Chrome, Safari, Firefox and Edge; iOS 16 and later; Android 11 and later.
- The interface is in English. Content can be in any language, including te reo Māori, and search treats macronised and unmacronised spellings as equivalent.
- All prices exclude GST. Hours are estimates; the Supplier bears any overrun within agreed scope (Section 11).
- Hosting figures are estimates from published pricing and are not a quote from the providers. Aesium is billed directly by each provider.

## 10. Client responsibilities

- Name one decision-maker with authority to approve scope, designs and releases.
- Attend the discovery workshops, answer decisions and review requests within three business days, and complete acceptance testing within ten business days of each phase release.
- Supply content, artwork, audio, video links, copy and the approved genre list by the dates agreed at kick-off, and enter content through the platform once the relevant templates are live. The Supplier imports the initial set only (work package 22).
- Open the third-party accounts listed in Section 8.4, including a GitHub organisation that holds the code, and grant the Supplier access.
- Provide legal documents and confirm licensing and rights positions. Licensing is outside this Statement of Work.
- Coordinate artists: Stripe Connect onboarding for each artist who will be paid through the shop, and event set-up on the ticketing platform.
- Provide two to four staff members for training and acceptance testing.

## 11. Commercial terms

- **Engagement.** Fixed price per phase based on the hours in Section 5. The Supplier bears any overrun in delivering the agreed scope of a phase; the Client is never invoiced for hours beyond the fixed price.
- **Change control.** Any change to scope, sequence or acceptance criteria while a phase is in motion is raised as a written change request by either party. The Supplier responds within three business days with the hours, price, schedule effect and any new dependency. No change is built until the Client approves the change request in writing. Approved changes are priced at the hourly rate and invoiced with the next milestone, or drawn from the contingency reserve if the Client prefers.
- **Contingency reserve.** The 10% reserve in Section 8.1 is held for approved change requests only. It is invoiced only as used, and any unused balance is never charged.
- **Payment schedule.** Phase 1: 20% on signing, 40% at beta (M2) and 40% at release (M3). Phases 2 and 3: 50% at beta and 50% at release. Invoices are due within 14 days. GST is added to every invoice. Overdue amounts accrue interest at 1% per month, and the Supplier may pause work on written notice once an invoice is 14 days overdue.
- **Acceptance.** Each phase release is accepted when the acceptance criteria in Section 2 and the work package descriptions are met, or ten business days after release if no material defects are reported.
- **Defects and warranty.** Defects found during acceptance are fixed at no charge. Each phase carries a 30-day warranty from its production release for defects in the delivered work.
- **Maintenance.** After the warranty period for each phase, maintenance is provided at the same rate of NZD 150 per hour excluding GST, billed monthly in arrears against a log of hours, with no minimum. Maintenance covers keeping the platform current and secure: dependency and framework updates, security patches, monitoring and backup checks including a quarterly restore rehearsal, and fixes for defects found after the warranty. Four to eight hours a month is typical for a platform of this size; larger updates such as a major .NET or SvelteKit release are estimated in advance. New features are not maintenance and go through change control. Response targets: a production outage or failed payments within one business day; anything else within three business days. A fixed monthly retainer can be agreed instead if Aesium prefers a predictable cost.
- **Intellectual property.** Aesium owns the platform code, design and content on payment of each phase. Code is committed to Aesium's GitHub organisation from the first day and stays there. The Supplier retains ownership of pre-existing tools, libraries and generic components and grants Aesium a perpetual, royalty-free licence to use them within the platform. Open-source components remain under their own licences.
- **Third-party services.** Aesium contracts directly with AWS, Cloudflare, Stripe, the ticketing platform, SoundCloud, YouTube, Auth0 (Option C), Plausible and any other provider, and is bound by their terms.
- **Confidentiality.** Both parties keep the other's non-public information confidential during and after the engagement.
- **Subcontracting.** The Supplier performs the work personally and engages others only with Aesium's written consent, remaining responsible for their work.
- **Termination.** Either party may end the engagement on 30 days' written notice. The Client pays for work completed to the date of termination, pro rata against the milestones, and the Supplier hands over the code, documentation and all account access on payment. Either party may end the engagement immediately if the other commits a material breach that is not remedied within 14 days of written notice, or becomes insolvent.
- **Liability.** Neither party is liable to the other for indirect or consequential loss, including loss of profit or revenue. Each party's total liability under this Statement of Work is limited to the fees paid or payable for the phase in which the claim arises. These limits do not apply to breach of confidentiality, infringement of the other party's intellectual property, fraud, or any liability that cannot be limited by law. Both parties are in trade and agree that the Consumer Guarantees Act 1993 does not apply.
- **Force majeure.** Neither party is liable for delay caused by events beyond its reasonable control, provided it tells the other promptly and works to limit the effect.
- **Disputes.** The named decision-makers meet within ten business days of a written notice of dispute. If the dispute is unresolved after a further ten business days, the parties attempt mediation in New Zealand before any court proceedings, except where urgent relief is needed.
- **Governing law.** New Zealand law and New Zealand courts.
- **Whole agreement.** This Statement of Work is incorporated into a short-form services agreement in standard New Zealand form, signed by both parties before kick-off. Where the two conflict on scope, price or schedule, this Statement of Work prevails; on all other matters the services agreement prevails. Changes to either are made in writing and signed by both parties.

## 12. Decisions

### 12.1 Required before kick-off

| Decision | Options | Affects |
|---|---|---|
| Audio hosting | Base (self-hosted) or Option A (SoundCloud); whether to keep both | Work packages 9 and 10, running cost |
| Video hosting | Base (Cloudflare Stream), Option B (YouTube), or Vimeo | Work package 11, running cost, advertising exposure |
| Authentication | Base (ASP.NET Core Identity) or Option C (Auth0) | Work package 3, running cost, where account data lives |
| Ticketing platform | Humanitix (assumed) or Eventbrite | Work package 18, booking fees |
| Commerce platform | Base (custom shop on Stripe Connect) or Option D (Shopify Collective) | Work package 20, the stretch package, running cost, artists' own Shopify plans |
| Physical goods stretch package | Take up in Phase 3, defer, or leave out | Section 5.2, Phase 3 duration |
| Music licence position | Confirmed by Aesium before self-hosted audio goes live; outside this Statement of Work | Phase 1 launch content |
| Admin visibility of audience activity | Aggregates only, or per-user detail | Work packages 17 and 19, privacy policy |
| Hosting region | Auckland if fully available, otherwise Sydney | Work package 2 |

### 12.2 Settled in the discovery workshops (work package 1)

Time for these is allocated in work package 1, and each decision is recorded in the decision log.

| Decision | What is settled | Affects |
|---|---|---|
| Genre list | Initial list, granularity, and who controls it | Work package 7, search, related artists |
| Artist profiles | Required fields before publishing; related-artist rules (genre only, or genre plus collective and series links); when the grouped presentation is used | Work package 12 |
| Player | Whether volume and mute persist across visits; mobile behaviour where the device restricts volume control | Work package 10 |
| Submissions | Fields and files the form accepts, and what populates a draft record | Work package 19 |
| Cart | Drawer or page; whether a signed-in shopper's cart is kept across visits | Work package 20 |
| Analytics | Which events are tracked, including genre filter and search use; who receives the monthly summary | Work package 16 |
| Store specifics, at the start of Phase 3 | Merchant of record, GST treatment, refund and customer-service responsibility, and the default commission, with Aesium's accountant | Work package 20 and Section 5.2 |

## Appendix A. Detailed hour breakdown

| Work package | Item | Hours |
|---|---|---|
| 1. Discovery, decisions & design mock-ups | Decision workshops for Section 12.2, written decision log | 12 |
| 1. Discovery, decisions & design mock-ups | Wireframes and visual mock-ups for screens the concept does not cover: Now Playing bar and full-view player, volume control, cart drawer and checkout hand-off, account area and library, admin back office and edit-in-place controls, submission form, genre pages, event page with embedded ticketing, email templates; two review rounds each | 24 |
| 2. Platform foundations & infrastructure | Repository in Aesium's GitHub organisation, solution structure, environments, CI/CD pipelines | 8 |
| 2. Platform foundations & infrastructure | AWS via CDK: ECS service across two availability zones, Multi-AZ RDS PostgreSQL with point-in-time recovery, Secrets Manager, container registry, load balancer, TLS | 16 |
| 2. Platform foundations & infrastructure | Cloudflare: Pages project, R2 buckets and custom domains, image transformations, DNS, basic firewall rules | 6 |
| 2. Platform foundations & infrastructure | Logging, error tracking, uptime alerts | 4 |
| 3. Accounts & permissions | Staff sign-in, Administrator and Editor roles, two-factor, password reset | 10 |
| 3. Accounts & permissions | Audience registration, sign-in, password reset, profile, account deletion and data export | 14 |
| 3. Accounts & permissions | Authorisation policies and session handling across API and front end | 6 |
| 4. Content model & edit-in-place | Data model and migrations for every content type and relationship | 12 |
| 4. Content model & edit-in-place | Edit-in-place framework: inline text, rich text, artwork slots, relationship pickers, autosave, validation, required-field rules | 30 |
| 4. Content model & edit-in-place | Slugs, page metadata, social sharing cards | 6 |
| 5. Credits & rights metadata | Collaborator records (writer, photographer, filmmaker, producer, designer) with roles on any content item; credits shown on public pages | 6 |
| 5. Credits & rights metadata | Rights holder, licence terms and cleared uses on assets and content items; archive export | 6 |
| 6. Publishing workflow | Publishing states on every type, scheduler job, preview links, publish event hooks | 12 |
| 7. Tagging & classification | Genre list management, multi-select, fixed classifications, filters, genre pages | 8 |
| 8. Media assets | Direct-to-R2 upload, asset records, responsive variants, alt text, media library, reuse, orphan clean-up | 16 |
| 9. Audio hosting & delivery | Multipart upload, processing job (duration, waveform peaks, streaming rendition), expiring delivery URLs, publish-state enforcement, play counting | 20 |
| 10. Audio player | Persistent Now Playing bar, full-view player, immediate switching, seek, volume and mute, lock-screen and keyboard controls, session state | 24 |
| 11. Video hosting & playback | Direct upload to Cloudflare Stream, processing webhooks, branded player, thumbnails, view counts | 12 |
| 11. Video hosting & playback | Caption track upload in the admin and display in the player | 2 |
| 12. Content types & pages | Content types and pages, as itemised in Section 5.1 | 102 |
| 13. Search & discovery | Full-text search across content with accent-insensitive matching, results page, genre filtering, related content | 10 |
| 14. Design system & front-end build | Design tokens, typography, component library, responsive layouts, dark mode, accessibility (WCAG 2.1 AA), motion | 28 |
| 15. Email deliverability & SEO | Sending domain in SES, DKIM, SPF and DMARC records, production access, bounce and complaint handling into a suppression list, one-click unsubscribe headers | 8 |
| 15. Email deliverability & SEO | Sitemap, robots, canonical URLs, structured data for artists, mixes, articles, events and products | 6 |
| 16. Analytics & reporting | Plausible set-up and platform event recording | 6 |
| 16. Analytics & reporting | Reporting views mapped to the Operating Model's measures, date ranges, CSV export | 8 |
| 16. Analytics & reporting | Monthly summary email to staff | 2 |
| 17. Audience activity & notifications | Follow, like, save, private library, aggregate follower counts | 10 |
| 17. Audience activity & notifications | Notification preferences, publish-triggered emails to followers, email templates, sent log | 14 |
| 18. Ticketing integration | Ticketing platform account link, event records linked to ticketed events, embedded checkout on event pages | 8 |
| 18. Ticketing integration | Sync of tickets sold and attendees into reporting (Humanitix's API is read-only with no webhooks, so counts are polled; Eventbrite sends webhooks), free-event RSVP through the same platform, plain-link fallback for events sold elsewhere | 8 |
| 19. Admin back office & submissions | Dashboard, content lists with status filters, staff management, settings, audit log | 16 |
| 19. Admin back office & submissions | Structured submission form with genre nomination, review queue, conversion to a draft record | 10 |
| 20. Commerce & payments | Cart drawer and badge, guest checkout, Stripe Checkout, order and payment records, webhooks, order emails | 18 |
| 20. Commerce & payments | Stripe Connect onboarding for artists, commission rate per artist with per-product override, refunds, admin order and payout views, reconciliation export | 22 |
| 21. Quality, security & performance | API and end-to-end test suites, performance tuning, security review, privacy checks, load test | 28 |
| 22. Launch & handover | Content import, staff training, documentation, go-live checklist, two weeks of hypercare | 16 |
| 23. Project management & communication | Project management and communication | 48 |
| Total | | 622 |

## Appendix B. Changes from version 1.0

- Editorial moved into Phase 1 so that guest spots launch with their write-ups. Phases renamed and mapped to the Operating Model's roadmap, with each phase committable separately.
- New work packages: discovery, decisions and design mock-ups (1); credits and rights metadata (5); email deliverability and SEO (15); ticketing integration (18). Work packages renumbered.
- Analytics expanded into reporting views mapped to the Operating Model's measures. Caption tracks added to the branded video player. Commission rate per artist with per-product override added to commerce.
- Physical goods commerce priced as a separate stretch package.
- Production moved to two availability zones with a Multi-AZ database and point-in-time recovery; running costs updated.
- Authentication added as Option C with an Auth0 comparison and later-migration cost. Shopify assessed against Aesium's criteria for a commerce platform, with Shopify Collective priced as Option D.
- SoundCloud licensing wording corrected, and the two-hour upload limit on free SoundCloud accounts noted.
- Lead-time dependencies listed. Content entry stated as staff work. Licensing of any kind stated as outside scope.
- Commercial terms expanded: change control, contingency use, payment split, maintenance at the same hourly rate, termination, liability, subcontracting, force majeure and disputes.
- Base configuration hours from 522 to 622; price from NZD 78,300 to NZD 93,300.
