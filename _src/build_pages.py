#!/usr/bin/env python3
"""
Article hub (/artikel/) and article pages (/artikel/<slug>/) in the same design
system and voice as the homepage: shared header, footer, CSS, ID/EN toggle and
WhatsApp CTAs. Static HTML (no client-side rendering), so the full article text is
in the page for search and AI engines.

Called from build.py. Article content lives in _src/articles/*.py.
"""
import html, json, os, re
from urllib.parse import quote

import build
import build_home as H
from build_home import en, icon, WA_GLYPH, wa_pair, wa_cta
from page_css import PAGE_CSS

SITE = build.SITE_BASE
AUTHOR_IMG = "/p8/author-timothy.jpeg"
UTM = "utm_source=physio8&utm_medium=referral"


def esc(s):
    return html.escape(s, quote=True)


def rich(s):
    """Escape article text and turn [n] citations into links to the reference list."""
    t = esc(s)
    return re.sub(r"\[(\d+)\]", lambda m: f'<a class="cite" href="#ref-{m.group(1)}">[{m.group(1)}]</a>', t)


def T(id_html, en_html, tag="span", cls="", extra=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c}{extra} data-en="{esc(en_html)}">{id_html}</{tag}>'


def subpage(s):
    """Homepage header/footer → absolute links for pages under /artikel/."""
    s = s.replace('href="#', 'href="/#').replace('href="/#main"', 'href="#main"')
    s = s.replace('href="/#artikel"', 'href="/artikel/"')
    s = s.replace('src="./p8/', 'src="/p8/')
    return s


def wa_article(a):
    src = a["wa"]
    return (build.wa_link(src),
            f"https://wa.me/{build.WA_NUMBER}?text=" + quote(f"Hi Physio8, I would like to book an assessment. (from {src})", safe=""))


def wa_btn(pair, label_id, label_en, cls="btn btn-primary"):
    return (f'<a class="{cls}" href="{esc(pair[0])}" data-en-href="{esc(pair[1])}" target="_blank" rel="noopener noreferrer">'
            f'{WA_GLYPH}{T(label_id, label_en)}</a>')


def card(a, w=800, h=500):
    d = build.fmt_date_short(a["published"])
    im = a["image"]
    heads = " ".join(b[2] + " " + b[3] for b in a.get("blocks", []) if b and b[0] == "h2")
    summ = " ".join(a.get("keywords_primary", []) + a.get("keywords_secondary", []))
    hay = esc((a["title"][0] + " " + a["title"][1] + " " + a["excerpt"][0] + " " + a["excerpt"][1] + " " + a["tag"][0] + " " + a["tag"][1] + " " + heads + " " + summ).lower())
    return (f'<a class="acard rv" href="/artikel/{a["slug"]}/" data-tag="{esc(a["tag"][0])}" data-q="{hay}">'
            f'<figure class="photo"><img src="{esc(build.img(a, w, h))}" width="{w}" height="{h}" alt="{esc(im["alt"][0])}" data-en-alt="{esc(im["alt"][1])}" loading="lazy" decoding="async">'
            f'<figcaption class="credit">{T("Foto", "Photo")}: {esc(im["name"])} / Unsplash</figcaption></figure>'
            f'<div class="body"><p class="meta">{T(esc(a["tag"][0]) + " · " + d[0], esc(a["tag"][1]) + " · " + d[1])}</p>'
            f'<h3 data-en="{esc(a["title"][1])}">{esc(a["title"][0])}</h3><p class="ex" data-en="{esc(a["excerpt"][1])}">{esc(a["excerpt"][0])}</p>'
            f'<span class="link-arrow more">{T("Baca selengkapnya", "Read more")}{icon("arrow")}</span></div></a>')


# ------------------------------------------------------------------ article blocks
def block(b):
    k = b[0]
    if k == "h2":
        return f'<h2 id="{b[1]}" data-en="{esc(b[3])}">{esc(b[2])}</h2>'
    if k == "p":
        return f'<p data-en="{esc(rich(b[2]))}">{rich(b[1])}</p>'
    if k in ("ul", "ol"):
        items = "".join(f'<li data-en="{esc(rich(x[1]))}">{rich(x[0])}</li>' for x in b[1])
        return f'<{k} class="list">{items}</{k}>'
    if k == "table":
        rows = b[1]
        n = len(rows[0]) // 2
        head = "".join(f'<th scope="col" data-en="{esc(rows[0][n + j])}">{esc(rows[0][j])}</th>' for j in range(n))
        body = ""
        for r in rows[1:]:
            body += "<tr>" + "".join(f'<td data-en="{esc(rich(r[n + j]))}">{rich(r[j])}</td>' for j in range(n)) + "</tr>"
        return f'<div class="tbl"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
    if k == "stats":
        return '<div class="stats">' + "".join(f'<div><b>{esc(x[0])}</b><span data-en="{esc(x[2])}">{esc(x[1])}</span></div>' for x in b[1]) + "</div>"
    if k == "callout":
        rows = "".join(f'<div class="row"><dt data-en="{esc(r[2])}">{esc(r[0])}</dt><dd data-en="{esc(rich(r[3]))}">{rich(r[1])}</dd></div>' for r in b[3])
        return f'<div class="callout"><p data-en="{esc(b[2])}">{esc(b[1])}</p><dl>{rows}</dl></div>'
    raise ValueError("unknown block " + k)


SHARE_ICONS = {
    "link": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    "li": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"/></svg>',
}


def share(a):
    url = build.url_of(a["slug"])
    wa = "https://wa.me/?text=" + quote(a["title"][0] + " — " + url, safe="")
    li = "https://www.linkedin.com/sharing/share-offsite/?url=" + quote(url, safe="")
    return (f'<div class="share">{T("Bagikan", "Share", cls="lbl")}'
            f'<button type="button" class="copy" data-url="{url}" aria-label="Salin tautan" data-en-aria-label="Copy link" title="Salin tautan" data-en-title="Copy link">{SHARE_ICONS["link"]}</button>'
            f'<a href="{esc(wa)}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp" title="WhatsApp">{WA_GLYPH}</a>'
            f'<a href="{esc(li)}" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" title="LinkedIn">{SHARE_ICONS["li"]}</a></div>')


AUTHOR_TXT = {
    "role": ("Contributing Writer · Athletic Trainer &amp; Physiotherapist", "Contributing Writer · Athletic Trainer &amp; Physiotherapist"),
    "bio": ("Athletic trainer dan fisioterapis dengan sepuluh tahun pengalaman klinis dan lapangan. Saat ini menjabat sebagai Athletic Trainer di Jakarta Intercultural School. Sebelumnya, ia bekerja sebagai fisioterapis di PhysioActive serta Eastwest Physiotherapy &amp; Rehabilitation, dan selama empat tahun menangani sisi medis Persatuan Rugby Union Indonesia. Fokusnya adalah return to sport, cedera olahraga, dan concussion assessment.",
            "An athletic trainer and physiotherapist with ten years of clinical and sideline practice. Currently Athletic Trainer at Jakarta Intercultural School, previously a physical therapist at PhysioActive and Eastwest Physiotherapy &amp; Rehabilitation, and four years on the medical side of Persatuan Rugby Union Indonesia. His focus is return to sport, sports injuries and concussion assessment."),
    "cred": ("B.Sc. Physical Therapy, Saxion University of Applied Sciences · Sport Performance Enhancement, HAN University of Applied Sciences · FAIR · ICIR · CPR &amp; AED · Penulis “The Miseducation of DOMS”",
             "B.Sc. Physical Therapy, Saxion University of Applied Sciences · Sport Performance Enhancement, HAN University of Applied Sciences · FAIR · ICIR · CPR &amp; AED · Author of “The Miseducation of DOMS”"),
}


def page(head, body, meta, extra_js=""):
    js = H.JS.replace("__META__", json.dumps(meta, ensure_ascii=False)).replace("__ICONX__", json.dumps(icon("x")))
    css = (H.CSS + PAGE_CSS).replace(".rv{opacity:0", "html.js .rv{opacity:0").replace(".rv.in{", "html.js .rv.in{")
    return f"""<!doctype html>
<html lang="id">
<head>
{head}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap">
<link rel="preconnect" href="https://images.unsplash.com">
<script>document.documentElement.classList.add('js')</script>
<style>{css}</style>
</head>
<body>
{body}
<script>{js}</script>
<script>{extra_js}</script>
</body>
</html>
"""


ARTICLE_JS = r"""
(function(){
  var d=document, bar=d.querySelector('.hdr .progress i'), art=d.querySelector('.prose');
  function prog(){ if(!art||!bar) return; var r=art.getBoundingClientRect(), h=r.height-window.innerHeight*0.6;
    var p=Math.min(1,Math.max(0,(-r.top+120)/Math.max(h,1))); bar.style.width=(p*100)+'%'; }
  window.addEventListener('scroll',prog,{passive:true}); prog();
  var links=[].slice.call(d.querySelectorAll('.toc a')), heads=links.map(function(a){return d.getElementById(a.getAttribute('href').slice(1))});
  function spy(){ var cur=0; heads.forEach(function(h,i){ if(h && h.getBoundingClientRect().top<140) cur=i; });
    links.forEach(function(a,i){a.classList.toggle('on',i===cur)}); }
  window.addEventListener('scroll',spy,{passive:true}); spy();
  var toast=d.querySelector('.toast');
  d.querySelectorAll('.share .copy').forEach(function(b){ b.addEventListener('click',function(){
    var u=b.getAttribute('data-url'); function done(){ if(toast){toast.classList.add('show'); setTimeout(function(){toast.classList.remove('show')},1800);} }
    if(navigator.clipboard){navigator.clipboard.writeText(u).then(done,done)} else { var t=d.createElement('textarea'); t.value=u; d.body.appendChild(t); t.select(); try{d.execCommand('copy')}catch(e){} d.body.removeChild(t); done(); }
  }); });
})();
"""

HUB_JS = r"""
(function(){
  var d=document, cards=[].slice.call(d.querySelectorAll('.hub-grid .acard')), q=d.getElementById('q'),
      chips=[].slice.call(d.querySelectorAll('.chips button')), cnt=d.querySelector('.count b'), empty=d.querySelector('.empty'), tag='';
  function run(){ var s=(q.value||'').trim().toLowerCase(), n=0;
    cards.forEach(function(c){ var ok=(!tag||c.getAttribute('data-tag')===tag)&&(!s||c.getAttribute('data-q').indexOf(s)>-1); c.hidden=!ok; if(ok){n++; c.classList.add('in')} });
    cnt.textContent=n; empty.style.display=n?'none':'block'; }
  q.addEventListener('input',run);
  chips.forEach(function(b){ b.addEventListener('click',function(){ tag=b.getAttribute('data-tag'); chips.forEach(function(x){x.setAttribute('aria-pressed',String(x===b))}); run(); }); });
})();
"""


def build_article(a, bys):
    head = build.article_head(a, bys).replace('\n<script src="../../support.js"></script>', "")
    pub_id, pub_en = build.fmt_date_id(a["published"]), build.fmt_date_en(a["published"])
    mod_id, mod_en = build.fmt_date_id(a["modified"]), build.fmt_date_en(a["modified"])
    hdr = subpage(H.header()).replace("</header>", '<div class="progress" aria-hidden="true"><i></i></div></header>', 1)
    im = a["image"]
    prof = im["profile"] + "?" + UTM
    toc = [(b[1], b[2], b[3]) for b in a["blocks"] if b[0] == "h2"] + [("faq", "Pertanyaan yang sering muncul", "Frequently asked questions"), ("referensi", "Referensi", "References")]
    toc_html = "".join(f'<li><a href="#{i}" data-en="{esc(e)}">{esc(t)}</a></li>' for i, t, e in toc)
    summary = "".join(f'<li>{icon("ccheck")}<span data-en="{esc(rich(t[1]))}">{rich(t[0])}</span></li>' for t in a["takeaways"])
    blocks = "\n".join(block(b) for b in a["blocks"])
    faqs = "".join(f'<details><summary><span data-en="{esc(f[1])}">{esc(f[0])}</span>{icon("plus")}</summary><p data-en="{esc(f[3])}">{esc(f[2])}</p></details>' for f in a["faqs"])
    refs = "".join(f'<li id="ref-{n}">{esc(r[0])} <a href="{esc(r[1])}" target="_blank" rel="noopener">{esc(r[1].replace("https://", ""))}</a></li>' for n, r in enumerate(a["refs"], 1))
    rel = "".join(card(bys[s]) for s in a["related"])
    wap = wa_article(a)
    body = f"""{hdr}
<main id="main">
<section class="art-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/" data-en="Home">Beranda</a><span class="sl">/</span><a href="/artikel/" data-en="Articles">Artikel</a><span class="sl">/</span><span data-en="{esc(a['tag'][1])}">{esc(a['tag'][0])}</span></nav>
    <p class="eyebrow" data-en="{esc(a['tag'][1])}">{esc(a['tag'][0])}</p>
    <h1 class="art-title" data-en="{esc(a['title'][1])}">{esc(a['title'][0])}</h1>
    <p class="art-dek" data-en="{esc(a['dek'][1])}">{esc(a['dek'][0])}</p>
    <div class="byline">
      <div class="by-who"><img src="{AUTHOR_IMG}" width="48" height="48" alt="Timothy Abieza"><div><b>Timothy Abieza, B.Sc. PT</b>{T(f"Terbit {pub_id} · Diperbarui {mod_id}", f"Published {pub_en} · Updated {mod_en}")}</div></div>
      {share(a)}
    </div>
    <figure class="photo art-photo"><img src="{esc(build.img(a, 1600, 800))}" srcset="{esc(build.img(a, 800, 400))} 800w, {esc(build.img(a, 1600, 800))} 1600w" sizes="(max-width: 1200px) 100vw, 1200px" width="1600" height="800" alt="{esc(im['alt'][0])}" data-en-alt="{esc(im['alt'][1])}" fetchpriority="high" decoding="async">
      <figcaption class="credit">{T("Foto", "Photo")}: <a href="{esc(prof)}" target="_blank" rel="noopener">{esc(im['name'])}</a> / <a href="https://unsplash.com/?{esc(UTM)}" target="_blank" rel="noopener">Unsplash</a></figcaption></figure>
  </div>
</section>
<section class="art-body">
  <div class="wrap art-grid">
    <article class="prose">
      <div class="summary"><h2 data-en="Summary">Ringkasan</h2><ul>{summary}</ul></div>
      {blocks}
      <h2 id="faq" data-en="Frequently asked questions">Pertanyaan yang sering muncul</h2>
      {faqs}
      {wa_cta("Punya pertanyaan tentang kondisimu?", "Have a question about your condition?", "Tanyakan ke fisioterapis", "Ask a physiotherapist", wap)}
      <h2 id="referensi" data-en="References">Referensi</h2>
      <p class="refs-note" data-en="Numbers in square brackets in the text refer to this list.">Nomor dalam kurung siku di dalam teks merujuk ke daftar ini.</p>
      <ol class="refs">{refs}</ol>
      <div class="author"><img src="{AUTHOR_IMG}" width="72" height="72" alt="Timothy Abieza" loading="lazy"><div>
        <p class="k" data-en="About the author">Tentang penulis</p><b>Timothy Abieza, B.Sc. PT</b>
        <p class="role" data-en="{esc(AUTHOR_TXT['role'][1])}">{AUTHOR_TXT['role'][0]}</p>
        <p class="bio" data-en="{esc(AUTHOR_TXT['bio'][1])}">{AUTHOR_TXT['bio'][0]}</p>
        <p class="cred" data-en="{esc(AUTHOR_TXT['cred'][1])}">{AUTHOR_TXT['cred'][0]}</p></div></div>
      <div class="share-end">{share(a)}</div>
      <p class="disc-note" data-en="This article is educational and does not replace an in-person clinical assessment. Treatment decisions are always based on individual examination. For a suspected fracture, tendon rupture, chest pain, or loss of bladder or bowel control, contact emergency care.">Artikel ini bersifat edukatif dan bukan pengganti pemeriksaan klinis langsung. Keputusan penanganan selalu didasarkan pada pemeriksaan individual. Untuk dugaan patah tulang, ruptur tendon, nyeri dada, atau kehilangan kontrol buang air, hubungi layanan medis darurat.</p>
    </article>
    <aside class="art-aside">
      <nav class="toc" aria-label="Isi artikel" data-en-aria-label="On this page"><p data-en="On this page">Isi artikel</p><ol>{toc_html}</ol></nav>
      <div class="side-cta"><b data-en="{esc(a['side'][0][1])}">{esc(a['side'][0][0])}</b><p data-en="{esc(a['side'][1][1])}">{esc(a['side'][1][0])}</p>
        {wa_btn(wap, "Jadwalkan via WhatsApp", "Book on WhatsApp", "btn btn-white")}</div>
    </aside>
  </div>
</section>
<section class="sec" id="terkait">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow" data-en="Keep reading">Baca juga</p><h2 class="h2" data-en="More articles for you">Artikel lainnya untukmu</h2></div>
      <p><a class="link-arrow" href="/artikel/">{T("Lihat semua artikel", "See all articles")}{icon("arrow")}</a></p></div>
    <div class="rel">{rel}</div>
  </div>
</section>
{H.booking()}
</main>
{subpage(H.footer())}
<div class="toast" role="status" aria-live="polite" data-en="Link copied">Tautan disalin</div>"""
    meta = {"id": {"title": a["meta_title"], "desc": a["meta_desc"]},
            "en": {"title": a["title"][1] + " | Physio8", "desc": a["excerpt"][1]}}
    return page(head, body, meta, ARTICLE_JS)


def build_hub(arts):
    url = build.url_of()
    title = "Tips dan Panduan Seputar Cedera dari Fisioterapis | Physio8"
    desc = ("Tips dan panduan dari fisioterapis Physio8: cedera olahraga, nyeri punggung, leher kaku, cedera lari, "
            "padel, rehabilitasi ACL, dan kapan perlu ke fisioterapis. Lengkap dengan rujukan jurnal.")
    ld = build.js({"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": url + "#blog", "url": url, "name": "Artikel & Panduan Physio8",
         "description": desc, "inLanguage": "id-ID", "author": build.AUTHOR, "publisher": build.PUBLISHER,
         "blogPost": [{"@type": "BlogPosting", "headline": a["title"][0], "url": build.url_of(a["slug"]),
                       "datePublished": a["published"], "dateModified": a["modified"],
                       "image": build.img(a, 1200, 630), "author": {"@type": "Person", "name": "Timothy Abieza"}}
                      for a in arts]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Beranda", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Artikel", "item": url}]},
    ]})
    head = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#2F1F71">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Physio8">
<meta property="og:locale" content="id_ID">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{build.SHARE_IMAGE}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Fasad klinik Physio8 di Paramount Gading Serpong">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{build.SHARE_IMAGE}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script type="application/ld+json">
{ld}
</script>"""
    tags = []
    for a in arts:
        if a["tag"] not in tags:
            tags.append(a["tag"])
    chips = f'<button type="button" data-tag="" aria-pressed="true" data-en="All">Semua</button>' + "".join(
        f'<button type="button" data-tag="{esc(t[0])}" aria-pressed="false" data-en="{esc(t[1])}">{esc(t[0])}</button>' for t in tags)
    cards = "".join(card(a) for a in arts)
    gen = wa_pair("Halo Physio8, saya punya pertanyaan setelah membaca artikel di website.", "Hi Physio8, I have a question after reading an article on your website.")
    body = f"""{subpage(H.header())}
<main id="main">
<section class="hub-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/" data-en="Home">Beranda</a><span class="sl">/</span><span data-en="Articles">Artikel</span></nav>
    <p class="eyebrow" data-en="Articles">Artikel</p>
    <h1 data-en="Tips and guides on injuries">Tips dan panduan seputar cedera</h1>
    <p class="lede" data-en="Written by our physiotherapists, with journal references. Find answers about your pain, how long recovery takes and when it is time to get checked.">Ditulis oleh fisioterapis kami, lengkap dengan rujukan jurnal. Temukan jawaban seputar nyeri yang kamu alami, berapa lama pemulihannya, dan kapan perlu diperiksa.</p>
  </div>
</section>
<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="hub-tools">
      <label class="search">{icon("search")}<span class="sr" data-en="Search articles">Cari artikel</span><input id="q" type="search" placeholder="Cari keluhan, misalnya nyeri lutut" data-en-placeholder="Search, e.g. knee pain" autocomplete="off"></label>
      <div class="chips" role="group" aria-label="Kategori" data-en-aria-label="Category">{chips}</div>
      <p class="count"><b>{len(arts)}</b> {T("artikel", "articles")}</p>
    </div>
    <div class="hub-grid">{cards}</div>
    <p class="empty" data-en="No matching articles yet. Try another keyword, or ask us directly on WhatsApp.">Belum ada artikel yang cocok. Coba kata kunci lain, atau tanyakan langsung melalui WhatsApp.</p>
    {wa_cta("Tidak menemukan yang kamu cari?", "Can't find what you are looking for?", "Tanyakan ke fisioterapis", "Ask a physiotherapist", gen)}
  </div>
</section>
{H.booking()}
</main>
{subpage(H.footer())}"""
    meta = {"id": {"title": title, "desc": desc},
            "en": {"title": "Tips and Guides on Injuries from Physiotherapists | Physio8",
                   "desc": "Guides from Physio8 physiotherapists on sports injuries, back pain, stiff necks, running injuries, padel, ACL rehab and when to see a physiotherapist."}}
    return page(head, body, meta, HUB_JS)
