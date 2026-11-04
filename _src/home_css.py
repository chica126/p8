CSS = r"""
:root{
  --purple:#2F1F71;--purple-700:#261859;--purple-900:#1A1142;--purple-50:#F4F2FA;--purple-100:#E7E3F4;--purple-200:#CBC3E8;
  --teal:#008699;--teal-text:#00707F;--teal-50:#E6F4F6;
  --lime:#A6B717;--lime-text:#6C7800;--lime-50:#F6F8E3;
  --ink:#1A1142;--body:#3B3752;--muted:#686480;--faint:#9A97AE;
  --bg:#FFFFFF;--surface:#F7F6FA;--surface-2:#EFEDF5;--line:#E5E2EE;--line-strong:#D3CFE0;
  --radius:24px;--radius-sm:14px;--pill:999px;
  --max:1200px;--gutter:clamp(16px,4vw,32px);--sec:clamp(64px,9vw,120px);
  --font:"Plus Jakarta Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --shadow:0 1px 2px rgba(26,17,66,.06),0 8px 24px rgba(26,17,66,.06);
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;font-family:var(--font);font-size:17px;line-height:1.65;color:var(--body);background:var(--bg);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
img,svg{display:block;max-width:100%}
figure{margin:0}
a{color:var(--purple);text-decoration:none}
a:hover{color:var(--teal-text)}
:focus-visible{outline:3px solid var(--teal);outline-offset:3px;border-radius:6px}
h1,h2,h3,h4{color:var(--ink);margin:0;line-height:1.15;letter-spacing:-.02em;font-weight:700;text-wrap:balance}
p{margin:0;text-wrap:pretty}
ul,ol{margin:0;padding:0;list-style:none}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--gutter)}
.sec{padding:var(--sec) 0 0}
.sec.tint,.sec.dark,.sec:has(+ .tint),.sec:has(+ .dark),.sec:last-child{padding-bottom:var(--sec)}
.sec.tint{background:var(--surface)}
.eyebrow{display:flex;align-items:center;gap:10px;font-size:14px;font-weight:600;color:var(--teal-text);margin-bottom:16px}
.eyebrow::before{content:"";width:22px;height:2px;border-radius:2px;background:var(--lime)}
.h2{font-size:clamp(30px,4vw,46px);font-weight:700}
.lede{font-size:clamp(17px,1.6vw,19px);color:var(--muted);max-width:640px;margin-top:18px}
.sec-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:end;margin-bottom:56px}
.sec-head .lede{margin-top:0}
.skip{position:absolute;left:-9999px;top:8px;background:var(--purple);color:#fff;padding:10px 16px;border-radius:var(--pill);z-index:100}
.skip:focus{left:8px;color:#fff}
.tnum{font-variant-numeric:tabular-nums}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;height:52px;padding:0 26px;border-radius:var(--pill);font-weight:600;font-size:16px;line-height:1;white-space:nowrap;transition:background .2s ease,color .2s ease,border-color .2s ease,transform .2s ease;border:1.5px solid transparent}
.btn svg{width:20px;height:20px;flex:0 0 auto}
.btn-primary{background:var(--purple);color:#fff}
.btn-primary:hover{background:var(--purple-700);color:#fff;transform:translateY(-1px)}
.btn-ghost{border-color:var(--line-strong);color:var(--purple);background:#fff}
.btn-ghost:hover{border-color:var(--purple);color:var(--purple)}
.btn-white{background:#fff;color:var(--purple)}
.btn-white:hover{background:var(--purple-50);color:var(--purple)}
.btn-outline-white{border-color:rgba(255,255,255,.35);color:#fff}
.btn-outline-white:hover{border-color:#fff;color:#fff}
.link-arrow{display:inline-flex;align-items:center;gap:8px;font-weight:600;color:var(--purple)}
.link-arrow svg{width:18px;height:18px;transition:transform .2s ease}
.link-arrow:hover svg{transform:translateX(3px)}

/* announcement */
.notice{background:var(--purple-900);color:#E7E3F4;font-size:14px}
.notice .wrap{display:flex;align-items:center;justify-content:center;gap:12px;min-height:44px;padding-top:8px;padding-bottom:8px;text-align:center;flex-wrap:wrap}
.notice strong{color:#fff;font-weight:600}
.notice a{color:#D8E37A;font-weight:600;text-decoration:underline;text-underline-offset:3px}
.notice .dot{width:6px;height:6px;border-radius:50%;background:var(--lime);flex:0 0 auto}

/* header */
.hdr{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.94);backdrop-filter:saturate(1.4) blur(10px);-webkit-backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid transparent;transition:border-color .2s ease}
.hdr.scrolled{border-bottom-color:var(--line)}
.hdr .wrap{display:flex;align-items:center;gap:28px;height:84px}
.brand{display:flex;align-items:center;flex:0 0 auto}
.brand img{height:60px;width:auto}
.nav{display:flex;align-items:center;gap:26px;font-size:15px;font-weight:500}
.nav a{color:var(--body)}
.nav a:hover{color:var(--purple)}
.hdr-right{margin-left:auto;display:flex;align-items:center;gap:14px}
.lang{display:flex;padding:3px;gap:2px;border:1px solid var(--line);border-radius:var(--pill);background:var(--surface)}
.lang button{font:600 12.5px/1 var(--font);border:0;background:transparent;color:var(--muted);padding:7px 11px;border-radius:var(--pill);cursor:pointer}
.lang button[aria-pressed="true"]{background:var(--purple);color:#fff}
.hdr .btn{height:44px;padding:0 20px;font-size:15px}
.menu-btn{display:none;width:44px;height:44px;border-radius:50%;border:1px solid var(--line);background:#fff;color:var(--purple);align-items:center;justify-content:center;cursor:pointer}
.menu-btn svg{width:22px;height:22px}
.mnav{display:none}

/* hero */
.hero{padding:clamp(40px,6vw,80px) 0 clamp(56px,7vw,96px)}
.hero .wrap{display:grid;grid-template-columns:minmax(0,1.02fr) minmax(0,1fr);gap:clamp(32px,5vw,72px);align-items:center}
.hero-k{font-size:15px;font-weight:600;color:var(--teal-text);margin-bottom:22px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.hero-k .sep{width:4px;height:4px;border-radius:50%;background:var(--faint)}
.hero h1{display:flex;flex-direction:column;gap:22px}
.hero .display{font-size:clamp(46px,6.6vw,88px);font-weight:800;letter-spacing:-.035em;line-height:.98;color:var(--ink)}
.hero .display span{display:block}
.hero .display .c2{color:var(--teal)}
.hero .display .c3{color:var(--lime-text)}
.hero .h1-sub{font-size:clamp(19px,1.9vw,23px);font-weight:600;letter-spacing:-.01em;line-height:1.4;color:var(--ink);max-width:520px}
.hero .lede{max-width:540px;margin-top:20px}
.hero-cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:34px}
.hero-facts{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:34px;padding-top:26px;border-top:1px solid var(--line);font-size:14.5px;color:var(--muted)}
.hero-facts li{display:flex;align-items:center;gap:8px}
.hero-facts svg{width:18px;height:18px;color:var(--teal);flex:0 0 auto}
.hero-media{position:relative}
.photo{position:relative;border-radius:var(--radius);overflow:hidden;background:var(--surface-2)}
.photo img{width:100%;height:100%;object-fit:cover}
.photo .credit{position:absolute;right:12px;bottom:10px;font-size:11px;color:rgba(255,255,255,.92);text-shadow:0 1px 3px rgba(0,0,0,.45)}
.photo .credit a{color:inherit;text-decoration:underline;text-underline-offset:2px}
.hero-media{margin-bottom:0}
.hero-media .photo{aspect-ratio:1008/1062}
.hero-photo picture{display:block;width:100%;height:100%}
.hero-photo img{object-position:50% 40%}
.hero-card{position:absolute;left:-32px;bottom:-40px;background:#fff;border-radius:20px;box-shadow:0 20px 50px rgba(26,17,66,.16);padding:20px 22px;width:min(380px,88%)}
.hero-card .t{font-size:13px;font-weight:600;color:var(--teal-text)}
.hero-card .n{font-size:18px;font-weight:700;color:var(--ink);margin-top:4px;line-height:1.3}
.flow{display:flex;align-items:center;gap:5px;margin-top:14px;flex-wrap:wrap;font-size:12.5px;font-weight:600;color:var(--purple)}
.flow span{padding:5px 9px;border-radius:var(--pill);background:var(--purple-50)}
.flow i{width:8px;height:1.5px;background:var(--line-strong)}

/* numbers */
.numbers{border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.numbers ul{display:grid;grid-template-columns:repeat(4,minmax(0,1fr))}
.numbers li{padding:30px 24px;border-left:1px solid var(--line)}
.numbers li:first-child{border-left:0;padding-left:0}
.numbers b{display:block;font-size:clamp(34px,3.6vw,46px);font-weight:700;letter-spacing:-.03em;color:var(--purple);line-height:1}
.numbers span{display:block;margin-top:10px;font-size:15px;color:var(--muted);line-height:1.45}

/* pathway */
.steps{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:0;position:relative}
.step{padding:0 14px 0 0}
.step .bar{height:6px;border-radius:6px;margin-bottom:22px;margin-right:4px}
.step .no{font-size:14px;font-weight:700;letter-spacing:.02em}
.step h3{font-size:19px;margin-top:6px;letter-spacing:-.01em}
.step p{font-size:14.5px;line-height:1.55;color:var(--muted);margin-top:8px}
.phase{display:grid;grid-template-columns:2fr 6fr;margin-top:30px;font-size:13.5px;font-weight:600;color:var(--muted)}
.phase div{border-top:1.5px solid var(--line-strong);padding-top:10px;margin-right:14px;position:relative}
.phase div::before{content:"";position:absolute;left:0;top:-4px;width:7px;height:7px;border-radius:50%;background:var(--line-strong)}
.pathway-foot{margin-top:44px;display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;padding:22px 26px;background:var(--surface);border-radius:var(--radius)}
.pathway-foot p{color:var(--body);font-size:16px;max-width:720px}

/* method */
.method{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(32px,6vw,80px);align-items:start}
.method .photo{aspect-ratio:4/5;position:sticky;top:110px}
.mlist li{display:grid;grid-template-columns:112px minmax(0,1fr);gap:24px;padding:28px 0;border-top:1px solid var(--line)}
.mlist li:last-child{border-bottom:1px solid var(--line)}
.mlist .rng{font-size:13.5px;font-weight:600;color:var(--teal-text);padding-top:4px}
.mlist h3{font-size:21px}
.mlist p{margin-top:8px;color:var(--muted)}
.mlist .tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.mlist .tags span{font-size:13px;font-weight:500;color:var(--purple);border:1px solid var(--purple-100);background:var(--purple-50);padding:5px 12px;border-radius:var(--pill)}

/* assessment (dark) */
.dark{background:var(--purple-900);color:#D9D4EE}
.dark h2,.dark h3{color:#fff}
.dark .eyebrow{color:#C9D46B}
.dark .lede{color:#B8B1D8}
.dark .sec-head{align-items:start}
.scan-flow{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:28px}
.scan-flow li{display:flex;align-items:center;gap:10px;font-size:15px;font-weight:600;color:#fff}
.scan-flow li span{width:28px;height:28px;border-radius:50%;border:1.5px solid rgba(255,255,255,.35);display:inline-flex;align-items:center;justify-content:center;font-size:13px}
.scan-flow li + li::before{content:"";width:28px;height:1.5px;background:rgba(255,255,255,.3)}
.tools{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr) minmax(0,1fr);gap:20px}
.tool{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:var(--radius);padding:26px;display:flex;flex-direction:column}
.tool .viz{background:rgba(255,255,255,.04);border-radius:16px;height:230px;display:flex;align-items:center;justify-content:center;margin-bottom:24px;padding:14px}
.tool .viz svg{width:100%;height:100%}
.tool h3{font-size:20px}
.tool p{margin-top:8px;color:#B8B1D8;font-size:15.5px}
.dark-foot{margin-top:40px;font-size:15px;color:#B8B1D8;max-width:760px}

/* pilates */
.pil{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(32px,6vw,80px);align-items:center}
.pil .photo{aspect-ratio:5/6}
.tracks{margin-top:34px;display:grid;gap:14px}
.track .lbl{display:flex;justify-content:space-between;gap:12px;font-size:14px;margin-bottom:8px}
.track .lbl b{color:var(--ink);font-weight:700}
.track .lbl span{color:var(--muted)}
.track .row{display:grid;grid-template-columns:repeat(8,1fr);gap:4px}
.track .row i{height:10px;border-radius:3px;background:var(--surface-2)}
.track .row i.on{background:var(--purple)}
.track.p2 .row i.on{background:var(--lime)}
.track .row i.half{background:var(--purple-200)}
.track.p2 .row i.half{background:#D8DF9A}
.track-nums{display:grid;grid-template-columns:repeat(8,1fr);gap:4px;font-size:12px;color:var(--faint);font-weight:600}
.reasons{margin-top:36px;display:grid;gap:22px}
.reasons li{display:grid;grid-template-columns:44px minmax(0,1fr);gap:16px}
.reasons .ix{font-size:14px;font-weight:700;color:var(--teal-text);padding-top:2px}
.reasons h3{font-size:19px}
.reasons p{margin-top:6px;color:var(--muted);font-size:16px}
.reasons a{color:var(--purple);text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--purple-200)}

/* values */
.values{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:16px}
.value{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:26px 22px}
.value .l{width:48px;height:48px;border-radius:50%;background:var(--purple);color:#fff;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:700}
.value h3{font-size:17px;margin-top:20px;line-height:1.3}
.value p{margin-top:8px;font-size:15px;color:var(--muted);line-height:1.55}
.trained{margin-top:20px;display:grid;grid-template-columns:auto minmax(0,1fr);gap:22px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:24px 28px}
.trained .ic{width:52px;height:52px;border-radius:16px;background:var(--teal-50);color:var(--teal);display:flex;align-items:center;justify-content:center}
.trained .ic svg{width:26px;height:26px}
.trained h3{font-size:18px}
.trained p{color:var(--muted);font-size:15.5px;margin-top:4px}

/* team */
.lead{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);align-items:start;gap:clamp(28px,5vw,64px);align-items:stretch;background:var(--surface);border-radius:32px;padding:clamp(24px,4vw,48px)}
.lead-id{background:var(--purple);border-radius:var(--radius);color:#fff;display:flex;flex-direction:column;position:relative;overflow:hidden}
.lead-photo{aspect-ratio:525/552;background:var(--purple-50)}
.lead-photo picture,.lead-photo img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 20%}
.lead-info{padding:24px 28px 28px}
.lead-id .mono{width:88px;height:88px;border-radius:50%;background:#fff;color:var(--purple);display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:700;letter-spacing:-.02em}
.lead-id .role{font-size:14px;font-weight:600;color:#D8E37A}
.lead-id .name{font-size:28px;font-weight:700;line-height:1.2;margin-top:6px;color:#fff}
.lead-id .yrs{display:flex;align-items:baseline;gap:10px;margin-top:18px;padding-top:16px;border-top:1px solid rgba(255,255,255,.18)}
.lead-id .yrs b{font-size:40px;font-weight:700;line-height:1;letter-spacing:-.03em}
.lead-id .yrs span{font-size:14px;color:#CBC3E8;line-height:1.4}
.lead-id .loop{position:absolute;right:-40px;top:-30px;width:220px;opacity:.12}
.lead-bio p.big{font-size:clamp(18px,1.8vw,21px);color:var(--ink);font-weight:500;line-height:1.55}
.creds{margin-top:28px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 28px}
.creds li{display:grid;grid-template-columns:22px minmax(0,1fr);gap:10px;font-size:15.5px;color:var(--body);line-height:1.5}
.creds svg{width:20px;height:20px;color:var(--teal);margin-top:2px}

/* pricing */
.price-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.pcard{border:1px solid var(--line);border-radius:var(--radius);padding:30px;background:#fff;display:flex;flex-direction:column}
.pcard.senior{border-color:var(--purple-200);background:linear-gradient(#fff,#fff) padding-box}
.pcard .head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px}
.pcard h3{font-size:22px}
.pcard .sub{font-size:15px;color:var(--muted);margin-top:4px}
.pcard .tag{font-size:12.5px;font-weight:600;color:var(--purple);background:var(--purple-50);padding:5px 11px;border-radius:var(--pill);white-space:nowrap}
.prow{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px 16px;align-items:baseline;padding:18px 0;border-top:1px solid var(--line)}
.prow:first-of-type{margin-top:22px}
.prow .k{font-weight:600;color:var(--ink);font-size:16px}
.prow .k small{display:block;font-weight:400;color:var(--muted);font-size:14px;margin-top:2px}
.prow .v{text-align:right;font-weight:700;color:var(--ink);font-size:21px;letter-spacing:-.01em;white-space:nowrap}
.prow .v small{display:block;font-weight:500;color:var(--muted);font-size:13.5px;letter-spacing:0;margin-top:2px}
.pcard .btn{margin-top:auto;align-self:flex-start}
.pcard .foot{padding-top:22px;margin-top:6px}
.addons{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin-top:20px}
.addon{display:flex;justify-content:space-between;align-items:center;gap:16px;border:1px solid var(--line);border-radius:var(--radius-sm);padding:20px 24px;background:#fff}
.addon b{display:block;color:var(--ink);font-size:16.5px}
.addon span{display:block;font-size:14.5px;color:var(--muted)}
.addon .v{font-weight:700;color:var(--ink);font-size:19px;white-space:nowrap}
.terms{margin-top:20px;font-size:14.5px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px 18px}
.terms b{color:var(--body);font-weight:600}
.terms li{display:flex;align-items:center;gap:8px}
.terms li::before{content:"";width:5px;height:5px;border-radius:50%;background:var(--faint)}
.terms li.k::before{display:none}
.soft{margin-top:48px;border-radius:28px;background:var(--lime-50);border:1px solid #E3E8B5;padding:clamp(22px,3.5vw,40px)}
.soft-top{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:start}
.soft .k{font-size:14px;font-weight:700;color:var(--lime-text)}
.soft h3{font-size:clamp(24px,2.6vw,32px);margin-top:6px}
.soft .lede{color:var(--body);margin-top:10px;max-width:620px;font-size:17px}
.offs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:28px}
.off{background:#fff;border-radius:18px;padding:18px 20px}
.off .p{font-size:26px;font-weight:700;color:var(--ink);letter-spacing:-.02em;line-height:1.1}
.off .d{font-size:14px;color:var(--muted);margin-top:6px;line-height:1.45}
.soft-table{margin-top:20px;background:#fff;border-radius:18px;overflow:hidden}
.soft-table table{width:100%;border-collapse:collapse;font-size:15.5px}
.soft-table th,.soft-table td{padding:14px 18px;text-align:right;border-top:1px solid var(--line);white-space:nowrap}
.soft-table th:first-child,.soft-table td:first-child{text-align:left}
.soft-table thead th{border-top:0;font-size:13.5px;font-weight:600;color:var(--muted);background:#FBFBF4}
.soft-table td b{color:var(--ink)}
.soft-table td s{display:block;color:var(--faint);font-size:13px;text-decoration-thickness:1px}
.soft .note{margin-top:16px;font-size:14px;color:var(--muted)}


/* injuries */
.injuries{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.inj{display:flex;flex-direction:column;gap:10px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:28px;color:inherit;transition:border-color .2s ease,box-shadow .2s ease,transform .2s ease}
.inj:hover{border-color:var(--purple-200);box-shadow:var(--shadow);transform:translateY(-2px);color:inherit}
.inj h3{font-size:22px}
.inj p{color:var(--muted);font-size:16px}
.inj .link-arrow{margin-top:auto;padding-top:8px;font-size:15px}
.inj.big{grid-column:span 2;background:var(--purple);border-color:var(--purple)}
.inj.big h3{color:#fff;font-size:clamp(26px,2.6vw,34px)}
.inj.big p{color:#CBC3E8;font-size:17.5px;max-width:560px}
.inj.big .link-arrow{color:#D8E37A}
/* services (no prices) */
.svcs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.svc{border:1px solid var(--line);border-radius:var(--radius);padding:26px;background:#fff}
.svc h3{font-size:19px}
.svc p{margin-top:8px;color:var(--muted);font-size:15.5px}
.price-cta{display:flex;flex-direction:column;align-items:flex-start;justify-content:space-between;gap:18px;background:var(--purple-50);border-radius:var(--radius);padding:26px}
.price-cta p{font-size:17px;font-weight:600;color:var(--ink);line-height:1.45}
.trained-note{margin-top:24px;padding-top:20px;border-top:1px solid var(--line);font-size:15px;color:var(--muted)}

/* location */
.loc{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:20px;align-items:stretch}
.map{border-radius:var(--radius);overflow:hidden;min-height:440px;background:var(--surface-2);position:relative}
.map iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.loc-card{border:1px solid var(--line);border-radius:var(--radius);padding:32px;display:flex;flex-direction:column;gap:22px;background:#fff}
.loc-card address{font-style:normal;font-size:17px;line-height:1.6;color:var(--body)}
.loc-card address b{display:block;font-size:22px;color:var(--ink);font-weight:700;letter-spacing:-.01em;margin-bottom:6px}
.access{display:grid;gap:14px;padding-top:22px;border-top:1px solid var(--line)}
.access li{display:grid;grid-template-columns:36px minmax(0,1fr);gap:12px;font-size:15.5px}
.access .ic{width:36px;height:36px;border-radius:12px;background:var(--surface);color:var(--purple);display:flex;align-items:center;justify-content:center}
.access .ic svg{width:19px;height:19px}
.access b{display:block;color:var(--ink);font-weight:600;font-size:14.5px}
.access span{color:var(--muted)}
.loc-card .acts{display:flex;gap:10px;flex-wrap:wrap;margin-top:auto}
.loc-card .btn{height:46px;padding:0 20px;font-size:15px}

/* articles */
.arts{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:20px}
.acard{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;transition:box-shadow .2s ease,transform .2s ease;color:inherit}
.acard:hover{box-shadow:var(--shadow);transform:translateY(-2px);color:inherit}
.acard .photo{border-radius:0;aspect-ratio:16/10}
.acard .body{padding:24px 26px 26px;display:flex;flex-direction:column;gap:10px;flex:1}
.acard .meta{font-size:13.5px;font-weight:600;color:var(--teal-text)}
.acard h3{font-size:21px;line-height:1.3}
.acard p{font-size:15.5px;color:var(--muted)}
.acard .more{margin-top:auto;padding-top:6px}
.acard.feat h3{font-size:clamp(23px,2.3vw,28px)}
.acard.feat .photo{aspect-ratio:16/10}
.alist{display:grid;gap:20px;grid-template-rows:repeat(3,auto)}
.acard.row{flex-direction:row}
.acard.row .photo{aspect-ratio:auto;width:38%;flex:0 0 38%}
.acard.row .body{padding:20px 22px}
.acard.row h3{font-size:18px}
.acard.row .ex{display:none}
.by{margin-top:26px;font-size:14.5px;color:var(--muted)}

/* faq */
.faq{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(32px,6vw,80px)}
.faq details{border-top:1px solid var(--line)}
.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:20px;align-items:center;padding:22px 0;font-size:18px;font-weight:600;color:var(--ink)}
.faq summary::-webkit-details-marker{display:none}
.faq summary svg{width:22px;height:22px;flex:0 0 auto;color:var(--purple);transition:transform .2s ease}
.faq details[open] summary svg{transform:rotate(45deg)}
.faq .a{padding:0 0 24px;color:var(--muted);max-width:680px}

/* booking */
.book{background:var(--purple-50);color:var(--body);border-radius:32px;padding:clamp(28px,5vw,64px);display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:clamp(28px,5vw,64px);align-items:center}
.book h2{color:var(--ink)}
.book .lede{color:var(--muted)}
.book .acts{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.channels{display:grid;gap:12px}
.channel{display:grid;grid-template-columns:46px minmax(0,1fr) auto;gap:16px;align-items:center;background:#fff;border:1px solid var(--purple-100);border-radius:18px;padding:16px 18px;color:var(--ink);transition:border-color .2s ease,box-shadow .2s ease}
.channel:hover{border-color:var(--purple-200);box-shadow:var(--shadow);color:var(--ink)}
.channel .ic{width:46px;height:46px;border-radius:14px;background:var(--purple-50);color:var(--purple);display:flex;align-items:center;justify-content:center}
.channel .ic svg{width:22px;height:22px}
.channel b{display:block;font-weight:600;font-size:16px}
.channel span{display:block;font-size:14px;color:var(--muted);line-height:1.45}
.channel .go{width:20px;height:20px;color:var(--purple)}

/* footer */
.ftr{padding:80px 0 40px;background:var(--purple);color:#CBC3E8;margin-top:var(--sec)}
#booking{padding-bottom:0}
.ftr .top{display:grid;grid-template-columns:minmax(0,1.4fr) repeat(3,minmax(0,1fr));gap:40px}
.ftr .logo{height:96px;width:auto}
.ftr .about{margin-top:22px;font-size:15px;color:#CBC3E8;max-width:340px}
.ftr h4{font-size:14px;font-weight:600;color:#D8E37A;margin-bottom:16px;letter-spacing:0}
.ftr ul{display:grid;gap:10px;font-size:15px}
.ftr ul a{color:#fff}
.ftr ul a:hover{color:#D8E37A}
.ftr address{font-style:normal;font-size:15px;color:#fff;line-height:1.6}
.ftr .bottom{margin-top:56px;padding-top:24px;border-top:1px solid rgba(255,255,255,.16);display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;font-size:13.5px;color:#A096D4}
.ftr .bottom .tl{color:#fff;font-weight:500}
.ftr .disc{margin-top:14px;font-size:13px;color:#A096D4;max-width:820px;line-height:1.6}

/* wa fab */
.p8-wa-fab{position:fixed;right:24px;bottom:24px;z-index:60;width:60px;height:60px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--purple);border:2px solid #fff;color:#fff;box-shadow:0 0 0 3px var(--lime),0 10px 24px rgba(26,17,66,.3);transition:transform .2s ease,background .2s ease}
.p8-wa-fab:hover{background:var(--purple-700);color:#fff;transform:translateY(-3px)}
.p8-wa-fab svg{width:30px;height:30px}

[data-until].expired{display:none !important}

/* reveal */
@media (prefers-reduced-motion:no-preference){
  .rv{opacity:0;transform:translateY(14px);transition:opacity .6s ease,transform .6s ease}
  .rv.in{opacity:1;transform:none}
}

/* responsive */
@media (max-width:1080px){
  .nav{gap:18px;font-size:14.5px}
  .steps{grid-template-columns:repeat(4,minmax(0,1fr));row-gap:36px}
  .phase{display:none}
  .values{grid-template-columns:repeat(3,minmax(0,1fr))}
  .tools{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .tools .tool:last-child{grid-column:1/-1}
  .offs{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:920px){
  .injuries,.svcs{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .nav,.hdr .btn-desk{display:none}
  .menu-btn{display:inline-flex}
  .mnav{position:fixed;inset:84px 0 0 0;background:#fff;z-index:49;padding:24px var(--gutter) 40px;overflow:auto}
  .mnav.open{display:block}
  .mnav a{display:block;padding:16px 0;border-bottom:1px solid var(--line);font-size:19px;font-weight:600;color:var(--ink)}
  .mnav .btn{margin-top:24px;width:100%;color:#fff}
  .hero .wrap,.method,.pil,.lead,.loc,.arts,.faq,.book,.sec-head{grid-template-columns:minmax(0,1fr)}
  .sec-head{gap:16px;margin-bottom:40px}
  .hero-media{max-width:560px}
  .hero-media .photo{aspect-ratio:1008/1062}
  .hero-media{margin-bottom:0}
  .hero-card{left:16px;bottom:16px}
  .method .photo{position:relative;top:0;aspect-ratio:16/10}
  .pil .photo{aspect-ratio:16/11}
  .numbers ul{grid-template-columns:repeat(2,minmax(0,1fr))}
  .numbers li:nth-child(3){border-left:0;padding-left:0}
  .numbers li:nth-child(n+3){border-top:1px solid var(--line)}
  .ftr .top{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .ftr .top > :first-child{grid-column:1/-1}
  .map{min-height:340px}
}
@media (max-width:640px){
  .injuries,.svcs{grid-template-columns:minmax(0,1fr)}
  .inj.big{grid-column:auto}
  .price-cta .btn{width:100%}
  body{font-size:16px}
  .hdr .wrap{height:72px;gap:12px}
  .brand img{height:50px}
  .mnav{inset:72px 0 0 0}
  .hdr-right{gap:10px}
  .hero-k{font-size:14px}
  .hero-cta .btn{flex:1 1 100%}
  .steps{grid-template-columns:minmax(0,1fr);row-gap:0}
  .step{display:grid;grid-template-columns:44px minmax(0,1fr);gap:0 14px;padding:0 0 22px;position:relative}
  .step .bar{grid-row:1/4;width:6px;height:auto;margin:0 0 0 16px}
  .step .no{grid-column:2}
  .step h3,.step p{grid-column:2}
  .values{grid-template-columns:minmax(0,1fr)}
  .value{display:grid;grid-template-columns:48px minmax(0,1fr);gap:0 18px;padding:20px}
  .value .l{grid-row:1/3}
  .value h3{margin-top:2px}
  .trained{grid-template-columns:minmax(0,1fr)}
  .tools{grid-template-columns:minmax(0,1fr)}
  .mlist li{grid-template-columns:minmax(0,1fr);gap:6px}
  .price-grid,.addons,.creds{grid-template-columns:minmax(0,1fr)}
  .pcard{padding:22px}
  .prow .v{font-size:19px}
  .soft-top{grid-template-columns:minmax(0,1fr)}
  .soft-table{overflow-x:auto}
  .soft-table table{min-width:520px}
  .offs{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .acard.row{flex-direction:column}
  .acard.row .photo{width:100%;flex:none;aspect-ratio:16/9}
  .acard.row .ex{display:block}
  .loc-card{padding:22px}
  .ftr .top{grid-template-columns:minmax(0,1fr)}
  .p8-wa-fab{right:16px;bottom:16px;width:56px;height:56px}
  .hero-card{position:relative;left:auto;bottom:auto;margin:-28px 14px 0;width:auto}
  .off:first-child{grid-column:1/-1}
  .channel{grid-template-columns:42px minmax(0,1fr)}
  .channel .go{display:none}
  .tool .viz{height:200px}
  .notice{font-size:13px}
  .notice .dot,.hero-k .sep{display:none}
  .hero-k{gap:2px 10px}
}
@media (max-width:380px){.lang{display:none}}
@media print{.hdr,.notice,.p8-wa-fab,.mnav{display:none}}
"""
