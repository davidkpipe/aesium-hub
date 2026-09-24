# Aesium Hub

A self-contained static single-page site. Everything (markup, the `dc-runtime`
JavaScript, and all fonts) is bundled into [`index.html`](index.html) — there is
no build step and no external assets to fetch.

## Docs site

The working documents in [`docs/`](docs/README.md) are also rendered as styled
HTML pages that sit next to the markdown (`docs/index.html`,
`docs/statement-of-work.html`, and so on). The HTML is committed, so Pages still
needs no build step. After editing any markdown under `docs/`, regenerate the
pages with:

```bash
python3 tools/build-docs.py
```

On the deployed site the docs live under `/docs/`, for example
`https://<project>.pages.dev/docs/` and
`https://<project>.pages.dev/docs/statement-of-work`.

## Deploy to Cloudflare Pages (GitHub-connected)

1. Push this repo to GitHub (already wired to `github.com/davidkpipe/aesium-hub`).
2. In the Cloudflare dashboard go to **Workers & Pages → Create → Pages →
   Connect to Git** and pick the `aesium-hub` repo.
3. Use these build settings:
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `/`
   - **Production branch:** `main`
4. **Save and Deploy.** Every push to `main` redeploys automatically.

To add a custom domain later: **Pages project → Custom domains → Set up a
domain**.

## Possible follow-ups (not done yet)

The page currently ships as a self-unpacking bundle: each visit base64-decodes
and gunzips ~470 KB before it renders, and there is no `<title>`, meta
description, favicon, or Open Graph/Twitter card. Unbundling it into real files
(`index.html` + `runtime.js` + `fonts/`) and adding those tags would make it
faster, cacheable, and link/SEO-friendly.
