"""Generate assets/banner.svg: a pixel-art design canvas built live by a swarm of cursors.

Run:  python scripts/banner.py
Everything is plain SVG + SMIL so it animates inside a GitHub README <img>.
"""
from pathlib import Path

T = 22.0          # loop length in seconds
W, H = 880, 344
EASE = "0.45 0 0.25 1"

BG = "#0d0d0f"
WHITE = "#f2f2f2"
GRAY = "#8a8a93"
DIM = "#5a5a63"
RED = "#8b5cf6"  # main accent (violet)
CYAN = "#22d3ee"
YELLOW = "#facc15"
PURPLE = "#60a5fa"
GREEN = "#4ade80"
PINK = "#f472b6"

# ---------------------------------------------------------------- pixel font (5x7)
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "J": ["..###", "...#.", "...#.", "...#.", "#..#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    " ": ["....."] * 7,
}
# tiny 3x5 digits for the rulers
DIGITS = {
    "0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"],
    "2": ["###", "..#", "###", "#..", "###"], "3": ["###", "..#", "###", "..#", "###"],
    "4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "###", "..#", "###"],
    "6": ["###", "#..", "###", "#.#", "###"], "7": ["###", "..#", "..#", "..#", "..#"],
    "8": ["###", "#.#", "###", "#.#", "###"], "9": ["###", "#.#", "###", "..#", "###"],
}

ARROW_OUT = [  # O = outline, F = fill
    "O.........", "OO........", "OFO.......", "OFFO......", "OFFFO.....", "OFFFFO....",
    "OFFFFFO...", "OFFFFFFO..", "OFFFOOOO..", "OFOFFO....", "OO.OFFO...", "O...OFFO..",
    ".....OO...",
]


def g(v):
    """Format a number compactly."""
    return f"{v:.2f}".rstrip("0").rstrip(".")


def bitmap_path(rows, x, y, px, on="#"):
    """Merge horizontal runs of a bitmap into one compact path string."""
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] in on:
                s = c
                while c < len(row) and row[c] in on:
                    c += 1
                w = (c - s) * px
                out.append(f"M{g(x + s * px)} {g(y + r * px)}h{g(w)}v{g(px)}h-{g(w)}z")
            else:
                c += 1
    return "".join(out)


def text_path(s, x, y, px):
    return "".join(bitmap_path(FONT[ch], x + i * 6 * px, y, px) for i, ch in enumerate(s))


def text_w(s, px):
    return len(s) * 6 * px - px


# ---------------------------------------------------------------- animation helpers
def _frames(pts):
    """Pad a list of (seconds, value) to cover the full loop with strictly rising keyTimes."""
    pts = sorted(pts, key=lambda p: p[0])
    if pts[0][0] > 0:
        pts = [(0, pts[0][1])] + pts
    if pts[-1][0] < T:
        pts = pts + [(T, pts[-1][1])]
    fixed, last = [], -1.0
    for t, v in pts:
        t = max(t, last + 0.01)
        fixed.append((min(t, T), v))
        last = t
    fixed[-1] = (T, fixed[-1][1])
    return fixed


def anim(attr, pts, mode="linear", ease=False):
    f = _frames(pts)
    kt = ";".join(f"{t / T:.4f}" for t, _ in f)
    vals = ";".join(str(v) for _, v in f)
    extra = ""
    if ease and mode != "discrete":
        mode = "spline"
        extra = f' keySplines="{";".join([EASE] * (len(f) - 1))}"'
    return (f'<animate attributeName="{attr}" dur="{T}s" repeatCount="indefinite" '
            f'calcMode="{mode}" keyTimes="{kt}" values="{vals}"{extra}/>')


def move(pts):
    f = _frames(pts)
    kt = ";".join(f"{t / T:.4f}" for t, _ in f)
    vals = ";".join(f"{g(x)} {g(y)}" for _, (x, y) in f)
    ks = ";".join([EASE] * (len(f) - 1))
    return (f'<animateTransform attributeName="transform" type="translate" dur="{T}s" '
            f'repeatCount="indefinite" calcMode="spline" keyTimes="{kt}" values="{vals}" keySplines="{ks}"/>')


def show(t_in, t_out=None, fade=0.05):
    pts = [(0, 0), (t_in, 0), (t_in + fade, 1)]
    if t_out is not None:
        pts += [(t_out, 1), (t_out + fade, 0)]
    return anim("opacity", pts)


def hide_at(t):
    return anim("opacity", [(0, 1), (t, 1), (t + 0.01, 0)])


# ---------------------------------------------------------------- building blocks
_clip_id = [0]


def typed(s, x, y, px, color, steps, caret_until=None, blink=False):
    """Text revealed by a stepping clip. steps = [(t, chars_visible), ...]."""
    _clip_id[0] += 1
    cid = f"c{_clip_id[0]}"
    adv = 6 * px
    h = 7 * px
    seq = []
    for t, n in steps:
        seq.append((t, n))
    width = anim("width", [(t, n * adv) for t, n in seq], "discrete")
    caret_x = anim("x", [(t, x + n * adv) for t, n in seq], "discrete")
    start = seq[0][0]
    end = caret_until if caret_until is not None else seq[-1][0] + 0.4
    out = [f'<clipPath id="{cid}"><rect x="{x}" y="{y - 2}" height="{h + 4}" width="0">{width}</rect></clipPath>',
           f'<path d="{text_path(s, x, y, px)}" fill="{color}" clip-path="url(#{cid})"/>']
    cls = ' class="bl"' if blink else ""
    out.append(f'<rect{cls} y="{y}" width="{max(2, px)}" height="{h}" fill="{RED if blink else WHITE}">'
               f'{caret_x}{show(start, end, 0.01)}</rect>')
    return "".join(out)


def type_steps(n, t0, dt, back=False):
    if back:
        return [(t0 + i * dt, n - i) for i in range(n + 1)]
    return [(t0 + i * dt, i) for i in range(n + 1)]


def label_tag(text, color, x=12, y=22):
    w = len(text) * 6 + 5
    return (f'<g transform="translate({x} {y})"><rect width="{w}" height="13" fill="{color}"/>'
            f'<path d="{text_path(text, 3, 3, 1)}" fill="{BG}"/></g>')


def selbox(x, y, w, h, color, t0, t1, t_off, tag=None):
    """A selection rectangle dragged open between t0 and t1, removed at t_off."""
    r = (f'<rect x="{x}" y="{y}" width="0" height="0" fill="{color}" fill-opacity=".08" '
         f'stroke="{color}" stroke-width="2">'
         f'{anim("width", [(t0, 0), (t1, w)], ease=True)}{anim("height", [(t0, 0), (t1, h)], ease=True)}</rect>')
    return f'<g>{show(t0, t_off)}{r}</g>'


def handles(x, y, w, h, color, t_in, t_out):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{color}" stroke-width="2"/>'
    for cx, cy in [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]:
        s += f'<rect x="{cx - 3}" y="{cy - 3}" width="6" height="6" fill="{BG}" stroke="{color}" stroke-width="2"/>'
    return f'<g>{show(t_in, t_out)}{s}</g>'


def cursor(name, color, kf):
    pts = [(t, (x, y)) for t, x, y in kf]
    shadow = bitmap_path(ARROW_OUT, 2, 2, 2, on="OF")
    outline = bitmap_path(ARROW_OUT, 0, 0, 2, on="O")
    fill = bitmap_path(ARROW_OUT, 0, 0, 2, on="F")
    return (f'<g>{move(pts)}{show(kf[0][0], None, 0.25)}'
            f'<path d="{shadow}" fill="{BG}"/><path d="{fill}" fill="{color}"/>'
            f'<path d="{outline}" fill="{WHITE}"/>{label_tag(name, color)}</g>')


# ---------------------------------------------------------------- scene
def rulers():
    ticks = []
    for x in range(32, 869, 8):
        n = x - 32
        h = 8 if n % 64 == 0 else 3
        ticks.append(f"M{x} {24 - h}h1v{h}h-1z")
        if n % 64 == 0 and n:
            for i, d in enumerate(str(n)):
                ticks.append(bitmap_path(DIGITS[d], x + 3 + i * 4, 10, 1))
    for y in range(32, 333, 8):
        n = y - 32
        h = 8 if n % 64 == 0 else 3
        ticks.append(f"M{24 - h} {y}h{h}v1h-{h}z")
    return (f'<g>{show(0.05, None, 0.3)}<rect x="32" y="8" width="836" height="16" fill="#111114"/>'
            f'<rect x="8" y="32" width="16" height="300" fill="#111114"/>'
            f'<path d="{"".join(ticks)}" fill="{DIM}"/></g>')


def canvas():
    return (f'<g>{show(0.15, None, 0.35)}<rect x="32" y="32" width="836" height="300" fill="#101013"/>'
            f'<rect x="32" y="32" width="836" height="300" fill="url(#gr)"/>'
            f'<rect x="32" y="32" width="836" height="300" fill="none" stroke="#2a2a30" stroke-width="2"/></g>')


def monitor():
    fx, fy, fw, fh = 616, 64, 232, 156
    parts = []
    # frame dragged open by the AI cursor
    parts.append(f'<rect x="{fx}" y="{fy}" width="0" height="0" fill="#2e2e35">'
                 f'{anim("width", [(2.0, 0), (2.8, fw)], ease=True)}{anim("height", [(2.0, 0), (2.8, fh)], ease=True)}</rect>')
    parts.append(f'<g>{show(2.8, None, 0.2)}'
                 f'<rect x="{fx + 10}" y="{fy + 10}" width="{fw - 20}" height="{fh - 20}" fill="#0b0b0d"/>'
                 f'<rect x="{fx + 100}" y="{fy + fh}" width="32" height="14" fill="#2e2e35"/>'
                 f'<rect x="{fx + 76}" y="{fy + fh + 14}" width="80" height="8" fill="#2e2e35"/></g>')
    # bars drawn by the UI cursor
    for (bx, by, bw, col, t0, t1) in [(640, 90, 150, RED, 3.0, 3.6), (656, 108, 112, WHITE, 3.8, 4.3),
                                       (656, 124, 72, GRAY, 4.5, 4.9)]:
        parts.append(f'<rect x="{bx}" y="{by}" width="0" height="8" fill="{col}">'
                     f'{anim("width", [(t0, 0), (t1, bw)], ease=True)}</rect>')
    # little bar chart pulled up by the DB cursor
    heights = [18, 30, 24, 40, 34, 50]
    for i, hgt in enumerate(heights):
        t0 = 5.8 + i * 0.2
        col = RED if i == len(heights) - 1 else "#3a3a42"
        parts.append(f'<rect x="{648 + i * 20}" y="196" width="12" height="0" fill="{col}">'
                     f'{anim("height", [(t0, 0), (t0 + 0.35, hgt)], ease=True)}'
                     f'{anim("y", [(t0, 196), (t0 + 0.35, 196 - hgt)], ease=True)}</rect>')
    # GO button, clicked by QA
    parts.append(f'<g>{show(7.4, None, 0.15)}'
                 f'<rect x="782" y="172" width="44" height="24" fill="#14532d">{anim("fill", [(10.6, "#14532d"), (10.61, GREEN), (10.9, GREEN), (10.91, "#14532d")], "discrete")}</rect>'
                 f'<path d="{text_path("GO", 793, 177, 2)}" fill="{GREEN}">{anim("fill", [(10.6, GREEN), (10.61, BG), (10.9, BG), (10.91, GREEN)], "discrete")}</path></g>')
    return "".join(parts)


def pills():
    out = []
    for (y, text, col, dark, t) in [(256, "OPEN TO WORK", GREEN, "#0f2a1a", 11.0),
                                    (292, "FREELANCE", PURPLE, "#1e1533", 11.3)]:
        w = text_w(text, 2) + 40
        out.append(f'<g>{show(t, None, 0.1)}<rect x="652" y="{y}" width="{w}" height="26" fill="{dark}" '
                   f'stroke="{col}" stroke-width="2"/>'
                   f'<rect class="bl" x="662" y="{y + 9}" width="8" height="8" fill="{col}"/>'
                   f'<path d="{text_path(text, 680, y + 6, 2)}" fill="{col}"/></g>')
    return "".join(out)


def palette():
    x, y = 452, 148
    sw = [WHITE, GRAY, RED, GREEN, CYAN, YELLOW]
    s = f'<rect x="{x}" y="{y}" width="148" height="56" fill="#18181d" stroke="#2a2a30" stroke-width="2"/>'
    s += f'<path d="{text_path("FILL", x + 8, y + 7, 1)}" fill="{GRAY}"/>'
    for i, c in enumerate(sw):
        s += f'<rect x="{x + 8 + i * 22}" y="{y + 24}" width="14" height="14" fill="{c}"/>'
    s += (f'<rect x="{x + 6}" y="{y + 22}" width="18" height="18" fill="none" stroke="{WHITE}" stroke-width="2">'
          f'{anim("x", [(9.2, x + 6), (9.21, x + 6 + 2 * 22)], "discrete")}</rect>')
    return f'<g>{show(8.5, 10.0, 0.08)}{s}</g>'


# ---------------------------------------------------------------- 8-bit characters
def sprite(rows, palette, x, y, px):
    """Draw a multi-colour bitmap: one merged path per colour."""
    width = max(len(r) for r in rows)
    rows = [r.ljust(width, ".") for r in rows]
    return "".join(f'<path d="{bitmap_path(rows, x, y, px, on=k)}" fill="{c}"/>'
                   for k, c in palette.items() if any(k in r for r in rows))


SNORLAX = [
    "....OO..........OO....",
    "...OBBO........OBBO...",
    "...OBBBOOOOOOOOBBBO...",
    "..OBBBBBBBBBBBBBBBBO..",
    "..OBBBCCCCCCCCCCBBBO..",
    "..OBBCCOOCCCCOOCCBBO..",
    "..OBBCCCCCCCCCCCCBBO..",
    "..OBBCCCCOOOOCCCCBBO..",
    ".OBBBBCCCCCCCCCCBBBBO.",
    "OBBBBBBBCCCCCCBBBBBBBO",
    "OBBOBBCCCCCCCCCCBBOBBO",
    "OBBOBCCCCCCCCCCCCBOBBO",
    "OWWOBCCCCCCCCCCCCBOWWO",
    ".OOOBCCCCCCCCCCCCBOOO.",
    "...OBCCCCCCCCCCCCBO...",
    "..OBBcCCCCCCCCCCcBBO..",
    ".OCCCOBBBBBBBBBBOCCCO.",
    ".OCWCOOOOOOOOOOOOCWCO.",
    "..OOO............OOO..",
]
SNORLAX_PAL = {"O": "#163845", "B": "#3d8aa3", "C": "#efe0bf", "c": "#d6c39c", "W": "#f2f2f2"}

_CHAR_BODY = [
    "..OYYRRRRRRRRROOOOOO.....",
    "...OOYRRRRRRRRRO.........",
    ".....OYYYYRRRRRRO........",
    ".....OYYYYYRRRRRRO.......",
    "......OYYYYRRRRRRRO......",
    ".......OYYYRRRRRRRRO..OO.",
    "........OORRRRRRRRRROOFFO",
    ".........OrRRO.OrRRRRROFYFO",
    "........OWOO...OWOOOOO.OFO",
]
CHARIZARD_UP = [
    "..............OO.........",
    ".............OwwO.....OO.",
    "............OwWWwO..OwwO.",
    "...OOO.....OwWWWwO.OwWwO.",
    "..OrRRO....OwWWWWwOwWWwO.",
    ".ORERRRO...OwWWWWWwWWWwO.",
    "ORRRRRRRO..OwWWWWWWWWwO..",
    "ORRRRRRRRO.OwwWWWWWWwO...",
    ".OOYRRRRRROOOwwwwwwwO....",
] + _CHAR_BODY
CHARIZARD_DOWN = [
    ".........................",
    ".........................",
    ".........................",
    "...OOO...................",
    "..OrRRO..................",
    ".ORERRRO....OOOOOOOOOO...",
    "ORRRRRRRO..OwWWWWWWWWwOO.",
    "ORRRRRRRRO.OwwWWWWWWWWwwO",
    ".OOYRRRRRROOOwwwwwwwwwwO.",
] + _CHAR_BODY
CHARIZARD_PAL = {"O": "#3a1408", "R": "#f08030", "r": "#c85a1c", "Y": "#f8d878", "W": "#3a9aa8",
                 "w": "#25606c", "E": "#f2f2f2", "F": "#ff4d2e"}

FIRE_A = [
    "......YYooFF",
    "...YYYYYooooFF",
    "YYYYYYYYYooooFF",
    "...YYYYYooooFF",
    "......YYooFF",
]
FIRE_B = [
    ".........ooFF",
    "....YYYYoooFFF",
    ".YYYYYYYYYoooFF",
    "YYYYYYYYoooFF",
    ".....YYoooF",
]
FIRE_PAL = {"Y": "#ff4d2e", "o": "#ff9f1c", "F": "#ffe066"}  # red tip, yellow at the mouth

ZZZ = ["#####", "...#.", "..#..", ".#...", "#####"]


def snorlax(t_in):
    px, x, y = 5, 478, 237
    body = sprite(SNORLAX, SNORLAX_PAL, x, y, px)
    zs = []
    for i, (dx, size, delay) in enumerate([(0, 2, 0.0), (14, 3, 1.0), (32, 4, 2.0)]):
        zx, zy = x + 80 + dx, y - 4 - i * 12
        zs.append(
            f'<g opacity="0"><path d="{bitmap_path(ZZZ, zx, zy, size)}" fill="{WHITE}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.2;.7;1" dur="3s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 8;0 -10" dur="3s" begin="{delay}s" repeatCount="indefinite"/></g>')
    breathe = ('<animateTransform attributeName="transform" type="translate" values="0 0;0 -2;0 0" '
               'dur="3s" repeatCount="indefinite"/>')
    drop = move([(t_in, (0, -120)), (t_in + 0.6, (0, 0))])
    return f'<g>{show(t_in, None, 0.1)}<g>{drop}<g>{breathe}{body}</g>{"".join(zs)}</g></g>'


def charizard():
    px = 4
    up = sprite(CHARIZARD_UP, CHARIZARD_PAL, 0, 0, px)
    down = sprite(CHARIZARD_DOWN, CHARIZARD_PAL, 0, 0, px)
    flap = f'<g class="fa">{up}</g><g class="fb">{down}</g>'
    # fire comes out of the mouth (left side, row 7) and flickers between two frames
    fx = -len(FIRE_A[2]) * px
    fire = (f'<g>{show(9.4, 11.0, 0.05)}'
            f'<g class="fa">{sprite(FIRE_A, FIRE_PAL, fx, 20, px)}</g>'
            f'<g class="fb">{sprite(FIRE_B, FIRE_PAL, fx, 20, px)}</g></g>')
    path = move([(3.0, (920, 20)), (4.6, (500, 50)), (9.4, (492, 56)), (11.0, (492, 56)),
                 (14.0, (510, 40)), (17.5, (496, 52)), (20.4, (-140, -20))])
    bob = ('<animateTransform attributeName="transform" type="translate" values="0 0;0 4;0 0" '
           'dur="1s" repeatCount="indefinite"/>')
    return f'<g>{show(3.0, 20.4, 0.05)}<g>{path}<g>{bob}{fire}{flap}</g></g></g>'


def build():
    body = [rulers(), canvas()]

    # 1. small label
    body.append(selbox(56, 44, 168, 24, RED, 0.6, 1.1, 2.2))
    body.append(typed("HADESXZC.DEV", 62, 49, 2, GRAY, type_steps(12, 1.2, 0.06)))

    # 2. first name
    body.append(selbox(56, 70, 282, 75, CYAN, 0.9, 1.6, 2.8))
    body.append(typed("JOMER", 62, 76, 9, WHITE, type_steps(5, 1.8, 0.12)))

    # 3. last name (white, later recoloured red through the palette)
    body.append(selbox(56, 144, 390, 75, YELLOW, 1.2, 1.9, 3.6))
    body.append(f'<g>{hide_at(9.4)}{typed("IGNACIO", 62, 150, 9, WHITE, type_steps(7, 2.5, 0.12))}</g>')
    body.append(f'<g>{show(9.4, None, 0.01)}<path d="{text_path("IGNACIO", 62, 150, 9)}" fill="{RED}"/></g>')
    body.append(handles(56, 144, 390, 75, YELLOW, 8.1, 10.0))
    body.append(palette())

    # 4. role
    body.append(selbox(56, 222, 372, 29, PURPLE, 1.5, 2.2, 5.0))
    body.append(typed("FULL-STACK DEVELOPER", 62, 226, 3, WHITE, type_steps(20, 3.6, 0.06)))

    # 5. rotating line: type, delete, type again
    body.append(selbox(56, 258, 340, 22, GREEN, 1.8, 2.5, 7.0))
    a = "WEB / MOBILE / BACKEND / AI"
    b = "OPEN FOR FREELANCE"
    steps_a = type_steps(len(a), 5.2, 0.06) + type_steps(len(a), 13.0, 0.03, back=True)[1:]
    body.append(f'<g>{hide_at(13.9)}{typed(a, 62, 262, 2, GRAY, steps_a, caret_until=13.85)}</g>')
    body.append(typed(b, 62, 262, 2, GRAY, type_steps(len(b), 14.0, 0.06), caret_until=15.1))
    body.append(f'<rect class="bl" x="{62 + len(b) * 12 + 2}" y="262" width="10" height="14" fill="{RED}">{show(15.1)}</rect>')

    # right side
    body.append(monitor())
    body.append(pills())
    # Pokemon are switched off for now. Uncomment to bring them back.
    # body.append(snorlax(0.6))
    # body.append(charizard())

    swarm = [
        cursor("JOMER", RED, [(0.3, -20, 40), (0.6, 56, 44), (1.1, 224, 68), (2.4, 300, 36),
                              (5.0, 500, 60), (8.0, 560, 110), (12.0, 470, 300), (15.5, 540, 236),
                              (18.5, 600, 300), (21.2, 900, 320)]),
        cursor("UI", CYAN, [(0.5, 900, 60), (0.9, 56, 70), (1.6, 338, 145), (3.0, 640, 90),
                            (3.6, 790, 98), (3.8, 656, 108), (4.3, 768, 116), (4.5, 656, 124),
                            (4.9, 728, 132), (6.5, 760, 150), (11.0, 700, 40), (16.0, 820, 150),
                            (21.0, 920, 120)]),
        cursor("UX", YELLOW, [(0.8, -20, 200), (1.2, 56, 144), (1.9, 446, 219), (4.0, 480, 120),
                              (7.6, 460, 200), (8.1, 300, 180), (8.9, 466, 178), (9.2, 510, 178),
                              (10.5, 520, 240), (15.0, 380, 300), (21.0, -30, 300)]),
        cursor("DB", PURPLE, [(1.1, -20, 260), (1.5, 56, 222), (2.2, 428, 251), (4.2, 520, 250),
                              (5.8, 654, 196), (7.2, 760, 150), (12.0, 560, 300), (16.0, 300, 320),
                              (21.0, -30, 330)]),
        cursor("QA", GREEN, [(1.4, 300, 360), (1.8, 56, 258), (2.5, 396, 280), (5.0, 480, 300),
                             (9.6, 600, 290), (10.6, 806, 186), (12.0, 700, 300), (16.0, 500, 280),
                             (21.0, 300, 360)]),
        cursor("AI", PINK, [(1.6, 920, 30), (2.0, 616, 64), (2.8, 848, 220), (4.0, 860, 160),
                            (8.0, 700, 40), (10.8, 640, 250), (11.4, 760, 300), (12.5, 840, 240),
                            (16.0, 840, 60), (21.0, 920, 40)]),
    ]

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'shape-rendering="crispEdges" role="img" aria-label="Jomer Ignacio, full-stack developer: web, '
        f'mobile, backend and AI. Open to work and open for freelance. A swarm of design cursors builds this banner live.">\n'
        f'<style>@keyframes bl{{50%{{opacity:0}}}}.bl{{animation:bl 1s steps(1) infinite}}'
        f'.fa{{animation:bl .4s steps(1) infinite}}.fb{{animation:bl .4s steps(1) -.2s infinite}}</style>\n'
        f'<rect width="{W}" height="{H}" fill="{BG}"/>\n'
        f'<defs><pattern id="gr" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<rect width="2" height="2" fill="#fff" opacity=".06"/></pattern></defs>\n'
        f'<g>{anim("opacity", [(0, 1), (21.0, 1), (21.6, 0)])}\n'
        + "\n".join(body) + "\n" + "\n".join(swarm) +
        "\n</g></svg>\n"
    )
    out = Path(__file__).resolve().parent.parent / "assets" / "banner.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"wrote {out} ({len(svg) // 1024} KB)")


if __name__ == "__main__":
    build()
