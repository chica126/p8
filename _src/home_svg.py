"""Inline SVG pieces for the homepage: Lucide icons (2px stroke) and the three
assessment diagrams (pose keypoints, range-of-motion gauge, squat screen)."""
import math

_IC = {
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "ccheck": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "car": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
    "train": '<path d="M8 3.1V7a4 4 0 0 0 8 0V3.1"/><path d="m9 15-1-1"/><path d="m15 15 1-1"/><path d="M9 19c-2.8 0-5-2.2-5-5v-4a8 8 0 0 1 16 0v4c0 2.8-2.2 5-5 5Z"/><path d="m8 19-2 3"/><path d="m16 19 2 3"/>',
    "building": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
    "insta": '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>',
    "menu": '<line x1="4" x2="20" y1="7" y2="7"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="17" y2="17"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "cap": '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
    "scan": '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><path d="M7 12h10"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "brief": '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
    "award": '<path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_IC[name]}</svg>')


WA_GLYPH = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2C6.6 2.2 2.2 6.6 2.2 12c0 1.7.45 3.35 1.28 4.8L2.2 21.8l5.12-1.27c1.4.77 2.99 1.17 4.68 1.17 5.4 0 9.8-4.4 9.8-9.8S17.4 2.2 12 2.2zm0 17.8c-1.5 0-2.97-.4-4.25-1.16l-.3-.18-3.04.75.8-2.93-.2-.31A8.1 8.1 0 0 1 3.9 12c0-4.47 3.63-8.1 8.1-8.1s8.1 3.63 8.1 8.1-3.63 8-8.1 8zm4.45-6.06c-.24-.12-1.44-.71-1.66-.79-.22-.08-.38-.12-.55.12-.16.24-.63.79-.77.95-.14.16-.28.18-.53.06-.24-.12-1.03-.38-1.96-1.21-.72-.65-1.21-1.44-1.36-1.69-.14-.24-.01-.37.11-.5.11-.11.24-.28.37-.43.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.43-.06-.12-.55-1.32-.75-1.81-.2-.47-.4-.41-.55-.42h-.47c-.16 0-.43.06-.65.3-.22.24-.85.83-.85 2.03s.87 2.35.99 2.51c.12.16 1.72 2.62 4.16 3.68.58.25 1.03.4 1.39.51.58.19 1.11.16 1.53.1.47-.07 1.44-.59 1.64-1.16.2-.57.2-1.06.14-1.16-.06-.1-.22-.16-.46-.28z"/></svg>')

# colours used inside the dark assessment section
_LINE = "rgba(255,255,255,.78)"
_DOT = "#D3DC6E"
_PLUMB = "#3CC3D3"
_LEVEL = "#D3DC6E"
_LABEL = "#B8B1D8"


def _skeleton(kp, edges, dx=0, head=None):
    out = []
    for a, b in edges:
        (x1, y1), (x2, y2) = kp[a], kp[b]
        out.append(f'<line x1="{x1+dx:.1f}" y1="{y1:.1f}" x2="{x2+dx:.1f}" y2="{y2:.1f}"/>')
    lines = f'<g stroke="{_LINE}" stroke-width="2" stroke-linecap="round">{"".join(out)}</g>'
    dots = "".join(f'<circle cx="{x+dx:.1f}" cy="{y:.1f}" r="2.6"/>' for k, (x, y) in kp.items() if k != "head")
    hx, hy = kp["head"]
    h = f'<circle cx="{hx+dx:.1f}" cy="{hy:.1f}" r="7" fill="none" stroke="{_LINE}" stroke-width="2"/>'
    return lines + h + f'<g fill="{_DOT}">{dots}</g>'


def posture_svg(labels):
    """Four-view pose-keypoint overlay (front, right, back, left)."""
    front = {"head": (45, 16), "neck": (45, 29), "lsh": (31, 35), "rsh": (59, 33), "lel": (27, 58), "rel": (63, 57),
             "lwr": (25, 79), "rwr": (65, 78), "lhip": (36, 80), "rhip": (54, 79), "lkn": (36, 108), "rkn": (54, 108),
             "lan": (36, 137), "ran": (54, 137)}
    fedges = [("head", "neck"), ("neck", "lsh"), ("neck", "rsh"), ("lsh", "lel"), ("lel", "lwr"), ("rsh", "rel"),
              ("rel", "rwr"), ("lsh", "lhip"), ("rsh", "rhip"), ("lhip", "rhip"), ("lhip", "lkn"), ("lkn", "lan"),
              ("rhip", "rkn"), ("rkn", "ran")]
    side = {"head": (50, 16), "neck": (47, 29), "sh": (44, 37), "el": (46, 60), "wr": (50, 81), "hip": (44, 81),
            "kn": (46, 109), "an": (44, 137), "toe": (55, 139)}
    sedges = [("head", "neck"), ("neck", "sh"), ("sh", "el"), ("el", "wr"), ("sh", "hip"), ("hip", "kn"),
              ("kn", "an"), ("an", "toe")]
    back = {k: (90 - x, y) for k, (x, y) in front.items()}
    back["lhip"], back["rhip"] = (54, 81), (36, 79)
    left = {k: (90 - x, y) for k, (x, y) in side.items()}
    panels = [(front, fedges, 45), (side, sedges, 44), (back, fedges, 45), (left, sedges, 46)]
    parts = []
    for i, (kp, ed, px) in enumerate(panels):
        dx = i * 92
        plumb = f'<line x1="{px+dx}" y1="4" x2="{px+dx}" y2="150" stroke="{_PLUMB}" stroke-width="1.5" stroke-dasharray="3 4"/>'
        lvl = ""
        if ed is fedges:
            a, b = kp["lsh"], kp["rsh"]
            m = (b[1] - a[1]) / (b[0] - a[0])
            y1, y2 = a[1] + (14 - a[0]) * m, a[1] + (76 - a[0]) * m
            lvl = f'<line x1="{14+dx}" y1="{y1:.1f}" x2="{76+dx}" y2="{y2:.1f}" stroke="{_LEVEL}" stroke-width="1.5" stroke-dasharray="2 3"/>'
            a, b = kp["lhip"], kp["rhip"]
            m = (b[1] - a[1]) / (b[0] - a[0])
            y1, y2 = a[1] + (20 - a[0]) * m, a[1] + (70 - a[0]) * m
            lvl += f'<line x1="{20+dx}" y1="{y1:.1f}" x2="{70+dx}" y2="{y2:.1f}" stroke="{_LEVEL}" stroke-width="1.5" stroke-dasharray="2 3"/>'
        parts.append(f'<rect x="{dx+2}" y="0" width="86" height="154" rx="10" fill="rgba(255,255,255,.03)" stroke="rgba(255,255,255,.08)"/>'
                     + plumb + lvl + _skeleton(kp, ed, dx))
        parts.append(f'<text x="{dx+45}" y="172" text-anchor="middle" font-size="11" font-weight="600" fill="{_LABEL}" '
                     f'font-family="Plus Jakarta Sans, sans-serif" data-en="{labels[i][1]}">{labels[i][0]}</text>')
    return f'<svg viewBox="0 0 364 178" role="img" aria-label="Pemetaan postur dari empat sisi">{"".join(parts)}</svg>'


def rom_svg():
    cx, cy, r = 120, 132, 98
    ticks = []
    for deg in range(0, 181, 15):
        t = math.radians(deg)
        ln = 12 if deg % 90 == 0 else 7
        x1, y1 = cx + r * math.cos(t), cy - r * math.sin(t)
        x2, y2 = cx + (r - ln) * math.cos(t), cy - (r - ln) * math.sin(t)
        ticks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    lab = ""
    for deg, txt in [(0, "0°"), (90, "90°"), (180, "180°")]:
        t = math.radians(deg)
        x, y = cx + (r + 14) * math.cos(t), cy - (r + 14) * math.sin(t)
        anchor = "start" if deg == 0 else ("end" if deg == 180 else "middle")
        if deg == 0:
            x -= 4
        if deg == 180:
            x += 4
        lab += f'<text x="{x:.1f}" y="{y+ (4 if deg != 90 else 0):.1f}" text-anchor="{anchor}">{txt}</text>'
    a = 150
    ra = 70
    ex, ey = cx + ra * math.cos(math.radians(a)), cy - ra * math.sin(math.radians(a))
    arc = f'<path d="M{cx+ra} {cy} A{ra} {ra} 0 0 0 {ex:.1f} {ey:.1f}" fill="none" stroke="{_PLUMB}" stroke-width="10" stroke-linecap="round" opacity=".9"/>'
    nx, ny = cx + (r - 18) * math.cos(math.radians(a)), cy - (r - 18) * math.sin(math.radians(a))
    needle = (f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>'
              f'<line x1="{cx}" y1="{cy}" x2="{cx+r-18}" y2="{cy}" stroke="rgba(255,255,255,.45)" stroke-width="2" stroke-linecap="round"/>'
              f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="5" fill="{_DOT}"/><circle cx="{cx}" cy="{cy}" r="5" fill="#fff"/>')
    base = f'<path d="M{cx-r} {cy} A{r} {r} 0 0 1 {cx+r} {cy}" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="2"/>'
    return (f'<svg viewBox="-14 0 268 150" role="img" aria-label="Pengukuran rentang gerak">{base}'
            f'<g stroke="rgba(255,255,255,.4)" stroke-width="1.5">{"".join(ticks)}</g>{arc}{needle}'
            f'<g font-size="11" font-weight="600" fill="{_LABEL}" font-family="Plus Jakarta Sans, sans-serif">{lab}</g></svg>')


def squat_svg():
    kp = {"head": (112, 30), "neck": (106, 42), "sh": (101, 50), "el": (124, 66), "wr": (148, 69), "hip": (70, 98),
          "kn": (118, 110), "an": (93, 146), "toe": (118, 148)}
    edges = [("head", "neck"), ("neck", "sh"), ("sh", "hip"), ("sh", "el"), ("el", "wr"), ("hip", "kn"),
             ("kn", "an"), ("an", "toe")]
    kx, ky = kp["kn"]
    a1 = math.atan2(kp["hip"][1] - ky, kp["hip"][0] - kx)
    a2 = math.atan2(kp["an"][1] - ky, kp["an"][0] - kx)
    rr = 17
    p1 = (kx + rr * math.cos(a1), ky + rr * math.sin(a1))
    p2 = (kx + rr * math.cos(a2), ky + rr * math.sin(a2))
    arc = f'<path d="M{p1[0]:.1f} {p1[1]:.1f} A{rr} {rr} 0 0 0 {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{_PLUMB}" stroke-width="2.5"/>'
    hx, hy = kp["hip"]
    guide = (f'<line x1="40" y1="{hy}" x2="150" y2="{hy}" stroke="{_LEVEL}" stroke-width="1.5" stroke-dasharray="2 3"/>'
             f'<line x1="40" y1="{ky}" x2="150" y2="{ky}" stroke="{_LEVEL}" stroke-width="1.5" stroke-dasharray="2 3" opacity=".6"/>'
             f'<line x1="30" y1="151" x2="170" y2="151" stroke="rgba(255,255,255,.25)" stroke-width="1.5"/>')
    trunk_t = (f'<line x1="{hx}" y1="{hy}" x2="{hx}" y2="40" stroke="{_PLUMB}" stroke-width="1.5" stroke-dasharray="3 4"/>')
    return (f'<svg viewBox="0 0 200 160" role="img" aria-label="Squat screen">{guide}{trunk_t}{arc}'
            + _skeleton(kp, edges) + '</svg>')


def loop_svg(fill="#fff"):
    """Simplified infinity loop outline used as a faint decorative mark (not the logo)."""
    return (f'<svg viewBox="0 0 200 100" aria-hidden="true"><path d="M50 15c-19 0-35 16-35 35s16 35 35 35c22 0 38-24 50-35 '
            f'12-11 28-35 50-35 19 0 35 16 35 35s-16 35-35 35c-22 0-38-24-50-35-12-11-28-35-50-35z" fill="none" '
            f'stroke="{fill}" stroke-width="10"/></svg>')
