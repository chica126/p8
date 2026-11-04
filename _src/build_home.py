#!/usr/bin/env python3
"""
Physio8 homepage generator  ->  index.html  (URL: https://physio8.id/)

Content source: Physio8 Company Profile 2026 (project file) + the latest logo
(Physiotherapy & Recovery lockup). Static HTML in Bahasa Indonesia so search and
AI engines read the full page; English is swapped in client-side from the
data-en / data-en-<attr> attributes on each element (ID | EN toggle).

Run via build.py (it calls build_home), or on its own:  python3 _src/build_home.py
Clinic details live in the CONFIG block below. Prices are not shown on the site (per client,
Nov 2026): visitors are sent to WhatsApp. PRICES is kept for reference only.
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

PRICES = {  # reference only, not published (client: "contact us" pricing). single, pkg 4, pkg 8
    "std": (485000, 450000, 410000),
    "snr": (585000, 545000, 495000),
}
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
NAV = [("cedera", "Cedera olahraga", "Sports injuries"), ("metode", "Metode", "Method"), ("harga", "Layanan", "Services"),
       ("tim", "Tim", "Team"), ("lokasi", "Lokasi", "Location"), ("artikel", "Artikel", "Articles")]

STEPS = [
    ("Assess", "Pemeriksaan klinis dan pengukuran gerak dengan kamera.", "A clinical exam and movement measured on camera."),
    ("Diagnose", "Penjelasan masalahnya, rencana terapi, dan perkiraan biayanya.", "What the problem is, the treatment plan and what it will cost."),
    ("Relieve", "Nyeri diturunkan dulu sampai target yang disepakati.", "Pain brought down first, to the level we agreed."),
    ("Rebuild", "Rentang gerak dan kekuatan dasar dibangun lagi.", "Range of motion and basic strength built back."),
    ("Strengthen", "Latihan beban dan clinical Pilates.", "Strength training and clinical Pilates."),
    ("Retrain", "Latihan gerakan khas olahragamu, lalu tes ulang.", "Drills for the movements your sport needs, then a re-test."),
    ("Return", "Tes kesiapan sebelum kamu kembali main.", "A readiness test before you go back to playing."),
    ("Maintain", "Latihan rutin dan cek berkala supaya kondisimu terjaga.", "Regular training and check-ins to keep you in shape."),
]

METHOD = [
    ("01–02", "Pemeriksaan dan pengukuran", "Assessment and measurement",
     "Selain pemeriksaan klinis, postur dan gerakmu direkam dengan kamera berbasis AR. Hasil hari pertama ini jadi patokan untuk sesi-sesi berikutnya.",
     "Alongside a clinical exam, your posture and movement are recorded with an AR camera. Day one becomes the reference point for every session after.",
     [("Postur 4 sisi", "Posture from 4 sides"), ("Rentang gerak", "Range of motion"), ("Squat screen", "Squat screen")]),
    ("03–04", "Terapi", "Treatment",
     "Terapi manual dan alat bantu yang dipilih sesuai protokol untuk kondisimu.",
     "Manual therapy and modalities chosen by protocol for your condition.",
     [("Terapi manual", "Manual therapy"), ("Ultrasound", "Ultrasound"), ("Dry needling", "Dry needling"), ("TENS", "TENS"), ("Infrared", "Infrared")]),
    ("05–06", "Clinical Pilates", "Clinical Pilates",
     "Pilates yang dipandu fisioterapis, ditambah latihan beban bertahap, untuk membangun kekuatan dan kontrol gerak.",
     "Physio-guided Pilates plus gradual strength work to build strength and movement control.", []),
    ("02–08", "Rencana tertulis", "A written plan",
     "Sebelum terapi dimulai, kamu sudah tahu diagnosisnya, perkiraan jumlah sesi, dan total biayanya.",
     "Before treatment starts you know the diagnosis, roughly how many sessions it takes and the total cost.", []),
    ("06 & 08", "Tes ulang", "Re-tests",
     "Pengukuran hari pertama diulang, jadi perubahannya kelihatan dalam angka.",
     "The day-one measurements are repeated, so you can see the change in numbers.", []),
]

INJURIES = [
    ("Padel &amp; tenis", "Padel &amp; tennis", "nyeri-bahu-padel",
     "Bahu nyeri saat smash atau servis, tennis elbow, pergelangan tangan, dan betis yang tertarik saat lari pendek di lapangan.",
     "Shoulder pain on smashes and serves, tennis elbow, sore wrists, and calves that pull on short sprints across the court."),
    ("Lari", "Running", "runners-knee-shin-splints-achilles",
     "Runner's knee, shin splints, dan tendon Achilles yang kaku tiap pagi.",
     "Runner's knee, shin splints and an Achilles that is stiff every morning."),
    ("Futsal &amp; sepak bola", "Futsal &amp; football", "nyeri-setelah-olahraga-weekend",
     "Hamstring tertarik, keseleo pergelangan kaki, dan nyeri yang muncul dua hari setelah main.",
     "Pulled hamstrings, sprained ankles and the soreness that shows up two days after a game."),
    ("Setelah operasi", "After surgery", "rehabilitasi-pasca-operasi-acl",
     "Program setelah rekonstruksi ACL atau operasi bahu, sampai lolos tes untuk kembali bermain.",
     "Rehab after ACL reconstruction or shoulder surgery, through to the return-to-sport tests."),
    ("Punggung &amp; leher", "Back &amp; neck", "nyeri-pinggang-duduk-lama",
     "Pinggang dan leher pegal karena duduk lama atau kerja di depan layar. Tidak harus atlet untuk datang.",
     "A sore lower back or stiff neck from long hours at a desk. You do not have to be an athlete to come in."),
]

CREDS = [
    ("18+ tahun praktik klinis, sejak 2008", "18+ years in clinical practice, since 2008"),
    ("Sertifikasi dry needling, Australian Physiotherapy Association", "Certified in dry needling, Australian Physiotherapy Association"),
    ("Sertifikasi Mulligan Concept", "Certified in the Mulligan Concept"),
    ("Sarjana Fisioterapi, Universitas Esa Unggul", "Bachelor of Physiotherapy, Esa Unggul University"),
    ("Pernah mengajar di program studi fisioterapi Universitas Esa Unggul", "Former physiotherapy lecturer at Esa Unggul University"),
    ("Pelatihan podiatri dan dasar women's health", "Trained in podiatry and basic women's health"),
]

FAQ = [
    ("Apakah saya perlu surat rujukan dokter?", "Do I need a doctor's referral?",
     "Tidak. Kamu bisa langsung datang ke fisioterapis (Permenkes No. 65 Tahun 2015 tentang Standar Pelayanan Fisioterapi). Kalau dari pemeriksaan kami ada yang perlu dicek dokter, misalnya butuh rontgen atau MRI, kami rujuk ke dokter spesialis dan jelaskan alasannya.",
     "No. You can see a physiotherapist directly (Ministry of Health Regulation No. 65/2015). If our exam shows something a doctor should look at, such as a need for an X-ray or MRI, we refer you to a specialist and explain why."),
    ("Saya bukan atlet. Boleh datang?", "I'm not an athlete. Can I still come?",
     "Boleh. Fokus kami memang cedera olahraga, tapi kami juga menangani nyeri punggung, leher kaku karena kerja, dan pemulihan setelah operasi.",
     "Yes. Sports injuries are our focus, but we also treat back pain, a stiff neck from desk work and recovery after surgery."),
    ("Apa yang terjadi di kunjungan pertama?", "What happens at the first visit?",
     "Kami tanya soal keluhan dan olahragamu, cek tanda bahaya, lalu rekam postur dan gerakmu dengan kamera dan lakukan pemeriksaan klinis. Di akhir kunjungan kamu tahu apa masalahnya, rencana terapinya, dan perkiraan biayanya.",
     "We ask about your injury and your sport, screen for red flags, record your posture and movement on camera and do a clinical exam. By the end you know what the problem is, the plan and roughly what it will cost."),
    ("Berapa biayanya?", "How much does it cost?",
     "Info harga terbaru bisa ditanyakan langsung lewat WhatsApp. Kamu bisa bayar per sesi atau ambil paket 4 atau 8 sesi.",
     "Ask us on WhatsApp for current prices. You can pay per session or take a package of 4 or 8 sessions."),
    ("Apa bedanya clinical Pilates dengan kelas Pilates biasa?", "How is clinical Pilates different from a regular Pilates class?",
     "Clinical Pilates dipandu fisioterapis yang tahu kondisi dan hasil pengukuranmu. Latihannya dipilih sesuai tahap pemulihan dan bebannya dinaikkan pelan-pelan. Ini bagian dari terapi, bukan kelas umum.",
     "Clinical Pilates is run by a physiotherapist who knows your condition and your measurements. Exercises match your stage of recovery and load goes up gradually. It is part of your treatment rather than a group class."),
    ("Bagaimana cara membuat jadwal?", "How do I book?",
     f"Chat kami di WhatsApp {WA_DISPLAY}. Pengingat jadwal dan latihan rumahmu juga kami kirim lewat WhatsApp.",
     f"Message us on WhatsApp at {WA_DISPLAY}. Reminders and your home exercises come through WhatsApp too."),
    ("Di mana lokasi Physio8?", "Where is Physio8?",
     "Ruko Hudson Blok B No. 29, Paramount Gading Serpong, Medang, Pagedangan, Kabupaten Tangerang, Banten 15334. Sekitar 4,8 km dari gerbang tol West BSD 1.",
     "Ruko Hudson Blok B No. 29, Paramount Gading Serpong, Medang, Pagedangan, Tangerang Regency, Banten 15334. About 4.8 km from the West BSD 1 toll gate."),
]

TITLE = ("Physio8 — Fisioterapi Cedera Olahraga & Clinical Pilates di Gading Serpong",
         "Physio8 — Sports Injury Physiotherapy & Clinical Pilates in Gading Serpong")
DESC = ("Fisioterapi untuk cedera olahraga padel, tenis, lari, dan futsal, plus clinical Pilates, di Paramount Gading Serpong. Gerakmu diukur dengan kamera AR, lalu dilatih sampai siap main lagi.",
        "Physiotherapy for padel, tennis, running and futsal injuries, plus clinical Pilates, in Paramount Gading Serpong. Your movement is measured with an AR camera, then trained until you are ready to play again.")

WA_PRICE = (wa("Halo Physio8, saya ingin tanya harga layanan fisioterapi. (dari website)"),
            wa("Hi Physio8, I would like to ask about your prices. (from the website)"))


def header():
    links = "".join(f'<a href="#{a}"{en(e)}>{i}</a>' for a, i, e in NAV)
    return f"""<a class="skip" href="#main"{en("Skip to content")}>Lewati ke konten</a>
<header class="hdr">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Physio8"><img src="./p8/logo-full.svg" alt="Physio8 — Physiotherapy &amp; Recovery" width="90" height="60"></a>
    <nav class="nav" aria-label="Utama" data-en-aria-label="Main">{links}</nav>
    <div class="hdr-right">
      <div class="lang" role="group" aria-label="Bahasa / Language">
        <button type="button" data-lang="id" aria-pressed="true">ID</button><button type="button" data-lang="en" aria-pressed="false">EN</button>
      </div>
      <a class="btn btn-primary btn-desk" {wa_attrs()}><span{en("Book a session")}>Buat jadwal</span></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu">{icon("menu")}</button>
    </div>
  </div>
</header>
<div class="mnav" id="mnav">{links}<a class="btn btn-primary" {wa_attrs()}><span{en("Book a session")}>Buat jadwal</span></a></div>"""


def hero():
    facts = [("Satu terapis untuk satu pasien", "One therapist per patient"),
             ("Gerakmu diukur dengan kamera AR", "Your movement measured with an AR camera"),
             ("Dipimpin fisioterapis berpengalaman 18 tahun", "Led by a physiotherapist with 18 years' experience")]
    fl = "".join(f'<li>{icon("ccheck")}<span{en(e)}>{i}</span></li>' for i, e in facts)
    return f"""<section class="hero" id="main">
  <div class="wrap">
    <div>
      <p class="hero-k"><span{en("Sports physiotherapy")}>Fisioterapi olahraga</span><span class="sep" aria-hidden="true"></span><span>Paramount Gading Serpong</span></p>
      <h1>
        <span class="display"><span>Recover.</span><span class="c2">Move.</span><span class="c3">Repeat.</span></span>
        <span class="h1-sub"{en("Physiotherapy for sports injuries in Gading Serpong, from the padel and tennis court to your running route.")}>Fisioterapi untuk cedera olahraga di Gading Serpong, dari lapangan padel dan tenis sampai rute larimu.</span>
      </h1>
      <p class="lede"{en("Shoulder hurts on every smash? Elbow sore after a match, or a knee that complains on your runs? We find the cause, measure how you move, then build a programme to get you back to playing.")}>Bahu sakit setiap smash? Siku nyeri setelah main, atau lutut yang protes waktu lari? Kami cari penyebabnya, ukur gerakmu, lalu susun programnya sampai kamu bisa main lagi.</p>
      <div class="hero-cta">
        <a class="btn btn-primary" {wa_attrs()}>{WA_GLYPH}<span{en("Book a session")}>Buat jadwal</span></a>
        <a class="btn btn-ghost" {wa_attrs(WA_PRICE)}><span{en("Ask about prices")}>Tanya harga</span>{icon("arrow")}</a>
      </div>
      <ul class="hero-facts">{fl}</ul>
    </div>
    <div class="hero-media">
      <figure class="photo hero-photo"><picture><source type="image/webp" srcset="./p8/hero-fasad-640.webp 640w, ./p8/hero-fasad.webp 1008w" sizes="(max-width: 920px) 100vw, 50vw"><img src="./p8/hero-fasad.jpg" width="1008" height="1062" alt="Fasad klinik Physio8 di Ruko Hudson, Paramount Gading Serpong" data-en-alt="The Physio8 clinic front at Ruko Hudson, Paramount Gading Serpong" fetchpriority="high" decoding="async"></picture></figure>
    </div>
  </div>
</section>"""


def injuries():
    cards = ""
    for k, (ti, te, slug, di, de) in enumerate(INJURIES):
        cls = "inj rv" + (" big" if k == 0 else "")
        cards += (f'<a class="{cls}" href="/artikel/{slug}/"><h3{en(te)}>{ti}</h3><p{en(de)}>{di}</p>'
                  f'<span class="link-arrow"><span{en("Read the guide")}>Baca panduannya</span>{icon("arrow")}</span></a>')
    return f"""<section class="sec" id="cedera">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow"{en("Sports injuries")}>Cedera olahraga</p><h2 class="h2"{en("Injuries we treat")}>Cedera yang kami tangani</h2></div>
      <p class="lede"{en("We focus on people who play padel, tennis, run or play futsal. Injuries like these often start small, get ignored because you can still play, and end up keeping you off the court.")}>Fokus kami pemain padel, tenis, pelari, dan pemain futsal. Cedera seperti ini biasanya mulai dari nyeri kecil, dibiarkan karena masih bisa main, lalu lama-lama bikin kamu berhenti.</p>
    </div>
    <div class="injuries">{cards}</div>
  </div>
</section>"""


def pathway():
    steps = ""
    for k, (name, i, e) in enumerate(STEPS):
        c = journey(k)
        steps += (f'<li class="step rv"><div class="bar" style="background:{c}"></div>'
                  f'<span class="no" style="color:{c if k < 6 else "#6C7800"}">{k+1:02d}</span>'
                  f'<h3>{name}</h3><p{en(e)}>{i}</p></li>')
    return f"""<section class="sec tint" id="metode">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Physio8 Pathway</p><h2 class="h2"{en("From injury back to the court")}>Dari cedera sampai balik ke lapangan</h2></div>
      <p class="lede"{en("The programme has eight steps. The first two happen in the clinic: we examine you and explain what is going on. After that you come in for treatment sessions and do home exercises in between, which we keep track of.")}>Programnya ada delapan tahap. Dua tahap pertama di klinik: kami periksa dan jelaskan masalahnya. Setelah itu kamu datang untuk sesi terapi, dan di sela-selanya mengerjakan latihan di rumah yang kami pantau.</p>
    </div>
    <ol class="steps">{steps}</ol>
    <div class="phase" aria-hidden="true"><div{en("In the clinic")}>Di klinik</div><div{en("Clinic sessions + home exercises")}>Sesi di klinik + latihan di rumah</div></div>
    <div class="pathway-foot">
      <p{en("You move to the next step once the target for the current one is reached. At steps 6 and 8 we measure again and compare it with your first day.")}>Kamu pindah ke tahap berikutnya kalau target tahap sebelumnya sudah tercapai. Di tahap 6 dan 8 kami ukur ulang, lalu bandingkan dengan hasil hari pertama.</p>
      <a class="link-arrow" href="/artikel/physio8-pathway-delapan-tahap/"><span{en("Read more")}>Baca penjelasan lengkapnya</span>{icon("arrow")}</a>
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
      <p class="eyebrow"{en("What we do")}>Apa yang kami kerjakan</p>
      <h2 class="h2"{en("What the programme includes")}>Isi program terapinya</h2>
      <p class="lede" style="margin-bottom:36px"{en("Every patient goes through the same process, so the quality of your care does not depend on which therapist is on duty.")}>Setiap pasien melewati alur yang sama, jadi kualitasnya tidak bergantung pada terapis yang sedang bertugas.</p>
      <ul class="mlist">{rows}</ul>
    </div>
  </div>
</section>"""


def assessment():
    tools = [
        (posture_svg([("Depan", "Front"), ("Kanan", "Right"), ("Belakang", "Back"), ("Kiri", "Left")]),
         "Postur dari empat sisi", "Posture from four sides",
         "Kamera AR merekam posturmu dari depan, kanan, belakang, dan kiri.", "An AR camera records your posture from the front, right, back and left."),
        (rom_svg(), "Rentang gerak", "Range of motion",
         "Seberapa jauh leher, punggung, dan bahumu bisa bergerak, diukur dengan kamera dan giroskop.", "How far your neck, back and shoulders move, measured by camera and gyroscope."),
        (squat_svg(), "Squat screen", "Squat screen",
         "Cara kamu jongkok memperlihatkan banyak hal soal pinggul, lutut, dan pergelangan kaki.", "The way you squat says a lot about your hips, knees and ankles."),
    ]
    cards = "".join(f'<div class="tool rv"><div class="viz">{svg}</div><h3{en(te)}>{ti}</h3><p{en(de)}>{di}</p></div>'
                    for svg, ti, te, di, de in tools)
    flow = "".join(f"<li><span>{n}</span>{w}</li>" for n, w in enumerate(["Scan", "Check", "Plan", "Re-scan"], 1))
    return f"""<section class="sec dark" id="asesmen">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow"{en("Your first visit")}>Kunjungan pertama</p><h2 class="h2"{en("We measure before we treat")}>Kami ukur dulu sebelum terapi</h2></div>
      <div><p class="lede"{en("On your first visit we record your posture and movement with an AR camera and measure your range of motion. We repeat it in the middle and at the end of the programme, so you can see the progress yourself.")}>Di kunjungan pertama, postur dan gerakmu kami rekam dengan kamera AR, dan rentang gerakmu diukur. Pengukuran ini kami ulang di tengah dan akhir program, jadi kamu bisa lihat sendiri perkembangannya.</p>
      <ol class="scan-flow" aria-label="Scan, Check, Plan, Re-scan">{flow}</ol></div>
    </div>
    <div class="tools">{cards}</div>
    <p class="dark-foot"{en("A physiotherapist always reads these measurements together with the clinical exam.")}>Semua hasil pengukuran ini tetap dibaca fisioterapis bersama hasil pemeriksaan klinis.</p>
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
    r2_id = (f'Tinjauan Cochrane menemukan Pilates membantu mengurangi nyeri punggung bawah kronis dibanding intervensi minimal '
             f'(<a href="{yam}" target="_blank" rel="noopener">Yamato, 2015</a>). Latihan yang disertai edukasi juga menurunkan risiko nyeri punggung bawah datang lagi '
             f'(<a href="{ste}" target="_blank" rel="noopener">Steffens, 2016</a>).')
    r2_en = (f'A Cochrane review found Pilates helped chronic low back pain more than minimal intervention '
             f'(<a href="{yam}" target="_blank" rel="noopener">Yamato, 2015</a>). Exercise with education also lowered the chance of low back pain coming back '
             f'(<a href="{ste}" target="_blank" rel="noopener">Steffens, 2016</a>).')
    return f"""<section class="sec tint" id="pilates">
  <div class="wrap pil">
    {photo(IMG_PILATES, 960, 1152)}
    <div>
      <p class="eyebrow">Clinical Pilates</p>
      <h2 class="h2"{en("Why Pilates is part of the programme")}>Kenapa ada Pilates di program kami</h2>
      <div class="tracks">
        {track("p1", "Fisioterapi", "Physiotherapy", "nyeri · rentang gerak · jaringan cedera", "pain · range of motion · injured tissue", {1, 2, 3, 4}, {5, 6, 7})}
        {track("p2", "Clinical Pilates", "Clinical Pilates", "kekuatan inti · kontrol · postur", "core strength · control · posture", {5, 6, 7, 8}, {4})}
        <div class="track-nums" aria-hidden="true">{nums}</div>
      </div>
      <ul class="reasons">
        <li><span class="ix">01</span><div><h3{en("Pain gone does not mean recovered")}>Nyeri hilang belum berarti pulih</h3><p{en("Once the pain settles, the muscles around the injury are usually still weak. Go straight back to playing and the same injury often returns.")}>Setelah nyeri turun, otot di sekitar area cedera biasanya masih lemah. Kalau langsung kembali main, cedera yang sama sering datang lagi.</p></div></li>
        <li><span class="ix">02</span><div><h3{en("There is research behind it")}>Ada dasar risetnya</h3><p{en(r2_en)}>{r2_id}</p></div></li>
        <li><span class="ix">03</span><div><h3{en("Adjusted to you")}>Disesuaikan dengan kondisimu</h3><p{en("Run by the physiotherapist who has your measurements, with load increased gradually and checked again at steps 6 and 8.")}>Dipandu fisioterapis yang memegang hasil pengukuranmu, bebannya dinaikkan pelan-pelan, lalu dicek ulang di tahap 6 dan 8.</p></div></li>
      </ul>
    </div>
  </div>
</section>"""


def team():
    creds = "".join(f'<li>{icon("check")}<span{en(e)}>{i}</span></li>' for i, e in CREDS)
    return f"""<section class="sec" id="tim">
  <div class="wrap">
    <p class="eyebrow"{en("Our team")}>Tim kami</p>
    <h2 class="h2" style="margin-bottom:40px"{en("Meet our physiotherapist")}>Kenalan dengan fisioterapis kami</h2>
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
        <p class="big"{en("Ika has spent 18 years treating patients at clinics across Jakarta, including as a senior physiotherapist, and has taught physiotherapy at Esa Unggul University. At Physio8 she leads the clinical team and makes sure every treatment plan follows the same standard.")}>Ika sudah 18 tahun menangani pasien di berbagai klinik di Jakarta, termasuk sebagai senior physiotherapist, dan pernah mengajar di program studi fisioterapi Universitas Esa Unggul. Di Physio8, Ika memimpin tim klinis dan memastikan setiap rencana terapi mengikuti standar yang sama.</p>
        <ul class="creds">{creds}</ul>
        <p class="trained-note"{en("Team protocols and training follow KNGF guidelines (the Royal Dutch Society for Physical Therapy) and University of Melbourne research.")}>Protokol dan pelatihan tim mengacu pada pedoman KNGF (asosiasi fisioterapi Belanda) dan riset University of Melbourne.</p>
      </div>
    </div>
  </div>
</section>"""


def pricing():
    svc = [("Movement &amp; Posture Assessment", "Movement &amp; Posture Assessment",
            "Pemeriksaan pertama: wawancara, pengukuran gerak dengan kamera, dan pemeriksaan klinis.",
            "Your first visit: an interview, movement measured on camera and a clinical exam."),
           ("Fisioterapi", "Physiotherapy",
            "Sesi satu terapis untuk satu pasien, dengan fisioterapis atau fisioterapis senior. Bisa per sesi atau paket 4 dan 8 sesi.",
            "One therapist, one patient, with a physiotherapist or senior physiotherapist. Per session or in packages of 4 and 8."),
           ("Clinical Pilates", "Clinical Pilates",
            "Pilates yang dipandu fisioterapis, bagian dari tahap 5 sampai 8.",
            "Physio-guided Pilates, part of steps 5 to 8."),
           ("Targeted lite treatment", "Targeted lite treatment",
            "Sesi singkat 15 menit untuk satu area keluhan.", "A short 15-minute session for one problem area."),
           ("Kinesio taping", "Kinesio taping",
            "Taping untuk menopang otot atau sendi supaya kamu tetap bisa aktif.", "Taping to support a muscle or joint so you can stay active.")]
    cards = "".join(f'<div class="svc rv"><h3{en(te)}>{ti}</h3><p{en(de)}>{di}</p></div>' for ti, te, di, de in svc)
    return f"""<section class="sec" id="harga">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow"{en("Services")}>Layanan</p><h2 class="h2"{en("Services and prices")}>Layanan dan harga</h2></div>
      <p class="lede"{en("For current prices, just ask us on WhatsApp. After your first visit, the estimated number of sessions and the total cost go into your written plan.")}>Untuk info harga terbaru, langsung tanya kami lewat WhatsApp. Setelah pemeriksaan pertama, perkiraan jumlah sesi dan total biayanya kami tuliskan di rencana terapimu.</p>
    </div>
    <div class="svcs">{cards}<div class="price-cta rv"><p{en("Prices, packages and available times: ask us directly.")}>Harga, paket, dan jadwal kosong bisa ditanyakan langsung.</p>
      <a class="btn btn-primary" {wa_attrs(WA_PRICE)}>{WA_GLYPH}<span{en("Ask on WhatsApp")}>Tanya via WhatsApp</span></a></div></div>
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
      <div><p class="eyebrow"{en("Location")}>Lokasi</p><h2 class="h2">Paramount Gading Serpong</h2></div>
      <p class="lede"{en("You will find us in the Ruko Hudson row at Paramount Gading Serpong.")}>Klinik kami ada di deretan Ruko Hudson, Paramount Gading Serpong.</p>
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
    feat = bys["nyeri-bahu-padel"]
    rest = [bys[s] for s in ("runners-knee-shin-splints-achilles", "rehabilitasi-pasca-operasi-acl", "nyeri-setelah-olahraga-weekend")]

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
      <div><p class="eyebrow"{en("Articles")}>Artikel</p><h2 class="h2"{en("Reading on injuries and recovery")}>Bacaan seputar cedera dan pemulihan</h2></div>
      <div><p class="lede"{en("Written by our physiotherapists, with journal references. From padel shoulder injuries to when pain is worth getting checked.")}>Ditulis fisioterapis kami, lengkap dengan rujukan jurnal. Mulai dari cedera bahu pemain padel sampai kapan nyeri perlu diperiksa.</p>
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
      <p class="lede"{en("Have another question? Ask us on WhatsApp and a physiotherapist will answer.")}>Ada pertanyaan lain? Tanya lewat WhatsApp, fisioterapis kami yang jawab.</p></div>
    <div>{items}</div>
  </div>
</section>"""


def booking():
    ch = [(f'href="{esc(WA_BOOK[0])}" data-en-href="{esc(WA_BOOK[1])}" target="_blank" rel="noopener noreferrer"', WA_GLYPH, f"WhatsApp · {WA_DISPLAY}",
           "Buat jadwal, pengingat, dan latihan rumahmu.", "Bookings, reminders and your home exercises."),
          (f'href="{IG}" target="_blank" rel="noopener noreferrer"', icon("insta"), "Instagram · @physio8.id",
           "Cerita pasien, hasil tes ulang, dan kabar klinik.", "Patient stories, re-test results and clinic news."),
          (f'href="{CAREERS}" target="_blank" rel="noopener noreferrer"', icon("brief"), "Karier · Glints",
           "Kami sedang membuka lowongan.", "We are hiring.")]
    cl = ""
    for k, (attrs, ic, t, di, de) in enumerate(ch):
        tt = f'<b{en("Careers · Glints")}>{t}</b>' if k == 2 else f"<b>{t}</b>"
        cl += f'<a class="channel" {attrs}><span class="ic">{ic}</span><div>{tt}<span{en(de)}>{di}</span></div>{icon("arrow", "go")}</a>'
    return f"""<section class="sec" id="booking">
  <div class="wrap">
    <div class="book rv">
      <div>
        <p class="eyebrow"{en("Book a session")}>Buat jadwal</p>
        <h2 class="h2"{en("Tell us what is bothering you")}>Ceritakan keluhanmu ke kami</h2>
        <p class="lede"{en("Message us on WhatsApp: what the injury is, how long you have had it and which sport you play. We will help you set up your first visit.")}>Chat kami di WhatsApp: cedera apa, sudah berapa lama, dan olahraga apa yang kamu mainkan. Nanti kami bantu atur jadwal kunjungan pertamamu.</p>
        <div class="acts"><a class="btn btn-primary" {wa_attrs()}>{WA_GLYPH}<span{en("Chat on WhatsApp")}>Chat via WhatsApp</span></a>
        <a class="btn btn-ghost" {wa_attrs(WA_PRICE)}><span{en("Ask about prices")}>Tanya harga</span></a></div>
      </div>
      <div class="channels">{cl}</div>
    </div>
  </div>
</section>"""


def footer():
    cols = [("Physio8", "Physio8", [("#cedera", "Cedera olahraga", "Sports injuries"), ("#metode", "Physio8 Pathway", "Physio8 Pathway"),
                                    ("#pilates", "Clinical Pilates", "Clinical Pilates"), ("#harga", "Layanan", "Services"),
                                    ("#tim", "Tim", "Team"), ("#faq", "FAQ", "FAQ")]),
            ("Artikel", "Articles", [("/artikel/nyeri-bahu-padel/", "Cedera bahu pemain padel", "Padel shoulder injuries"),
                                     ("/artikel/runners-knee-shin-splints-achilles/", "Cedera lari", "Running injuries"),
                                     ("/artikel/rehabilitasi-pasca-operasi-acl/", "Rehabilitasi ACL", "ACL rehab"),
                                     ("/artikel/nyeri-setelah-olahraga-weekend/", "Nyeri setelah olahraga", "Soreness after sport"),
                                     ("/artikel/", "Semua artikel", "All articles")])]
    cc = ""
    for hi, he, links in cols:
        cc += f'<div><h4{en(he)}>{hi}</h4><ul>' + "".join(f'<li><a href="{h}"{en(e)}>{i}</a></li>' for h, i, e in links) + "</ul></div>"
    return f"""<footer class="ftr">
  <div class="wrap">
    <div class="top">
      <div><img class="logo" src="./p8/logo-full-white.svg" alt="Physio8 — Physiotherapy &amp; Recovery" width="240" height="160">
        <p class="about"{en("Sports physiotherapy and clinical Pilates in Paramount Gading Serpong.")}>Fisioterapi olahraga dan clinical Pilates di Paramount Gading Serpong.</p></div>
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
    clinic = {
        "@context": "https://schema.org", "@type": ["Physiotherapy", "MedicalClinic"], "@id": SITE + "#clinic",
        "name": "Physio8", "alternateName": "Physio8 Physiotherapy & Recovery",
        "description": DESC[0], "url": SITE, "logo": SITE + "p8/logo-full.png", "image": SITE + "og-physio8.jpg",
        "telephone": WA_DISPLAY.replace(" ", "").replace("-", ""), "address": addr,
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]}, "hasMap": MAP_LINK,
        "areaServed": "Gading Serpong, Tangerang", "currenciesAccepted": "IDR", "sameAs": [IG],
        "medicalSpecialty": "PhysicalTherapy",
        "knowsAbout": ["Sports injuries", "Padel injuries", "Tennis elbow", "Running injuries", "ACL rehabilitation", "Clinical Pilates"],
        "availableService": [{"@type": "MedicalTherapy", "name": x} for x in
                             ("Sports injury physiotherapy", "Clinical Pilates", "Manual therapy", "Dry needling", "Kinesio taping",
                              "Movement & Posture Assessment", "Post-surgery rehabilitation")],
        "employee": {"@type": "Person", "name": "Ika Setia Ningsih", "honorificSuffix": "S.Ft", "jobTitle": "Lead Physiotherapist", "image": SITE + "p8/ika-setia-ningsih.jpg",
                     "alumniOf": {"@type": "CollegeOrUniversity", "name": "Universitas Esa Unggul"}},
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
    body = "\n".join([header(), "<main>", hero(), injuries(), pathway(), method(), assessment(), pilates(), team(),
                      pricing(), location(), articles(arts, img_fn, date_fn), faq(), booking(), "</main>", footer()])
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
