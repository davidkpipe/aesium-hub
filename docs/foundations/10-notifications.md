# 10 · Notifications

| | |
|---|---|
| **Type** | Shared foundation |
| **Used by** | Audience account area, Artist Profiles (follow), Publishing Workflow (publish triggers), Events |
| **Source** | §1, §14, §19 |

## Purpose

Let audience members receive updates from the artists they follow, controlled by their own preferences.

## What it must provide (V1)

- Notification preferences in the account area.
- Sending an update when relevant content is published (a followed artist publishes a mix, video, article or event).
- Email delivery at minimum; browser notifications to be confirmed.
- Respect scheduling and unpublishing: notify only on actual publication.

## Data it owns

- Notification preferences per user: channel, type, enabled.
- Sent-notification log: user, type, content, sent at, read at.

## Depends on

- Accounts & Permissions.
- Audience Activity (who follows whom).
- Publishing Workflow (publish events as triggers).
- Hosting & Infrastructure (email provider, background jobs).

## Build options

A transactional email provider (Postmark, SendGrid, Resend or similar) triggered by publish events. Browser push adds a service worker and a permission flow.

## Later

- Digest emails, in-app notification centre, mobile push.

## Open questions

- Email and / or browser notification requirements.
- Which events trigger a notification and how often.
