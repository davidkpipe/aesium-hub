# Events

| | |
|---|---|
| **Type** | Content type |
| **Foundations required (V1)** | CMS & Content Model, Publishing Workflow, Media Assets, Admin, Search, Analytics |
| **Foundations optional** | Commerce & Payments (only if Aesium hosts checkout or RSVP), Video (recordings), Accounts (RSVP), Notifications |
| **Source** | §11, §2, §15 |

## What it is

Upcoming and Past event listings with a featured "Next Up" event. Cards show date, venue, artists and a ticket / RSVP action. Events connect to artists and Series; recordings connect back into the content system afterwards.

## Record

- Title, slug, description, artwork.
- Start / end date-time, venue.
- Action: external ticket link, Aesium RSVP, or Aesium checkout, with destination.
- Publish status. Upcoming / Past derived from dates.

## Relationships

- Artists (many-to-many), Series (optional).
- Event recordings (videos).
- RSVPs or ticket orders, if Aesium hosts them.

## V1 behaviours

- Create / edit / publish; automatic upcoming / past.
- Ticket / RSVP destination or integration.
- Shown on relevant Artist and Series pages.

## Build options

| Option | Meaning | Implication |
|---|---|---|
| External ticketing / RSVP | Third party handles checkout; Aesium links to it | Less build; external dependency and fees |
| Aesium-hosted checkout | Aesium manages the transaction with a payment provider such as Stripe | More control and integration; more operational responsibility |
| Hybrid | External ticketing for paid events, Aesium RSVP for free events | Flexible, but two mechanisms to manage |

## Open questions

- One system or separate flows for paid and free events?
- Does Aesium sell tickets itself or primarily market / link to events?
- Are external event listings / API integrations required?
- Live venue music licensing is separate from on-demand mix licensing. A cleared physical event does not automatically clear its recording for on-demand publishing.
