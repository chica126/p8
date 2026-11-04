"""Extra CSS for the article hub and article pages (on top of the homepage CSS)."""
PAGE_CSS = r"""
/* reading progress */
.hdr .progress{position:absolute;left:0;right:0;bottom:-1px;height:3px;background:transparent}
.hdr .progress i{display:block;height:100%;width:0;background:linear-gradient(90deg,#2F1F71,#008699 55%,#A6B717);transition:width .1s linear}

/* breadcrumb */
.crumbs{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:14px;color:var(--muted);margin-bottom:22px}
.crumbs a{color:var(--muted)}
.crumbs a:hover{color:var(--purple)}
.crumbs .sl{color:var(--faint)}

/* article hero */
.art-hero{padding:clamp(28px,4vw,48px) 0 0}
.art-title{font-size:clamp(34px,4.6vw,56px);font-weight:800;letter-spacing:-.03em;line-height:1.08;max-width:920px}
.art-dek{font-size:clamp(18px,1.8vw,21px);color:var(--muted);max-width:780px;margin-top:20px;line-height:1.6}
.byline{display:flex;align-items:center;justify-content:space-between;gap:18px 28px;flex-wrap:wrap;margin-top:30px;padding:18px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.by-who{display:flex;align-items:center;gap:14px}
.by-who img{width:48px;height:48px;border-radius:50%;object-fit:cover}
.by-who b{display:block;color:var(--ink);font-size:15.5px}
.by-who span{display:block;font-size:14px;color:var(--muted)}
.share{display:flex;align-items:center;gap:10px}
.share .lbl{font-size:14px;font-weight:600;color:var(--muted);margin-right:2px}
.share a,.share button{width:42px;height:42px;border-radius:50%;border:1px solid var(--line);background:#fff;color:var(--purple);display:inline-flex;align-items:center;justify-content:center;cursor:pointer;transition:all .2s ease;padding:0}
.share a:hover,.share button:hover{background:var(--purple);border-color:var(--purple);color:#fff}
.share svg{width:18px;height:18px}
.art-photo{aspect-ratio:2/1;margin-top:32px}
.toast{position:fixed;left:50%;bottom:32px;transform:translateX(-50%);background:var(--ink);color:#fff;font-size:14px;font-weight:500;padding:12px 22px;border-radius:999px;z-index:90;opacity:0;pointer-events:none;transition:opacity .25s ease}
.toast.show{opacity:1}

/* article body */
.art-body{padding:clamp(40px,5vw,64px) 0 0}
.art-grid{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:clamp(32px,6vw,80px);align-items:start}
.prose{max-width:740px;min-width:0}
.prose > h2{font-size:clamp(24px,2.6vw,30px);margin:52px 0 16px;scroll-margin-top:110px}
.prose > p{font-size:18px;line-height:1.75;margin:0 0 18px;color:var(--body)}
.prose ul.list,.prose ol.list{margin:0 0 22px;display:grid;gap:10px}
.prose ul.list li{position:relative;padding-left:24px;font-size:17.5px;line-height:1.65}
.prose ul.list li::before{content:"";position:absolute;left:4px;top:.72em;width:7px;height:7px;border-radius:50%;background:var(--teal)}
.prose ol.list{counter-reset:n}
.prose ol.list li{position:relative;padding-left:40px;font-size:17.5px;line-height:1.65;counter-increment:n}
.prose ol.list li::before{content:counter(n);position:absolute;left:0;top:1px;width:26px;height:26px;border-radius:50%;background:var(--purple-50);color:var(--purple);font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center}
.cite{font-size:.72em;font-weight:700;color:var(--teal-text);vertical-align:super;line-height:0;margin-left:1px;white-space:nowrap}
.cite:hover{color:var(--purple)}
.summary{background:var(--purple-50);border-radius:var(--radius);padding:28px 30px;margin-bottom:12px}
.summary h2{font-size:20px;margin-bottom:14px}
.summary ul{display:grid;gap:12px}
.summary li{display:grid;grid-template-columns:22px minmax(0,1fr);gap:10px;font-size:16.5px;line-height:1.6;color:var(--body)}
.summary li svg{width:20px;height:20px;color:var(--teal);margin-top:2px}
.tbl{overflow-x:auto;margin:6px 0 24px;border:1px solid var(--line);border-radius:18px}
.tbl table{width:100%;border-collapse:collapse;font-size:15.5px;min-width:520px}
.tbl th,.tbl td{text-align:left;padding:14px 16px;border-top:1px solid var(--line);vertical-align:top;line-height:1.5}
.tbl thead th{border-top:0;background:var(--surface);font-size:14px;font-weight:600;color:var(--ink)}
.tbl td:first-child{font-weight:600;color:var(--ink)}
.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:6px 0 24px}
.stats div{background:var(--surface);border-radius:18px;padding:20px}
.stats b{display:block;font-size:34px;font-weight:700;letter-spacing:-.02em;color:var(--purple);line-height:1}
.stats span{display:block;margin-top:8px;font-size:14.5px;color:var(--muted);line-height:1.4}
.callout{border:1px solid var(--line);border-radius:20px;padding:22px 24px;margin:6px 0 24px}
.callout > p{font-weight:600;color:var(--ink);margin-bottom:10px}
.callout dl{margin:0;display:grid}
.callout .row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:6px 20px;padding:12px 0;border-top:1px solid var(--line)}
.callout .row:first-child{border-top:0}
.callout dt{font-weight:600;color:var(--ink);font-size:15.5px}
.callout dd{margin:0;color:var(--body);font-size:15.5px}
.prose details{border-top:1px solid var(--line)}
.prose details:last-of-type{border-bottom:1px solid var(--line)}
.prose summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:16px;align-items:center;padding:18px 0;font-size:17px;font-weight:600;color:var(--ink)}
.prose summary::-webkit-details-marker{display:none}
.prose summary svg{width:20px;height:20px;flex:0 0 auto;color:var(--purple);transition:transform .2s ease}
.prose details[open] summary svg{transform:rotate(45deg)}
.prose details p{padding:0 0 20px;color:var(--muted);font-size:16.5px;line-height:1.7}
.refs{display:grid;gap:10px;counter-reset:r;font-size:14.5px;color:var(--muted)}
.refs li{position:relative;padding-left:38px;line-height:1.55;scroll-margin-top:110px}
.refs li::before{counter-increment:r;content:"[" counter(r) "]";position:absolute;left:0;top:0;font-weight:700;color:var(--teal-text)}
.refs li:target{background:var(--lime-50);border-radius:8px}
.refs a{color:var(--purple);word-break:break-all}
.prose > p.refs-note{font-size:15px;color:var(--muted);margin:0 0 16px}
.author{display:grid;grid-template-columns:72px minmax(0,1fr);gap:20px;background:var(--surface);border-radius:var(--radius);padding:26px;margin-top:48px}
.author img{width:72px;height:72px;border-radius:50%;object-fit:cover}
.author .k{font-size:13.5px;font-weight:600;color:var(--teal-text)}
.author b{display:block;font-size:19px;color:var(--ink);margin-top:2px}
.author .role{font-size:14.5px;color:var(--muted)}
.author p.bio{margin-top:12px;font-size:15.5px;line-height:1.65;color:var(--body)}
.author p.cred{margin-top:10px;font-size:13.5px;color:var(--muted);line-height:1.6}
.prose > p.disc-note{margin:28px 0 0;font-size:13.5px;color:var(--faint);line-height:1.65}
.share-end{margin-top:36px;padding-top:24px;border-top:1px solid var(--line)}

/* aside */
.art-aside{position:sticky;top:108px;display:grid;grid-template-columns:minmax(0,1fr);gap:16px}
.art-aside > *{min-width:0}
.toc{border:1px solid var(--line);border-radius:20px;padding:22px}
.toc p{font-size:13.5px;font-weight:600;color:var(--muted);margin-bottom:12px}
.toc ol{display:grid;gap:4px}
.toc a{display:block;overflow-wrap:anywhere;font-size:14.5px;line-height:1.45;color:var(--body);padding:6px 10px;border-radius:10px;border-left:2px solid transparent}
.toc a:hover{background:var(--surface);color:var(--purple)}
.toc a.on{color:var(--purple);font-weight:600;background:var(--purple-50)}
.side-cta{background:var(--purple);color:#CBC3E8;border-radius:20px;padding:24px}
.side-cta b{display:block;color:#fff;font-size:19px;line-height:1.3}
.side-cta p{margin-top:8px;font-size:15px;line-height:1.6}
.side-cta .btn{margin-top:16px;width:100%;height:46px;font-size:15px}

/* related + hub grid */
.rel,.hub-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.hub-hero{padding:clamp(28px,4vw,48px) 0 0}
.hub-hero h1{font-size:clamp(36px,4.8vw,58px);font-weight:800;letter-spacing:-.03em;line-height:1.06;max-width:820px}
.hub-tools{display:flex;flex-wrap:wrap;align-items:center;gap:14px 20px;margin:36px 0 28px;padding:18px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.search{position:relative;flex:1 1 280px;max-width:380px}
.search svg{position:absolute;left:16px;top:50%;transform:translateY(-50%);width:18px;height:18px;color:var(--muted)}
.search input{width:100%;height:48px;border-radius:999px;border:1px solid var(--line-strong);padding:0 18px 0 44px;font:500 15px var(--font);color:var(--ink);background:#fff}
.search input:focus{outline:none;border-color:var(--purple);box-shadow:0 0 0 3px var(--purple-50)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips button{font:500 14px var(--font);height:38px;padding:0 16px;border-radius:999px;border:1px solid var(--line-strong);background:#fff;color:var(--body);cursor:pointer}
.chips button[aria-pressed="true"]{background:var(--purple);border-color:var(--purple);color:#fff}
.count{margin-left:auto;font-size:14px;color:var(--muted)}
.empty{display:none;padding:40px 0;color:var(--muted);font-size:16px}
.acard[hidden]{display:none}

@media (max-width:1080px){
  .art-grid{grid-template-columns:minmax(0,1fr)}
  .art-aside{position:static;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .rel,.hub-grid{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
}
@media (max-width:640px){
  .art-aside{grid-template-columns:minmax(0,1fr)}
  .toc{display:none}
  .art-photo{aspect-ratio:4/3}
  .prose > p{font-size:17px}
  .stats{grid-template-columns:minmax(0,1fr)}
  .callout .row{grid-template-columns:minmax(0,1fr)}
  .author{grid-template-columns:minmax(0,1fr)}
  .rel,.hub-grid{grid-template-columns:minmax(0,1fr)}
  .count{margin-left:0}
}
"""
