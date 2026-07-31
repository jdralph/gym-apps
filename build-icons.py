import os
from PIL import Image, ImageDraw

M = 2048                      # master render size
NAVY   = (0x0B, 0x1B, 0x3E)
YELLOW = (0xFF, 0xD4, 0x00)
INK    = (0x0C, 0x0E, 0x11)
BLUE   = (0x0B, 0x3F, 0xD8)
WHITE  = (0xFF, 0xFF, 0xFF)
RED    = (0xE0, 0x1B, 0x1B)

S = M / 180.0                 # design grid is 180 units square
CLEAR = (0, 0, 0, 0)


def layer():
    im = Image.new("RGBA", (M, M), CLEAR)
    return im, ImageDraw.Draw(im)


def b(x0, y0, x1, y1):
    return [x0 * S, y0 * S, x1 * S, y1 * S]


# ---------------------------------------------------------------- whistle
def whistle():
    """Flat tapered mouthpiece rising into a round barrel, window at the join."""
    im, d = layer()
    Y = YELLOW + (255,)

    d.ellipse(b(80, 56, 160, 136), fill=Y)                                  # barrel
    d.rounded_rectangle(b(16, 77, 126, 115), radius=7 * S, fill=Y,          # mouthpiece
                        corners=(True, False, False, True))
    d.rounded_rectangle(b(84, 58, 107, 101), radius=5 * S, fill=CLEAR,      # window
                        corners=(False, False, True, True))

    return im.rotate(26, resample=Image.BICUBIC, center=(M / 2, M / 2)), NAVY


# -------------------------------------------------------------- stopwatch
def stopwatch():
    im, d = layer()
    Y = YELLOW + (255,)
    cx, cy, r = 90, 102, 51

    d.rounded_rectangle(b(82, 24, 98, 44), radius=5 * S, fill=Y)            # crown
    d.rounded_rectangle(b(84, 38, 96, 58), radius=3 * S, fill=Y)            # neck
    d.ellipse(b(cx - r, cy - r, cx + r, cy + r), outline=Y, width=int(12 * S))
    d.line([(cx * S, cy * S), ((cx + 22) * S, (cy - 24) * S)], fill=Y, width=int(11 * S))
    d.ellipse(b(cx - 8, cy - 8, cx + 8, cy + 8), fill=Y)
    return im, NAVY


# ---------------------------------------------------------- colour swatches
def swatches():
    im, d = layer()
    m, g = 23, 11
    cell = (180 - 2 * m - g) / 2
    for i, c in enumerate([BLUE, WHITE, YELLOW, RED]):
        x = m + (i % 2) * (cell + g)
        y = m + (i // 2) * (cell + g)
        d.rounded_rectangle(b(x, y, x + cell, y + cell), radius=10 * S, fill=c + (255,))
    return im, INK


# ------------------------------------------------------------------ compose
def compose(art, bg, size, fill):
    """Trim the artwork, scale it to `fill` of the tile, centre it on `bg`."""
    art = art.crop(art.getbbox())
    w, h = art.size
    k = (M * fill) / max(w, h)
    art = art.resize((max(1, round(w * k)), max(1, round(h * k))), Image.LANCZOS)
    tile = Image.new("RGB", (M, M), bg)
    tile.paste(art, ((M - art.width) // 2, (M - art.height) // 2), art)
    return tile.resize((size, size), Image.LANCZOS)


OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
os.makedirs(OUT, exist_ok=True)

for name, fn in [("home", whistle), ("timer", stopwatch), ("react", swatches)]:
    art, bg = fn()
    for size in (180, 192, 512):
        compose(art.copy(), bg, size, 0.78).save(f"{OUT}/icon-{name}-{size}.png")
    # Android adaptive icons crop to a shape, so pull the artwork well inside
    compose(art.copy(), bg, 512, 0.58).save(f"{OUT}/icon-{name}-512-maskable.png")

print("icons written to " + OUT)
