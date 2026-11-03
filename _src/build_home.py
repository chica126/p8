#!/usr/bin/env python3
"""
Physio8 homepage generator  ->  index.html  (URL: https://physio8.id/)

Content source: Physio8 Company Profile 2026 (project file) + the latest logo
(Physiotherapy & Recovery lockup). Static HTML in Bahasa Indonesia so search and
AI engines read the full page; English is swapped in client-side from the
data-en / data-en-<attr> attributes on each element (ID | EN toggle).

Run via build.py (it calls build_home), or on its own:  python3 _src/build_home.py
Prices and clinic details live in the CONFIG block below. The soft-opening offer is
switched off (SHOW_SOFT = False); set it to True to show the banner and offer block again.
"""
import html, json, os, sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from home_css import CSS
from home_svg import icon, WA_GLYPH, posture_svg, rom_svg, squat_svg, loop_svg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://physio8.id/"

# ------------------------------------------------------------------ CONFIG
WA = "6281511488080"
WA_DISPLAY = "+62 815-1148-8080"
IG = "https://www.instagram.com/physio8.id/"
CAREERS = "https://glints.com/id/en/companies/physio8/7f663fbd-1efe-4650-8293-0537e3ce1c95"
MAP_EMBED = ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3965.957632458893!2d106.6246716!3d-6.2693024999999984"
             "!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69fdcf5e3ed823%3A0xe086797d26b0250d!2sPhysio8"
             "!5e0!3m2!1sid!2sid!4v1790002287669!5m2!1sid!2sid")
MAP_LINK = "https://www.google.com/maps/search/?api=1&query=Physio8+Ruko+Hudson+Paramount+Gading+Serpong"
GEO = (-6.2693025, 106.6246716)
SHOW_SOFT = False
SOFT_UNTIL = "2026-12-31"          # soft-opening block disappears after this date (WIB)

PRICES = {  # rupiah per session: single, package of 4, package of 8
    "std": (485000, 450000, 410000),
    "snr": (585000, 545000, 495000),
}
SOFT_OFF = (5, 8, 10)             # % off per session: single, pkg 4, pkg 8
LITE, TAPING = 80000, 100000

IMG_HERO = {"src": "https://images.unsplash.com/photo-1649751361457-01d3a696c7e6", "name": "yury kirillov",
            "profile": "https://unsplash.com/@relievemassage",
            "alt": ("Fisioterapis memeriksa lutut pasien yang berbaring", "A physiotherapist examining a patient's knee")}
IMG_METHOD = {"src": "https://images.unsplash.com/photo-1645005512942-a17817fb7c11", "name": "Sincerely Media",
              "profile": "https://unsplash.com/@sincerelymedia",
              "alt": ("Fisioterapis memandu latihan lengan dengan resistance band", "A physiotherapist guiding a resistance-band arm exercise")}
IMG_PILATES = {"src": "https://images.unsplash.com/photo-1717500251688-1c369ec2ab44", "name": "Ahmet Kurt",
               "profile": "https://unsplash.com/@ahmetkurt",
               "alt": ("Instruktur memandu latihan Pilates di reformer", "An instructor guiding a Pilates exercise on a reformer")}
UTM = "utm_source=physio8&utm_medium=referral"


# ------------------------------------------------------------------ helpers
def esc(s):
    return html.escape(s, quote=True)


def en(s):
    """English text for the element's innerHTML (swapped in by the language toggle)."""
    return f' data-en="{esc(s)}"'


def rp(n):
    return "Rp " + f"{n:,}".replace(",", ".")


def wa(text):
    return f"https://wa.me/{WA}?text=" + quote(text, safe="")


WA_BOOK = (wa("Halo Physio8, saya ingin membuat jadwal Movement & Posture Assessment. (dari website)"),
           wa("Hi Physio8, I would like to book a Movement & Posture Assessment. (from the website)"))


def wa_attrs(pair=WA_BOOK):
    return f'href="{esc(pair[0])}" data-en-href="{esc(pair[1])}" target="_blank" rel="noopener noreferrer"'


def unsplash(img, w, h):
    return f"{img['src']}?w={w}&h={h}&q=80&auto=format&fit=crop&crop=faces,entropy"


def photo(img, w, h, cls="photo", eager=False, sizes="(max-width: 920px) 100vw, 50vw"):
    srcset = ", ".join(f"{unsplash(img, int(w*f), int(h*f))} {int(w*f)}w" for f in (0.5, 1, 1.5))
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    prof = img["profile"] + "?" + UTM
    return (f'<figure class="{cls}"><img src="{esc(unsplash(img, w, h))}" srcset="{esc(srcset)}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{esc(img["alt"][0])}" data-en-alt="{esc(img["alt"][1])}" {load} decoding="async">'
            f'<figcaption class="credit"><span{en("Photo")}>Foto</span>: <a href="{esc(prof)}" target="_blank" rel="noopener">{esc(img["name"])}</a> / '
            f'<a href="https://unsplash.com/?{esc(UTM)}" target="_blank" rel="noopener">Unsplash</a></figcaption></figure>')


def mix(c1, c2, t):
    a = [int(c1[i:i+2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i+2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def journey(i, n=8):
    """purple -> teal -> lime, the brand's progress ramp."""
    t = i / (n - 1)
    return mix("#2F1F71", "#008699", t / .5) if t <= .5 else mix("#008699", "#A6B717", (t - .5) / .5)


# ------------------------------------------------------------------ content
NAV = [("metode", "Metode", "Method"), ("pilates", "Clinical Pilates", "Clinical Pilates"), ("harga", "Harga", "Prices"),
       ("tim", "Tim", "Team"), ("lokasi", "Lokasi", "Location"), ("artikel", "Artikel", "Articles")]

STEPS = [
    ("Assess", "Diukur dengan teknologi dan pemeriksaan klinis.", "Measured with technology and a clinical exam."),
    ("Diagnose", "Movement Report: diagnosis fisioterapi, rencana, dan biaya.", "Movement Report: physiotherapy diagnosis, plan and cost."),
    ("Relieve", "Nyeri turun sampai target yang disepakati.", "Pain brought down to the agreed target."),
    ("Rebuild", "Rentang gerak dan kapasitas beban dibangun kembali.", "Range of motion and load capacity rebuilt."),
    ("Strengthen", "Clinical Pilates dan pembebanan progresif.", "Clinical Pilates and progressive loading."),
    ("Retrain", "Pola gerak yang lebih baik, lalu tes ulang.", "Better movement patterns, then a re-test."),
    ("Return", "Tes kesiapan dan laporan akhir terapi.", "Readiness test and discharge report."),
    ("Maintain", "Pilates, program rumah, dan tes ulang berkala.", "Pilates, a home plan and periodic re-tests."),
]

METHOD = [
    ("01–02", "Diagnostik berbantuan alat", "Tool-assisted diagnostic",
     "Computer vision berbasis AR mengukur postur, gerak, dan rentang gerak, bersama pemeriksaan klinis lengkap. Hari pertama menjadi baseline-mu, dalam angka.",
     "AR-assisted computer vision measures posture, movement and range of motion alongside a full clinical exam. Day one becomes your baseline, in numbers.",
     [("Postur 4 sisi", "4-view posture"), ("Rentang gerak", "Range of motion"), ("Squat screen", "Squat screen")]),
    ("03–04", "Penanganan", "Treatment",
     "Terapi manual dan modalitas yang dipilih sesuai protokol, bukan kebiasaan terapis.",
     "Manual therapy and modalities chosen by protocol, not by habit.",
     [("Terapi manual", "Manual therapy"), ("Ultrasound", "Ultrasound"), ("Dry needling", "Dry needling"), ("TENS", "TENS"), ("Infrared", "Infrared")]),
    ("05–06", "Clinical Pilates", "Clinical Pilates",
     "Pilates yang dipandu fisioterapis dan pembebanan progresif, untuk membangun kekuatan dan kontrol yang menurunkan risiko cedera berulang.",
     "Physio-guided Pilates and progressive loading that build the strength and control that lower the risk of re-injury.", []),
    ("02–08", "Rencana pemulihan", "Recovery plan",
     "Diagnosis, penyebab, jumlah sesi, dan total biaya disampaikan tertulis sebelum terapi dimulai.",
     "Diagnosis, cause, number of sessions and total cost, in writing, before therapy starts.", []),
    ("06 & 08", "Tes ulang setelah terapi", "Post-treatment re-test",
     "Pengukuran yang sama diulang di tahap 6 dan 8, lalu dibandingkan berdampingan dengan hari pertama.",
     "The same measurements repeated at steps 6 and 8, side by side with day one.", []),
]

VALUES = [
    ("E", "Evidence-based practice", "Baseline diukur, lalu dites ulang. Bukti perkembangan adalah hasil yang kamu bawa pulang.",
     "Measured baselines, re-tested. The evidence is the product."),
    ("I", "Intentional engagement", "Satu pasien dalam satu waktu. Tidak ada layanan ala ban berjalan.",
     "One patient at a time. No production-line care."),
    ("G", "Guide every step", "Delapan tahap, masing-masing dijelaskan. Kamu selalu tahu apa yang berikutnya.",
     "Eight steps, each explained. You always know what comes next."),
    ("H", "Highest standards of hygiene", "Klinik yang bersih tanpa cela, dengan ruang putih yang memperlihatkannya.",
     "A spotless clinic, and white space that shows it."),
    ("T", "Total patient trust", "Harga dipublikasikan, linimasa yang jujur, termasuk kabar yang kurang menyenangkan.",
     "Published prices, honest timelines, bad news included."),
]

CREDS = [
    ("18+ tahun praktik klinis, sejak 2008", "18+ years in clinical practice, since 2008"),
    ("Sertifikasi dry needling, Australian Physiotherapy Association", "Certified in dry needling, Australian Physiotherapy Association"),
    ("Sertifikasi Mulligan Concept", "Certified in the Mulligan Concept"),
    ("Sarjana Fisioterapi, Universitas Esa Unggul", "Bachelor of Physiotherapy, Esa Unggul University"),
    ("Mantan staf pengajar fisioterapi, Universitas Esa Unggul", "Former physiotherapy faculty staff, Esa Unggul University"),
    ("Pelatihan podiatri dan dasar women's health", "Trained in podiatry and basic women's health"),
]

FAQ = [
    ("Apakah saya perlu surat rujukan dokter?", "Do I need a doctor's referral?",
     "Tidak. Pasien dapat datang langsung ke fisioterapis sesuai Standar Pelayanan Fisioterapi (Permenkes No. 65 Tahun 2015). Bila temuan kami mengarah ke kondisi yang memerlukan pencitraan atau tindakan medis, kami merujukmu ke dokter spesialis dan menjelaskan alasannya.",
     "No. You can see a physiotherapist directly under Indonesia's physiotherapy service standard (Ministry of Health Regulation No. 65/2015). If our findings point to a condition that needs imaging or medical treatment, we refer you to a specialist and explain why."),
    ("Apa yang terjadi di kunjungan pertama?", "What happens at the first visit?",
     "Movement & Posture Assessment: wawancara dan skrining tanda bahaya, pemetaan postur dari empat sisi, pengukuran rentang gerak, squat screen, lalu pemeriksaan klinis. Kamu pulang dengan diagnosis fisioterapi, rencana pemulihan, dan total biayanya.",
     "The Movement & Posture Assessment: an interview and red-flag screen, four-view posture mapping, range-of-motion measurement, a squat screen, then a clinical exam. You leave with a physiotherapy diagnosis, a recovery plan and its total cost."),
    ("Apa bedanya clinical Pilates dengan kelas Pilates biasa?", "How is clinical Pilates different from a regular Pilates class?",
     "Clinical Pilates dipandu fisioterapis yang memegang data pengukuranmu. Latihannya dipilih sesuai tahap pemulihan, bebannya dinaikkan bertahap, dan hasilnya dites ulang di tahap 6 dan 8. Fokusnya kekuatan inti, kontrol, dan postur.",
     "Clinical Pilates is guided by the physiotherapist who holds your measurements. Exercises are chosen for your stage of recovery, load is progressed step by step, and results are re-tested at steps 6 and 8. The focus is core strength, control and posture."),
    ("Apakah saya harus membeli paket?", "Do I have to buy a package?",
     "Tidak. Kamu bisa membayar per sesi. Paket 4 sesi (berlaku 8 minggu) dan 8 sesi (berlaku 14 minggu) menurunkan harga per sesi. Jumlah sesi yang kamu butuhkan kami tulis di rencana pemulihan.",
     "No. You can pay per session. Packages of 4 sessions (valid 8 weeks) and 8 sessions (valid 14 weeks) lower the price per session. The number of sessions you need is written in your recovery plan."),
    ("Bagaimana cara membuat jadwal?", "How do I book?",
     f"Lewat WhatsApp di {WA_DISPLAY}. Pengingat jadwal dan program rumahmu juga dikirim lewat WhatsApp.",
     f"On WhatsApp at {WA_DISPLAY}. Appointment reminders and your home programme come through WhatsApp too."),
    ("Di mana lokasi Physio8?", "Where is Physio8?",
     "Ruko Hudson Blok B No. 29, Paramount Gading Serpong, Medang, Pagedangan, Kabupaten Tangerang, Banten 15334 — sekitar 4,8 km dari gerbang tol West BSD 1.",
     "Ruko Hudson Blok B No. 29, Paramount Gading Serpong, Medang, Pagedangan, Tangerang Regency, Banten 15334 — about 4.8 km from the West BSD 1 toll gate."),
]

TITLE = ("Physio8 — Klinik Fisioterapi & Clinical Pilates di Gading Serpong",
         "Physio8 — Physiotherapy & Clinical Pilates Clinic in Gading Serpong")
DESC = ("Fisioterapi dan clinical Pilates di Paramount Gading Serpong. Asesmen postur berbantuan AR, Physio8 Pathway delapan tahap, dan harga per sesi yang dipublikasikan.",
        "Physiotherapy and clinical Pilates in Paramount Gading Serpong. AR-assisted posture assessment, the eight-step Physio8 Pathway and published per-session prices.")


# ------------------------------------------------------------------ sections
def header():
    links = "".join(f'<a href="#{a}"{en(e)}>{i}</a>' for a, i, e in NAV)
    mlinks = "".join(f'<a href="#{a}"{en(e)}>{i}</a>' for a, i, e in NAV)
    soft = (f'<div class="notice" data-until="{SOFT_UNTIL}"><div class="wrap"><span class="dot" aria-hidden="true"></span>'
            f'<p{en("<strong>Soft opening, November–December 2026.</strong> Your first visit is on us, including the Movement &amp; Posture Assessment.")}>'
            f'<strong>Soft opening November–Desember 2026.</strong> Kunjungan pertama ditanggung Physio8, termasuk Movement &amp; Posture Assessment.</p>'
            f'<a href="#harga"{en("See the details")}>Lihat ketentuan</a></div></div>')
    return f"""<a class="skip" href="#main"{en("Skip to content")}>Lewati ke konten</a>
{soft if SHOW_SOFT else ""}
<header class="hdr">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Physio8"><img src="./p8/logo-full.svg" alt="Physio8 — Physiotherapy &amp; Recovery" width="90" height="60"></a>
    <nav class="nav" aria-label="Utama" data-en-aria-label="Main">{links}</nav>
    <div class="hdr-right">
      <div class="lang" role="group" aria-label="Bahasa / Language">
        <button type="button" data-lang="id" aria-pressed="true">ID</button><button type="button" data-lang="en" aria-pressed="false">EN</button>
      </div>
      <a class="btn btn-primary btn-desk" {wa_attrs()}><span{en("Book an assessment")}>Buat jadwal asesmen</span></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu">{icon("menu")}</button>
    </div>
  </div>
</header>
<div class="mnav" id="mnav">{mlinks}<a class="btn btn-primary" {wa_attrs()}><span{en("Book an assessment")}>Buat jadwal asesmen</span></a></div>"""


def hero():
    facts = [("Satu terapis, satu pasien", "One therapist, one patient"),
             ("Protokol KNGF dan riset University of Melbourne", "KNGF protocols and University of Melbourne research"),
             ("Harga per sesi dipublikasikan", "Per-session prices published")]
    fl = "".join(f'<li>{icon("ccheck")}<span{en(e)}>{i}</span></li>' for i, e in facts)
    return f"""<section class="hero" id="main">
  <div class="wrap">
    <div>
      <p class="hero-k"><span{en("Physiotherapy &amp; clinical Pilates")}>Fisioterapi &amp; clinical Pilates</span><span class="sep" aria-hidden="true"></span><span>Paramount Gading Serpong</span></p>
      <h1>
        <span class="display"><span>Recover.</span><span class="c2">Move.</span><span class="c3">Repeat.</span></span>
        <span class="h1-sub"{en("Specialist physiotherapy and clinical Pilates in Gading Serpong, measured from day one.")}>Klinik fisioterapi dan clinical Pilates di Gading Serpong, terukur sejak hari pertama.</span>
      </h1>
      <p class="lede"{en("Every recovery starts with numbers. Your posture, range of motion and movement are measured with AR-assisted computer vision and a clinical exam. You get a physiotherapy diagnosis, an eight-step plan and its total cost before therapy starts.")}>Setiap pemulihan dimulai dari angka. Postur, rentang gerak, dan pola gerakmu diukur dengan computer vision berbasis AR dan pemeriksaan klinis. Kamu mendapat diagnosis fisioterapi, rencana delapan tahap, dan total biayanya sebelum terapi dimulai.</p>
      <div class="hero-cta">
        <a class="btn btn-primary" {wa_attrs()}>{WA_GLYPH}<span{en("Book an assessment")}>Buat jadwal asesmen</span></a>
        <a class="btn btn-ghost" href="#harga"><span{en("See prices")}>Lihat harga</span>{icon("arrow")}</a>
      </div>
      <ul class="hero-facts">{fl}</ul>
    </div>
    <div class="hero-media">
      <figure class="photo hero-photo"><picture><source type="image/webp" srcset="./p8/hero-fasad-640.webp 640w, ./p8/hero-fasad.webp 1008w" sizes="(max-width: 920px) 100vw, 50vw"><img src="./p8/hero-fasad.jpg" width="1008" height="1062" alt="Fasad klinik Physio8 di Ruko Hudson, Paramount Gading Serpong" data-en-alt="The Physio8 clinic front at Ruko Hudson, Paramount Gading Serpong" fetchpriority="high" decoding="async"></picture></figure>
    </div>
  </div>
</section>"""


def numbers():
    items = [("8", "tahap Physio8 Pathway, dari asesmen sampai pemeliharaan", "steps in the Physio8 Pathway, from assessment to maintenance"),
             ("4", "sisi pemetaan postur dengan computer vision", "views of computer-vision posture mapping"),
             ("1:1", "satu terapis untuk satu pasien di setiap sesi", "one therapist for one patient, every session"),
             ("18+", "tahun pengalaman klinis lead physiotherapist kami", "years of clinical experience behind our lead physiotherapist")]
    li = "".join(f'<li><b class="tnum">{n}</b><span{en(e)}>{i}</span></li>' for n, i, e in items)
    return f'<div class="numbers"><div class="wrap"><ul>{li}</ul></div></div>'


def pathway():
    steps = ""
    for k, (name, i, e) in enumerate(STEPS):
        c = journey(k)
        steps += (f'<li class="step rv"><div class="bar" style="background:{c}"></div>'
                  f'<span class="no" style="color:{c if k < 6 else "#6C7800"}">{k+1:02d}</span>'
                  f'<h3>{name}</h3><p{en(e)}>{i}</p></li>')
    return f"""<section class="sec" id="metode">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Physio8 Pathway</p><h2 class="h2"{en("Eight steps, one method")}>Delapan tahap, satu metode</h2></div>
      <p class="lede"{en("You always know which step you are on, what its target is and what comes next. Steps 1–2 happen in the clinic; steps 3–8 run hybrid, clinic sessions plus a home programme we monitor.")}>Kamu selalu tahu sedang di tahap mana, apa targetnya, dan apa yang datang berikutnya. Tahap 1–2 berlangsung di klinik; tahap 3–8 berjalan hibrida, sesi di klinik ditambah program rumah yang kami pantau.</p>
    </div>
    <ol class="steps">{steps}</ol>
    <div class="phase" aria-hidden="true"><div{en("In clinic")}>Di klinik</div><div{en("Hybrid: clinic sessions + home programme")}>Hibrida: sesi klinik + program rumah</div></div>
    <div class="pathway-foot">
      <p{en("Every step has a measured exit criterion. You move up because you have progressed, and the re-tests at steps 6 and 8 show it next to your day-one numbers.")}>Setiap tahap punya kriteria keluar yang terukur. Kamu naik tahap karena adanya progres, dan tes ulang di tahap 6 dan 8 memperlihatkannya di samping angka hari pertama.</p>
      <a class="link-arrow" href="/artikel/physio8-pathway-delapan-tahap/"><span{en("Read the full pathway")}>Baca penjelasan lengkap</span>{icon("arrow")}</a>
    </div>
  </div>
</section>"""


def method():
    rows = ""
    for rng, ti, te, di, de, tags in METHOD:
        tg = ""
        if tags:
            tg = '<div class="tags">' + "".join(f'<span{en(e)}>{i}</span>' if i != e else f"<span>{i}</span>" for i, e in tags) + "</div>"
        lbl = ("Tahap ", "Steps ")
        rows += (f'<li class="rv"><span class="rng"><span{en(lbl[1] + rng.replace("&", "&amp;"))}>{lbl[0]}{rng.replace("&", "&amp;")}</span></span>'
                 f'<div><h3{en(te)}>{ti}</h3><p{en(de)}>{di}</p>{tg}</div></li>')
    return f"""<section class="sec">
  <div class="wrap method">
    {photo(IMG_METHOD, 900, 1125)}
    <div>
      <p class="eyebrow"{en("Methodology")}>Metodologi</p>
      <h2 class="h2"{en("How the steps become a method")}>Bagaimana tahapan menjadi metode</h2>
      <p class="lede" style="margin-bottom:36px"{en("The same structure for every patient, so the plan does not depend on which therapist you see.")}>Struktur yang sama untuk setiap pasien, sehingga rencanamu tidak bergantung pada terapis mana yang menangani.</p>
      <ul class="mlist">{rows}</ul>
    </div>
  </div>
</section>"""


def assessment():
    tools = [
        (posture_svg([("Depan", "Front"), ("Kanan", "Right"), ("Belakang", "Back"), ("Kiri", "Left")]),
         "Postur dengan computer vision", "Posture, by computer vision",
         "Pemetaan berbantuan AR dari empat sisi: depan, kanan, belakang, dan kiri.", "AR-assisted mapping from four views: front, right, back and left."),
        (rom_svg(), "Rentang gerak", "Range of motion",
         "Leher, punggung, dan bahu, diukur dengan kamera dan giroskop.", "Neck, back and shoulders, measured by camera and gyroscope."),
        (squat_svg(), "Gerak fungsional", "Functional movement",
         "Squat screen memberi data gerak yang cepat dan objektif.", "Squat screens give fast, objective movement data."),
    ]
    cards = "".join(f'<div class="tool rv"><div class="viz">{svg}</div><h3{en(te)}>{ti}</h3><p{en(de)}>{di}</p></div>'
                    for svg, ti, te, di, de in tools)
    flow = "".join(f"<li><span>{n}</span>{w}</li>" for n, w in enumerate(["Scan", "Check", "Plan", "Re-scan"], 1))
    return f"""<section class="sec dark" id="asesmen">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow"{en("Tool-assisted diagnostic")}>Diagnostik berbantuan alat</p><h2 class="h2"{en("Measured, not guessed")}>Diukur, bukan ditebak</h2></div>
      <div><p class="lede"{en("Your first visit, the Movement &amp; Posture Assessment, turns how you stand and move into numbers. The same scan is repeated later, so progress is something you can see.")}>Kunjungan pertamamu, Movement &amp; Posture Assessment, mengubah cara kamu berdiri dan bergerak menjadi angka. Pemindaian yang sama diulang kemudian, sehingga perkembangan bisa kamu lihat sendiri.</p>
      <ol class="scan-flow" aria-label="Scan, Check, Plan, Re-scan">{flow}</ol></div>
    </div>
    <div class="tools">{cards}</div>
    <p class="dark-foot"{en("Measurements sit alongside a full clinical exam by a physiotherapist. The technology supports clinical judgement; it does not replace it.")}>Pengukuran ini berjalan bersama pemeriksaan klinis lengkap oleh fisioterapis. Teknologi membantu penilaian klinis, bukan menggantikannya.</p>
  </div>
</section>"""


def pilates():
    def track(cls, ti, te, si, se, on, half):
        cells = "".join(f'<i class="{"on" if k in on else ("half" if k in half else "")}"></i>' for k in range(1, 9))
        return (f'<div class="track {cls}"><div class="lbl"><b{en(te)}>{ti}</b><span{en(se)}>{si}</span></div>'
                f'<div class="row">{cells}</div></div>')
    nums = "".join(f"<span>{k:02d}</span>" for k in range(1, 9))
    yam = "https://doi.org/10.1002/14651858.CD010265.pub2"
    ste = "https://doi.org/10.1001/jamainternmed.2015.7431"
    r2_id = (f'Tinjauan Cochrane menemukan Pilates lebih efektif dibanding intervensi minimal untuk nyeri punggung bawah kronis '
             f'(<a href="{yam}" target="_blank" rel="noopener">Yamato, 2015</a>). Latihan yang disertai edukasi menurunkan risiko episode nyeri punggung bawah '
             f'(<a href="{ste}" target="_blank" rel="noopener">Steffens, 2016</a>).')
    r2_en = (f'A Cochrane review found Pilates more effective than minimal intervention for chronic low back pain '
             f'(<a href="{yam}" target="_blank" rel="noopener">Yamato, 2015</a>). Exercise combined with education lowered the risk of further low back pain episodes '
             f'(<a href="{ste}" target="_blank" rel="noopener">Steffens, 2016</a>).')
    return f"""<section class="sec tint" id="pilates">
  <div class="wrap pil">
    {photo(IMG_PILATES, 960, 1152)}
    <div>
      <p class="eyebrow"{en("Why clinical Pilates")}>Mengapa clinical Pilates</p>
      <h2 class="h2"{en("Pain relief is just step one")}>Meredakan nyeri baru tahap pertama</h2>
      <div class="tracks">
        {track("p1", "Fisioterapi", "Physiotherapy", "nyeri · rentang gerak · jaringan cedera", "pain · range of motion · injured tissue", {1, 2, 3, 4}, {5, 6, 7})}
        {track("p2", "Clinical Pilates", "Clinical Pilates", "kekuatan inti · kontrol · postur", "core strength · control · posture", {5, 6, 7, 8}, {4})}
        <div class="track-nums" aria-hidden="true">{nums}</div>
      </div>
      <ul class="reasons">
        <li><span class="ix">01</span><div><h3{en("Recovery goes on")}>Pemulihan berlanjut</h3><p{en("Pain relief alone does not train strength or control. Skip that stage and the pattern behind the injury often stays.")}>Meredakan nyeri saja tidak melatih kekuatan dan kontrol. Bila tahap ini dilewati, pola yang menyebabkan cedera sering tetap ada.</p></div></li>
        <li><span class="ix">02</span><div><h3{en("Backed by evidence")}>Didukung bukti</h3><p{en(r2_en)}>{r2_id}</p></div></li>
        <li><span class="ix">03</span><div><h3{en("Dosed to you")}>Dosis sesuai kebutuhanmu</h3><p{en("Guided by the physiotherapist who knows your measurements, progressed step by step and re-tested at steps 6 and 8.")}>Dipandu fisioterapis yang memegang data pengukuranmu, ditingkatkan bertahap, dan dites ulang di tahap 6 dan 8.</p></div></li>
      </ul>
    </div>
  </div>
</section>"""


def values():
    cards = "".join(f'<li class="value rv"><span class="l" aria-hidden="true">{l}</span><h3>{t}</h3><p{en(e)}>{i}</p></li>'
                    for l, t, i, e in VALUES)
    return f"""<section class="sec tint" id="nilai">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow"{en("Core values · E.I.G.H.T.")}>Nilai kami · E.I.G.H.T.</p><h2 class="h2"{en("Evidence-based care, measured progress")}>Perawatan berbasis bukti, progres yang terukur</h2></div>
      <p class="lede"{en("Five commitments, spelled by the number our name is built on. Every plan, message and decision at Physio8 traces back to one of them.")}>Lima komitmen, dieja dari angka yang menjadi nama kami. Setiap rencana, pesan, dan keputusan di Physio8 berakar pada salah satunya.</p>
    </div>
    <ul class="values">{cards}</ul>
    <div class="trained rv"><span class="ic">{icon("cap")}</span><div><h3{en("Trained on international methods")}>Dilatih dengan metode internasional</h3>
      <p{en("Protocols and training follow KNGF guidelines (Royal Dutch Society for Physical Therapy) and University of Melbourne research. Every therapist is certified on them before treating alone.")}>Protokol dan pelatihan mengikuti pedoman KNGF (Royal Dutch Society for Physical Therapy) dan riset University of Melbourne. Setiap terapis disertifikasi pada protokol ini sebelum menangani pasien sendiri.</p></div></div>
  </div>
</section>"""


def team():
    creds = "".join(f'<li>{icon("check")}<span{en(e)}>{i}</span></li>' for i, e in CREDS)
    return f"""<section class="sec" id="tim">
  <div class="wrap">
    <p class="eyebrow"{en("Lead physiotherapist")}>Lead physiotherapist</p>
    <h2 class="h2" style="margin-bottom:40px"{en("One clinical standard, led by experience")}>Satu standar klinis, dipimpin pengalaman</h2>
    <div class="lead rv">
      <div class="lead-id">
        <figure class="lead-photo"><picture><source type="image/webp" srcset="./p8/ika-setia-ningsih.webp"><img src="./p8/ika-setia-ningsih.jpg" width="525" height="552" alt="Ika Setia Ningsih, S.Ft, Lead Physiotherapist Physio8" data-en-alt="Ika Setia Ningsih, S.Ft, Lead Physiotherapist at Physio8" loading="lazy" decoding="async"></picture></figure>
        <div class="lead-info">
          <p class="role"{en("Lead Physiotherapist")}>Lead Physiotherapist</p>
          <p class="name">Ika Setia Ningsih, S.Ft</p>
          <div class="yrs"><b class="tnum">18+</b><span{en("years of hands-on<br>practice since 2008")}>tahun praktik<br>langsung sejak 2008</span></div>
        </div>
      </div>
      <div class="lead-bio">
        <p class="big"{en("18 years of hands-on practice across Jakarta clinics, including senior physiotherapist roles, and former physiotherapy faculty staff at Esa Unggul University. Ika leads Physio8's clinical team, so every plan follows one clinical standard.")}>18 tahun praktik langsung di berbagai klinik di Jakarta, termasuk sebagai senior physiotherapist, dan pernah menjadi staf pengajar fisioterapi di Universitas Esa Unggul. Ika memimpin tim klinis Physio8, sehingga setiap rencana mengikuti satu standar klinis.</p>
        <ul class="creds">{creds}</ul>
      </div>
    </div>
  </div>
</section>"""


def pricing():
    def card(key, ti, te, si, se, cls=""):
        s, p4, p8 = PRICES[key]
        rows = (f'<div class="prow"><span class="k"><span{en("Single session")}>Satu sesi</span><small{en("Pay as you go")}>Bayar per kedatangan</small></span>'
                f'<span class="v tnum">{rp(s)}<small{en("per session")}>per sesi</small></span></div>'
                f'<div class="prow"><span class="k"><span{en("Package of 4")}>Paket 4 sesi</span><small{en("Valid 8 weeks")}>Berlaku 8 minggu</small></span>'
                f'<span class="v tnum">{rp(p4)}<small{en(f"per session · {rp(p4*4)} total")}>per sesi · total {rp(p4*4)}</small></span></div>'
                f'<div class="prow"><span class="k"><span{en("Package of 8")}>Paket 8 sesi</span><small{en("Valid 14 weeks")}>Berlaku 14 minggu</small></span>'
                f'<span class="v tnum">{rp(p8)}<small{en(f"per session · {rp(p8*8)} total")}>per sesi · total {rp(p8*8)}</small></span></div>')
        return (f'<article class="pcard {cls} rv"><div class="head"><div><h3>{ti}</h3><p class="sub"{en(se)}>{si}</p></div></div>'
                f'{rows}<div class="foot"><a class="btn btn-ghost" {wa_attrs()}><span{en("Book on WhatsApp")}>Jadwalkan via WhatsApp</span>{icon("arrow")}</a></div></article>')
    std = card("std", "Physiotherapy Standard", "Physiotherapy Standard", "Sesi fisioterapi satu terapis, satu pasien.", "A one-to-one physiotherapy session.")
    snr = card("snr", "Physiotherapy Senior", "Physiotherapy Senior", "Sesi fisioterapi satu terapis, satu pasien, dengan fisioterapis senior.", "A one-to-one physiotherapy session with a senior physiotherapist.", "senior")
    terms = [("Tidak dapat dikembalikan", "Non-refundable"), ("Tidak dapat diuangkan", "Cannot be cashed out"),
             ("Tidak dapat dipindahtangankan", "Non-transferable"), ("Tidak dapat ditukar atau di-upgrade (Standard ke Senior)", "No exchange or upgrade (Standard to Senior)")]
    tl = f'<li class="k"><b{en("Package terms:")}>Ketentuan paket:</b></li>' + "".join(f"<li{en(e)}>{i}</li>" for i, e in terms)
    # soft opening
    offs = (f'<div class="off"><p class="p"{en("Free")}>Tanpa biaya</p><p class="d"{en("First visit: Movement &amp; Posture Assessment, your baseline and a plan with its total cost")}>Kunjungan pertama: Movement &amp; Posture Assessment, baseline-mu, dan rencana beserta total biayanya</p></div>'
            + "".join(f'<div class="off"><p class="p">{pc}%</p><p class="d"{en(f"off every session · {le}")}>potongan setiap sesi · {li}</p></div>'
                      for pc, li, le in zip(SOFT_OFF, ("satu sesi", "paket 4 sesi", "paket 8 sesi"), ("single session", "package of 4", "package of 8"))))
    trs = ""
    for key, name in (("std", "Physiotherapy Standard"), ("snr", "Physiotherapy Senior")):
        tds = "".join(f'<td class="tnum"><b>{rp(round(p * (100 - o) / 100))}</b><s>{rp(p)}</s></td>' for p, o in zip(PRICES[key], SOFT_OFF))
        trs += f"<tr><th scope=\"row\">{name}</th>{tds}</tr>"
    soft = f"""<div class="soft rv" data-until="{SOFT_UNTIL}">
      <div class="soft-top"><div><p class="k"{en("Soft opening · November–December 2026")}>Soft opening · November–Desember 2026</p>
        <h3{en("Your first visit is on us")}>Kunjungan pertama ditanggung Physio8</h3>
        <p class="lede"{en("Your baseline, measured with AR-assisted computer vision, and a plan with its total cost. Sessions booked during the soft opening are priced below.")}>Baseline-mu diukur dengan computer vision berbasis AR, lalu kamu menerima rencana beserta total biayanya. Sesi yang dipesan selama soft opening mengikuti harga di bawah.</p></div>
        <a class="btn btn-primary" {wa_attrs()}>{WA_GLYPH}<span{en("Book your first visit")}>Jadwalkan kunjungan pertama</span></a></div>
      <div class="offs">{offs}</div>
      <div class="soft-table"><table><thead><tr><th scope="col"{en("Per session")}>Per sesi</th><th scope="col"{en("Single")}>Satu sesi</th><th scope="col"{en("Package of 4")}>Paket 4 sesi</th><th scope="col"{en("Package of 8")}>Paket 8 sesi</th></tr></thead><tbody>{trs}</tbody></table></div>
      <p class="note"{en("One free first visit per new patient. Package terms apply (validity 8 or 14 weeks). Reductions do not combine; targeted lite treatment and kinesio taping stay at the normal price.")}>Satu kunjungan pertama tanpa biaya untuk setiap pasien baru. Ketentuan paket berlaku (masa berlaku 8 atau 14 minggu). Potongan tidak dapat digabung; targeted lite treatment dan kinesio taping tetap harga normal.</p>
    </div>"""
    return f"""<section class="sec" id="harga">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow"{en("Services and prices")}>Layanan dan harga</p><h2 class="h2"{en("Published prices, per session")}>Harga per sesi, dipublikasikan</h2></div>
      <p class="lede"{en("Your recovery plan states the number of sessions and the total cost before therapy starts. Packages are optional.")}>Rencana pemulihanmu mencantumkan jumlah sesi dan total biaya sebelum terapi dimulai. Paket bersifat pilihan, bukan kewajiban.</p>
    </div>
    <div class="price-grid">{std}{snr}</div>
    <div class="addons">
      <div class="addon rv"><div><b>Targeted lite treatment</b><span{en("15 minutes · one focused area")}>15 menit · satu area fokus</span></div><span class="v tnum">{rp(LITE)}</span></div>
      <div class="addon rv"><div><b>Kinesio taping</b><span{en("Per application")}>Per aplikasi</span></div><span class="v tnum">{rp(TAPING)}</span></div>
    </div>
    <ul class="terms">{tl}</ul>
    {soft if SHOW_SOFT else ""}
  </div>
</section>"""


def location():
    acc = [("car", "Mobil", "By car", "Gerbang tol West BSD 1: 4,8 km · Legok: 6,1 km", "West BSD 1 toll gate: 4.8 km · Legok: 6.1 km"),
           ("train", "Kereta", "By train", "KRL ke Stasiun Rawa Buntu, 7,6 km", "KRL to Rawa Buntu station, 7.6 km"),
           ("building", "Sekitar", "Nearby", "UMN 1,6 km · Summarecon Mall Serpong 3,2 km", "UMN 1.6 km · Summarecon Mall Serpong 3.2 km")]
    al = "".join(f'<li><span class="ic">{icon(ic)}</span><div><b{en(te)}>{ti}</b><span{en(de)}>{di}</span></div></li>' for ic, ti, te, di, de in acc)
    return f"""<section class="sec" id="lokasi">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow"{en("Our location")}>Lokasi kami</p><h2 class="h2">Paramount Gading Serpong</h2></div>
      <p class="lede"{en("Our clinic is in the Ruko Hudson row at Paramount Gading Serpong, Tangerang.")}>Klinik kami berada di deretan Ruko Hudson, Paramount Gading Serpong, Tangerang.</p>
    </div>
    <div class="loc">
      <div class="map"><iframe src="{esc(MAP_EMBED)}" title="Peta lokasi Physio8" data-en-title="Map of Physio8's location" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>
      <div class="loc-card">
        <address><b>Physio8</b>Ruko Hudson Blok B No. 29<br>Paramount Gading Serpong<br>Medang, Pagedangan<br><span{en("Tangerang Regency, Banten 15334")}>Kabupaten Tangerang, Banten 15334</span></address>
        <ul class="access">{al}</ul>
        <div class="acts">
          <a class="btn btn-primary" href="{esc(MAP_LINK)}" target="_blank" rel="noopener noreferrer">{icon("pin")}<span{en("Open in Google Maps")}>Buka di Google Maps</span></a>
          <a class="btn btn-ghost" {wa_attrs()}>{WA_GLYPH}<span>WhatsApp</span></a>
        </div>
      </div>
    </div>
  </div>
</section>"""


def articles(arts, img_fn, date_fn):
    bys = {a["slug"]: a for a in arts}
    feat = bys["asesmen-gerak-dan-postur"]
    rest = [bys[s] for s in ("nyeri-setelah-olahraga-weekend", "nyeri-pinggang-duduk-lama", "nyeri-bahu-padel")]

    def card(a, cls, w, h):
        d = date_fn(a["published"])
        im = a["image"]
        return (f'<a class="acard {cls} rv" href="/artikel/{a["slug"]}/">'
                f'<figure class="photo"><img src="{esc(img_fn(a, w, h))}" width="{w}" height="{h}" alt="{esc(im["alt"][0])}" data-en-alt="{esc(im["alt"][1])}" loading="lazy" decoding="async">'
                f'<figcaption class="credit"><span{en("Photo")}>Foto</span>: {esc(im["name"])} / Unsplash</figcaption></figure>'
                f'<div class="body"><p class="meta"><span{en(a["tag"][1] + " · " + d[1])}>{a["tag"][0]} · {d[0]}</span></p>'
                f'<h3{en(a["title"][1])}>{esc(a["title"][0])}</h3><p class="ex"{en(a["excerpt"][1])}>{esc(a["excerpt"][0])}</p>'
                f'<span class="link-arrow more"><span{en("Keep reading")}>Lanjut baca</span>{icon("arrow")}</span></div></a>')
    lst = "".join(card(a, "row", 600, 450) for a in rest)
    return f"""<section class="sec" id="artikel">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow"{en("Articles and guides")}>Artikel dan panduan</p><h2 class="h2"{en("Recovery guides from our physiotherapists")}>Panduan pemulihan dari fisioterapis kami</h2></div>
      <div><p class="lede"{en("The reasoning behind each exercise: what is being repaired, how long it takes and when you should get checked. Every guide cites journals and clinical guidelines.")}>Alasan di balik setiap latihan: apa yang sedang diperbaiki, berapa lama waktunya, dan kapan kamu perlu diperiksa. Setiap panduan merujuk jurnal dan pedoman klinis.</p>
      <p style="margin-top:18px"><a class="link-arrow" href="/artikel/"><span{en("All articles")}>Semua artikel</span>{icon("arrow")}</a></p></div>
    </div>
    <div class="arts">{card(feat, "feat", 1000, 625)}<div class="alist">{lst}</div></div>
  </div>
</section>"""


def faq():
    items = "".join(f'<details class="rv"><summary><span{en(qe)}>{qi}</span>{icon("plus")}</summary><p class="a"{en(ae)}>{ai}</p></details>'
                    for qi, qe, ai, ae in FAQ)
    return f"""<section class="sec" id="faq">
  <div class="wrap faq">
    <div><p class="eyebrow">FAQ</p><h2 class="h2"{en("Frequently asked questions")}>Pertanyaan yang sering muncul</h2>
      <p class="lede"{en("Something not covered here? Ask us on WhatsApp; a physiotherapist replies.")}>Pertanyaanmu belum terjawab? Tanyakan lewat WhatsApp; fisioterapis kami yang akan menjawab.</p></div>
    <div>{items}</div>
  </div>
</section>"""


def booking():
    ch = [(f'href="{esc(WA_BOOK[0])}" data-en-href="{esc(WA_BOOK[1])}" target="_blank" rel="noopener noreferrer"', WA_GLYPH, f"WhatsApp · {WA_DISPLAY}",
           "Pemesanan jadwal, pengingat, dan program rumahmu.", "Bookings, reminders and your home programme."),
          (f'href="{IG}" target="_blank" rel="noopener noreferrer"', icon("insta"), "Instagram · @physio8.id",
           "Cerita progres, hasil tes ulang, dan kabar klinik.", "Progress stories, re-test results and clinic news."),
          (f'href="{CAREERS}" target="_blank" rel="noopener noreferrer"', icon("brief"), "Karier · Glints",
           "Kami membuka lowongan di seluruh tim klinik.", "We are hiring across the clinic team.")]
    cl = ""
    for k, (attrs, ic, t, di, de) in enumerate(ch):
        tt = f'<b{en("Careers · Glints")}>{t}</b>' if k == 2 else f"<b>{t}</b>"
        cl += f'<a class="channel" {attrs}><span class="ic">{ic}</span><div>{tt}<span{en(de)}>{di}</span></div>{icon("arrow", "go")}</a>'
    return f"""<section class="sec" id="booking">
  <div class="wrap">
    <div class="book rv">
      <div>
        <p class="eyebrow"{en("Book an assessment")}>Buat jadwal asesmen</p>
        <h2 class="h2"{en("Start from your baseline")}>Mulai dari baseline-mu</h2>
        <p class="lede"{en("Book the Movement &amp; Posture Assessment on WhatsApp. You leave with your numbers, a physiotherapy diagnosis and a plan with its total cost.")}>Jadwalkan Movement &amp; Posture Assessment lewat WhatsApp. Kamu pulang dengan angka awal, diagnosis fisioterapi, dan rencana beserta total biayanya.</p>
        <div class="acts"><a class="btn btn-primary" {wa_attrs()}>{WA_GLYPH}<span{en("Book on WhatsApp")}>Jadwalkan via WhatsApp</span></a>
        <a class="btn btn-ghost" href="#harga"><span{en("See prices")}>Lihat harga</span></a></div>
      </div>
      <div class="channels">{cl}</div>
    </div>
  </div>
</section>"""


def footer():
    cols = [("Physio8", "Physio8", [("#metode", "Physio8 Pathway", "Physio8 Pathway"), ("#pilates", "Clinical Pilates", "Clinical Pilates"),
                                    ("#harga", "Harga", "Prices"), ("#tim", "Tim", "Team"), ("#faq", "FAQ", "FAQ")]),
            ("Artikel", "Articles", [("/artikel/nyeri-pinggang-duduk-lama/", "Nyeri punggung bawah", "Low back pain"),
                                     ("/artikel/leher-kaku-kerja-kantor/", "Postur &amp; kerja kantor", "Posture &amp; desk work"),
                                     ("/artikel/runners-knee-shin-splints-achilles/", "Cedera lari", "Running injuries"),
                                     ("/artikel/rehabilitasi-pasca-operasi-acl/", "Rehabilitasi pasca operasi", "Post-surgery rehab"),
                                     ("/artikel/", "Semua artikel", "All articles")])]
    cc = ""
    for hi, he, links in cols:
        cc += f'<div><h4{en(he)}>{hi}</h4><ul>' + "".join(f'<li><a href="{h}"{en(e)}>{i}</a></li>' for h, i, e in links) + "</ul></div>"
    return f"""<footer class="ftr">
  <div class="wrap">
    <div class="top">
      <div><img class="logo" src="./p8/logo-full-white.svg" alt="Physio8 — Physiotherapy &amp; Recovery" width="240" height="160">
        <p class="about"{en("Specialist physiotherapy and clinical Pilates in Gading Serpong. One therapist, one patient, one method.")}>Fisioterapi spesialis dan clinical Pilates di Gading Serpong. Satu terapis, satu pasien, satu metode.</p></div>
      {cc}
      <div><h4{en("Visit")}>Kunjungi</h4><address>Ruko Hudson Blok B No. 29<br>Paramount Gading Serpong<br>Medang, Pagedangan<br><span{en("Tangerang Regency, Banten 15334")}>Kab. Tangerang, Banten 15334</span></address>
        <ul style="margin-top:14px"><li><a {wa_attrs()}>WhatsApp {WA_DISPLAY}</a></li><li><a href="{IG}" target="_blank" rel="noopener noreferrer">Instagram @physio8.id</a></li><li><a href="{CAREERS}" target="_blank" rel="noopener noreferrer"{en("Careers")}>Karier</a></li></ul></div>
    </div>
    <div class="bottom"><span>© 2026 Physio8</span><span class="tl">Recover. Move. Repeat — for life.</span></div>
    <p class="disc"{en("Information on this site is educational and does not replace an in-person clinical assessment. For a suspected fracture, chest pain, or loss of bladder or bowel control, contact emergency care.")}>Informasi di situs ini bersifat edukatif dan bukan pengganti pemeriksaan klinis langsung. Untuk dugaan patah tulang, nyeri dada, atau kehilangan kontrol buang air, hubungi layanan medis darurat.</p>
  </div>
</footer>
<a class="p8-wa-fab" {wa_attrs()} aria-label="Chat WhatsApp Physio8" title="WhatsApp">{WA_GLYPH}</a>"""


def jsonld():
    addr = {"@type": "PostalAddress", "streetAddress": "Ruko Hudson Blok B No. 29, Paramount Gading Serpong",
            "addressLocality": "Medang, Pagedangan", "addressRegion": "Kabupaten Tangerang, Banten",
            "postalCode": "15334", "addressCountry": "ID"}

    def offer(name, price, desc=None):
        o = {"@type": "Offer", "name": name, "price": price, "priceCurrency": "IDR"}
        if desc:
            o["description"] = desc
        return o
    s, s4, s8 = PRICES["std"]
    n, n4, n8 = PRICES["snr"]
    clinic = {
        "@context": "https://schema.org", "@type": ["Physiotherapy", "MedicalClinic"], "@id": SITE + "#clinic",
        "name": "Physio8", "alternateName": "Physio8 Physiotherapy & Recovery",
        "description": DESC[0], "url": SITE, "logo": SITE + "p8/logo-full.png", "image": SITE + "og-physio8.jpg",
        "telephone": WA_DISPLAY.replace(" ", "").replace("-", ""), "address": addr,
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]}, "hasMap": MAP_LINK,
        "areaServed": "Gading Serpong, Tangerang", "priceRange": f"{rp(LITE)} – {rp(n)}",
        "currenciesAccepted": "IDR", "sameAs": [IG],
        "medicalSpecialty": "PhysicalTherapy",
        "availableService": [{"@type": "MedicalTherapy", "name": x} for x in
                             ("Physiotherapy", "Clinical Pilates", "Manual therapy", "Dry needling", "Kinesio taping",
                              "Movement & Posture Assessment")],
        "employee": {"@type": "Person", "name": "Ika Setia Ningsih", "honorificSuffix": "S.Ft", "jobTitle": "Lead Physiotherapist", "image": SITE + "p8/ika-setia-ningsih.jpg",
                     "alumniOf": {"@type": "CollegeOrUniversity", "name": "Universitas Esa Unggul"}},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Physio8 prices", "itemListElement": [
            offer("Physiotherapy Standard — single session", s), offer("Physiotherapy Standard — package of 4", s4 * 4, "Valid 8 weeks"),
            offer("Physiotherapy Standard — package of 8", s8 * 8, "Valid 14 weeks"),
            offer("Physiotherapy Senior — single session", n), offer("Physiotherapy Senior — package of 4", n4 * 4, "Valid 8 weeks"),
            offer("Physiotherapy Senior — package of 8", n8 * 8, "Valid 14 weeks"),
            offer("Targeted lite treatment (15 min)", LITE), offer("Kinesio taping (per application)", TAPING)]},
        "slogan": "Recover. Move. Repeat — for life.",
    }
    site = {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "#website", "url": SITE, "name": "Physio8",
            "inLanguage": ["id-ID", "en"], "publisher": {"@id": SITE + "#clinic"}}
    faqs = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, _, a, _ in FAQ]}
    return "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (clinic, site, faqs))


JS = r"""
(function(){
  var d=document, KEY='p8-lang', store=new WeakMap();
  var META=__META__;
  var hdr=d.querySelector('.hdr');
  function onScroll(){hdr.classList.toggle('scrolled', window.scrollY>8)}
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
  // mobile menu
  var mb=d.querySelector('.menu-btn'), mn=d.getElementById('mnav'), IM=mb.innerHTML, IX=__ICONX__;
  function setMenu(o){mn.classList.toggle('open',o); mb.setAttribute('aria-expanded',String(o)); mb.innerHTML=o?IX:IM; d.body.style.overflow=o?'hidden':''}
  mb.addEventListener('click',function(){setMenu(!mn.classList.contains('open'))});
  mn.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){setMenu(false)})});
  // time-limited blocks (soft opening)
  var now=new Date();
  d.querySelectorAll('[data-until]').forEach(function(el){ if(now>new Date(el.getAttribute('data-until')+'T23:59:59+07:00')) el.classList.add('expired'); });
  // language
  function apply(lang){
    d.querySelectorAll('[data-en]').forEach(function(el){
      if(!store.has(el)) store.set(el, el.innerHTML);
      el.innerHTML = lang==='en' ? el.getAttribute('data-en') : store.get(el);
    });
    d.querySelectorAll('*').forEach(function(el){
      if(!el.attributes) return;
      for(var i=0;i<el.attributes.length;i++){
        var at=el.attributes[i]; if(at.name.indexOf('data-en-')!==0) continue;
        var name=at.name.slice(8), k='data-id-'+name;
        if(!el.hasAttribute(k)) el.setAttribute(k, el.getAttribute(name)||'');
        el.setAttribute(name, lang==='en' ? at.value : el.getAttribute(k));
      }
    });
    d.documentElement.lang = lang;
    d.title = META[lang].title;
    var m=d.querySelector('meta[name="description"]'); if(m) m.setAttribute('content', META[lang].desc);
    d.querySelectorAll('.lang button').forEach(function(b){b.setAttribute('aria-pressed', String(b.getAttribute('data-lang')===lang))});
    try{localStorage.setItem(KEY, lang)}catch(e){}
  }
  d.querySelectorAll('.lang button').forEach(function(b){b.addEventListener('click',function(){apply(b.getAttribute('data-lang'))})});
  var saved='id'; try{saved=localStorage.getItem(KEY)||'id'}catch(e){}
  if(saved==='en') apply('en');
  // gentle reveal
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in'); io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    d.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
  } else { d.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')}); }
})();
"""


def build_home(arts, img_fn, date_fn):
    meta = {"id": {"title": TITLE[0], "desc": DESC[0]}, "en": {"title": TITLE[1], "desc": DESC[1]}}
    js = JS.replace("__META__", json.dumps(meta, ensure_ascii=False)).replace("__ICONX__", json.dumps(icon("x")))
    body = "\n".join([header(), "<main>", hero(), numbers(), pathway(), method(), assessment(), pilates(), team(),
                      pricing(), values(), location(), articles(arts, img_fn, date_fn), faq(), booking(), "</main>", footer()])
    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(TITLE[0])}</title>
<meta name="description" content="{esc(DESC[0])}">
<link rel="canonical" href="{SITE}">
<link rel="alternate" hreflang="id" href="{SITE}">
<link rel="alternate" hreflang="x-default" href="{SITE}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#2F1F71">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Physio8">
<meta property="og:locale" content="id_ID">
<meta property="og:locale:alternate" content="en_US">
<meta property="og:url" content="{SITE}">
<meta property="og:title" content="{esc(TITLE[0])}">
<meta property="og:description" content="{esc(DESC[0])}">
<meta property="og:image" content="{SITE}og-physio8.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Fasad klinik Physio8 di Paramount Gading Serpong">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(TITLE[0])}">
<meta name="twitter:description" content="{esc(DESC[0])}">
<meta name="twitter:image" content="{SITE}og-physio8.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap">
<link rel="preconnect" href="https://images.unsplash.com">
<script>document.documentElement.classList.add('js')</script>
<style>{CSS.replace(".rv{opacity:0", "html.js .rv{opacity:0").replace(".rv.in{", "html.js .rv.in{")}</style>
{jsonld()}
</head>
<body>
{body}
<script>{js}</script>
</body>
</html>
"""


if __name__ == "__main__":
    import build
    arts = build.load_articles()
    out = os.path.join(ROOT, "index.html")
    open(out, "w", encoding="utf-8").write(build_home(arts, build.img, build.fmt_date_short))
    print("index.html written", os.path.getsize(out), "bytes")
