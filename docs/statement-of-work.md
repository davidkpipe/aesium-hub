# Aesium Platform Statement of Work

*Design, build and launch of Version 1 of the Aesium platform on .NET, SvelteKit and PostgreSQL, hosted on AWS with media on Cloudflare R2, with priced options for SoundCloud audio hosting and YouTube video.*

| | |
|---|---|
| **Client** | Aesium |
| **Supplier** | David Pipe |
| **Version** | 1.0, 23 September 2026, draft for review |
| **Basis** | *Aesium Platform Requirements & Build Options* and the derived working documents in `docs/` (foundations, content types, entity model) |
| **Currency** | Build pricing in NZD excluding GST. Hosting and service costs in USD unless stated. |

## 1. Overview

This Statement of Work covers the design, build, hosting set-up and launch of Version 1 of the Aesium platform: a New Zealand cultural platform for DJ mixes, artists, series, editorial, video, events and an artist shop.

It sets out scope, the technical approach, deliverables with hour estimates, the delivery plan, two hosting options for audio and video with their trade-offs, build pricing, monthly running costs, assumptions, and commercial terms.

The build is a custom platform rather than a configured content management product. Staff edit pages in place on the live templates; the database record is the source of truth and the page templates are code. This keeps the editing experience close to the audience experience and avoids a second administration system.

## 2. Objectives

- Launch a fast, branded platform where audiences discover artists, listen to mixes without interruption while browsing, and follow the artists they care about.
- Give Aesium staff one place to manage every record and the relationships between records, editing pages directly.
- Keep running costs low and predictable for a New Zealand audience.
- Leave a clean foundation for later phases (membership, artist self-service, recommendations) without a rebuild.

Success criteria at launch:

- Every V1 content type can be created, connected, scheduled, published and unpublished by staff without developer help.
- Playback continues across page navigation on desktop and mobile.
- Public pages reach a Lighthouse performance score of 90 or better on mobile, with Largest Contentful Paint under 2.0 seconds on a typical New Zealand 4G connection.
- Public pages meet WCAG 2.1 AA.
- Staging and production are reproducible from code, with automated deploys and nightly database backups.

## 3. Scope

### 3.1 In scope (Version 1)

Shared foundations, built once and used across every feature:

| # | Foundation | V1 scope |
|---|---|---|
| 01 | Accounts & permissions | Free audience accounts; staff sign-in with roles. Artists do not log in. |
| 02 | CMS & content model | Records, relationships and the shared hub-page pattern for artist profiles and series; edit-in-place editing. |
| 03 | Publishing workflow | Draft, scheduled, published, unpublished; scheduler; featured and homepage placement. |
| 04 | Tagging & classification | Managed genre list with multi-select on mixes; fixed classifications kept per area. |
| 05 | Media assets | Image upload, storage, responsive variants, alt text, reuse across records. |
| 06 | Audio hosting | Upload or connect mix audio; deliver it to the player; respect publishing state. |
| 07 | Audio player | Persistent Now Playing bar, full-view player, immediate switching, volume and mute. |
| 08 | Video hosting | Upload or connect video; branded playback; thumbnails; view counts. |
| 09 | Audience activity | Follow, like, save; private library; public aggregate follower counts. |
| 10 | Notifications | Preferences and email updates when a followed artist publishes. |
| 11 | Commerce & cart | Products with artist attribution; cart; guest checkout hand-off. |
| 12 | Payments | Card processing, refunds, transaction records, automatic Aesium and artist split. |
| 13 | Admin back office | Dashboard, content lists, staff, settings, genre list, featured slots. |
| 14 | Content submission | Structured public submission form with genre nomination and staff review. |
| 15 | Search & discovery | Keyword search across content including genre; genre filtering and genre pages. |
| 16 | Analytics | Web analytics, plays, views, follows, shop activity, admin performance views. |
| 17 | Hosting & infrastructure | AWS application and database, Cloudflare front end and media, backups, monitoring. |

Content types and pages: Artist profiles, Mixes, Series, Editorial articles, Videos, Events, Products and Shop, Homepage with curated placements, audience account area, and static pages (About, Contact, Privacy, Terms).

### 3.2 Out of scope

- Membership or paywall. Audience accounts stay free.
- Artist self-service accounts and artist-facing analytics.
- Queue, playlist and autoplay; resuming playback or cart across visits.
- Tagging beyond genre on mixes (mood, BPM, region) and recommendations.
- Aesium-hosted ticket checkout for events. V1 links to external ticketing and supports free RSVP.
- Native mobile apps.
- Content production: copywriting, photography, video production, audio mastering, artwork.
- Legal documents (privacy policy, terms of use, artist agreements), music licensing negotiations and accounting set-up.
- Migration of historical content beyond the initial import in work package 18.
- Ongoing support and maintenance after the warranty period. This is available under a separate support agreement.

## 4. Technical approach

### 4.1 Stack

| Layer | Choice | Reason |
|---|---|---|
| Back end | .NET 10 (ASP.NET Core minimal APIs), Entity Framework Core | Long-term support release; strongly typed; runs well in a small container. |
| Database | PostgreSQL 17 on Amazon RDS | Relational model fits the content graph; JSONB for flexible fields; built-in full-text search covers V1. |
| Front end | SvelteKit on Svelte 5 | Client-side navigation keeps the player alive between pages; server rendering for search engines and sharing; small bundles. |
| Front-end hosting | Cloudflare Pages | Edge delivery with New Zealand points of presence; generous free tier. |
| Application hosting | Amazon ECS Express Mode on Fargate, ap-southeast-6 (Auckland) with ap-southeast-2 (Sydney) as fallback | Managed containers, nothing to patch, data stays in New Zealand where the region supports every service. |
| Media storage | Cloudflare R2 | No egress fees; S3-compatible API; served through Cloudflare's CDN on an Aesium domain. |
| Images | Cloudflare Image Transformations | Responsive variants generated on demand from the original. |
| Audio (base) | Self-hosted on R2 with a custom player | Full control over the listening experience. See Option A. |
| Video (base) | Cloudflare Stream | Branded player and adaptive streaming inside the same Cloudflare account. See Option B. |
| Editing | Edit-in-place on rendered templates; TipTap for rich text | The page is the editor. Templates are code; records are data. |
| Authentication | ASP.NET Core Identity for staff and audience; email sign-in; two-factor for staff | No per-user fees; can be swapped for a managed provider later without changing the data model. |
| Background jobs | Hangfire | Scheduled publishing, media processing, notification sending. |
| Payments | Stripe Checkout and Stripe Connect | Supported in New Zealand; automatic split between Aesium and artist accounts. |
| Email | Amazon SES | Transactional and notification email at very low cost. |
| Analytics | Plausible | Privacy-friendly and cookie-free, which simplifies NZ Privacy Act compliance. |
| Infrastructure as code | AWS CDK; GitHub Actions | Staging and production defined in code; automated test and deploy on every change. |

### 4.2 Editing model

Staff sign in and switch any page into edit mode. Text, rich text, artwork slots, dates and classifications become editable where they sit on the page. Relationships (artist on a mix, episodes in a series, videos on an event) are set through pickers that search existing records. Changes save automatically as a draft; a publishing bar shows status and offers schedule, publish and unpublish. A back office covers what does not belong on a page: content lists with filters, the genre list, featured slots, staff, submissions, orders and settings.

### 4.3 Player architecture

The audio player is written against a small provider interface (load, play, pause, seek, volume, progress events). The self-hosted provider and the SoundCloud provider both implement it, so the hosting decision in Option A changes the provider, not the site. The same pattern applies to video.

### 4.4 Environments and delivery

- Staging and production, each with its own database, buckets and secrets.
- Preview deployments of the front end for every change under review.
- Nightly automated database backups with 14-day retention; media buckets versioned.
- Uptime monitoring, error tracking and log retention of 30 days.

## 5. Deliverables and hour estimates

Hours are estimates of the effort to deliver working, tested functionality using the Supplier's delivery approach, which leans heavily on generated scaffolding, reusable components and automated testing. Each work package includes its own automated tests and short technical notes. A detailed breakdown is in Appendix A.

| Work package | What it delivers | Hours | Phase |
|---|---|---|---|
| 1. Platform foundations & infrastructure | Repositories, CI/CD, staging and production on AWS via CDK, Cloudflare set-up, logging and alerts | 32 | 1 |
| 2. Accounts & permissions | Staff sign-in with roles and two-factor; audience registration, sign-in, recovery, profile, deletion and data export | 30 | 1, 2 |
| 3. Content model & edit-in-place | Data model for every record and relationship; inline editing framework on rendered pages; slugs and SEO metadata | 48 | 1 |
| 4. Publishing workflow | Draft, scheduled, published, unpublished on every type; scheduler; preview links; publish hooks | 12 | 1 |
| 5. Tagging & classification | Managed genre list, multi-select, fixed classifications, filters, genre pages | 8 | 1 |
| 6. Media assets | Direct-to-R2 upload, responsive variants, alt text, media library, reuse, clean-up | 16 | 1 |
| 7. Audio hosting & delivery | Large-file upload, processing, waveform, delivery, play counting (base: self-hosted on R2) | 20 | 1 |
| 8. Audio player | Persistent Now Playing bar, full-view player, immediate switching, volume and mute, lock-screen controls | 24 | 1 |
| 9. Video hosting & playback | Upload, processing, branded player, thumbnails, view counts (base: Cloudflare Stream) | 12 | 2 |
| 10. Content types & pages | Templates and behaviours for every content type, homepage placements, account area, static pages | 104 | 1, 2, 3 |
| 11. Audience activity & notifications | Follow, like, save, private library, follower counts; preferences; publish-triggered email | 24 | 2 |
| 12. Commerce & payments | Cart, guest checkout, Stripe Checkout, Stripe Connect split, refunds, orders, reporting | 36 | 3 |
| 13. Admin back office & submissions | Dashboard, content lists, staff, settings, audit log; submission form and review queue | 26 | 2 |
| 14. Search & discovery | Full-text search, results page, genre filtering, related content | 10 | 1 |
| 15. Analytics | Web analytics, custom events, admin performance views | 8 | 1 |
| 16. Design system & front-end build | Tokens, typography, components, responsive layouts, dark mode, accessibility | 28 | 1 |
| 17. Quality, security & performance | End-to-end tests, performance tuning, security and privacy review, load test | 28 | 1, 2, 3 |
| 18. Launch & handover | Content import, staff training, documentation, go-live, two weeks of hypercare | 16 | 1, 2, 3 |
| Subtotal, build | | 482 | |
| 19. Project management & communication | Planning, weekly reviews and demos, decision log, reporting | 40 | All |
| Total | | 522 | |

Content types and pages (work package 10) in detail:

| Page or content type | Included | Hours |
|---|---|---|
| Artist profiles | Hub page pattern, Experiences grid and filters, related artists from shared genres, follow button and follower count, external links, releases, grouped presentation for artists with little content | 18 |
| Mixes | Listing with genre filter, detail page, tracklist, credits, series episode display, like and save | 14 |
| Series | Hub page reuse, episode ordering, collected videos, articles, products and links | 12 |
| Editorial articles | Rich text layout, images, pull quote, "In Their Words" section on profiles | 12 |
| Videos | Listing, detail page, video categories, artist, series and event links, like and save | 8 |
| Events | Upcoming and Past, Next Up, venue, ticket link or RSVP, recordings | 12 |
| Products and Shop | Listing, detail page, shop categories, artist attribution, series placement | 12 |
| Homepage & featured placements | Curated slots with ordering and start and end dates, latest and featured content | 12 |
| Static pages, navigation and footer | About, Contact, Privacy, Terms; header, footer, cart icon | 4 |
| Total | | 104 |

## 6. Delivery plan

The build is delivered in three phases. Each phase ends with a working, deployable release that Aesium can put in front of real users.

| Phase | Focus | Build hours | PM hours | Total hours | Duration |
|---|---|---|---|---|---|
| 1. Discover & listen | Infrastructure, staff accounts, content model and editing, publishing, genres, media, audio, player, artist profiles, mixes, series, homepage, static pages, search, analytics, design system | 304 | 24 | 328 | 10 to 11 weeks |
| 2. Audience & editorial | Audience accounts, follow, like and save, notifications, editorial, video, events, admin dashboard, submissions | 120 | 10 | 130 | 4 weeks |
| 3. Shop & payments | Products, cart, checkout, Stripe Connect, orders, refunds, reporting | 58 | 6 | 64 | 2 to 3 weeks |
| Total | | 482 | 40 | 522 | 16 to 18 weeks |

Milestones:

| Milestone | Week | Evidence |
|---|---|---|
| M0 Kick-off | 0 | Decisions in Section 12 confirmed; accounts and access in place |
| M1 Foundations | 3 | Staging live on AWS; staff sign-in; content model migrated; edit-in-place working on the artist template |
| M2 Phase 1 beta | 8 | Artists, mixes, series, homepage, player and search working end to end on staging with real content |
| M3 Phase 1 launch | 11 | Production live; hypercare begins |
| M4 Phase 2 release | 15 | Audience accounts, follow, notifications, editorial, video, events, submissions live |
| M5 Phase 3 release | 18 | Shop and payments live; reconciliation report available |
| M6 Handover | 18 | Documentation, training and warranty start |

Durations assume decisions and content arrive when needed and a delivery cadence of roughly 30 hours per week on the project.

## 7. Hosting options for audio and video

Two decisions from the requirements (§24) shape the product, the build and the running cost: where mix audio lives, and where video lives. The base configuration keeps both under Aesium's control. Each option below swaps a provider, describes what changes in the interface, lists the downsides, and prices the difference.

### 7.1 Audio: self-hosted on R2 (base) or SoundCloud (Option A)

| | Base: self-hosted on R2 | Option A: SoundCloud |
|---|---|---|
| Where audio lives | Aesium's R2 bucket, served on an Aesium domain | SoundCloud, on Aesium's account or the artist's own account |
| How staff add a mix | Upload the file on the mix page; processing runs in the background | Upload on soundcloud.com, then paste the track link on the mix page |
| Player | Fully custom bar and full-view player | Custom bar controlling a SoundCloud widget that must remain visible |
| Licensing | Aesium's responsibility; online licences from APRA AMCOS and Recorded Music NZ must be in place before launch | Covered by SoundCloud's platform licences under its terms; Aesium should still confirm its position |
| Play analytics | In Aesium's database and reports | On SoundCloud; Aesium records play starts only |
| Build hours | 20 (work package 7, audio hosting) + 24 (work package 8, audio player) | 14 (SoundCloud integration) + 30 (work package 8 with the widget adapter). Net change: 0 |
| Monthly cost | R2 storage about USD 1 to 3; music licences from about NZD 510 a year on the published small-service tariffs, otherwise quoted | Artist Pro plan USD 99 a year (NZD 135 when bought from New Zealand), or free on artists' accounts |

Interface changes with Option A:

- The Now Playing bar carries a compact SoundCloud widget. SoundCloud's terms require its player and branding to stay visible and unobscured, so the bar shows a slim SoundCloud strip (track link, logo) alongside Aesium's own play, pause, progress and volume controls, which drive the widget through its API.
- Artwork, waveform and duration come from SoundCloud. The full-view player shows SoundCloud's waveform rather than a custom one.
- Mixes are added by pasting a SoundCloud link. There is no audio upload in Aesium's admin in V1. SoundCloud now issues API credentials to Artist Pro subscribers, so upload from Aesium through SoundCloud's API can be added later (about 8 hours).
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
- Workflow. Every mix is uploaded twice: to SoundCloud, then linked in Aesium.

Upsides of Option A:

- No storage, transcoding or delivery to run. Waveforms and encodes are provided.
- Licensing exposure sits with the platform rather than with Aesium.
- Many artists already publish to SoundCloud, and their existing audiences and play counts carry over.
- Fast path to launch if the OneMusic position is unresolved.

Alternative considered: Mixcloud. It is built for DJ mixes and its licensing for mixes is the most established of the three. Its widget must also stay visible and, for free listeners, restricts seeking within a mix, which conflicts with the required player behaviour. Mixcloud Pro costs USD 11.25 a month on the annual plan (USD 15 monthly). It can be priced as a variant of Option A if Aesium prefers it.

### 7.2 Video: Cloudflare Stream (base) or YouTube (Option B)

| | Base: Cloudflare Stream | Option B: YouTube |
|---|---|---|
| Where video lives | Aesium's Cloudflare account | Aesium's YouTube channel, or the artist's own channel |
| How staff add a video | Upload on the video page; processing runs in the background | Upload in YouTube Studio, then paste the link on the video page |
| Player | Aesium-branded player, adaptive streaming | YouTube's player inside Aesium's page |
| Advertising | None | YouTube may show ads before or during videos |
| View analytics | In Aesium's database and reports | In YouTube Studio; Aesium records play starts, and can pull view counts |
| Build hours | 12 (work package 9, video hosting) | 8 (YouTube integration). Net change: minus 4 |
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

Alternative considered: Vimeo. It gives an ad-free, brandable player with domain-restricted embedding and privacy controls for a fixed subscription (Starter USD 12 a month on the annual plan with 2 TB of storage; Standard USD 25 with 4 TB), with no per-minute charge. It sits between the two options on cost and control and can be substituted for Cloudflare Stream at no change to build hours.

### 7.3 Option combinations

| Configuration | Build hours change | Monthly cost change | Notes |
|---|---|---|---|
| Base: R2 audio, Cloudflare Stream video | 0 | 0 | Full control; music licences required before audio launch |
| Option A only: SoundCloud audio | 0 | plus USD 0 to 8; removes the music licence fees | Player provider swap |
| Option B only: YouTube video | minus 4 | about minus USD 45 at launch volume, more as viewing grows | Provider swap |
| Options A and B | minus 4 | about minus USD 38 at launch; removes the music licence fees | Lowest running cost, least control |
| Base plus SoundCloud adapter kept | plus 20 | 0 | Both audio providers available; mixes can be self-hosted or linked |
| Base plus YouTube adapter kept | plus 8 | 0 | Both video providers available |

Recommendation: keep the base configuration for audio, because the listening experience is the product, and build the SoundCloud adapter (plus 20 hours) so that individual mixes can be linked where licensing or an artist's preference requires it, and so the site can launch on linked audio if the licences are not yet in place. For video, launch with YouTube (Option B) and the click-to-play facade, since the video library is small at launch and advertising exposure is limited to the videos Aesium chooses to embed. Move to Cloudflare Stream when a branded, ad-free experience matters more than the per-minute cost; the provider interface makes that a 12-hour change.

## 8. Pricing

### 8.1 Build

Rate: NZD 150 per hour, excluding GST. This is the assumed rate for this draft and is the only input to the figures below; change the rate and every figure scales.

| Phase | Hours | Price (NZD, ex GST) |
|---|---|---|
| 1. Discover & listen | 328 | 49,200 |
| 2. Audience & editorial | 130 | 19,500 |
| 3. Shop & payments | 64 | 9,600 |
| Total, base configuration | 522 | 78,300 |
| Contingency reserve (10%, drawn only with written approval) | 52 | 7,800 |

Option adjustments to the total:

| Option | Hours | Price (NZD, ex GST) |
|---|---|---|
| Option A: SoundCloud instead of self-hosted audio | 0 | 0 |
| Option B: YouTube instead of Cloudflare Stream | minus 4 | minus 600 |
| SoundCloud adapter kept alongside self-hosting | plus 20 | plus 3,000 |
| YouTube adapter kept alongside Cloudflare Stream | plus 8 | plus 1,200 |
| Recommended configuration (base audio plus SoundCloud adapter, YouTube video) | 538 | 80,700 |

Rate sensitivity for the base configuration (522 hours):

| Rate (NZD per hour) | 120 | 150 | 180 |
|---|---|---|---|
| Total (NZD, ex GST) | 62,640 | 78,300 | 93,960 |

### 8.2 Running costs

Estimated monthly costs at launch volume: about 10,000 page views a month, 300 mixes averaging 150 MB, 60 videos averaging 40 minutes, 2,000 video views a month, 20,000 emails a month, one application container and a single-zone database. Figures are in USD and drawn from the providers' published price lists on 23 September 2026, using the Auckland region (ap-southeast-6), which runs about 10% above Sydney. There is no extra charge for ECS Express Mode.

| Item | Base | Options A and B | Notes |
|---|---|---|---|
| AWS: application container (0.5 vCPU, 1 GB, always on) | 24 | 24 | A second container for redundancy adds about 24 |
| AWS: load balancer | 25 | 25 | Created by ECS Express Mode; billed hourly plus usage |
| AWS: PostgreSQL db.t4g.micro, 20 GB storage, backups | 22 | 22 | Multi-zone standby doubles this |
| AWS: secrets, container registry, logs, data transfer | 7 | 7 | |
| Cloudflare: Workers Paid plan for server rendering | 5 | 5 | Free tier may be enough at launch |
| Cloudflare: R2 storage (about 50 GB) | 1 | 0 | No egress charges; first 10 GB free |
| Cloudflare: image transformations | 3 | 3 | First 5,000 unique transformations free |
| Cloudflare: Stream (2,400 minutes stored, 30,000 minutes watched) | 45 | 0 | Storage prepaid in 1,000-minute blocks; grows with library and viewing |
| SoundCloud Artist Pro (annual plan) | 0 | 8 | USD 99 a year; not needed if mixes stay on artists' own accounts |
| YouTube | 0 | 0 | |
| Plausible Analytics, Starter plan (10,000 page views) | 9 | 9 | 19 at 100,000 page views; Growth plan 14 |
| Amazon SES (20,000 emails) | 2 | 2 | Sydney rate; SES pricing is not yet listed for Auckland |
| Error tracking and uptime monitoring | 0 | 0 | Free tiers at this scale |
| Domain and DNS | 2 | 2 | Annual registration averaged |
| Total per month | about 145 | about 107 | |
| Total per year | about 1,740 | about 1,280 | |

Not included above: music licences for self-hosted streaming (Section 8.4, base configuration only), Stripe processing fees (Section 8.3), and any paid support plans.

Growth scenario, ten times the launch volume (100,000 page views, two containers, a larger database, 30,000 minutes stored and 300,000 minutes watched):

| Configuration | Monthly (USD) | What drives it |
|---|---|---|
| Base | about 630 | Cloudflare Stream is about 70% of the total |
| Options A and B | about 185 | Compute and database; media delivery costs nothing |

### 8.3 Transaction and usage fees

| Fee | Amount | Applies to |
|---|---|---|
| Stripe card processing, New Zealand cards | 2.65% + NZD 0.30 per successful charge (Stripe's Connect page shows 2.7%; confirm at sign-up) | Every shop order |
| Stripe card processing, international cards | 3.5% + NZD 0.30, plus 2% where currency conversion is needed | Orders paid with non-NZ cards |
| Stripe Connect, Aesium sets its own pricing | NZD 2 per connected artist account in any month it is paid, plus 0.25% + NZD 0.25 per payout | Artist share of each order |
| Stripe disputes | NZD 25 per dispute, refunded if won | Chargebacks |
| Amazon SES | USD 0.10 per 1,000 emails | Notification and transactional email |
| Cloudflare R2 | USD 0.015 per GB-month; USD 4.50 per million writes; USD 0.36 per million reads | Media beyond the free tier |
| Cloudflare Stream | USD 5 per 1,000 minutes stored; USD 1 per 1,000 minutes watched | Base video configuration |

### 8.4 Costs outside this Statement of Work

These are the Client's, and are not included in the figures above:

- Music licences for on-demand streaming of mixes (base audio configuration). OneMusic NZ licenses premises, not websites; online use is licensed separately by APRA AMCOS (compositions) and Recorded Music NZ (recordings). APRA AMCOS publishes an Online Mini Licence at NZD 250 to 1,000 a year per category of use for services earning under NZD 12,000 a year; Recorded Music NZ publishes an Audio Webcast Licence at NZD 260 plus GST a year for non-interactive webcasts and quotes on-demand services case by case. Whether an on-demand mix player fits the fixed tariffs or needs a quoted licence must be confirmed with both bodies.
- Rights clearance for video: music synchronisation, footage, likeness, and attendee permissions for filmed events.
- Domain registration, business email, and the Stripe, AWS, Cloudflare, SoundCloud, YouTube and Plausible accounts, which are opened in Aesium's name.
- Legal documents: privacy policy, terms of use, artist agreements, refund policy.
- Accounting and tax advice on the artist money flow and Aesium's commission.
- Paid support plans on any third-party service.

## 9. Assumptions and dependencies

- The existing Aesium mockup and brand (typefaces, palette, layouts) is the design source. No separate design phase is included; each template gets up to two rounds of visual refinement during build.
- One Administrator role and one Editor role are enough for V1. Further roles are a change.
- Artists do not log in. Content arrives through the structured submission form or directly to staff.
- Notifications are email only in V1. Browser push is a later addition.
- The shop is Aesium-managed: products are records in Aesium, orders go through one unified cart and Stripe Checkout, and Stripe Connect splits each order between Aesium and the artist. Aesium handles customer service and refunds through Stripe. Fulfilment stays with artists.
- Events link to external ticketing. Free events can take an RSVP from a signed-in audience member. No Aesium ticket checkout.
- Search uses PostgreSQL full-text search. A dedicated search engine is a later option.
- The application runs in ap-southeast-6 (Auckland) if ECS, RDS and the supporting services are available there at kick-off; otherwise in ap-southeast-2 (Sydney) with a documented migration path.
- Self-hosted audio does not go live until Aesium holds the online music licences described in Section 8.4. The build proceeds regardless; only public playback is gated.
- Browser support: the current and previous major versions of Chrome, Safari, Firefox and Edge; iOS 16 and later; Android 11 and later.
- English only. All prices exclude GST. Hours are estimates; see Section 11 for how variances are handled.
- Hosting figures are estimates from published pricing and are not a quote from the providers. Aesium is billed directly by each provider.

## 10. Client responsibilities

- Name one decision-maker with authority to approve scope, designs and releases.
- Answer decisions and review requests within three business days, and complete acceptance testing within ten business days of each phase release.
- Supply content, artwork, audio, video links, copy and the approved genre list by the dates agreed at kick-off.
- Open the third-party accounts listed in Section 8.4 and grant the Supplier access.
- Provide legal documents and confirm licensing and rights positions.
- Provide two to four staff members for training and acceptance testing.

## 11. Commercial terms

- **Engagement.** Fixed price per phase based on the hours in Section 5. Work outside the described scope is agreed in writing through change control before it starts and priced at the same hourly rate.
- **Payment schedule.** 20% of the Phase 1 price on signing; the balance of each phase in two milestone payments on beta (M2, M4 or M5 equivalent) and on release. Invoices are due within 14 days. GST is added to every invoice.
- **Acceptance.** Each phase release is accepted when the acceptance criteria in Section 2 and the work package descriptions are met, or ten business days after release if no material defects are reported.
- **Defects and warranty.** Defects found during acceptance are fixed at no charge. Each phase carries a 30-day warranty from its production release for defects in the delivered work.
- **Support.** After warranty, support and small improvements are available under a monthly retainer, priced separately.
- **Intellectual property.** Aesium owns the platform code, design and content on payment of each phase. The Supplier retains ownership of pre-existing tools, libraries and generic components and grants Aesium a perpetual, royalty-free licence to use them within the platform.
- **Third-party services.** Aesium contracts directly with AWS, Cloudflare, Stripe, SoundCloud, YouTube, Plausible and any other provider, and is bound by their terms.
- **Confidentiality.** Both parties keep the other's non-public information confidential during and after the engagement.
- **Governing law.** New Zealand.

## 12. Decisions required before kick-off

| Decision | Options | Affects |
|---|---|---|
| Audio hosting | Base (self-hosted) or Option A (SoundCloud); whether to keep both | Work packages 7 and 8, licensing, running cost |
| Video hosting | Base (Cloudflare Stream), Option B (YouTube), or Vimeo | Work package 9, running cost, advertising exposure |
| Music licensing | APRA AMCOS and Recorded Music NZ licences in place before Phase 1 launch, or launch with linked audio | Phase 1 launch content |
| Genre list | Initial list and who controls it | Work package 5, search, related artists |
| Staff roles | Administrator only, or Administrator plus Editor | Work packages 2 and 13 |
| Submissions | Structured public form (assumed) or manual entry only | Work package 13 |
| Commerce model | Aesium-managed products with unified cart and Stripe Connect (assumed) | Work package 12 |
| Events | External ticketing plus free RSVP (assumed) | Work package 10 |
| Admin visibility of audience activity | Aggregates only, or per-user detail | Work packages 11 and 13, privacy policy |
| Hosting region | Auckland if fully available, otherwise Sydney | Work package 1 |
| Hourly rate and payment schedule | Confirm the figures in Sections 8 and 11 | Pricing |

## Appendix A. Detailed hour breakdown

| Work package | Item | Hours |
|---|---|---|
| 1. Platform foundations & infrastructure | Repository, solution structure, environments, CI/CD pipelines | 8 |
| 1. Platform foundations & infrastructure | AWS via CDK: ECS Express Mode service, RDS PostgreSQL, Secrets Manager, container registry, load balancer, TLS, backups | 14 |
| 1. Platform foundations & infrastructure | Cloudflare: Pages project, R2 buckets and custom domains, image transformations, DNS, basic firewall rules | 6 |
| 1. Platform foundations & infrastructure | Logging, error tracking, uptime alerts | 4 |
| 2. Accounts & permissions | Staff sign-in, roles, two-factor, password reset | 10 |
| 2. Accounts & permissions | Audience registration, sign-in, password reset, profile, account deletion and data export | 14 |
| 2. Accounts & permissions | Authorisation policies and session handling across API and front end | 6 |
| 3. Content model & edit-in-place | Data model and migrations for every content type and relationship | 12 |
| 3. Content model & edit-in-place | Edit-in-place framework: inline text, rich text, artwork slots, relationship pickers, autosave, validation, required-field rules | 30 |
| 3. Content model & edit-in-place | Slugs, SEO metadata, social sharing cards | 6 |
| 4. Publishing workflow | Publishing states on every type, scheduler job, preview links, publish event hooks | 12 |
| 5. Tagging & classification | Genre list management, multi-select, fixed classifications, filters, genre pages | 8 |
| 6. Media assets | Direct-to-R2 upload, asset records, responsive variants, alt text, media library, reuse, orphan clean-up | 16 |
| 7. Audio hosting & delivery | Multipart upload, processing job (duration, waveform peaks, streaming rendition), delivery URLs, publish-state enforcement, play counting | 20 |
| 8. Audio player | Persistent Now Playing bar, full-view player, immediate switching, seek, volume and mute, lock-screen and keyboard controls, session state | 24 |
| 9. Video hosting & playback | Direct upload to Cloudflare Stream, processing webhooks, branded player, thumbnails, view counts | 12 |
| 10. Content types & pages | Content types and pages, as itemised in Section 5 | 104 |
| 11. Audience activity & notifications | Follow, like, save, private library, aggregate follower counts | 10 |
| 11. Audience activity & notifications | Notification preferences, publish-triggered emails to followers, email templates, sent log | 14 |
| 12. Commerce & payments | Cart drawer and badge, guest checkout, Stripe Checkout, order and payment records, webhooks, order emails | 18 |
| 12. Commerce & payments | Stripe Connect onboarding for artists, commission split, refunds, admin order and payout views, reconciliation export | 18 |
| 13. Admin back office & submissions | Dashboard, content lists with status filters, staff management, settings, audit log | 16 |
| 13. Admin back office & submissions | Structured submission form with genre nomination, review queue, conversion to a draft record | 10 |
| 14. Search & discovery | Full-text search across content, results page, genre filtering, related content | 10 |
| 15. Analytics | Web analytics, custom events (plays, views, follows, cart), admin performance views | 8 |
| 16. Design system & front-end build | Design tokens, typography, component library, responsive layouts, dark mode, accessibility (WCAG 2.1 AA), motion | 28 |
| 17. Quality, security & performance | API and end-to-end test suites, performance tuning, security review, privacy checks, load test | 28 |
| 18. Launch & handover | Content import, staff training, documentation, go-live checklist, two weeks of hypercare | 16 |
| 19. Project management & communication | Project management and communication | 40 |
| Total | | 522 |
