"""Generate the LED dot-matrix SVGs for the shivpatel2468 profile README.

Every SVG is self-contained (no JS, no external fonts) so it renders inside GitHub's <img> sandbox.
Run:  python gen.py <out_dir>
Tweak points are the CONSTANTS block below.
"""

import sys
from pathlib import Path

# ----------------------------------------------------------------------------- CONSTANTS (tweak here)
ROSE = "#ff3f78"
GOLD = "#ffcc33"
NAME = "SHIV PATEL"
BRAND = "DESKDOT"
HANDLE = "github.com/shivpatel2468"
PILL = "DeskDot 3.8.0 is out"
TAGLINES = [
    "building DeskDot, a live companion for 32×32 LED panels",
    "async Python engine · React studio · MCP server for agents",
    "116 apps · 25 games · a fruit-fly brain that plays them",
    "phones become controllers · a provably-fair casino night",
]
STATS = [  # (value, label) shown on the slot-machine reels; all from the DeskDot README
    ("116", "APPS"),
    ("25", "GAMES"),
    ("70+", "LIVE SOURCES"),
    ("21", "MCP TOOLS"),
    ("4,400+", "TESTS"),
]
TICKER = "1,024 PIXELS.  ZERO SUBSCRIPTIONS.  THANKS FOR STOPPING BY  ✦  "

THEMES = {
    "dark": dict(
        bg="#0a090d", bg2="#121018", ink="#f5f3f7", sub="#a19cab", faint="#6d6878",
        orb_a=0.20, orb_b=0.13, grid="#ffffff", grid_o=0.045, border_a="#ffffff", border_o=0.10,
        pill_bg="#ffffff", pill_o=0.06, chip_bg="#17151d",
    ),
    "light": dict(
        bg="#fbf8f3", bg2="#f3eee6", ink="#1b1720", sub="#5d5766", faint="#8f8898",
        orb_a=0.16, orb_b=0.20, grid="#1b1720", grid_o=0.05, border_a="#1b1720", border_o=0.10,
        pill_bg="#ffffff", pill_o=0.75, chip_bg="#ffffff",
    ),
}

# ----------------------------------------------------------------------------- 5x7 bitmap font
F = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "✦": ["00100", "00100", "01110", "11111", "01110", "00100", "00100"],
    " ": ["000", "000", "000", "000", "000", "000", "000"],
}


def text_cols(s: str) -> list[list[int]]:
    """Return the text as a list of columns, each a list of lit row indices (0..6)."""
    cols: list[list[int]] = []
    for i, ch in enumerate(s):
        g = F[ch]
        for x in range(len(g[0])):
            cols.append([y for y in range(7) if g[y][x] == "1"])
        if i != len(s) - 1:
            cols.append([])
    return cols


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def led_defs(prefix: str = "") -> str:
    return f"""
    <radialGradient id="{prefix}ledR" cx="50%" cy="45%" r="55%">
      <stop offset="0" stop-color="#ffe3ea"/><stop offset=".42" stop-color="{ROSE}"/><stop offset="1" stop-color="#b8104a"/>
    </radialGradient>
    <radialGradient id="{prefix}ledG" cx="50%" cy="45%" r="55%">
      <stop offset="0" stop-color="#fff7d6"/><stop offset=".42" stop-color="{GOLD}"/><stop offset="1" stop-color="#c98a00"/>
    </radialGradient>
    <filter id="{prefix}glow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="3.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="{prefix}goldleaf" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#fff1b8"/><stop offset=".22" stop-color="#e2b23b"/>
      <stop offset=".5" stop-color="#fff4c9"/><stop offset=".74" stop-color="#b9861c"/><stop offset="1" stop-color="#f4d77a"/>
    </linearGradient>
    <linearGradient id="{prefix}glass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".10"/><stop offset=".35" stop-color="#ffffff" stop-opacity=".02"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="{prefix}sheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset=".5" stop-color="#ffffff" stop-opacity=".13"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>"""


def panel_frame(x, y, w, h, pitch, rdot, prefix="") -> tuple[str, str]:
    """Return (defs, body) for a dark LED panel with a gold-leaf bezel and unlit dot grid."""
    defs = f"""
    <pattern id="{prefix}dots" x="{x}" y="{y}" width="{pitch}" height="{pitch}" patternUnits="userSpaceOnUse">
      <circle cx="{pitch / 2}" cy="{pitch / 2}" r="{rdot}" fill="#1d1a24"/>
    </pattern>
    <clipPath id="{prefix}pclip"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/></clipPath>"""
    body = f"""
  <rect x="{x - 9}" y="{y - 9}" width="{w + 18}" height="{h + 18}" rx="18" fill="#050407"/>
  <rect x="{x - 9.5}" y="{y - 9.5}" width="{w + 19}" height="{h + 19}" rx="18.5" fill="none" stroke="url(#{prefix}goldleaf)" stroke-width="1.6"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#08070b"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="url(#{prefix}dots)"/>"""
    return defs, body


# ----------------------------------------------------------------------------- header
def header(theme: str) -> str:
    t = THEMES[theme]
    W, H = 1200, 440
    pitch, r = 12, 4.4
    cols_n, rows_n = 74, 19
    pw, ph = cols_n * pitch, rows_n * pitch
    px, py = (W - pw) // 2, 92
    name_cols = text_cols(NAME)
    brand_cols = text_cols(BRAND)
    # two little twinkling stars either side of the brand
    star = text_cols("✦")
    brand_full = star + [[], [], [], []] + brand_cols + [[], [], [], []] + star
    rows = [(name_cols, 2, "R", 0.0), (brand_full, 10, "G", 1.55)]

    cycle = 12.0
    lit: list[str] = []
    css_cols: list[str] = []
    gid = 0
    for cols, row0, col_fill, t0 in rows:
        off = (cols_n - len(cols)) // 2
        for ci, ys in enumerate(cols):
            if not ys:
                continue
            delay = t0 + ci * 0.024
            cx = px + (off + ci) * pitch + pitch / 2
            circles = "".join(
                f'<circle cx="{cx:.1f}" cy="{py + (row0 + yy) * pitch + pitch / 2:.1f}" r="{r}"/>' for yy in ys
            )
            lit.append(f'<g class="c" style="animation-delay:{delay:.3f}s" fill="url(#led{col_fill})">{circles}</g>')
            gid += 1

    # rotating tagline lines (terminal style)
    n = len(TAGLINES)
    seg = 100 / n
    lines = []
    for i, s in enumerate(TAGLINES):
        lines.append(
            f'<text class="ln" style="animation-delay:{i * 4}s" x="{W / 2}" y="{py + ph + 66}" text-anchor="middle">'
            f'<tspan fill="{ROSE}">❯ </tspan>{esc(s)}<tspan class="cur" fill="{GOLD}"> ▌</tspan></text>'
        )
    pdefs, pbody = panel_frame(px, py, pw, ph, pitch, r)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
  <title id="t">Shiv Patel — builder of DeskDot</title>
  <desc id="d">An LED dot-matrix sign that lights up column by column: SHIV PATEL in rose, DESKDOT in gold. Below it: {esc(" / ".join(TAGLINES))}.</desc>
  <defs>{led_defs()}{pdefs}
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_o"]}"/></pattern>
    <radialGradient id="fade" cx="50%" cy="45%" r="70%"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <mask id="gm"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
    <filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="70"/></filter>
    <linearGradient id="border" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="{t["border_a"]}" stop-opacity="{t["border_o"] + 0.05}"/>
      <stop offset=".5" stop-color="{t["border_a"]}" stop-opacity="{t["border_o"] / 2}"/>
      <stop offset="1" stop-color="{GOLD}" stop-opacity=".45"/>
    </linearGradient>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="24"/></clipPath>
  </defs>
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, "Cascadia Code", Menlo, Consolas, "Liberation Mono", monospace; }}
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif; }}
    .c {{ opacity: 0; animation: on {cycle}s linear infinite both; }}
    @keyframes on {{
      0% {{ opacity: 0; }} 1.2% {{ opacity: 1; }} 2.5% {{ opacity: .82; }} 4% {{ opacity: 1; }}
      74% {{ opacity: 1; }} 77% {{ opacity: 0; }} 100% {{ opacity: 0; }}
    }}
    .lit {{ animation: breathe 3.2s ease-in-out infinite alternate; }}
    @keyframes breathe {{ to {{ filter: brightness(1.18); }} }}
    .sheen {{ animation: sheen {cycle}s ease-in-out infinite; }}
    @keyframes sheen {{ 0%, 38% {{ transform: translateX(-420px); }} 60%, 100% {{ transform: translateX({pw + 420}px); }} }}
    .orb1 {{ animation: d1 16s ease-in-out infinite alternate; }}
    .orb2 {{ animation: d2 19s ease-in-out infinite alternate; }}
    @keyframes d1 {{ to {{ transform: translate(160px, 50px); }} }}
    @keyframes d2 {{ to {{ transform: translate(-180px, -40px); }} }}
    .ln {{ opacity: 0; animation: cyc 16s infinite; }}
    @keyframes cyc {{
      0% {{ opacity: 0; transform: translateY(8px); }} 3%, 22% {{ opacity: 1; transform: translateY(0); }}
      25%, 100% {{ opacity: 0; transform: translateY(-8px); }}
    }}
    .cur {{ animation: blink 1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    .dot {{ animation: pulse 2s ease-in-out infinite; }}
    @keyframes pulse {{ 50% {{ opacity: .3; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .c, .ln:first-of-type {{ animation: none; opacity: 1; }}
      .sheen, .orb1, .orb2, .cur, .dot, .lit {{ animation: none; }}
    }}
  </style>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
    <circle class="orb1" cx="220" cy="90" r="170" fill="{ROSE}" opacity="{t["orb_a"]}" filter="url(#blur)"/>
    <circle class="orb2" cx="990" cy="360" r="190" fill="{GOLD}" opacity="{t["orb_b"]}" filter="url(#blur)"/>
    <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gm)"/>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="24" fill="none" stroke="url(#border)"/>

  <g class="mono" font-size="15">
    <rect x="40" y="28" width="{len(PILL) * 9.1 + 46:.0f}" height="34" rx="17" fill="{t["pill_bg"]}" fill-opacity="{t["pill_o"]}" stroke="{t["border_a"]}" stroke-opacity=".12"/>
    <circle class="dot" cx="58" cy="45" r="4" fill="{GOLD if theme == "dark" else "#e0a100"}"/>
    <text x="72" y="50.5" fill="{t["sub"]}">{esc(PILL)}</text>
    <text x="{W - 40}" y="50.5" text-anchor="end" fill="{t["faint"]}">{esc(HANDLE)}</text>
  </g>
{pbody}
  <g filter="url(#glow)"><g class="lit">{"".join(lit)}</g></g>
  <g clip-path="url(#pclip)">
    <rect x="{px}" y="{py}" width="{pw}" height="{ph * 0.42:.0f}" fill="url(#glass)"/>
    <rect class="sheen" x="{px - 120}" y="{py}" width="220" height="{ph}" fill="url(#sheen)" transform="skewX(-18)"/>
  </g>

  <g class="mono" font-size="21" fill="{t["ink"]}">{"".join(lines)}</g>
</svg>
"""


# ----------------------------------------------------------------------------- slot-machine stats
def reels(theme: str) -> str:
    t = THEMES[theme]
    W, H = 1200, 200
    n = len(STATS)
    gap = 18
    cw = (W - 80 - gap * (n - 1)) / n
    cell_h = 46
    digit_w = 28
    parts: list[str] = []
    styles: list[str] = []
    k = 0
    for i, (val, label) in enumerate(STATS):
        x0 = 40 + i * (cw + gap)
        parts.append(
            f'<rect x="{x0:.1f}" y="24" width="{cw:.1f}" height="150" rx="18" fill="{t["chip_bg"]}" fill-opacity="{0.9 if theme == "light" else 0.75}" stroke="url(#goldleaf)" stroke-opacity=".55"/>'
            f'<rect x="{x0 + 1:.1f}" y="25" width="{cw - 2:.1f}" height="60" rx="17" fill="url(#glass)"/>'
        )
        total_w = sum(digit_w if ch.isdigit() else 16 for ch in val)
        cx = x0 + (cw - total_w) / 2
        win_y = 52
        parts.append(
            f'<rect x="{cx - 10:.1f}" y="{win_y - 6}" width="{total_w + 20:.1f}" height="{cell_h + 12}" rx="10" fill="#08070b" stroke="#2a2531"/>'
        )
        for j, ch in enumerate(val):
            w = digit_w if ch.isdigit() else 16
            if ch.isdigit():
                target = int(ch)
                spins = 2 + i % 2
                seq = [str(d % 10) for d in range(0, 10 * spins + target + 1)]
                dist = (len(seq) - 1) * cell_h
                stop = 2.2 + i * 0.45 + j * 0.18  # reels stop left to right, like a slot machine
                name = f"r{k}"
                k += 1
                styles.append(
                    f"@keyframes {name} {{ 0% {{ transform: translateY(0); }} {stop / 14 * 100:.1f}% {{ transform: translateY(-{dist}px); }} 100% {{ transform: translateY(-{dist}px); }} }}"
                    f" .{name} {{ animation: {name} 14s cubic-bezier(.2,.75,.25,1.04) infinite; }}"
                )
                strip = "".join(
                    f'<text x="{cx + w / 2:.1f}" y="{win_y + 36 + n_ * cell_h}" text-anchor="middle">{d}</text>'
                    for n_, d in enumerate(seq)
                )
                parts.append(f'<g clip-path="url(#win)"><g class="{name}" fill="url(#dg)">{strip}</g></g>')
            else:
                parts.append(f'<text x="{cx + w / 2:.1f}" y="{win_y + 36}" text-anchor="middle" fill="{GOLD}">{esc(ch)}</text>')
            cx += w
        parts.append(
            f'<text x="{x0 + cw / 2:.1f}" y="150" text-anchor="middle" class="lbl" fill="{t["sub"]}">{esc(label)}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">DeskDot by the numbers: {esc(", ".join(f"{v} {l.lower()}" for v, l in STATS))}</title>
  <defs>{led_defs()}
    <clipPath id="win"><rect x="0" y="48" width="{W}" height="{cell_h + 4}"/></clipPath>
    <linearGradient id="dg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2c2"/><stop offset=".55" stop-color="{GOLD}"/><stop offset="1" stop-color="#e3a514"/></linearGradient>
  </defs>
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, "Cascadia Code", Menlo, Consolas, monospace; font-size: 40px; font-weight: 700; }}
    .lbl {{ font-size: 13px; font-weight: 600; letter-spacing: 3px; }}
    {" ".join(styles)}
    @media (prefers-reduced-motion: reduce) {{ g[class^="r"] {{ animation: none !important; }} }}
  </style>
  {"".join(parts)}
</svg>
"""


# ----------------------------------------------------------------------------- divider (running pixel)
def divider(theme: str) -> str:
    W, H = 1200, 24
    pitch = 12
    n = W // pitch
    base = "#d9d2c6" if theme == "light" else "#221f29"
    dots = "".join(f'<circle cx="{i * pitch + 6}" cy="12" r="2.6"/>' for i in range(n))
    trail = "".join(
        f'<circle cx="{-k * pitch}" cy="12" r="{3.6 - k * 0.35:.2f}" fill="{GOLD if k == 0 else ROSE}" opacity="{1 - k * 0.16:.2f}"/>'
        for k in range(6)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="divider">
  <style>.run {{ animation: run 6s steps({n}) infinite; }} @keyframes run {{ to {{ transform: translateX({W + 6 * pitch}px); }} }}
  @media (prefers-reduced-motion: reduce) {{ .run {{ animation: none; opacity: 0; }} }}</style>
  <g fill="{base}">{dots}</g>
  <g class="run" transform="translate(6 0)">{trail}</g>
</svg>
"""


# ----------------------------------------------------------------------------- footer ticker
def ticker(theme: str) -> str:
    t = THEMES[theme]
    pitch, r = 8, 3.0
    rows_n = 11
    cols_n = 120
    W, H = cols_n * pitch + 40, rows_n * pitch + 40
    px, py = 20, 20
    cols = text_cols(TICKER)
    # colour per character: digits, punctuation and the star are gold, letters rose
    col_char = []
    for i, ch in enumerate(TICKER):
        col_char += [ch] * (len(F[ch][0]) + (1 if i != len(TICKER) - 1 else 0))
    span = len(cols) * pitch
    lit = []
    for ci, ys in enumerate(cols):
        for yy in ys:
            fill = "ledR" if col_char[ci].isalpha() else "ledG"
            lit.append(
                f'<circle cx="{px + ci * pitch + pitch / 2}" cy="{py + (2 + yy) * pitch + pitch / 2}" r="{r}" fill="url(#{fill})"/>'
            )
    group = "".join(lit)
    pdefs, pbody = panel_frame(px, py, cols_n * pitch, rows_n * pitch, pitch, r)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">{esc(TICKER.replace("✦", "").strip())}</title>
  <defs>{led_defs()}{pdefs}</defs>
  <style>.scroll {{ animation: sc {span / 60:.1f}s steps({len(cols)}) infinite; }} @keyframes sc {{ to {{ transform: translateX(-{span}px); }} }}
  @media (prefers-reduced-motion: reduce) {{ .scroll {{ animation: none; }} }}</style>
  <rect width="{W}" height="{H}" fill="{t["bg"]}" fill-opacity="0"/>
{pbody}
  <g clip-path="url(#pclip)" filter="url(#glow)"><g class="scroll"><g>{group}</g><g transform="translate({span} 0)">{group}</g></g></g>
  <g clip-path="url(#pclip)"><rect x="{px}" y="{py}" width="{cols_n * pitch}" height="{rows_n * pitch * 0.45}" fill="url(#glass)"/></g>
</svg>
"""


# ----------------------------------------------------------------------------- repo card
def card(theme: str, title: str, desc: list[str], tags: list[tuple[str, str]], kicker: str) -> str:
    t = THEMES[theme]
    W, H = 580, 190
    desc_svg = "".join(
        f'<text x="28" y="{94 + i * 22}" class="sans" font-size="14.5" fill="{t["sub"]}">{esc(s)}</text>'
        for i, s in enumerate(desc)
    )
    x = 28
    chips = []
    for label, color in tags:
        w = len(label) * 7.4 + 30
        chips.append(
            f'<g><rect x="{x:.1f}" y="146" width="{w:.1f}" height="24" rx="12" fill="{t["pill_bg"]}" fill-opacity="{t["pill_o"]}" stroke="{t["border_a"]}" stroke-opacity=".12"/>'
            f'<circle cx="{x + 13:.1f}" cy="158" r="4" fill="{color}"/>'
            f'<text x="{x + 22:.1f}" y="162" class="mono" font-size="12" fill="{t["sub"]}">{esc(label)}</text></g>'
        )
        x += w + 8
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">{esc(title)}: {esc(" ".join(desc))}</title>
  <defs>{led_defs()}
    <filter id="b" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
    <clipPath id="cc"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <style>.mono {{ font-family: ui-monospace, SFMono-Regular, "Cascadia Code", Menlo, Consolas, monospace; }}
  .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif; }}</style>
  <g clip-path="url(#cc)">
    <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
    <circle cx="{W - 40}" cy="20" r="90" fill="{ROSE}" opacity="{t["orb_a"] * 0.8}" filter="url(#b)"/>
    <rect width="{W}" height="70" fill="url(#glass)"/>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="url(#goldleaf)" stroke-opacity=".6"/>
  <text x="28" y="40" class="mono" font-size="11.5" letter-spacing="2" fill="{GOLD if theme == "dark" else "#b07d00"}">{esc(kicker)}</text>
  <text x="28" y="68" class="sans" font-size="22" font-weight="700" fill="{t["ink"]}">{esc(title)}</text>
  {desc_svg}
  {"".join(chips)}
</svg>
"""


CARDS = {
    "card-mobile": dict(
        title="Mobile-Computing-VI",
        kicker="◆ REPO · ANDROID LABS",
        desc=["Hands-on Android experiments: Bluetooth, GPS, drawing,", "graphics primitives, notifications, a DBMS app and more."],
        tags=[("Java", "#b07219"), ("Kotlin", "#A97BFF"), ("Android", "#3ddc84")],
    ),
    "card-web": dict(
        title="idotmatrix.com/app",
        kicker="◆ LIVE · NO INSTALL",
        desc=["The whole DeskDot engine in your browser: open it in", "Chrome or Edge and connect the panel over Web Bluetooth."],
        tags=[("Web Bluetooth", ROSE), ("Netlify", "#32e6e2"), ("Chrome · Edge", GOLD)],
    ),
}


def main(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for th in THEMES:
        (out / f"header-{th}.svg").write_text(header(th), encoding="utf-8")
        (out / f"reels-{th}.svg").write_text(reels(th), encoding="utf-8")
        (out / f"divider-{th}.svg").write_text(divider(th), encoding="utf-8")
        (out / f"ticker-{th}.svg").write_text(ticker(th), encoding="utf-8")
        for name, c in CARDS.items():
            (out / f"{name}-{th}.svg").write_text(card(th, **c), encoding="utf-8")
    for p in sorted(out.glob("*.svg")):
        print(f"{p.stat().st_size:>8}  {p.name}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "out"))
