"""Pixel-art sprites rasterised from simple shapes, then auto-outlined and shaded.

Run `python scripts/sprites.py` to print ASCII previews.
"""
import math


class Grid:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = [["." for _ in range(w)] for _ in range(h)]

    def _set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = c

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(self.h):
            for x in range(self.w):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    self._set(x, y, c)

    def poly(self, pts, c):
        for y in range(self.h):
            for x in range(self.w):
                inside, j = False, len(pts) - 1
                for i in range(len(pts)):
                    xi, yi = pts[i]
                    xj, yj = pts[j]
                    if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                        inside = not inside
                    j = i
                if inside:
                    self._set(x, y, c)

    def line(self, a, b, width, c):
        (x0, y0), (x1, y1) = a, b
        dx, dy = x1 - x0, y1 - y0
        L = dx * dx + dy * dy or 1
        for y in range(self.h):
            for x in range(self.w):
                t = max(0, min(1, ((x - x0) * dx + (y - y0) * dy) / L))
                if math.hypot(x - (x0 + t * dx), y - (y0 + t * dy)) <= width / 2:
                    self._set(x, y, c)

    def curve(self, pts, w0, w1, c, steps=24):
        """Thick polyline whose width tapers from w0 to w1."""
        segs = list(zip(pts, pts[1:]))
        for i, (a, b) in enumerate(segs):
            for s in range(steps):
                t = (i + s / steps) / len(segs)
                p = (a[0] + (b[0] - a[0]) * s / steps, a[1] + (b[1] - a[1]) * s / steps)
                r = (w0 + (w1 - w0) * t) / 2
                self.ellipse(p[0], p[1], r, r, c)

    def dot(self, x, y, c):
        self._set(x, y, c)

    def outline(self, c):
        filled = [[v != "." for v in row] for row in self.px]
        for y in range(self.h):
            for x in range(self.w):
                if filled[y][x]:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h and filled[ny][nx]:
                        self.px[y][x] = c
                        break

    def shade(self, base, dark, edge):
        """Darken base pixels that sit on the bottom/right edge next to the outline."""
        snap = [row[:] for row in self.px]
        for y in range(self.h):
            for x in range(self.w):
                if snap[y][x] != base:
                    continue
                for dx, dy in ((1, 0), (0, 1), (1, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h and snap[ny][nx] in edge:
                        self.px[y][x] = dark
                        break

    def flip(self):
        self.px = [row[::-1] for row in self.px]
        return self

    def rows(self):
        return ["".join(r) for r in self.px]


def rot(pts, origin, deg):
    ox, oy = origin
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(ox + (x - ox) * ca - (y - oy) * sa, oy + (x - ox) * sa + (y - oy) * ca) for x, y in pts]


# ------------------------------------------------------------------ Snorlax
SNORLAX_PAL = {
    "K": "#10262f",  # outline
    "B": "#2f7088",  # body
    "b": "#1f5064",  # body shadow
    "C": "#f3e6c4",  # cream
    "c": "#d8c49a",  # cream shadow
    "W": "#ffffff",  # claws / teeth
    "P": "#a8845a",  # foot pad
    "E": "#10262f",  # face lines
}


def snorlax():
    g = Grid(38, 34)
    # arms behind the body
    g.ellipse(4.5, 19, 3.5, 5.5, "B")
    g.ellipse(32.5, 19, 3.5, 5.5, "B")
    # body and head
    g.ellipse(18.5, 21, 15, 11.5, "B")
    g.ellipse(18.5, 10, 11, 8, "B")
    # ears
    g.poly([(8, 7), (9, 0), (14, 4)], "B")
    g.poly([(29, 7), (28, 0), (23, 4)], "B")
    # face and belly
    g.ellipse(18.5, 12, 8.5, 4.6, "C")
    g.ellipse(18.5, 23, 11.5, 9.2, "C")
    # closed eyes, mouth, fangs
    for x in range(13, 16):
        g.dot(x, 11, "E")
    for x in range(21, 24):
        g.dot(x, 11, "E")
    for x in range(15, 23):
        g.dot(x, 14, "E")
    g.dot(16, 13, "W")
    g.dot(21, 13, "W")
    # claws on the hands
    for x in (3, 5):
        g.dot(x, 24, "W")
    for x in (32, 34):
        g.dot(x, 24, "W")
    # feet sticking forward
    for fx in (8.5, 28.5):
        g.ellipse(fx, 30, 5.5, 3.2, "C")
        g.ellipse(fx, 30.5, 2.4, 1.5, "P")
    g.outline("K")
    g.shade("B", "b", "K")
    g.shade("C", "c", "K")
    return g.rows()


# ------------------------------------------------------------------ Charizard (faces left)
CHARIZARD_PAL = {
    "K": "#2a1206",  # outline
    "O": "#f0802c",  # body
    "o": "#c0561a",  # body shadow
    "Y": "#f9d27a",  # belly
    "T": "#2f95a3",  # wing membrane
    "t": "#1d6370",  # wing shadow
    "W": "#ffffff",  # eye shine / claws
    "E": "#1a0a04",  # eye / mouth
    "R": "#ff4422",  # flame
    "F": "#ffa41c",
    "y": "#ffe45c",
}

SHOULDER = (21, 17)
WING = [(21, 17), (24, 7), (30, 1), (41, 4), (39, 10), (35, 11), (33, 15), (29, 16), (26, 20)]
WING_BONES = [((21, 17), (30, 1)), ((30, 1), (41, 4))]
FAR_WING = [(18, 15), (19, 6), (24, 2), (23, 10)]


def charizard(flap=0):
    g = Grid(46, 38)
    ang = 38 if flap else 0
    # far wing (behind everything)
    # tail with flame
    g.curve([(24, 29), (31, 30), (36, 27), (39, 22)], 4.5, 2.2, "O")
    g.ellipse(39.5, 17.5, 2.6, 4.2, "R")
    g.ellipse(39.5, 18.6, 1.6, 2.6, "F")
    g.ellipse(39.5, 19.6, 0.8, 1.4, "y")
    # back leg
    g.ellipse(15, 31, 3.2, 3.2, "o")
    g.ellipse(12.5, 34.5, 3.2, 1.4, "o")
    # torso
    g.ellipse(20, 24, 7.2, 8.4, "O")
    g.ellipse(16.5, 25, 4, 6.2, "Y")
    # front leg
    g.ellipse(22.5, 30, 4.2, 4.4, "O")
    g.ellipse(19.5, 34.6, 4, 1.5, "O")
    for x in (15, 17):
        g.dot(x, 35, "W")
    # neck
    g.curve([(18, 18), (14, 12), (11, 8)], 5, 4, "O")
    g.curve([(16, 19), (12.5, 13), (10, 10)], 2.2, 1.8, "Y")
    # head with snout and horns
    g.line((11, 5), (15, 1), 1.6, "O")
    g.line((12, 7), (16.5, 4), 1.6, "O")
    g.ellipse(9, 7, 4.8, 3.4, "O")
    g.ellipse(4.5, 8.5, 3.6, 2.4, "O")
    for x in range(1, 7):
        g.dot(x, 10, "E")
    g.dot(9, 6, "E")
    g.dot(8, 6, "W")
    g.dot(2, 7, "E")  # nostril
    # arm
    g.line((15, 20), (11, 23), 2.2, "O")
    g.dot(10, 24, "W")
    g.dot(9, 23, "W")
    # main wing, in front of the body
    g.poly(rot(WING, SHOULDER, ang), "T")
    for a, b in WING_BONES:
        a2, b2 = rot([a, b], SHOULDER, ang)
        g.line(a2, b2, 1.2, "O")
    g.outline("K")
    g.shade("O", "o", "K")
    g.shade("T", "t", "K")
    return g.rows()


FIRE = [
    "........RRR.....",
    "....RRRRFFFRR...",
    "..RRFFFFyyyFFR..",
    "RRFFyyyyyyyyyFF.",
    "..RRFFFFyyyFFR..",
    "....RRRRFFFRR...",
    "........RRR.....",
]
FIRE_PAL = {"R": "#ff4422", "F": "#ffa41c", "y": "#ffe45c"}


if __name__ == "__main__":
    for name, rows in [("SNORLAX", snorlax()), ("CHARIZARD up", charizard(0)), ("CHARIZARD down", charizard(1))]:
        print(name)
        for r in rows:
            print(r.replace(".", " "))
        print()
