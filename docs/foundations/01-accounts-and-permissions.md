# 01 · Accounts & Permissions

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Audience account area, Artist Profiles (follow), Mixes and Videos (like/save), Shop (optional account-linked cart), Admin / Back Office (all staff tasks) |
| **Source** | §1, §14, §16, §20, §22, §24 |

## Purpose

One identity layer for the two kinds of people who log in: audience members (free, public-facing) and Aesium staff (back office). Artists do not have accounts in V1. Aesium receives artist deliverables and manages profiles on their behalf.

## Account types

### Audience user

- Free. Membership / paid access was investigated and confirmed out of scope for V1.
- Registration, login, password recovery.
- Private account area / library (follows, likes, saves).
- Notification preferences.
- All activity is private. Only aggregate follower counts are public.
- Guest checkout in the Shop must work without an account.

### Staff / administrator

Access to the Admin / Back Office. Price the roles against the real workflow, not a large organisation. Possible roles:

| Role | Potential access |
|---|---|
| Administrator | Full platform, content and settings |
| Content / Editorial | Content, artists, Series, publishing, media |
| Events | Events, ticketing / RSVP information, event content |
| Commerce | Products, sales / reporting, commerce information |
| Contributor | Limited content creation / editing, no wider access |

One Administrator role may be enough for V1.

### Artist (not in V1)

Artists supply content and changes to Aesium; they do not log in. Future self-service would need artist accounts, permissions and a new workflow.

## What it must provide (V1)

- Authentication for audience and for staff. These can be separate systems (managed auth provider for the audience, CMS built-in auth for staff).
- Password recovery.
- Sessions that let the persistent player and cart keep working while browsing.
- A clear definition of what administrators can and cannot see of audience activity.
- NZ Privacy Act 2020 compliance for audience account and activity data.

## Data it owns

- Audience user: id, email, display name, auth-provider reference, created date, notification preferences.
- Staff user: id, email, name, role.

## Depends on

- Hosting & Infrastructure (auth provider, database).
- Admin / Back Office (role enforcement).

## Build options

| Option | Meaning | Implication |
|---|---|---|
| Managed authentication provider (Auth0, Clerk, Supabase) | Provider handles accounts and authentication | Less security work; provider dependency. Treated as the more established approach. |
| Custom authentication | Build accounts and auth directly | More control; materially more security and maintenance responsibility. |

## Later

- Artist self-service accounts.
- Account-linked playback and volume preferences.
- Cart persistence across devices tied to the account.

## Open questions

- Preferred authentication provider.
- Exact admin visibility into audience activity.
- Is one admin role enough for V1, or does access need separating?
- How many Aesium staff will use the system?
