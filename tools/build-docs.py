#!/usr/bin/env python3
"""Render every markdown file under docs/ to a styled HTML page next to it.

Run from the repository root:  python3 tools/build-docs.py
No dependencies beyond the Python 3 standard library. The generated pages are
committed, so the site needs no build step on Cloudflare Pages.
"""
from __future__ import annotations

import html
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE_NAME = "Aesium Platform"
REPO_URL = "https://github.com/davidkpipe/aesium-hub"
MERMAID_SRC = "https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.1/mermaid.min.js"

CONTENT_TYPE_ORDER = [
    "artist-profiles", "mixes", "series", "editorial-articles", "videos", "events", "products-shop",
]

# ---------------------------------------------------------------- inline markdown

INLINE_RULES = [
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)"), r"<em>\1</em>"),
    (re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
]
LINK_RX = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def rewrite_href(href: str) -> str:
    """Point relative markdown links at the generated HTML pages."""
    if re.match(r"^[a-z]+:", href) or href.startswith("#"):
        return href
    path, _, anchor = href.partition("#")
    if path.endswith(".md"):
        base = path[:-3]
        if base.endswith("README"):
            base = base[: -len("README")] + "index"
        path = base + ".html"
    return path + ("#" + anchor if anchor else "")


def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    for rx, rep in INLINE_RULES:
        out = rx.sub(rep, out)
    out = LINK_RX.sub(lambda m: f'<a href="{rewrite_href(m.group(2))}">{m.group(1)}</a>', out)
    return out


def strip_inline(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = LINK_RX.sub(r"\1", text)
    return text


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", strip_inline(text).lower()).strip("-")
    return s or "section"


# ---------------------------------------------------------------- tables

NUMERIC = re.compile(r"^[\s$€£NZDUS,.\d%–\-+~≈()xh/]*\d[\s$€£NZDUS,.\d%–\-+~≈()xh/]*$")


def is_numeric_cell(cell: str) -> bool:
    c = cell.strip()
    if not c or len(c) > 24:
        return False
    return bool(NUMERIC.match(c))


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_kv_table(rows: list[str]) -> bool:
    header = split_row(rows[0])
    if any(header) or len(header) != 2:
        return False
    return all(len(split_row(r)) == 2 for r in rows[2:])


def render_meta(rows: list[str]) -> str:
    out = ['<dl class="meta">']
    for r in rows[2:]:
        k, v = split_row(r)
        out.append(f"<div><dt>{inline(strip_inline(k))}</dt><dd>{inline(v)}</dd></div>")
    out.append("</dl>")
    return "\n".join(out)


def render_table(rows: list[str]) -> str:
    header = split_row(rows[0])
    body = [split_row(r) for r in rows[2:]]
    ncols = len(header)
    numeric_cols = []
    for i in range(ncols):
        vals = [b[i] for b in body if i < len(b) and b[i].strip()]
        numeric_cols.append(bool(vals) and all(is_numeric_cell(v) for v in vals))
    wide = ncols > 8
    out = [f'<div class="table-wrap{" wide" if wide else ""}"><table>', "<thead><tr>"]
    for i, h in enumerate(header):
        cls = ' class="num"' if numeric_cols[i] else ""
        out.append(f"<th{cls}>{inline(h)}</th>")
    out.append("</tr></thead><tbody>")
    for cells in body:
        first = cells[0].strip().strip("*").lower() if cells else ""
        is_total = first.startswith(("total", "subtotal"))
        out.append('<tr class="total">' if is_total else "<tr>")
        for i in range(ncols):
            v = cells[i] if i < len(cells) else ""
            cls = ' class="num"' if numeric_cols[i] else ""
            out.append(f"<td{cls}>{inline(v)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


# ---------------------------------------------------------------- lists

LIST_RX = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def render_list(items: list[tuple[int, bool, str]]) -> str:
    out: list[str] = []
    stack: list[tuple[int, str]] = []

    def open_list(indent: int, ordered: bool) -> None:
        tag = "ol" if ordered else "ul"
        out.append(f"<{tag}>")
        stack.append((indent, tag))

    for indent, ordered, text in items:
        if not stack or indent > stack[-1][0]:
            open_list(indent, ordered)
        else:
            while len(stack) > 1 and indent < stack[-1][0]:
                out.append(f"</li></{stack.pop()[1]}>")
            out.append("</li>")
        out.append(f"<li>{inline(text)}")
    while stack:
        out.append(f"</li></{stack.pop()[1]}>")
    return "\n".join(out)


# ---------------------------------------------------------------- document

class Page:
    def __init__(self, src: Path):
        self.src = src
        self.title = ""
        self.subtitle = ""
        self.meta_html = ""
        self.toc: list[tuple[str, str]] = []
        self.body = ""
        self.description = ""
        self.needs_mermaid = False

    @property
    def out(self) -> Path:
        name = "index.html" if self.src.name == "README.md" else self.src.with_suffix(".html").name
        return self.src.with_name(name)

    @property
    def rel(self) -> str:  # path relative to docs/, for navigation
        return self.out.relative_to(DOCS).as_posix()


def convert(md: str, page: Page) -> None:
    lines = md.splitlines()
    out: list[str] = []
    para: list[str] = []
    i, n = 0, len(lines)
    seen_h2 = False
    open_section = False

    def flush_para() -> None:
        nonlocal para
        if para:
            text = " ".join(s.strip() for s in para)
            if not page.description:
                page.description = strip_inline(text)[:200]
            out.append(f"<p>{inline(text)}</p>")
            para = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para()
            i += 1
            continue

        if stripped.startswith("# ") and not page.title:
            page.title = stripped[2:].strip()
            i += 1
            while i < n and not lines[i].strip():
                i += 1
            if i < n and re.fullmatch(r"\*[^*].*[^*]\*", lines[i].strip()):
                page.subtitle = lines[i].strip().strip("*")
                i += 1
            continue

        m = re.match(r"^(#{2,4})\s+(.*)$", stripped)
        if m:
            flush_para()
            level = len(m.group(1))
            text = m.group(2).strip()
            sid = slug(text)
            if level == 2:
                if open_section:
                    out.append("</section>")
                page.toc.append((sid, strip_inline(text)))
                out.append(f'<section class="sec" id="{sid}"><h2>{inline(text)}</h2>')
                open_section = True
                seen_h2 = True
            else:
                out.append(f'<h{level} id="{sid}">{inline(text)}</h{level}>')
            i += 1
            continue

        if stripped.startswith("```"):
            flush_para()
            lang = stripped[3:].strip()
            i += 1
            code: list[str] = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # closing fence
            if lang == "mermaid":
                page.needs_mermaid = True
                out.append('<figure class="diagram"><pre class="mermaid">' + html.escape("\n".join(code), quote=False) + "</pre></figure>")
            else:
                out.append("<pre><code>" + html.escape("\n".join(code), quote=False) + "</code></pre>")
            continue

        if stripped == "---":
            flush_para()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("|"):
            flush_para()
            rows: list[str] = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            if not seen_h2 and not page.meta_html and is_kv_table(rows):
                page.meta_html = render_meta(rows)
            else:
                out.append(render_table(rows))
            continue

        if stripped.startswith(">"):
            flush_para()
            quote: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(f'<aside class="callout">{inline(" ".join(q for q in quote if q))}</aside>')
            continue

        if LIST_RX.match(line):
            flush_para()
            items: list[tuple[int, bool, str]] = []
            while i < n:
                lm = LIST_RX.match(lines[i])
                if lm:
                    indent = len(lm.group(1).replace("\t", "  "))
                    items.append((indent, lm.group(2)[0].isdigit(), lm.group(3).strip()))
                    i += 1
                elif lines[i].strip() and lines[i].startswith("  ") and items:
                    ind, ordr, txt = items[-1]
                    items[-1] = (ind, ordr, txt + " " + lines[i].strip())
                    i += 1
                else:
                    break
            out.append(render_list(items))
            continue

        para.append(line)
        i += 1

    flush_para()
    if open_section:
        out.append("</section>")
    page.body = "\n".join(out)


# ---------------------------------------------------------------- chrome

STYLE = """
:root{
  --ground:#fbf9ef; --ground-2:#f4efe1; --ground-3:#ece5d6;
  --ink:#17120e; --ink-2:#3d332a; --muted:#7d6a52; --muted-2:#8a8175;
  --accent:#c8762f; --accent-deep:#b0633f; --accent-light:#e6b27a;
  --rule:#d9d0bd; --rule-soft:#e6dfcf;
  --display:"Fraunces",Georgia,"Times New Roman",serif;
  --body:"Hanken Grotesk","Helvetica Neue",Arial,sans-serif;
  --mono:"Space Mono","SFMono-Regular",Menlo,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme: dark){
  :root{
    color-scheme:dark;
    --ground:#17120e; --ground-2:#1d1813; --ground-3:#231c15;
    --ink:#f4efe1; --ink-2:#d8cfbf; --muted:#b3a895; --muted-2:#8a8175;
    --accent:#e6b27a; --accent-deep:#c8762f; --accent-light:#f0c993;
    --rule:#3a3128; --rule-soft:#2c251d;
  }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:var(--accent-deep);text-decoration-thickness:1px;text-underline-offset:2px}
a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.wrap{max-width:1080px;margin:0 auto;padding-block:0 72px;padding-inline:clamp(16px,4vw,40px)}
.topnav{display:flex;flex-wrap:wrap;align-items:center;gap:6px 22px;padding-block:18px;border-bottom:1px solid var(--rule);font-size:14px}
.topnav .brand{font-family:var(--display);font-weight:600;font-size:18px;color:var(--ink);text-decoration:none;margin-right:auto}
.topnav a:not(.brand){color:var(--ink-2);text-decoration:none;padding:4px 0;border-bottom:2px solid transparent}
.topnav a:not(.brand):hover,.topnav a[aria-current="page"]{color:var(--accent-deep);border-bottom-color:var(--accent)}
.mast{padding-block:44px 26px;border-bottom:1px solid var(--rule)}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.mast h1{font-family:var(--display);font-weight:500;font-size:clamp(32px,5vw,54px);line-height:1.05;margin:12px 0 10px;letter-spacing:-.01em;text-wrap:balance}
.mast .sub{font-size:18px;color:var(--ink-2);max-width:62ch;margin:0}
.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px 28px;margin:24px 0 0;padding-top:18px;border-top:1px solid var(--rule-soft)}
.meta div{font-size:14px;color:var(--ink-2)}
.meta dt{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}
.meta dd{margin:0}
.layout{display:grid;grid-template-columns:1fr;gap:32px;margin-top:32px}
@media (min-width:940px){.layout{grid-template-columns:220px minmax(0,1fr);gap:56px}}
.toc{position:sticky;top:0;align-self:start;font-size:14px;padding-top:6px}
.toc .eyebrow{font-size:11px;margin-bottom:10px}
.toc ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}
.toc a{color:var(--ink-2);text-decoration:none;display:block;padding:2px 0 2px 10px;border-left:2px solid transparent;line-height:1.35}
.toc a:hover{color:var(--accent-deep);border-left-color:var(--accent)}
@media (max-width:939px){.toc{position:static;border:1px solid var(--rule);border-radius:6px;padding:14px 16px;background:var(--ground-2)}.toc:empty{display:none}}
main{min-width:0;max-width:80ch}
.sec{padding-block:6px 22px;border-bottom:1px solid var(--rule-soft);margin-bottom:22px}
.sec:last-child{border-bottom:0}
h2{font-family:var(--display);font-weight:500;font-size:clamp(25px,3vw,32px);line-height:1.15;letter-spacing:-.01em;margin:22px 0 12px;text-wrap:balance}
h3{font-family:var(--display);font-weight:600;font-size:21px;line-height:1.25;margin:28px 0 10px;text-wrap:balance}
h4{font-family:var(--body);font-weight:700;font-size:15px;letter-spacing:.02em;text-transform:uppercase;color:var(--ink-2);margin:22px 0 8px}
p{margin:0 0 14px;max-width:70ch}
ul,ol{margin:0 0 16px;padding-left:22px;max-width:70ch}
li{margin-bottom:6px}
li>ul,li>ol{margin-top:6px;margin-bottom:0}
code{font-family:var(--mono);font-size:.86em;background:var(--ground-3);padding:1px 5px;border-radius:3px}
pre{background:var(--ground-2);border:1px solid var(--rule);border-radius:6px;padding:14px 16px;overflow-x:auto;font-size:13.5px;line-height:1.5}
pre code{background:none;padding:0;font-size:inherit}
hr{border:0;border-top:1px solid var(--rule);margin:28px 0}
.callout{border-left:3px solid var(--accent);background:var(--ground-2);padding:12px 16px;margin:18px 0 20px;font-size:15px;color:var(--ink-2);max-width:70ch}
.table-wrap{overflow-x:auto;margin:14px 0 22px;border:1px solid var(--rule);border-radius:6px;background:var(--ground-2)}
table{border-collapse:collapse;width:100%;font-size:14.5px;min-width:520px}
.wide table{font-size:13px}
th,td{padding:9px 12px;vertical-align:top;border-bottom:1px solid var(--rule-soft);text-align:left}
th{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:400;background:var(--ground-3);white-space:nowrap}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tbody tr:last-child td{border-bottom:0}
tr.total td{font-weight:700;background:var(--ground-3)}
tr.total td.num{color:var(--accent-deep)}
.diagram{margin:16px 0 24px;padding:16px;border:1px solid var(--rule);border-radius:6px;background:var(--ground-2);overflow-x:auto}
.diagram pre.mermaid{background:none;border:0;padding:0;margin:0;overflow:visible;font-family:var(--mono);white-space:pre}
.diagram svg{max-width:100%;height:auto}
.docs-index{margin-top:56px;padding-top:24px;border-top:1px solid var(--rule)}
.docs-index .cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:22px 32px;margin-top:14px}
.docs-index h2{font-size:14px;font-family:var(--mono);font-weight:400;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 8px}
.docs-index ul{list-style:none;padding:0;margin:0;font-size:14.5px}
.docs-index li{margin-bottom:5px}
.docs-index a{color:var(--ink-2);text-decoration:none}
.docs-index a:hover{color:var(--accent-deep);text-decoration:underline}
.foot{margin-top:36px;padding-top:18px;border-top:1px solid var(--rule-soft);font-family:var(--mono);font-size:12px;color:var(--muted);letter-spacing:.04em;display:flex;flex-wrap:wrap;gap:8px 24px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{.topnav,.toc,.docs-index{display:none}.layout{display:block}.wrap{padding:0}body{font-size:12.5px}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600'
         '&family=Hanken+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap">')

MERMAID_INIT = """<script src="%s"></script>
<script>
  mermaid.initialize({
    startOnLoad: true,
    theme: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'neutral',
    themeVariables: { fontFamily: 'Hanken Grotesk, Helvetica Neue, Arial, sans-serif' },
    er: { useMaxWidth: true }
  });
</script>""" % MERMAID_SRC


def eyebrow_for(page: Page) -> str:
    rel = page.rel
    if rel == "index.html":
        return "Working documents"
    if rel.startswith("foundations/"):
        return "Shared foundation"
    if rel.startswith("content-types/"):
        return "Content type"
    if rel == "entity-diagram.html":
        return "Reference"
    if rel == "statement-of-work.html":
        return "Commercial · Version 1.1"
    return "Document"


def nav_html(page: Page, root: str) -> str:
    items = [
        ("Overview", "index.html"),
        ("Foundations", "index.html#foundations"),
        ("Content types", "index.html#content-types"),
        ("Entity diagram", "entity-diagram.html"),
        ("Statement of work", "statement-of-work.html"),
    ]
    out = [f'<nav class="topnav" aria-label="Site"><a class="brand" href="{root}index.html">{SITE_NAME} docs</a>']
    for label, href in items:
        current = ' aria-current="page"' if href == page.rel else ""
        out.append(f'<a href="{root}{href}"{current}>{label}</a>')
    out.append(f'<a href="{REPO_URL}" rel="noopener">GitHub</a></nav>')
    return "".join(out)


def index_html(pages: list[Page], root: str) -> str:
    foundations = sorted((p for p in pages if p.rel.startswith("foundations/")), key=lambda p: p.rel)
    ctypes = sorted((p for p in pages if p.rel.startswith("content-types/")),
                    key=lambda p: CONTENT_TYPE_ORDER.index(p.src.stem) if p.src.stem in CONTENT_TYPE_ORDER else 99)
    others = [p for p in pages if p.rel in ("entity-diagram.html", "statement-of-work.html")]

    def col(title: str, items: list[Page]) -> str:
        lis = "".join(f'<li><a href="{root}{p.rel}">{html.escape(strip_inline(p.title))}</a></li>' for p in items)
        return f"<div><h2>{title}</h2><ul>{lis}</ul></div>"

    return ('<section class="docs-index" aria-label="All documents"><div class="eyebrow">All documents</div><div class="cols">'
            + col("Foundations", foundations) + col("Content types", ctypes)
            + col("Reference and commercial", sorted(others, key=lambda p: p.rel)) + "</div></section>")


def render_page(page: Page, pages: list[Page]) -> str:
    depth = len(Path(page.rel).parts) - 1
    root = "../" * depth
    title = strip_inline(page.title)
    toc_html = "".join(f'<li><a href="#{sid}">{html.escape(t)}</a></li>' for sid, t in page.toc)
    toc_block = f'<nav class="toc" aria-label="On this page"><div class="eyebrow">On this page</div><ol>{toc_html}</ol></nav>' if page.toc else '<nav class="toc" aria-label="On this page"></nav>'
    subtitle = f'<p class="sub">{inline(page.subtitle)}</p>' if page.subtitle else ""
    mermaid = MERMAID_INIT if page.needs_mermaid else ""
    desc = html.escape(page.description or f"{title} for the {SITE_NAME}.", quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · {SITE_NAME} docs</title>
<meta name="description" content="{desc}">
{FONTS}
<style>{STYLE}</style>
</head>
<body>
<div class="wrap">
{nav_html(page, root)}
<header class="mast">
  <div class="eyebrow">{eyebrow_for(page)}</div>
  <h1>{inline(page.title)}</h1>
  {subtitle}
  {page.meta_html}
</header>
<div class="layout">
  {toc_block}
  <main>
{page.body}
  </main>
</div>
{index_html(pages, root)}
<footer class="foot"><span>{SITE_NAME} · working documents</span><span>Source: <a href="{REPO_URL}/blob/main/docs/{page.src.relative_to(DOCS).as_posix()}">{page.src.relative_to(DOCS).as_posix()}</a></span></footer>
</div>
{mermaid}
</body>
</html>
"""


def main() -> int:
    sources = sorted(DOCS.rglob("*.md"))
    pages = [Page(src) for src in sources]
    for page in pages:
        convert(page.src.read_text(encoding="utf-8"), page)
        if not page.title:
            page.title = page.src.stem.replace("-", " ").title()
    for page in pages:
        page.out.write_text(render_page(page, pages), encoding="utf-8")
        print(f"{page.src.relative_to(ROOT)} -> {page.out.relative_to(ROOT)}")
    print(f"{len(pages)} pages written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
