"""Physio8 interval workout timer at /timer/ — same design system as the homepage."""
import json

import build
import build_home as H
from build_home import en, wa_cta, wa_pair
from build_pages import page, subpage, esc
from home_svg import icon

URL = build.SITE_BASE + "timer/"

# key, label_id, label_en, hint_id, hint_en, icon, default, min, max, kind
FIELDS = [
    ("p", "Persiapan", "Get ready", "Hitung mundur sebelum mulai", "Countdown before you start", "hourglass", 10, 0, 120, "t"),
    ("w", "Latihan", "Work", "Lama setiap gerakan", "Length of each exercise block", "dumbbell", 20, 5, 600, "t"),
    ("r", "Istirahat", "Rest", "Jeda di antara gerakan", "Pause between blocks", "wind", 10, 0, 600, "t"),
    ("c", "Putaran", "Rounds", "Latihan dan istirahat dalam satu set", "Work and rest pairs in one set", "repeat", 1, 1, 50, "n"),
    ("s", "Set", "Sets", "Ulangi seluruh putaran", "Repeat all rounds", "layers", 3, 1, 20, "n"),
    ("sr", "Istirahat antar set", "Rest between sets", "Jeda yang lebih panjang", "A longer break", "coffee", 20, 0, 600, "t"),
    ("cd", "Pendinginan", "Cool down", "Peregangan ringan di akhir", "Easy stretching at the end", "heart", 0, 0, 900, "t"),
]

PRESETS = [
    ("Tahan 20 dtk × 3 set", "Hold 20 s × 3 sets", {"p": 10, "w": 20, "r": 10, "c": 1, "s": 3, "sr": 20, "cd": 0}),
    ("Tahan 30 dtk × 4 set", "Hold 30 s × 4 sets", {"p": 10, "w": 30, "r": 10, "c": 1, "s": 4, "sr": 30, "cd": 0}),
]

TIMER_CSS = r"""
.tm-hero{padding:clamp(28px,4vw,48px) 0 0}
.tm-hero h1{font-size:clamp(36px,4.8vw,58px);font-weight:800;letter-spacing:-.03em;line-height:1.06;max-width:820px}
.tm-grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:24px;align-items:start;margin-top:40px}
.tm-card{border:1px solid var(--line);border-radius:var(--radius);background:#fff;padding:12px 26px 26px}
.tm-presets{display:flex;flex-wrap:wrap;gap:8px;padding:16px 0 18px;border-bottom:1px solid var(--line)}
.tm-presets p{width:100%;font-size:13.5px;font-weight:600;color:var(--muted);margin-bottom:2px}
.tm-presets button{font:500 14px var(--font);height:38px;padding:0 16px;border-radius:999px;border:1px solid var(--line-strong);background:#fff;color:var(--body);cursor:pointer}
.tm-presets button:hover{border-color:var(--purple);color:var(--purple)}
.tm-presets button[aria-pressed="true"]{background:var(--purple);border-color:var(--purple);color:#fff}
.tm-row{display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:14px;align-items:center;padding:14px 0;border-bottom:1px solid var(--line)}
.tm-row.off{opacity:.45}
.tm-ic{width:44px;height:44px;border-radius:14px;background:var(--purple-50);color:var(--purple);display:flex;align-items:center;justify-content:center}
.tm-ic svg{width:22px;height:22px}
.tm-row b{display:block;font-size:16px;color:var(--ink)}
.tm-row small{display:block;font-size:13.5px;color:var(--muted);line-height:1.4;margin-top:2px}
.step{display:flex;align-items:center;gap:6px}
.step button{width:44px;height:44px;border-radius:50%;border:1.5px solid var(--line-strong);background:#fff;color:var(--purple);display:flex;align-items:center;justify-content:center;cursor:pointer;touch-action:manipulation;-webkit-user-select:none;user-select:none}
.step button:hover{border-color:var(--purple)}
.step button:active{background:var(--purple-50)}
.step button:disabled{opacity:.35;cursor:default}
.step button svg{width:18px;height:18px}
.step output{min-width:70px;text-align:center;font-size:20px;font-weight:700;color:var(--ink);font-variant-numeric:tabular-nums}
.tm-name{padding:16px 0;border-bottom:1px solid var(--line)}
.tm-name label{display:block;font-size:14px;font-weight:600;color:var(--ink);margin-bottom:8px}
.tm-name input{width:100%;height:48px;border-radius:14px;border:1px solid var(--line-strong);padding:0 16px;font:500 16px var(--font);color:var(--ink)}
.tm-name input:focus,.tm-name input:focus-visible{outline:none;border-color:var(--purple);box-shadow:0 0 0 3px var(--purple-50)}
.tm-opts{display:flex;flex-wrap:wrap;gap:8px;padding-top:18px}
.tm-opt{display:inline-flex;align-items:center;gap:8px;height:40px;padding:0 14px;border-radius:999px;border:1px solid var(--line-strong);background:#fff;font:500 14px var(--font);color:var(--body);cursor:pointer}
.tm-opt svg{width:17px;height:17px}
.tm-opt[aria-pressed="true"]{background:var(--teal-50);border-color:var(--teal);color:var(--teal-text)}
.tm-side{position:sticky;top:104px;display:grid;gap:16px}
.tm-sum{background:var(--purple);color:#CBC3E8;border-radius:var(--radius);padding:30px}
.tm-sum .k{font-size:14px;font-weight:600;color:#C9D46B}
.tm-sum .big{font-size:clamp(56px,7vw,84px);font-weight:800;letter-spacing:-.03em;color:#fff;line-height:1;margin-top:10px;font-variant-numeric:tabular-nums}
.tm-sum .meta{margin-top:10px;font-size:15.5px}
.tm-sum .start{margin-top:24px;width:100%;height:60px;font-size:18px}
.tm-sum .start svg{width:22px;height:22px}
.tm-plan{margin-top:22px;display:flex;height:10px;border-radius:999px;overflow:hidden;background:rgba(255,255,255,.12)}
.tm-plan i{display:block;height:100%}
.tm-legend{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:12px;font-size:13px}
.tm-legend span{display:inline-flex;align-items:center;gap:6px}
.tm-legend span::before{content:"";width:9px;height:9px;border-radius:50%;background:var(--c)}
.tm-share{border:1px solid var(--line);border-radius:var(--radius);padding:24px;background:#fff}
.tm-share b{display:block;font-size:17px;color:var(--ink)}
.tm-share p{font-size:15px;color:var(--muted);margin-top:6px;line-height:1.55}
.tm-share .acts{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}
.tm-share .btn{height:46px;padding:0 18px;font-size:15px}
.tm-note{display:grid;grid-template-columns:22px minmax(0,1fr);gap:10px;background:var(--lime-50);border-radius:18px;padding:16px 18px;font-size:14.5px;line-height:1.6;color:var(--body)}
.tm-note svg{width:20px;height:20px;color:var(--lime-text);margin-top:2px}
.tm-how{margin-top:clamp(48px,6vw,72px)}
.tm-how ol{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;counter-reset:n}
.tm-how li{counter-increment:n;background:var(--surface);border-radius:var(--radius);padding:24px}
.tm-how li::before{content:counter(n);display:flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:50%;background:var(--purple);color:#fff;font-weight:700;font-size:14px;margin-bottom:14px}
.tm-how b{display:block;font-size:17px;color:var(--ink)}
.tm-how p{font-size:15px;color:var(--muted);margin-top:6px;line-height:1.6}
.tm-bar{display:none}

/* live stage (full screen) */
.stage{position:fixed;inset:0;z-index:200;display:none;flex-direction:column;color:#fff;background:var(--bgc,#2F1F71);transition:background .35s ease;padding:max(16px,env(safe-area-inset-top)) clamp(16px,4vw,40px) max(20px,env(safe-area-inset-bottom))}
.stage.on{display:flex}
.stage[data-ph="work"]{--bgc:#008699}
.stage[data-ph="rest"]{--bgc:#A6B717;color:#1A1142}
.stage[data-ph="prep"]{--bgc:#2F1F71}
.stage[data-ph="setrest"]{--bgc:#261859}
.stage[data-ph="cool"]{--bgc:#1A1142}
.stage[data-ph="done"]{--bgc:#2F1F71}
.st-top{display:flex;align-items:center;justify-content:space-between;gap:16px}
.st-top img{height:52px;width:auto}
.st-x{width:48px;height:48px;border-radius:50%;border:0;background:rgba(255,255,255,.16);color:inherit;display:flex;align-items:center;justify-content:center;cursor:pointer}
.stage[data-ph="rest"] .st-x{background:rgba(26,17,66,.1)}
.st-x svg{width:22px;height:22px}
.st-mid{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;min-height:0}
.st-ph{font-size:clamp(28px,5vw,56px);font-weight:800;letter-spacing:-.02em;line-height:1.05}
.st-name{font-size:clamp(17px,2.2vw,24px);font-weight:600;opacity:.9;margin-top:8px;min-height:1.3em}
.st-ring{position:relative;width:min(62vmin,460px);aspect-ratio:1;margin:clamp(12px,3vh,32px) 0}
.st-ring svg{position:absolute;inset:0;width:100%;height:100%;transform:rotate(-90deg)}
.st-ring circle{fill:none;stroke-width:6}
.st-ring .bg{stroke:currentColor;opacity:.18}
.st-ring .fg{stroke:currentColor;stroke-linecap:round;transition:stroke-dashoffset .25s linear}
.st-num{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:min(24vmin,190px);font-weight:800;letter-spacing:-.04em;font-variant-numeric:tabular-nums;line-height:1}
.st-num.long{font-size:min(17vmin,140px)}
.st-meta{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 22px;font-size:clamp(15px,1.8vw,19px);font-weight:600}
.st-meta span{opacity:.92}
.st-next{margin-top:8px;font-size:clamp(14px,1.6vw,17px);opacity:.82;min-height:1.4em}
.st-ctl{display:flex;align-items:center;justify-content:center;gap:clamp(14px,3vw,28px);padding-top:12px}
.st-ctl button{border:0;cursor:pointer;color:inherit;display:flex;align-items:center;justify-content:center;border-radius:50%;background:rgba(255,255,255,.16)}
.stage[data-ph="rest"] .st-ctl button{background:rgba(26,17,66,.1)}
.st-ctl .sm{width:60px;height:60px}
.st-ctl .sm svg{width:24px;height:24px}
.st-ctl .main{width:88px;height:88px;background:#fff;color:var(--purple)}
.stage[data-ph="rest"] .st-ctl .main{background:#1A1142;color:#fff}
.st-ctl .main svg{width:34px;height:34px}
.st-total{text-align:center;font-size:14px;opacity:.8;margin-top:12px;font-variant-numeric:tabular-nums}
.st-done{display:none;margin-top:18px;gap:10px;flex-wrap:wrap;justify-content:center}
.stage[data-ph="done"] .st-done{display:flex}
.stage[data-ph="done"] .st-ctl,.stage[data-ph="done"] .st-ring{display:none}
.st-done .btn{height:50px}
body.tm-live{overflow:hidden}

@media (max-width:920px){
  .tm-grid{grid-template-columns:minmax(0,1fr)}
  .tm-side{position:static}
  .tm-how ol{grid-template-columns:minmax(0,1fr)}
  .tm-bar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:60;align-items:center;gap:12px;padding:12px 16px max(12px,env(safe-area-inset-bottom));background:#fff;border-top:1px solid var(--line);box-shadow:0 -6px 20px rgba(26,17,66,.08)}
  .tm-bar .t{flex:1;min-width:0}
  .tm-bar .t b{display:block;font-size:20px;color:var(--ink);font-variant-numeric:tabular-nums;line-height:1.1}
  .tm-bar .t span{font-size:13px;color:var(--muted)}
  .tm-bar .btn{height:52px;padding:0 28px}
  body.has-bar .p8-wa-fab{display:none}
  body.has-bar .ftr{padding-bottom:110px}
}
@media (max-width:640px){
  .tm-card{padding:6px 18px 20px}
  .tm-row{grid-template-columns:minmax(0,1fr) auto;gap:10px}
  .tm-row .tm-ic{display:none}
  .step button{width:42px;height:42px}
  .step output{min-width:58px;font-size:18px}
  .st-top img{height:32px}
}
@media (orientation:landscape) and (max-height:520px){
  .st-ring{width:min(48vmin,300px);margin:6px 0}
  .st-num{font-size:min(20vmin,120px)}
  .st-ctl .main{width:64px;height:64px}
  .st-ctl .sm{width:48px;height:48px}
}
"""

TIMER_JS = r"""
(function(){
  var d=document, F=__FIELDS__, PRE=__PRESETS__, STORE='p8-timer', BASE=__URL__;
  var L={
    id:{prep:'Persiapan',work:'Latihan',rest:'Istirahat',setrest:'Istirahat antar set',cool:'Pendinginan',done:'Selesai',
        round:'Putaran',set:'Set',next:'Berikutnya',left:'Sisa',sec:'dtk',min:'mnt',intervals:'interval',total:'Total waktu',
        pause:'Jeda',resume:'Lanjut',copied:'Tautan disalin',doneMsg:'Kerja bagus. Catat bagaimana rasanya untuk fisioterapismu.',
        wa:'Halo, ini pengaturan timer latihan dari Physio8: ', voice:{prep:'Bersiap',work:'Mulai',rest:'Istirahat',setrest:'Istirahat antar set',cool:'Pendinginan',done:'Selesai'}},
    en:{prep:'Get ready',work:'Work',rest:'Rest',setrest:'Rest between sets',cool:'Cool down',done:'Done',
        round:'Round',set:'Set',next:'Next',left:'Left',sec:'sec',min:'min',intervals:'intervals',total:'Total time',
        pause:'Pause',resume:'Resume',copied:'Link copied',doneMsg:'Good work. Note how it felt for your physiotherapist.',
        wa:'Hi, here are my Physio8 workout timer settings: ', voice:{prep:'Get ready',work:'Go',rest:'Rest',setrest:'Rest between sets',cool:'Cool down',done:'Done'}}
  };
  function lang(){return d.documentElement.lang==='en'?'en':'id'}
  function T(k){return L[lang()][k]}
  var COLORS={prep:'#5B4BA0',work:'#008699',rest:'#A6B717',setrest:'#CBC3E8',cool:'#E7E3F4'};

  // ---------- state ----------
  var v={}, opt={beep:true,voice:false,vib:true}, name='';
  F.forEach(function(f){v[f.k]=f.d});
  try{var sv=JSON.parse(localStorage.getItem(STORE)||'null'); if(sv){F.forEach(function(f){if(typeof sv.v[f.k]==='number')v[f.k]=sv.v[f.k]}); if(sv.o)opt=Object.assign(opt,sv.o); if(typeof sv.n==='string')name=sv.n;}}catch(e){}
  var qs=new URLSearchParams(location.search), fromUrl=false;
  F.forEach(function(f){ if(qs.has(f.k)){ var n=parseInt(qs.get(f.k),10); if(!isNaN(n)){v[f.k]=n; fromUrl=true;} } });
  if(qs.has('n')){name=qs.get('n').slice(0,60); fromUrl=true;}
  F.forEach(function(f){v[f.k]=Math.min(f.max,Math.max(f.min,v[f.k]))});
  function save(){try{localStorage.setItem(STORE,JSON.stringify({v:v,o:opt,n:name}))}catch(e){}}

  function fmt(s){s=Math.max(0,Math.round(s)); var m=Math.floor(s/60), r=s%60; return m+':'+(r<10?'0':'')+r}
  function fmtField(f,x){return f.t==='t'?(x<60?x+' '+T('sec'):fmt(x)):String(x)}
  function stepOf(f,x,dir){ if(f.t!=='t') return 1; var b=dir>0?x:x-1; return b<60?5:(b<300?15:30); }

  // ---------- plan ----------
  function plan(){
    var seq=[];
    if(v.p>0) seq.push({ph:'prep',dur:v.p});
    for(var s=1;s<=v.s;s++){
      for(var c=1;c<=v.c;c++){
        seq.push({ph:'work',dur:v.w,c:c,s:s});
        var lastC=c===v.c, lastS=s===v.s;
        if(!lastC && v.r>0) seq.push({ph:'rest',dur:v.r,c:c,s:s});
        if(lastC && !lastS){ if(v.sr>0) seq.push({ph:'setrest',dur:v.sr,c:c,s:s}); else if(v.r>0) seq.push({ph:'rest',dur:v.r,c:c,s:s}); }
      }
    }
    if(v.cd>0) seq.push({ph:'cool',dur:v.cd});
    return seq;
  }
  function total(seq){return seq.reduce(function(a,x){return a+x.dur},0)}

  // ---------- settings UI ----------
  var rows={};
  d.querySelectorAll('.tm-row').forEach(function(row){
    var k=row.getAttribute('data-k'), f=F.filter(function(x){return x.k===k})[0], out=row.querySelector('output'),
        mi=row.querySelector('.mi'), pl=row.querySelector('.pl');
    rows[k]={row:row,f:f,out:out,mi:mi,pl:pl};
    function bump(dir){ var x=v[k]+dir*stepOf(f,v[k],dir); v[k]=Math.min(f.max,Math.max(f.min,x)); clearPreset(); refresh(); save(); }
    [[mi,-1],[pl,1]].forEach(function(p){ var b=p[0], dir=p[1], t1=null, t2=null;
      function stop(){clearTimeout(t1); clearInterval(t2); t1=t2=null}
      b.addEventListener('pointerdown',function(e){ if(e.button>0) return; bump(dir); t1=setTimeout(function(){t2=setInterval(function(){bump(dir)},90)},420); });
      ['pointerup','pointerleave','pointercancel','blur'].forEach(function(ev){b.addEventListener(ev,stop)});
      b.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){e.preventDefault(); bump(dir);} });
    });
  });
  var nameIn=d.getElementById('tm-n'); nameIn.value=name;
  nameIn.addEventListener('input',function(){name=nameIn.value.slice(0,60); save(); shareLinks();});
  var presetBtns=[].slice.call(d.querySelectorAll('.tm-presets button'));
  presetBtns.forEach(function(b,i){ b.addEventListener('click',function(){ var p=PRE[i]; Object.keys(p).forEach(function(k){v[k]=p[k]});
    presetBtns.forEach(function(x){x.setAttribute('aria-pressed',String(x===b))}); refresh(); save(); }); });
  function clearPreset(){presetBtns.forEach(function(x){x.setAttribute('aria-pressed','false')})}
  function markPreset(){ presetBtns.forEach(function(b,i){ var p=PRE[i], ok=Object.keys(p).every(function(k){return v[k]===p[k]}); b.setAttribute('aria-pressed',String(ok)); }); }
  d.querySelectorAll('.tm-opt').forEach(function(b){ var k=b.getAttribute('data-o'); b.setAttribute('aria-pressed',String(!!opt[k]));
    b.addEventListener('click',function(){ opt[k]=!opt[k]; b.setAttribute('aria-pressed',String(opt[k])); save(); if(k==='beep'&&opt[k]){unlock(); tone(880,.12)} if(k==='vib'&&opt[k]&&navigator.vibrate)navigator.vibrate(60); if(k==='voice'&&opt[k]){unlock(); say(T('voice').work)} }); });
  if(!('speechSynthesis' in window)){var vb=d.querySelector('[data-o="voice"]'); if(vb) vb.hidden=true;}
  if(!navigator.vibrate){var vv=d.querySelector('[data-o="vib"]'); if(vv) vv.hidden=true;}

  var sumBig=d.querySelector('.tm-sum .big'), sumMeta=d.querySelector('.tm-sum .meta'), planBar=d.querySelector('.tm-plan'),
      barT=d.querySelector('.tm-bar .t b'), barS=d.querySelector('.tm-bar .t span');
  function refresh(){
    Object.keys(rows).forEach(function(k){ var r=rows[k]; r.out.textContent=fmtField(r.f,v[k]); r.mi.disabled=v[k]<=r.f.min; r.pl.disabled=v[k]>=r.f.max; });
    rows.sr.row.classList.toggle('off', v.s<2); rows.r.row.classList.toggle('off', v.c<2);
    var seq=plan(), t=total(seq), n=seq.filter(function(x){return x.ph==='work'||x.ph==='rest'}).length;
    sumBig.textContent=fmt(t); barT.textContent=fmt(t);
    var pl=function(n,w){return n+' '+w.toLowerCase()+(lang()==='en'&&n!==1?'s':'')};
    var m=pl(v.s,T('set'))+' · '+pl(v.c,T('round'))+' · '+n+' '+T('intervals');
    sumMeta.textContent=m; barS.textContent=m;
    planBar.innerHTML=seq.map(function(x){return '<i style="flex:'+x.dur+';background:'+COLORS[x.ph]+'"></i>'}).join('');
    markPreset(); shareLinks();
  }

  // ---------- share ----------
  function link(){ var q=F.map(function(f){return f.k+'='+v[f.k]}).join('&'); if(name.trim()) q+='&n='+encodeURIComponent(name.trim()); return BASE+'?'+q; }
  var waA=d.getElementById('tm-wa');
  function shareLinks(){ waA.href='https://wa.me/?text='+encodeURIComponent(T('wa')+link()); }
  var toast=d.querySelector('.toast');
  d.getElementById('tm-copy').addEventListener('click',function(){ var u=link();
    function done(){toast.textContent=T('copied'); toast.classList.add('show'); setTimeout(function(){toast.classList.remove('show')},1800)}
    if(navigator.clipboard){navigator.clipboard.writeText(u).then(done,done)} else {done()} });

  // ---------- audio / voice / vibration / wake lock ----------
  var ac=null;
  function unlock(){ try{ if(!ac){var A=window.AudioContext||window.webkitAudioContext; if(A) ac=new A();} if(ac&&ac.state==='suspended') ac.resume(); }catch(e){} }
  function tone(f,len,vol){ if(!opt.beep||!ac) return; try{ var o=ac.createOscillator(), g=ac.createGain(), t=ac.currentTime;
    o.type='sine'; o.frequency.value=f; g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(vol||0.35,t+0.01); g.gain.exponentialRampToValueAtTime(0.0001,t+len);
    o.connect(g); g.connect(ac.destination); o.start(t); o.stop(t+len+0.02); }catch(e){} }
  function say(txt){ if(!opt.voice||!('speechSynthesis' in window)) return; try{ speechSynthesis.cancel(); var u=new SpeechSynthesisUtterance(txt); u.lang=lang()==='en'?'en-US':'id-ID'; u.rate=1.05; speechSynthesis.speak(u);}catch(e){} }
  function buzz(p){ if(opt.vib&&navigator.vibrate) try{navigator.vibrate(p)}catch(e){} }
  var lock=null;
  function wake(on){ try{ if(on&&'wakeLock' in navigator){ navigator.wakeLock.request('screen').then(function(l){lock=l}).catch(function(){}); } else if(!on&&lock){ lock.release(); lock=null; } }catch(e){} }
  d.addEventListener('visibilitychange',function(){ if(d.visibilityState==='visible'&&run&&!paused) wake(true); });

  // ---------- runner ----------
  var st=d.querySelector('.stage'), stPh=st.querySelector('.st-ph'), stName=st.querySelector('.st-name'), stNum=st.querySelector('.st-num'),
      fg=st.querySelector('.fg'), stMeta=st.querySelector('.st-meta'), stNext=st.querySelector('.st-next'), stTot=st.querySelector('.st-total'),
      bMain=st.querySelector('.main'), live=st.querySelector('.st-live'), C=2*Math.PI*48;
  fg.style.strokeDasharray=C;
  var seq=[], idx=0, endAt=0, remain=0, paused=false, run=false, lastSec=-1, raf=0, iv=0, TT=0;
  var IP=bMain.innerHTML, IR=__ICONPLAY__;
  function now(){return performance.now()}
  function start(){
    unlock(); seq=plan(); TT=total(seq); idx=0; run=true; paused=false;
    d.body.classList.add('tm-live'); st.classList.add('on'); wake(true);
    enter(0); loop(); clearInterval(iv); iv=setInterval(tick,250);
    bMain.focus({preventScroll:true});
  }
  function enter(i){
    idx=i; var x=seq[i]; if(!x){finish(); return;}
    remain=x.dur*1000; endAt=now()+remain; lastSec=-1;
    st.setAttribute('data-ph',x.ph);
    stPh.textContent=T(x.ph); stName.textContent=(x.ph==='work'&&name.trim())?name.trim():'';
    var m=[]; if(x.c&&v.c>1){m.push(T('round')+' '+x.c+'/'+v.c)} if(x.s&&v.s>1){m.push(T('set')+' '+x.s+'/'+v.s)}
    stMeta.innerHTML=m.map(function(t){return '<span>'+t+'</span>'}).join('');
    var nx=seq[i+1]; stNext.textContent=nx?(T('next')+': '+T(nx.ph)+' · '+fmtField({t:'t'},nx.dur)):'';
    live.textContent=T(x.ph)+(stName.textContent?', '+stName.textContent:'');
    if(i>0||x.ph!=='prep'){ tone(x.ph==='work'?1046:660,.45,.4); buzz(x.ph==='work'?[200,80,200]:300); }
    say(T('voice')[x.ph]);
    draw();
  }
  function finish(){
    run=false; clearInterval(iv); cancelAnimationFrame(raf); st.setAttribute('data-ph','done');
    stPh.textContent=T('done'); stName.textContent=T('doneMsg'); stMeta.innerHTML=''; stNext.textContent=''; stTot.textContent=T('total')+' '+fmt(TT);
    live.textContent=T('done'); tone(784,.18,.4); setTimeout(function(){tone(988,.18,.4)},200); setTimeout(function(){tone(1318,.5,.4)},400); buzz([200,100,200,100,400]); say(T('voice').done); wake(false);
  }
  function left(){return paused?remain:Math.max(0,endAt-now())}
  function draw(){
    var x=seq[idx]; if(!x) return; var ms=left(), s=Math.ceil(ms/1000);
    stNum.textContent=s>=60?fmt(s):String(s); stNum.classList.toggle('long',s>=60);
    fg.style.strokeDashoffset=String(C*(1-ms/(x.dur*1000)));
    var rest=ms/1000; for(var j=idx+1;j<seq.length;j++) rest+=seq[j].dur;
    stTot.textContent=T('left')+' '+fmt(Math.ceil(rest))+' / '+fmt(TT);
    if(s!==lastSec){ if(lastSec!==-1&&s<=3&&s>=1&&!paused){ tone(880,.12,.3); buzz(40); } lastSec=s; }
  }
  function tick(){ if(!run||paused) return; while(run&&left()<=0){ var over=now()-endAt; enter(idx+1); if(run){ endAt-=Math.min(over,remain-1); } } if(run) draw(); }
  function loop(){ cancelAnimationFrame(raf); (function f(){ tick(); if(run) raf=requestAnimationFrame(f); })(); }
  function toggle(){ if(!run) return; if(paused){ paused=false; endAt=now()+remain; bMain.innerHTML=IP; bMain.setAttribute('aria-label',T('pause')); wake(true); loop(); }
    else { remain=left(); paused=true; bMain.innerHTML=IR; bMain.setAttribute('aria-label',T('resume')); cancelAnimationFrame(raf); draw(); } }
  function stop(){ run=false; paused=false; clearInterval(iv); cancelAnimationFrame(raf); st.classList.remove('on'); d.body.classList.remove('tm-live'); bMain.innerHTML=IP; wake(false); try{speechSynthesis.cancel()}catch(e){} }
  function skip(){ if(!run) return; var wasP=paused; paused=false; enter(idx+1); if(run&&wasP){ remain=seq[idx].dur*1000; paused=true; bMain.innerHTML=IR; draw(); } }
  function back(){ if(!run) return; var j=(seq[idx].dur*1000-left()<1500&&idx>0)?idx-1:idx; var wasP=paused; paused=false; enter(j); if(wasP){ remain=seq[idx].dur*1000; paused=true; draw(); } }
  d.querySelectorAll('[data-act="start"]').forEach(function(b){b.addEventListener('click',start)});
  bMain.addEventListener('click',toggle);
  st.querySelector('[data-act="skip"]').addEventListener('click',skip);
  st.querySelector('[data-act="back"]').addEventListener('click',back);
  st.querySelectorAll('[data-act="stop"]').forEach(function(b){b.addEventListener('click',stop)});
  st.querySelector('[data-act="again"]').addEventListener('click',function(){stop(); start();});
  d.addEventListener('keydown',function(e){ if(!st.classList.contains('on')) return;
    if(e.key===' '||e.key==='k'){e.preventDefault(); toggle();} else if(e.key==='ArrowRight'){skip()} else if(e.key==='ArrowLeft'){back()} else if(e.key==='Escape'){stop()} });
  d.querySelectorAll('.lang button').forEach(function(b){b.addEventListener('click',function(){ setTimeout(function(){ refresh(); if(run){ var x=seq[idx]; stPh.textContent=T(x.ph); } },0); })});

  d.body.classList.add('has-bar');
  refresh();
  if(fromUrl){ var h=d.querySelector('.tm-from'); if(h) h.hidden=false; }
})();
"""


def _row(f):
    k, li, le, hi, he, ic, *_ = f
    return (f'<div class="tm-row" data-k="{k}"><span class="tm-ic">{icon(ic)}</span>'
            f'<div><b{en(le)}>{li}</b><small{en(he)}>{hi}</small></div>'
            f'<div class="step"><button type="button" class="mi" aria-label="Kurangi {li.lower()}" data-en-aria-label="Decrease {le.lower()}">{icon("minus")}</button>'
            f'<output aria-live="off"></output>'
            f'<button type="button" class="pl" aria-label="Tambah {li.lower()}" data-en-aria-label="Increase {le.lower()}">{icon("plus")}</button></div></div>')


def build_timer():
    title = "Timer Latihan untuk Program di Rumah | Physio8"
    desc = ("Timer latihan interval dari Physio8 untuk latihan pemulihan dan penguatan di rumah. "
            "Atur waktu latihan, istirahat, putaran dan set sesuai program dari fisioterapismu.")
    title_en = "Workout Timer for Your Home Programme | Physio8"
    desc_en = "Physio8's interval timer for recovery and strengthening exercise at home. Set work, rest, rounds and sets to match your physiotherapist's plan."
    ld = build.js({"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "@id": URL + "#app", "name": "Timer Latihan Physio8", "url": URL,
         "applicationCategory": "HealthApplication", "operatingSystem": "Web", "inLanguage": ["id-ID", "en"],
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "IDR"}, "publisher": build.PUBLISHER, "description": desc},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Beranda", "item": build.SITE_BASE},
            {"@type": "ListItem", "position": 2, "name": "Timer latihan", "item": URL}]},
    ]})
    head = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#2F1F71">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Physio8">
<meta property="og:locale" content="id_ID">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{build.SHARE_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script type="application/ld+json">
{ld}
</script>"""
    rows = "".join(_row(f) for f in FIELDS)
    presets = "".join(f'<button type="button" aria-pressed="false"{en(e)}>{i}</button>' for i, e, _ in PRESETS)
    ask = wa_pair("Halo Physio8, saya ingin dibuatkan program latihan untuk dilakukan di rumah.",
                  "Hi Physio8, I would like an exercise plan to do at home.")
    body = f"""{subpage(H.header())}
<main id="main">
<section class="tm-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/" data-en="Home">Beranda</a><span class="sl">/</span><span data-en="Workout timer">Timer latihan</span></nav>
    <p class="eyebrow" data-en="Exercise tool">Alat latihan</p>
    <h1 data-en="Workout timer for your home programme">Timer latihan untuk program di rumah</h1>
    <p class="lede" data-en="Set the work and rest times from your physiotherapist, then press Start. A sound and vibration mark every change, so you can focus on your movement.">Atur waktu latihan dan istirahat sesuai arahan fisioterapismu, lalu tekan Mulai. Bunyi dan getaran menandai setiap pergantian, jadi kamu cukup fokus pada gerakan.</p>
  </div>
</section>
<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="tm-grid">
      <div class="tm-card">
        <p class="tm-from" hidden style="margin-top:14px;padding:12px 16px;border-radius:14px;background:var(--teal-50);color:var(--teal-text);font-size:14.5px;font-weight:600" data-en="These settings came from the link you received. You can still adjust them.">Pengaturan ini berasal dari tautan yang kamu terima. Kamu tetap bisa mengubahnya.</p>
        <div class="tm-presets" role="group" aria-label="Pilihan cepat" data-en-aria-label="Quick picks"><p data-en="Quick picks">Pilihan cepat</p>{presets}</div>
        {rows}
        <div class="tm-name"><label for="tm-n" data-en="Exercise name (optional)">Nama latihan (opsional)</label>
          <input id="tm-n" type="text" maxlength="60" autocomplete="off" placeholder="Contoh: squat ke kursi" data-en-placeholder="e.g. sit-to-stand"></div>
        <div class="tm-opts" role="group" aria-label="Tanda" data-en-aria-label="Cues">
          <button type="button" class="tm-opt" data-o="beep">{icon("volume")}<span data-en="Sound">Bunyi</span></button>
          <button type="button" class="tm-opt" data-o="voice">{icon("megaphone")}<span data-en="Voice cues">Aba-aba suara</span></button>
          <button type="button" class="tm-opt" data-o="vib">{icon("vibrate")}<span data-en="Vibrate">Getar</span></button>
        </div>
      </div>
      <aside class="tm-side">
        <div class="tm-sum">
          <p class="k" data-en="Total time">Total waktu</p>
          <p class="big">0:00</p>
          <p class="meta"></p>
          <div class="tm-plan" aria-hidden="true"></div>
          <div class="tm-legend" aria-hidden="true"><span style="--c:#008699" data-en="Work">Latihan</span><span style="--c:#A6B717" data-en="Rest">Istirahat</span><span style="--c:#CBC3E8" data-en="Between sets">Antar set</span></div>
          <button type="button" class="btn btn-white start" data-act="start">{icon("play")}<span data-en="Start">Mulai</span></button>
        </div>
        <div class="tm-note">{icon("info")}<p data-en="Use the timing your physiotherapist gave you. Stop if you feel sharp pain, dizziness or chest pain.">Gunakan takaran dari fisioterapismu. Hentikan latihan jika muncul nyeri tajam, pusing, atau nyeri dada.</p></div>
        <div class="tm-share">
          <b data-en="Save or share these settings">Simpan atau bagikan pengaturan ini</b>
          <p data-en="The link opens this timer with the same settings. Handy for physiotherapists sending a programme to patients.">Tautan akan membuka timer ini dengan pengaturan yang sama. Praktis untuk fisioterapis yang mengirim program ke pasien.</p>
          <div class="acts"><button type="button" class="btn btn-ghost" id="tm-copy">{icon("link")}<span data-en="Copy link">Salin tautan</span></button>
            <a class="btn btn-ghost" id="tm-wa" href="https://wa.me/" target="_blank" rel="noopener noreferrer">{H.WA_GLYPH}<span data-en="Send via WhatsApp">Kirim via WhatsApp</span></a></div>
        </div>
      </aside>
    </div>
    <div class="tm-how">
      <div class="sec-head" style="margin-bottom:28px"><div><p class="eyebrow" data-en="How to use it">Cara menggunakan</p><h2 class="h2" data-en="Three steps to start">Tiga langkah untuk mulai</h2></div></div>
      <ol>
        <li><b data-en="Set your timing">Atur waktunya</b><p data-en="Pick a quick option or set work, rest, rounds and sets yourself.">Pilih salah satu pilihan cepat, atau atur sendiri waktu latihan, istirahat, putaran, dan set.</p></li>
        <li><b data-en="Place your phone where you can see it">Letakkan ponsel di tempat yang terlihat</b><p data-en="The screen stays on while the timer runs. Turn the volume up so you can hear each change.">Layar tetap menyala selama timer berjalan. Naikkan volume agar setiap pergantian terdengar.</p></li>
        <li><b data-en="Press Start and move">Tekan Mulai dan bergerak</b><p data-en="Tap the big button to pause. On a keyboard, Space pauses and the arrow keys skip.">Ketuk tombol besar untuk jeda. Di keyboard, tombol spasi untuk jeda dan tombol panah untuk melompat.</p></li>
      </ol>
    </div>
    {wa_cta("Belum punya program latihan di rumah?", "Don't have a home exercise plan yet?", "Tanyakan ke fisioterapis", "Ask a physiotherapist", ask)}
  </div>
</section>
{H.booking()}
</main>
{subpage(H.footer())}
<div class="tm-bar"><div class="t"><b>0:00</b><span></span></div><button type="button" class="btn btn-primary" data-act="start">{icon("play")}<span data-en="Start">Mulai</span></button></div>
<div class="stage" data-ph="prep" role="dialog" aria-modal="true" aria-label="Timer berjalan" data-en-aria-label="Timer running">
  <div class="st-top"><img src="/p8/logo-full-white.svg" alt="Physio8" width="60" height="40"><button type="button" class="st-x" data-act="stop" aria-label="Berhenti" data-en-aria-label="Stop">{icon("x")}</button></div>
  <div class="st-mid">
    <p class="st-ph"></p><p class="st-name"></p>
    <div class="st-ring"><svg viewBox="0 0 100 100" aria-hidden="true"><circle class="bg" cx="50" cy="50" r="48"/><circle class="fg" cx="50" cy="50" r="48"/></svg><div class="st-num" aria-hidden="true">0</div></div>
    <p class="st-meta"></p><p class="st-next"></p>
    <div class="st-done"><button type="button" class="btn btn-white" data-act="again">{icon("restart")}<span data-en="Do it again">Ulangi</span></button><button type="button" class="btn btn-white" data-act="stop" style="background:transparent;color:#fff;border-color:rgba(255,255,255,.5)"><span data-en="Back to settings">Kembali ke pengaturan</span></button></div>
  </div>
  <div class="st-ctl">
    <button type="button" class="sm" data-act="back" aria-label="Ulangi bagian ini" data-en-aria-label="Restart this block">{icon("restart")}</button>
    <button type="button" class="main" aria-label="Jeda" data-en-aria-label="Pause">{icon("pause")}</button>
    <button type="button" class="sm" data-act="skip" aria-label="Lewati" data-en-aria-label="Skip">{icon("skip")}</button>
  </div>
  <p class="st-total"></p>
  <p class="sr st-live" aria-live="polite"></p>
</div>
<div class="toast" role="status" aria-live="polite">Tautan disalin</div>"""
    fields = [{"k": f[0], "d": f[6], "min": f[7], "max": f[8], "t": f[9]} for f in FIELDS]
    js = (TIMER_JS.replace("__FIELDS__", json.dumps(fields)).replace("__PRESETS__", json.dumps([p[2] for p in PRESETS]))
          .replace("__URL__", json.dumps(URL)).replace("__ICONPLAY__", json.dumps(icon("play"))))
    meta = {"id": {"title": title, "desc": desc}, "en": {"title": title_en, "desc": desc_en}}
    html = page(head, body, meta, js)
    return html.replace("</style>", TIMER_CSS + "</style>", 1)
