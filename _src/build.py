#!/usr/bin/env python3
"""
Physio8 article builder.

Generates, from _src/articles/*.py and the two templates in _src/:
  artikel/index.html                 – the article hub   (URL: /artikel/)
  artikel/<slug>/index.html          – one page per article (URL: /artikel/<slug>/)
and small redirect stubs at the old file names.

Usage:  python3 _src/build.py          (run from the repository root)

Folders starting with "_" are not published by GitHub Pages (Jekyll), so this
folder stays private even though it lives in the repo.

When the site moves to its own domain, change SITE_BASE below and rebuild.
When Timothy has clinically reviewed the articles, set CLINICALLY_REVIEWED = True.
"""
import glob, html, importlib.util, json, os, re, sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_src")

SITE_BASE = "https://chica126.github.io/p8/"   # absolute base used for canonical / og / schema URLs
SHARE_IMAGE = SITE_BASE + "favicon.png"        # share-preview image for every page (1200x1200)
CLINICALLY_REVIEWED = False                    # flip to True only after the clinician has reviewed every article
WA_NUMBER = "6281511488080"
UTM = "utm_source=physio8&utm_medium=referral"

AUTHOR = {
    "@type": "Person", "name": "Timothy Abieza", "honorificSuffix": "B.Sc. PT",
    "jobTitle": "Contributing Writer, Athletic Trainer and Physiotherapist",
    "url": "https://www.linkedin.com/in/timothy-abieza-a040891a5",
    "sameAs": ["https://www.linkedin.com/in/timothy-abieza-a040891a5"],
    "knowsAbout": ["Return to sport", "Sports injuries", "Concussion assessment"],
    "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Saxion University of Applied Sciences"},
                 {"@type": "CollegeOrUniversity", "name": "HAN University of Applied Sciences"}],
}
PUBLISHER = {
    "@type": "MedicalBusiness", "name": "Physio8", "url": SITE_BASE,
    "logo": SITE_BASE + "favicon.png", "image": SITE_BASE + "p8/logo-lockup.png",
    "address": {"@type": "PostalAddress", "streetAddress": "Ruko Hudson, Gading Serpong",
                "addressLocality": "Tangerang", "addressRegion": "Banten", "addressCountry": "ID"},
    "geo": {"@type": "GeoCoordinates", "latitude": -6.2693025, "longitude": 106.6246716},
    "hasMap": "https://www.google.com/maps/search/?api=1&query=Physio8+Gading+Serpong",
    "sameAs": ["https://www.instagram.com/physio8.id/"],
}


# ---------------------------------------------------------------- helpers
def load_articles():
    arts = []
    for path in sorted(glob.glob(os.path.join(SRC, "articles", "*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        arts.append(mod.ARTICLE)
    arts.sort(key=lambda a: a["order"])
    for a in arts:  # reading time from the actual text (~200 words/min, +1 for tables and lists)
        a["read"] = max(3, -(-word_count(a) // 200) + 1)
    return arts


def esc(s):
    return html.escape(s, quote=True)


def js(v):
    """JSON is valid JS; escape '</' so nothing can close the <script> early."""
    return json.dumps(v, ensure_ascii=False).replace("</", "<\\/")


def img(a, w, h=None):
    """Unsplash CDN URL, cropped server-side to a landscape frame focused on faces/detail."""
    h = h or (w // 2 if w >= 1600 else w * 2 // 3)
    return a["image"]["src"] + f"?w={w}&h={h}&q=80&auto=format&fit=crop&crop=faces,entropy"


def credit(a):
    return f"Photo by {a['image']['name']} on Unsplash"


def profile(a):
    return a["image"]["profile"] + "?" + UTM


def url_of(slug=None):
    return SITE_BASE + ("artikel/" + slug + "/" if slug else "artikel/")


def wa_price_link():
    text = "Halo Physio8, saya ingin menanyakan harga asesmen dan sesi terapi."
    return f"https://wa.me/{WA_NUMBER}?text=" + quote(text, safe="")


def wa_link(src):
    text = f"Halo Physio8, saya ingin membuat jadwal asesmen. (dari {src})"
    return f"https://wa.me/{WA_NUMBER}?text=" + quote(text, safe="")


def replace_once(s, old, new, what):
    n = s.count(old)
    if n != 1:
        sys.exit(f"template change '{what}' expected 1 match, found {n}")
    return s.replace(old, new, 1)


def check_citations(a):
    text = json.dumps([a["blocks"], a["takeaways"], a["faqs"]], ensure_ascii=False)
    cited = {int(n) for n in re.findall(r"\[(\d+)\]", text)}
    total = len(a["refs"])
    missing = sorted(set(range(1, total + 1)) - cited)
    beyond = sorted(n for n in cited if n > total)
    if missing or beyond:
        sys.exit(f"{a['slug']}: uncited refs {missing}, citations without a ref {beyond}")


def word_count(a):
    parts = [a["dek"][0]] + [t[0] for t in a["takeaways"]]
    for b in a["blocks"]:
        k = b[0]
        if k in ("h2",):
            parts.append(b[2])
        elif k == "p":
            parts.append(b[1])
        elif k in ("ul", "ol"):
            parts += [x[0] for x in b[1]]
        elif k == "table":
            parts += [" ".join(r[:3]) for r in b[1]]
        elif k == "callout":
            parts.append(b[1]); parts += [x[0] + " " + x[1] for x in b[3]]
        elif k == "stats":
            parts += [x[1] for x in b[1]]
    parts += [f[0] + " " + f[2] for f in a["faqs"]]
    return len(" ".join(parts).split())


def fmt_date_id(iso):
    y, m, d = iso.split("-")
    months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
              "September", "Oktober", "November", "Desember"]
    return f"{int(d)} {months[int(m) - 1]} {y}"


def fmt_date_en(iso):
    y, m, d = iso.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December"]
    return f"{int(d)} {months[int(m) - 1]} {y}"


def add_class(s, needle, cls, what=None):
    """Add a class to the element whose opening tag contains `needle` (must be unique)."""
    n = s.count(needle)
    if n != 1:
        sys.exit(f"responsive hook '{what or cls}' expected 1 match, found {n}")
    i = s.find(needle)
    start = i if needle.startswith("<") else s.rfind("<", 0, i)
    j = start + 1
    while s[j] not in " >":
        j += 1
    return s[:j] + f' class="{cls}"' + s[j:]


RESPONSIVE_CSS = """
/* ---- plain editorial labels: no all-caps, no pill badges (applies site-wide) ---- */
[style*="text-transform:uppercase"],[style*="text-transform: uppercase"]{text-transform:none !important;letter-spacing:0 !important;font-size:var(--text-sm) !important}
[style*="background:var(--color-brand-subtle)"][style*="padding:5px"],[style*="background: var(--color-brand-subtle)"][style*="padding: 5px"],
[style*="background:var(--status-info-bg)"],[style*="background: var(--status-info-bg)"]{background:transparent !important;padding:0 !important;border-radius:0 !important;font-weight:600 !important}
[style*="background:var(--color-brand-subtle)"][style*="padding:5px"] > span:empty,[style*="background: var(--color-brand-subtle)"][style*="padding: 5px"] > span:empty{display:none !important}
[style*="background:var(--status-info-bg)"] svg,[style*="background: var(--status-info-bg)"] svg{display:none !important}
/* ---- responsive (inline styles need !important to be overridden) ---- */
img{max-width:100%}
@media (max-width: 960px){
  .p8-main{grid-template-columns:minmax(0,1fr) !important;gap:var(--space-8) !important}
  .p8-aside{display:none !important}
  .p8-book,.p8-hubhero,.p8-featured{grid-template-columns:minmax(0,1fr) !important;gap:var(--space-8) !important}
  .p8-footgrid{grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;gap:var(--space-8) !important}
  .p8-footgrid > :first-child{grid-column:1 / -1}
}
@media (max-width: 760px){
  .p8-nav{display:none !important}
  .p8-hdr{height:64px !important;gap:var(--space-3) !important}
  .p8-hdr img{height:34px !important}
  .p8-hdr-cta{padding:0 var(--space-4) !important;font-size:var(--text-xs) !important;height:36px !important}
  .p8-h1{font-size:clamp(30px,8.4vw,40px) !important}
  .p8-review{margin:0 !important}
  .p8-hero{aspect-ratio:4/3 !important;margin:var(--space-8) 0 var(--space-10) !important}
  .p8-stats{grid-template-columns:minmax(0,1fr) !important}
  .p8-tablewrap{overflow-x:auto !important;-webkit-overflow-scrolling:touch}
  .p8-table{min-width:560px}
  .p8-callrow{flex-direction:column !important;gap:var(--space-1) !important}
  .p8-callval{white-space:normal !important}
  .p8-authorbox{flex-direction:column !important}
  .p8-hubhero{padding-top:var(--space-12) !important}
  .p8-filter{position:static !important}
  .p8-filter label{min-width:0 !important;flex:1 1 100% !important}
  .p8-featured{padding:var(--space-4) !important}
  .p8-footgrid{grid-template-columns:minmax(0,1fr) !important}
  .p8-pad{padding:var(--card-pad) !important}
}
@media (max-width: 380px){
  .p8-lang{display:none !important}
}
"""


ICON_LINK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>'
ICON_WA = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.2C6.6 2.2 2.2 6.6 2.2 12c0 1.7.45 3.35 1.28 4.8L2.2 21.8l5.12-1.27c1.4.77 2.99 1.17 4.68 1.17 5.4 0 9.8-4.4 9.8-9.8S17.4 2.2 12 2.2zm0 17.8c-1.5 0-2.97-.4-4.25-1.16l-.3-.18-3.04.75.8-2.93-.2-.31A8.1 8.1 0 0 1 3.9 12c0-4.47 3.63-8.1 8.1-8.1s8.1 3.63 8.1 8.1-3.63 8-8.1 8zm4.45-6.06c-.24-.12-1.44-.71-1.66-.79-.22-.08-.38-.12-.55.12-.16.24-.63.79-.77.95-.14.16-.28.18-.53.06-.24-.12-1.03-.38-1.96-1.21-.72-.65-1.21-1.44-1.36-1.69-.14-.24-.01-.37.11-.5.11-.11.24-.28.37-.43.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.43-.06-.12-.55-1.32-.75-1.81-.2-.47-.4-.41-.55-.42h-.47c-.16 0-.43.06-.65.3-.22.24-.85.83-.85 2.03s.87 2.35.99 2.51c.12.16 1.72 2.62 4.16 3.68.58.25 1.03.4 1.39.51.58.19 1.11.16 1.53.1.47-.07 1.44-.59 1.64-1.16.2-.57.2-1.06.14-1.16-.06-.1-.22-.16-.46-.28z"></path></svg>'
ICON_LI = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"></path></svg>'
SHARE_BTN = ('display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;border-radius:50%;'
             'background:var(--surface-card);border:1px solid var(--border-subtle);color:var(--text-muted);cursor:pointer;'
             'transition:all 200ms ease;padding:0')
SHARE_HOVER = 'color:#fff;background:var(--color-brand);border-color:var(--color-brand);transform:translateY(-2px)'


def share_row(a):
    url = url_of(a["slug"])
    wa = "https://wa.me/?text=" + quote(a["title"][0] + " — " + url, safe="")
    li = "https://www.linkedin.com/sharing/share-offsite/?url=" + quote(url, safe="")
    return f"""
      <div style="display:flex;align-items:center;gap:var(--space-3);flex-wrap:wrap;margin-top:var(--space-12);padding-top:var(--space-8);border-top:1px solid var(--border-subtle)">
        <span style="font-size:var(--text-sm);font-weight:var(--weight-semibold);color:var(--text-muted);margin-right:var(--space-1)">{{{{ t.share }}}}</span>
        <button type="button" onClick="{{{{ copyLink }}}}" aria-label="{{{{ t.copyLink }}}}" title="{{{{ t.copyLink }}}}" style="{SHARE_BTN}" style-hover="{SHARE_HOVER}">{ICON_LINK}</button>
        <a href="{esc(wa)}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp" title="WhatsApp" style="{SHARE_BTN}" style-hover="{SHARE_HOVER}">{ICON_WA}</a>
        <a href="{esc(li)}" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" title="LinkedIn" style="{SHARE_BTN}" style-hover="{SHARE_HOVER}">{ICON_LI}</a>
      </div>
      <div role="status" aria-live="polite" style="position:fixed;left:50%;bottom:32px;transform:translateX(-50%);background:var(--surface-inverse);color:#fff;font-size:var(--text-sm);font-weight:var(--weight-medium);padding:12px 24px;border-radius:999px;z-index:999;pointer-events:none;transition:opacity 250ms ease;opacity:{{{{ toastOpacity }}}}">{{{{ t.copied }}}}</div>
"""


# ---------------------------------------------------------------- article page
def article_head(a, bys):
    url = url_of(a["slug"])
    title = a["meta_title"]
    desc = a["meta_desc"]
    graph = [
        {
            "@type": ["MedicalWebPage", "Article"], "@id": url + "#article", "url": url,
            "mainEntityOfPage": url, "headline": a["title"][0], "name": a["title"][0],
            "description": desc, "inLanguage": "id-ID",
            "image": [img(a, 1200, 630)], "datePublished": a["published"], "dateModified": a["modified"],
            "articleSection": a["tag"][0],
            "keywords": [a["keywords_primary"][0]] + [k.strip() for k in a["keywords_secondary"][0].split("·")],
            "about": {"@type": "MedicalCondition", "name": a["about"]},
            "audience": {"@type": "PeopleAudience", "geographicArea": {"@type": "Place", "name": "Gading Serpong, Tangerang"}},
            "author": AUTHOR, "publisher": PUBLISHER,
            "citation": [{"@type": "CreativeWork", "name": r[0], "url": r[1]} for r in a["refs"]],
            "wordCount": word_count(a),
        },
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Beranda", "item": SITE_BASE},
            {"@type": "ListItem", "position": 2, "name": "Artikel", "item": url_of()},
            {"@type": "ListItem", "position": 3, "name": a["crumb"][0], "item": url},
        ]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f[0], "acceptedAnswer": {"@type": "Answer", "text": f[2]}}
            for f in a["faqs"]]},
    ]
    if CLINICALLY_REVIEWED:
        graph[0]["reviewedBy"] = {"@type": "Person", "name": "Timothy Abieza",
                                  "jobTitle": "Athletic Trainer and Physiotherapist"}
        graph[0]["lastReviewed"] = a["modified"]
    ld = js({"@context": "https://schema.org", "@graph": graph})
    tags = "\n".join(f'<meta property="article:tag" content="{esc(k.strip())}">'
                     for k in a["keywords_secondary"][0].split("·"))
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#331079">
<meta name="author" content="Timothy Abieza, B.Sc. PT">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Physio8">
<meta property="og:locale" content="id_ID">
<meta property="og:title" content="{esc(a['title'][0])}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SHARE_IMAGE}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="1200">
<meta property="og:image:alt" content="Physio8 — studio fisioterapi di Gading Serpong">
<meta property="article:published_time" content="{a['published']}">
<meta property="article:modified_time" content="{a['modified']}">
<meta property="article:section" content="{esc(a['tag'][0])}">
{tags}
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(a['title'][0])}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SHARE_IMAGE}">
<link rel="icon" type="image/png" href="../../favicon.png">
<link rel="apple-touch-icon" href="../../favicon.png">
<script type="application/ld+json">
{ld}
</script>
<script src="../../support.js"></script>"""


def noscript_article(a):
    """Plain-HTML copy of the Indonesian article for crawlers and AI engines that do not run JS."""
    out = [f'<article lang="id" style="max-width:760px;margin:0 auto;padding:24px 16px;font-family:system-ui,sans-serif;line-height:1.65;color:#3D3B4C">',
           f'<p><a href="../../index.html">Beranda</a> · <a href="../index.html">Artikel</a> · {esc(a["tag"][0])}</p>',
           f'<h1>{esc(a["title"][0])}</h1>', f'<p><strong>{esc(a["dek"][0])}</strong></p>',
           f'<p>Timothy Abieza, B.Sc. PT · Terbit {fmt_date_id(a["published"])} · Diperbarui {fmt_date_id(a["modified"])}</p>',
           f'<figure><img src="{img(a, 1200)}" alt="{esc(a["image"]["alt"][0])}" width="1200" style="max-width:100%;height:auto">'
           f'<figcaption>{esc(a["image"]["alt"][0])}. Foto: <a href="{profile(a)}">{esc(a["image"]["name"])}</a> / '
           f'<a href="https://unsplash.com/?{UTM}">Unsplash</a></figcaption></figure>',
           '<h2>Ringkasan cepat</h2><ul>' + "".join(f"<li>{esc(t[0])}</li>" for t in a["takeaways"]) + "</ul>"]
    for b in a["blocks"]:
        k = b[0]
        if k == "h2":
            out.append(f'<h2 id="{b[1]}">{esc(b[2])}</h2>')
        elif k == "p":
            out.append(f"<p>{esc(b[1])}</p>")
        elif k in ("ul", "ol"):
            out.append(f"<{k}>" + "".join(f"<li>{esc(x[0])}</li>" for x in b[1]) + f"</{k}>")
        elif k == "table":
            rows = b[1]
            out.append("<table><thead><tr>" + "".join(f"<th>{esc(c)}</th>" for c in rows[0][:3]) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r[:3]) + "</tr>" for r in rows[1:])
                       + "</tbody></table>")
        elif k == "stats":
            out.append("<ul>" + "".join(f"<li>{esc(x[0])} — {esc(x[1])}</li>" for x in b[1]) + "</ul>")
        elif k == "callout":
            out.append(f"<p><strong>{esc(b[1])}</strong></p><ul>" +
                       "".join(f"<li>{esc(x[0])}: {esc(x[1])}</li>" for x in b[3]) + "</ul>")
    out.append('<h2 id="faq">Pertanyaan yang sering masuk</h2>')
    for f in a["faqs"]:
        out.append(f"<h3>{esc(f[0])}</h3><p>{esc(f[2])}</p>")
    out.append('<h2 id="referensi">Referensi</h2><ol>' +
               "".join(f'<li>{esc(r[0])} <a href="{esc(r[1])}">{esc(r[1])}</a></li>' for r in a["refs"]) + "</ol>")
    out.append(f'<p>Physio8 · Ruko Hudson, Gading Serpong, Tangerang, Banten. '
               f'<a href="{esc(wa_link(a["wa"]))}">Buat jadwal asesmen via WhatsApp</a>.</p>')
    out.append("<p><small>Artikel ini bersifat edukatif dan bukan pengganti pemeriksaan klinis langsung.</small></p></article>")
    return "<noscript>\n" + "\n".join(out) + "\n</noscript>"


def build_article(a, bys, tpl):
    s = tpl
    # 1. real <head>: static SEO, share and schema tags (visible to crawlers without JS)
    # 2. helmet keeps only what the runtime needs (its old meta + JSON-LD are dropped first)
    s = re.sub(r"<helmet>.*?(<link rel=\"stylesheet\")", r"<helmet>\n\1", s, count=1, flags=re.S)
    s = re.sub(r"<script type=\"application/ld\+json\">.*?</script>\n", "", s, count=1, flags=re.S)
    s = re.sub(r"<head>.*?</head>", lambda m: "<head>\n" + article_head(a, bys) + "\n</head>", s, count=1, flags=re.S)
    s = s.replace('href="./p8/styles.css"', 'href="../../p8/styles.css"')
    s = s.replace('src="./p8/', 'src="../../p8/')
    # 3. navigation paths (pages now live two folders deep)
    s = s.replace('href="./Artikel Hub.dc.html"', 'href="../index.html"')
    s = s.replace('href="./index.html"', 'href="../../index.html"')
    # 4. hero image + visible caption with photographer credit
    hero_old = '<image-slot id="art-hero" shape="rect" placeholder="Foto studio — fisioterapis mengukur range of motion lutut pasien"></image-slot>\n  </div>'
    hero_new = (f'<image-slot id="art-hero" shape="rect" placeholder="{esc(a["image"]["alt"][0])}" '
                f'src="{img(a, 1800)}" credit="{esc(credit(a))}" credit-href="{esc(a["image"]["profile"])}"></image-slot>\n  </div>\n'
                f'  <p style="margin:calc(var(--space-8) * -1) 0 var(--space-12);font-size:var(--text-xs);line-height:var(--leading-normal);color:var(--text-muted)">'
                f'{{{{ a.heroCaption }}}} · {{{{ t.photo }}}}: <a href="{esc(profile(a))}" target="_blank" rel="noopener noreferrer">{esc(a["image"]["name"])}</a> / '
                f'<a href="https://unsplash.com/?{UTM}" target="_blank" rel="noopener noreferrer">Unsplash</a></p>')
    s = replace_once(s, hero_old, hero_new, "hero")
    s = s.replace("aspect-ratio:21/9;margin:var(--space-10) 0 var(--space-12);", "aspect-ratio:21/9;margin:var(--space-10) 0 var(--space-12);", 1)
    # 5. WhatsApp booking link specific to this article
    s = re.sub(r'https://wa\.me/\d+\?text=[^"]+', esc(wa_link(a["wa"])), s)
    # 6. references section after the FAQ
    faq_end = "            </details>\n          </sc-for>\n        </div>\n      </section>\n"
    refs = faq_end + """
      <section style="margin-top:var(--space-16)">
        <h2 id="referensi" style="margin:0 0 var(--space-3);font-family:var(--font-display);font-size:var(--type-h3-size);font-weight:var(--weight-semibold);letter-spacing:var(--tracking-display);color:var(--text-heading);scroll-margin-top:110px">{{ t.refs }}</h2>
        <p style="margin:0 0 var(--space-6);font-size:var(--text-sm);line-height:var(--leading-relaxed);color:var(--text-muted)">{{ t.refsNote }}</p>
        <ol style="margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:var(--space-4)">
          <sc-for list="{{ refs }}" as="r" hint-placeholder-count="6">
            <li style="display:flex;gap:var(--space-3);font-size:var(--text-sm);line-height:var(--leading-relaxed);color:var(--text-body)">
              <span style="flex:0 0 auto;min-width:28px;font-family:var(--font-mono);font-size:var(--text-xs);color:var(--color-precision);padding-top:2px">{{ r.n }}</span>
              <span style="min-width:0">{{ r.text }} <a href="{{ r.url }}" target="_blank" rel="noopener noreferrer" style="word-break:break-word">{{ r.label }}</a></span>
            </li>
          </sc-for>
        </ol>
      </section>
"""
    s = replace_once(s, faq_end, refs, "refs")
    # 7. related cards link to real pages and show their photos
    s = replace_once(s, '<sc-for list="{{ related }}" as="r" hint-placeholder-count="3">\n        <a href="../../index.html"',
                     '<sc-for list="{{ related }}" as="r" hint-placeholder-count="3">\n        <a href="{{ r.href }}"', "related href")
    s = replace_once(s, '<image-slot id="{{ r.slotId }}" shape="rect" placeholder="{{ r.hint }}"></image-slot>',
                     '<image-slot id="{{ r.slotId }}" shape="rect" placeholder="{{ r.hint }}" src="{{ r.img }}" credit="{{ r.credit }}" credit-href="{{ r.creditHref }}"></image-slot>',
                     "related image")
    # 8. data script
    s = re.sub(r"const A = \{.*?\nconst T = \{", lambda m: data_js(a, bys) + "\nconst T = {", s, count=1, flags=re.S)
    s = re.sub(r"const SEO = \{.*?\n\};\n", lambda m: seo_js(a), s, count=1, flags=re.S)
    s = replace_once(s, "\nclass Component extends DCLogic {", "\n" + t_overrides(a) + "\nclass Component extends DCLogic {", "T overrides")
    s = replace_once(s, "        faqs:A.faqs.map(x => ({q:x[i], aText:x[2+i]}))\n      },",
                     "        faqs:A.faqs.map(x => ({q:x[i], aText:x[2+i]})),\n        heroCaption:A.heroCaption[i]\n      },\n"
                     "      refs: REFS.map((r, n) => ({n:\"[\"+(n+1)+\"]\", text:r[0], url:r[1], label:r[1].replace(/^https?:\\/\\//, \"\")})),",
                     "renderVals a")
    s = replace_once(s, "        tag:r.tag[i], title:r.title[i], slotId:r.read[1], hint:r.hint,\n",
                     "        tag:r.tag[i], title:r.title[i], slotId:r.read[1], hint:r.hint,\n"
                     "        href:r.href, img:r.img, credit:r.credit, creditHref:r.creditHref,\n", "renderVals related")
    # 8b. share row (copy link · WhatsApp · LinkedIn) before the author box
    author = '      <section style="margin-top:var(--space-16);display:flex;gap:var(--space-6);padding:var(--card-pad-lg)'
    s = replace_once(s, author, share_row(a) + "\n" + author, "share row")
    s = replace_once(s, 'state = {lang:"id", active:"", progress:"0%"};',
                     'state = {lang:"id", active:"", progress:"0%", copied:false};', "share state")
    s = replace_once(s, '      setId: () => this.setState({lang:"id"}),',
                     '      copyLink: () => {\n'
                     f'        const url = {js(url_of(a["slug"]))};\n'
                     '        const done = () => { this.setState({copied:true}); clearTimeout(this._ct); this._ct = setTimeout(() => this.setState({copied:false}), 2000); };\n'
                     '        const fallback = () => { const ta = document.createElement("textarea"); ta.value = url; ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); } catch (e) {} document.body.removeChild(ta); done(); };\n'
                     '        if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(url).then(done, fallback); else fallback();\n'
                     '      },\n'
                     '      toastOpacity: this.state.copied ? "1" : "0",\n'
                     '      setId: () => this.setState({lang:"id"}),', "share handler")
    # 9. crawler-readable copy
    s = replace_once(s, "</x-dc>\n", "</x-dc>\n" + noscript_article(a) + "\n", "noscript")
    # 10. responsive hooks + CSS
    for needle, cls in [
        ('padding:0 var(--layout-gutter);height:72px', "p8-hdr"),
        ('<nav style="display:flex;align-items:center;gap:var(--space-5);margin-left:var(--space-4)', "p8-nav"),
        ('<div style="display:flex;align-items:center;padding:3px;gap:2px;border:1px solid var(--border-subtle)', "p8-lang"),
        ('<a href="#book" style="display:inline-flex;align-items:center;height:var(--control-h-md)', "p8-hdr-cta"),
        ('<h1 style="margin:0 0 var(--space-5)', "p8-h1"),
        ('<p style="margin:0 0 0 auto;display:inline-flex', "p8-review"),
        ('aspect-ratio:21/9', "p8-hero"),
        ('grid-template-columns:minmax(0,260px) minmax(0,1fr)', "p8-main"),
        ('<aside style="position:sticky;top:96px', "p8-aside"),
        ('<div style="margin:0 0 var(--space-8);border:1px solid var(--border-subtle);border-radius:var(--radius-card);overflow:hidden">', "p8-tablewrap"),
        ('<table style="width:100%;border-collapse:collapse', "p8-table"),
        ('grid-template-columns:repeat(3,minmax(0,1fr))', "p8-stats"),
        ('<div style="display:flex;justify-content:space-between;gap:var(--space-5);padding-bottom:var(--space-3)', "p8-callrow"),
        ('<span style="font-family:var(--font-mono);color:var(--p8-lime-300);white-space:nowrap">', "p8-callval"),
        ('<section style="margin-top:var(--space-16);display:flex;gap:var(--space-6);padding:var(--card-pad-lg)', "p8-authorbox"),
        ('grid-template-columns:minmax(0,1.2fr) minmax(0,1fr)', "p8-book"),
    ]:
        s = add_class(s, needle, cls)
    hide_review = "" if CLINICALLY_REVIEWED else "\n.p8-review{display:none !important}\n"
    s = replace_once(s, "</style>\n</helmet>", RESPONSIVE_CSS + hide_review + "</style>\n</helmet>", "article css")
    s = s.replace("__WA_PRICE__", esc(wa_price_link()))
    return s


def data_js(a, bys):
    rev = ["Ditinjau klinis oleh Timothy Abieza, B.Sc. PT", "Clinically reviewed by Timothy Abieza, B.Sc. PT"] if CLINICALLY_REVIEWED \
        else ["Draf — menunggu tinjauan klinis", "Draft — awaiting clinical review"]
    A = {
        "category": a["tag"], "crumb": a["crumb"], "title": a["title"], "dek": a["dek"],
        "dateLine": [f"Terbit {fmt_date_id(a['published'])} · Diperbarui {fmt_date_id(a['modified'])}",
                     f"Published {fmt_date_en(a['published'])} · Updated {fmt_date_en(a['modified'])}"],
        "readLabel": [f"{a['read']} menit baca", f"{a['read']} min read"],
        "reviewLine": rev,
        "heroCaption": a["image"]["alt"],
        "takeaways": a["takeaways"],
        "faqs": [[f[0], f[1], f[2], f[3]] for f in a["faqs"]],
    }
    related = []
    for slug in a["related"]:
        r = bys[slug]
        related.append({"tag": r["tag"], "title": r["title"], "read": [r["read"], "rel-" + slug],
                        "hint": r["image"]["alt"][0], "href": f"../{slug}/index.html",
                        "img": img(r, 800), "credit": credit(r), "creditHref": r["image"]["profile"]})
    return (f"const A = {js(A)};\n\nconst B = {js(a['blocks'])};\n\n"
            f"const RELATED = {js(related)};\n\nconst REFS = {js(a['refs'])};\n")


def t_overrides(a):
    return (f"T.id.sideTitle = {js(a['side'][0][0])}; T.en.sideTitle = {js(a['side'][0][1])};\n"
            f"T.id.sideBody = {js(a['side'][1][0])}; T.en.sideBody = {js(a['side'][1][1])};\n"
            'T.id.refs = "Referensi"; T.en.refs = "References";\n'
            'T.id.refsNote = "Nomor dalam kurung siku di teks merujuk ke daftar ini. Tautan membuka sumber aslinya.";\n'
            'T.en.refsNote = "Numbers in square brackets in the text refer to this list. Links open the original source.";\n'
            'T.id.photo = "Foto"; T.en.photo = "Photo";\n'
            'T.id.priceLink = "Tanya harga via WhatsApp"; T.en.priceLink = "Ask for pricing on WhatsApp";\n'
            'T.id.share = "Bagikan"; T.en.share = "Share";\n'
            'T.id.copyLink = "Salin link"; T.en.copyLink = "Copy link";\n'
            'T.id.copied = "Link disalin"; T.en.copied = "Link copied";\n')


def seo_js(a):
    url = url_of(a["slug"])
    wc = word_count(a)
    n_h2 = sum(1 for b in a["blocks"] if b[0] == "h2")
    rows_id = [
        [f"Title tag ({len(a['meta_title'])} karakter)", a["meta_title"]],
        [f"Meta description ({len(a['meta_desc'])})", a["meta_desc"]],
        ["Slug", f"/artikel/{a['slug']}/"],
        ["Canonical", url],
        ["Kata kunci utama", a["keywords_primary"][0]],
        ["Kata kunci pendukung", a["keywords_secondary"][0]],
        ["Schema", "MedicalWebPage + Article (citation) · BreadcrumbList · FAQPage · MedicalBusiness"],
        ["Struktur heading", f"1 × H1 · {n_h2 + 2} × H2 (termasuk FAQ & Referensi)"],
        ["Referensi", f"{len(a['refs'])} sumber bernomor (jurnal, pedoman klinis, situs rumah sakit internasional)"],
        ["Versi tanpa JavaScript", "Ya — salinan HTML statis untuk crawler dan mesin AI"],
        ["Panjang", f"≈ {wc:,} kata (ID)".replace(",", ".")],
        ["Gambar", f"Unsplash — {a['image']['name']} (kredit di caption)"],
    ]
    rows_en = [
        [f"Title tag ({len(a['meta_title'])} chars)", a["meta_title"]],
        [f"Meta description ({len(a['meta_desc'])})", a["meta_desc"]],
        ["Slug", f"/artikel/{a['slug']}/"],
        ["Canonical", url],
        ["Primary keyword", a["keywords_primary"][1]],
        ["Supporting keywords", a["keywords_secondary"][1]],
        ["Schema", "MedicalWebPage + Article (citation) · BreadcrumbList · FAQPage · MedicalBusiness"],
        ["Heading structure", f"1 × H1 · {n_h2 + 2} × H2 (incl. FAQ & References)"],
        ["References", f"{len(a['refs'])} numbered sources (journals, clinical guidelines, international hospital sites)"],
        ["No-JavaScript version", "Yes — static HTML copy for crawlers and AI engines"],
        ["Length", f"≈ {wc:,} words (ID)"],
        ["Image", f"Unsplash — {a['image']['name']} (credited in caption)"],
    ]
    return f"const SEO = {js({'id': rows_id, 'en': rows_en})};\n"


# ---------------------------------------------------------------- hub page
def build_hub(arts, tpl):
    s = tpl
    url = url_of()
    title = "Artikel & Panduan Fisioterapi Berbasis Bukti | Physio8"
    desc = ("Panduan pemulihan berbasis bukti dari fisioterapis Physio8: nyeri punggung, leher kaku, cedera lari, "
            "padel, rehabilitasi ACL, dan kapan perlu ke fisioterapis.")
    ld = js({"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": url + "#blog", "url": url, "name": "Artikel & Panduan Physio8",
         "description": desc, "inLanguage": "id-ID", "author": AUTHOR, "publisher": PUBLISHER,
         "blogPost": [{"@type": "BlogPosting", "headline": a["title"][0], "url": url_of(a["slug"]),
                       "datePublished": a["published"], "dateModified": a["modified"],
                       "image": img(a, 1200, 630), "author": {"@type": "Person", "name": "Timothy Abieza"}}
                      for a in arts]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Beranda", "item": SITE_BASE},
            {"@type": "ListItem", "position": 2, "name": "Artikel", "item": url}]},
    ]})
    head = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#331079">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Physio8">
<meta property="og:locale" content="id_ID">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SHARE_IMAGE}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="1200">
<meta property="og:image:alt" content="Physio8 — studio fisioterapi di Gading Serpong">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SHARE_IMAGE}">
<link rel="icon" type="image/png" href="../favicon.png">
<link rel="apple-touch-icon" href="../favicon.png">
<script type="application/ld+json">
{ld}
</script>
<script src="../support.js"></script>"""
    s = re.sub(r"<helmet>.*?(<link rel=\"stylesheet\")", r"<helmet>\n\1", s, count=1, flags=re.S)
    s = re.sub(r"<script type=\"application/ld\+json\">.*?</script>\n", "", s, count=1, flags=re.S)
    s = re.sub(r"<head>.*?</head>", lambda m: "<head>\n" + head + "\n</head>", s, count=1, flags=re.S)
    s = s.replace('href="./p8/styles.css"', 'href="../p8/styles.css"').replace('src="./p8/', 'src="../p8/')
    s = s.replace('href="./Artikel Hub.dc.html"', 'href="./index.html"')
    s = s.replace('href="./index.html"', 'href="../index.html"')
    # the nav "Artikel" link (and any self link) should stay on this page
    s = s.replace('<a href="../index.html" style="color:var(--color-brand);font-weight:var(--weight-semibold);border-bottom:2px solid var(--color-energy)',
                  '<a href="./index.html" style="color:var(--color-brand);font-weight:var(--weight-semibold);border-bottom:2px solid var(--color-energy)')
    # drop the "9 panduan klinis · 2 bahasa" stat block from the hub hero
    s, n = re.subn(r'\n    <div style="display:flex;flex-direction:column;gap:var\(--space-4\);padding-bottom:[^"]*">.*?background:var\(--gradient-journey\)"></div>\n    </div>', '', s, count=1, flags=re.S)
    if n != 1:
        sys.exit("hub stats block not found")
    # copy: location is a fact, not the headline
    s = replace_once(s, ">Panduan pemulihan dari fisioterapis di Gading Serpong</h1>",
                     ">Panduan pemulihan dari fisioterapis Physio8</h1>", "hub h1")
    s = re.sub(r"Ditulis dan ditinjau oleh fisioterapis Physio8 yang praktik di Gading Serpong, BSD City\.",
               "Setiap klaim disertai referensi ke jurnal, pedoman klinis, atau situs rumah sakit internasional. Studio Physio8 berlokasi di Gading Serpong.", s)
    if "BSD" in s.split("<script type=\"text/x-dc\"")[0]:
        sys.exit("hub still mentions BSD")
    # featured + list cards: real links and photos
    s = replace_once(s, '<a href="./Artikel Detail.dc.html" style="display:grid', '<a href="{{ featured.href }}" style="display:grid', "hub featured link")
    s = replace_once(s, '<image-slot id="hub-featured" shape="rect" placeholder="Foto sesi asesmen — fisioterapis dan pasien di studio"></image-slot>',
                     '<image-slot id="hub-featured" shape="rect" placeholder="{{ featured.slotHint }}" src="{{ featured.img }}" credit="{{ featured.credit }}" credit-href="{{ featured.creditHref }}"></image-slot>',
                     "hub featured image")
    s = replace_once(s, '<a href="./Artikel Detail.dc.html" style="display:flex;flex-direction:column', '<a href="{{ a.href }}" style="display:flex;flex-direction:column', "hub list link")
    s = replace_once(s, '<image-slot id="{{ a.slotId }}" shape="rect" placeholder="{{ a.slotHint }}"></image-slot>',
                     '<image-slot id="{{ a.slotId }}" shape="rect" placeholder="{{ a.slotHint }}" src="{{ a.img }}" credit="{{ a.credit }}" credit-href="{{ a.creditHref }}"></image-slot>',
                     "hub list image")
    # footer topic links → the matching article
    topic = {"Nyeri punggung bawah": "nyeri-pinggang-duduk-lama", "Postur &amp; kerja kantor": "leher-kaku-kerja-kantor",
             "Cedera lari": "runners-knee-shin-splints-achilles", "Padel &amp; olahraga raket": "nyeri-bahu-padel",
             "Rehabilitasi pasca operasi": "rehabilitasi-pasca-operasi-acl"}
    for label, slug in topic.items():
        s = replace_once(s, f'<a href="../index.html">{label}</a>', f'<a href="./{slug}/index.html">{label}</a>', "topic " + slug)
    # data
    data = [{"slug": a["slug"], "tag": a["tag"][0], "tagEn": a["tag"][1], "read": a["read"],
             "date": a["date_label"][0], "dateEn": a["date_label"][1],
             "title": a["title"][0], "titleEn": a["title"][1],
             "excerpt": a["excerpt"][0], "excerptEn": a["excerpt"][1],
             "slotHint": a["image"]["alt"][0], "href": f"./{a['slug']}/index.html",
             "img": img(a, 900), "credit": credit(a), "creditHref": a["image"]["profile"]} for a in arts]
    s = re.sub(r"const ARTICLES = \[.*?\n\];\n", lambda m: f"const ARTICLES = {js(data)};\n", s, count=1, flags=re.S)
    s = replace_once(s, "      slotHint:a.slotHint\n    };",
                     "      slotHint:a.slotHint, href:a.href, img:a.img, credit:a.credit, creditHref:a.creditHref\n    };", "hub pick")
    # crawler-readable list
    nos = ['<noscript><section lang="id" style="max-width:760px;margin:0 auto;padding:24px 16px;font-family:system-ui,sans-serif">',
           '<h1>Artikel &amp; panduan fisioterapi Physio8</h1><ul>']
    for a in arts:
        nos.append(f'<li><a href="./{a["slug"]}/index.html">{esc(a["title"][0])}</a> — {esc(a["excerpt"][0])}</li>')
    nos.append("</ul><p>Physio8 · Ruko Hudson, Gading Serpong, Tangerang, Banten.</p></section></noscript>")
    s = replace_once(s, "</x-dc>\n", "</x-dc>\n" + "\n".join(nos) + "\n", "hub noscript")
    # responsive hooks + CSS
    for needle, cls in [
        ('padding:0 var(--layout-gutter);height:72px', "p8-hdr"),
        ('<nav style="display:flex;align-items:center;gap:var(--space-5);margin-left:var(--space-4)', "p8-nav"),
        ('<div style="display:flex;align-items:center;padding:3px;gap:2px;border:1px solid var(--border-subtle)', "p8-lang"),
        ('rel="noopener noreferrer" style="display:inline-flex;align-items:center;height:var(--control-h-md)', "p8-hdr-cta"),
        ('<h1 style="margin:0 0 var(--space-5)', "p8-h1"),
        ('grid-template-columns:minmax(0,1.35fr) minmax(0,1fr)', "p8-hubhero"),
        ('<div style="position:sticky;top:72px', "p8-filter"),
        ('grid-template-columns:minmax(0,1fr) minmax(0,1.1fr)', "p8-featured"),
        ('<div style="display:flex;gap:var(--space-6);align-items:flex-start;padding:var(--card-pad-lg);margin-bottom:var(--space-12)', "p8-authorbox p8-pad"),
        ('grid-template-columns:minmax(0,1.25fr) minmax(0,1fr)', "p8-book"),
        ('grid-template-columns:minmax(0,1.2fr) repeat(2,minmax(0,1fr))', "p8-footgrid"),
    ]:
        s = add_class(s, needle, cls)
    s = replace_once(s, "</style>\n</helmet>", RESPONSIVE_CSS + "</style>\n</helmet>", "hub css")
    s = s.replace("__WA_PRICE__", esc(wa_price_link()))
    return s


def redirect_stub(target, canonical, title):
    return f"""<!doctype html>
<html lang="id"><head><meta charset="utf-8">
<title>{esc(title)}</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{canonical}">
<meta http-equiv="refresh" content="0; url={target}">
</head><body><p>Halaman ini sudah pindah ke <a href="{target}">{target}</a>.</p></body></html>
"""


def build_sitemap(arts):
    """sitemap.xml (with image entries) + robots.txt at the repo root."""
    latest = max(a["modified"] for a in arts)
    urls = [(SITE_BASE, latest, "1.0", None), (url_of(), latest, "0.9", None)]
    urls += [(url_of(a["slug"]), a["modified"], "0.8", a) for a in arts]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for loc, mod, prio, a in urls:
        out.append(f"  <url>\n    <loc>{esc(loc)}</loc>\n    <lastmod>{mod}</lastmod>\n    <priority>{prio}</priority>")
        if a:
            out.append(f"    <image:image><image:loc>{esc(img(a, 1200, 630))}</image:loc></image:image>")
        out.append("  </url>")
    out.append("</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out))
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\nDisallow: /_src/\nDisallow: /_export/\n\n"
        f"Sitemap: {SITE_BASE}sitemap.xml\n")
    return len(urls)


def main():
    arts = load_articles()
    bys = {a["slug"]: a for a in arts}
    for a in arts:
        check_citations(a)
        for r in a["related"]:
            if r not in bys:
                sys.exit(f"{a['slug']}: unknown related slug {r}")
    tpl_a = open(os.path.join(SRC, "template-artikel.dc.html"), encoding="utf-8").read()
    tpl_h = open(os.path.join(SRC, "template-hub.dc.html"), encoding="utf-8").read()
    written = []
    for a in arts:
        out = os.path.join(ROOT, "artikel", a["slug"], "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(build_article(a, bys, tpl_a))
        written.append((out, word_count(a), len(a["refs"])))
    hub = os.path.join(ROOT, "artikel", "index.html")
    open(hub, "w", encoding="utf-8").write(build_hub(arts, tpl_h))
    open(os.path.join(ROOT, "Artikel Hub.dc.html"), "w", encoding="utf-8").write(
        redirect_stub("./artikel/index.html", url_of(), "Artikel — Physio8"))
    open(os.path.join(ROOT, "Artikel Detail.dc.html"), "w", encoding="utf-8").write(
        redirect_stub("./artikel/kapan-perlu-fisioterapi/index.html", url_of("kapan-perlu-fisioterapi"), "Kapan nyeri butuh fisioterapi — Physio8"))
    for path, wc, nref in written:
        print(f"{os.path.relpath(path, ROOT):55s} {wc:5d} words  {nref} refs")
    print("artikel/index.html (hub) + 2 redirect stubs")
    print(f"sitemap.xml ({build_sitemap(arts)} URLs) + robots.txt")


if __name__ == "__main__":
    main()
