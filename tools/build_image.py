#!/usr/bin/env python3
"""Build THE DAILY GLOBE front page for 20 November 2026.

Draws a single 1024x1024 newspaper front page from tools/stories.json
using Pillow and DejaVu fonts. Vector-drawn shapes and rendered text only:
no photos, no AI-generated images. Deterministic: same input bytes produce
the same output bytes (no clock, no randomness, no timestamps in the PNG).

Run:  python3 tools/build_image.py   (writes entry.png next to the repo root)
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (163, 22, 33)
BLUE = (31, 78, 121)
GREY = (90, 86, 78)
LIGHT = (232, 226, 210)
RULE = (120, 112, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    return ImageFont.truetype(path, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)            # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)              # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit in width px."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# --- simplified continent outlines (lon, lat), equirectangular ---
CONTINENTS = {
    "N. AMERICA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-85, 80),
                   (-75, 72), (-65, 60), (-55, 52), (-60, 45), (-70, 42),
                   (-75, 35), (-80, 30), (-85, 28), (-90, 21), (-95, 18),
                   (-100, 16), (-105, 20), (-110, 23), (-115, 28), (-120, 34),
                   (-125, 40), (-125, 48), (-135, 58), (-155, 60), (-165, 60)],
    "S. AMERICA": [(-80, 10), (-75, 5), (-70, 0), (-65, -5), (-55, -10),
                   (-45, -15), (-40, -22), (-48, -28), (-55, -35), (-60, -40),
                   (-65, -45), (-70, -52), (-72, -45), (-75, -35), (-78, -25),
                   (-80, -15), (-82, -5), (-80, 5)],
    "AFRICA": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
               (35, 28), (43, 12), (48, 10), (51, 2), (48, -5), (40, -15),
               (35, -25), (28, -33), (20, -35), (15, -28), (12, -18), (9, -2),
               (8, 4), (-8, 5), (-13, 8), (-17, 12)],
    "EURASIA": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
                (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
                (32, 68), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73),
                (90, 75), (100, 76), (110, 74), (120, 73), (130, 72),
                (140, 72), (150, 70), (160, 69), (170, 67), (178, 65),
                (178, 62), (170, 60), (162, 56), (158, 52), (150, 60),
                (142, 55), (140, 45), (135, 42), (130, 38), (127, 35),
                (122, 32), (120, 28), (115, 22), (110, 20), (108, 18),
                (105, 10), (103, 8), (100, 8), (98, 12), (95, 16), (92, 20),
                (90, 22), (86, 20), (82, 16), (80, 10), (77, 8), (75, 12),
                (72, 20), (68, 22), (62, 25), (58, 26), (55, 26), (52, 28),
                (50, 29), (48, 30), (44, 29), (42, 28), (40, 36), (36, 36),
                (33, 36), (30, 36), (27, 37), (23, 36), (20, 40), (18, 40),
                (15, 44), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37),
                (-6, 36), (-9, 37)],
    "AUSTRALIA": [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33),
                  (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
                  (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
                  (146, -19), (142, -15), (142, -11), (137, -12), (135, -12),
                  (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
}


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # margin

    # ---------- masthead ----------
    d.line([(mx, 14), (W - mx, 14)], fill=INK, width=3)
    title = data["title"]
    tf = SERIF_B(62)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 22), title, font=tf, fill=INK)
    tag = data["tagline"]
    tagf = SANS(15)
    d.text((mx, 96), "ONE DAY", font=SANS_B(13), fill=RED)
    d.text((W - mx - d.textlength("EVERY CONTINENT", font=SANS_B(13)), 96),
           "EVERY CONTINENT", font=SANS_B(13), fill=RED)
    tgw = d.textlength(tag, font=tagf)
    d.text(((W - tgw) / 2, 94), tag, font=tagf, fill=GREY)
    d.line([(mx, 122), (W - mx, 122)], fill=INK, width=2)
    date = data["date_line"]
    df = SERIF_B(21)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 130), date, font=df, fill=INK)
    d.line([(mx, 162), (W - mx, 162)], fill=INK, width=3)
    d.line([(mx, 166), (W - mx, 166)], fill=INK, width=1)

    # ---------- lead story ----------
    y = 180
    lead = data["lead"]
    d.text((mx, y), lead["kicker"], font=SANS_B(14), fill=RED)
    y += 22
    hf = SERIF_B(35)
    for ln in wrap(d, lead["headline"], hf, W - 2 * mx):
        d.text((mx, y), ln, font=hf, fill=INK)
        y += 40
    y += 4
    bf = SERIF(15)
    for ln in wrap(d, lead["deck"], bf, W - 2 * mx):
        d.text((mx, y), ln, font=bf, fill=INK)
        y += 21
    y += 4
    d.text((mx, y), lead["source"], font=SANS(10), fill=GREY)
    y += 18
    d.line([(mx, y), (W - mx, y)], fill=INK, width=2)
    y += 8

    # ---------- map + markets row ----------
    row_y, row_h = y, 168
    map_x, map_w = mx, 600
    mkt_x, mkt_w = mx + 612, W - mx - (mx + 612)
    # map panel
    d.rectangle([map_x, row_y, map_x + map_w, row_y + row_h],
                outline=RULE, width=1)
    d.text((map_x + 10, row_y + 8), "THE DAY ON THE MAP",
           font=SANS_B(13), fill=INK)
    d.text((map_x + 10, row_y + 28), "Where the day's biggest stories happened",
           font=SANS(11), fill=GREY)
    px0, py0 = map_x + 8, row_y + 46
    pw, ph = map_w - 16, 94

    def project(lon, lat):
        # crop the poles: lat range -55..80 so continents fill the panel
        return (px0 + (lon + 180) / 360.0 * pw,
                py0 + (80 - lat) / 135.0 * ph)

    for name, poly in CONTINENTS.items():
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(214, 206, 184), outline=(110, 102, 86))
    for dot in data["map_dots"]:
        cx, cy = project(dot["lon"], dot["lat"])
        r = 9
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                  outline=(255, 255, 255), width=2)
        label = str(dot["n"])
        lw = d.textlength(label, font=SANS_B(10))
        d.text((cx - lw / 2, cy - 7), label, font=SANS_B(10),
               fill=(255, 255, 255))
    legend = "  •  ".join("%d %s" % (dot["n"], dot["label"])
                          for dot in data["map_dots"])
    for ln in wrap(d, legend, SANS(9), map_w - 20):
        d.text((map_x + 10, py0 + ph + 4), ln, font=SANS(9), fill=GREY)
        py0 += 12
    # markets panel
    d.rectangle([mkt_x, row_y, mkt_x + mkt_w, row_y + row_h],
                outline=RULE, width=1)
    d.text((mkt_x + 10, row_y + 8), "MARKETS", font=SANS_B(13), fill=INK)
    d.text((mkt_x + 10, row_y + 28), "Stocks end mixed",
           font=SANS(11), fill=GREY)
    bx = mkt_x + 12
    by = row_y + 52
    bw = mkt_w - 24
    for i, m in enumerate(data["markets"]):
        yy = by + i * 22
        d.text((bx, yy), m["label"], font=SANS_B(12), fill=INK)
        bar_x = bx + 92
        bar_w = int(abs(m["value"]) / 3.0 * (bw - 150))
        d.rectangle([bar_x, yy + 2, bar_x + max(bar_w, 2), yy + 15],
                    fill=RED)
        d.text((bar_x + max(bar_w, 2) + 6, yy),
               "%.2f%%" % m["value"], font=SANS_B(12), fill=RED)
    ny = by + 4 * 22 + 4
    for ln in wrap(d, data["markets_note"], SANS(11), bw):
        d.text((bx, ny), ln, font=SANS(11), fill=GREY)
        ny += 14
    y = row_y + row_h + 8

    # ---------- story grid: 3 rows x 4 cols ----------
    blocks = data["blocks"]
    cols, rows = 4, 3
    gap_x, gap_y = 14, 8
    bw2 = (W - 2 * mx - (cols - 1) * gap_x) / cols
    bh2 = 116
    for idx, b in enumerate(blocks):
        r, c = divmod(idx, cols)
        x = mx + c * (bw2 + gap_x)
        yy = y + r * (bh2 + gap_y)
        d.text((x, yy), b["kicker"], font=SANS_B(10), fill=RED)
        hy = yy + 15
        hf2 = SERIF_B(15)
        hlines = wrap(d, b["headline"], hf2, bw2)[:3]
        hy = draw_lines(d, hlines, x, hy, hf2, INK, 19)
        bf2 = SANS(11)
        blines = wrap(d, b["body"], bf2, bw2)
        max_body = max(0, int((yy + bh2 - 14 - hy) / 14))
        shown = blines[:max_body]
        if len(blines) > max_body and shown:
            shown[-1] = shown[-1].rstrip() + " …"
        hy = draw_lines(d, shown, x, hy + 2, bf2, INK, 14)
        d.text((x, yy + bh2 - 13), b["source"], font=SANS(9), fill=GREY)
    y = y + rows * bh2 + (rows - 1) * gap_y + 10

    # ---------- by the numbers, one line ----------
    d.line([(mx, y), (W - mx, y)], fill=RULE, width=1)
    y += 7
    numline = "BY THE NUMBERS  —  " + "   •   ".join(
        "%s %s" % (n["big"], n["small"]) for n in data["numbers"])
    for ln in wrap(d, numline, SANS_B(11), W - 2 * mx):
        d.text((mx, y), ln, font=SANS_B(11), fill=INK)
        y += 15
    y += 2

    # ---------- in brief ----------
    d.line([(mx, y), (W - mx, y)], fill=INK, width=2)
    y += 7
    d.text((mx, y), "IN BRIEF", font=SANS_B(12), fill=RED)
    y += 17
    brief = data["in_brief"]
    col_w = (W - 2 * mx) / len(brief)
    top = y
    for i, item in enumerate(brief):
        cx = mx + i * col_w
        lines = wrap(d, item, SANS(10), col_w - 12)
        draw_lines(d, lines[:3], cx, top, SANS(10), INK, 13)
    y = top + 40

    # ---------- footer ----------
    d.line([(mx, y), (W - mx, y)], fill=RULE, width=1)
    fw = d.textlength(data["footer"], font=SANS(9))
    d.text(((W - fw) / 2, y + 6), data["footer"], font=SANS(9), fill=GREY)

    out = os.path.join(ROOT, "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    sys.exit(main())
