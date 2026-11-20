"""Draw THE DAILY GLOBE front page for 20 November 2026.

Reads tools/stories.json and renders a 1024x1024 newspaper front page
to entry.png next to the repository root. Standard library plus Pillow.
Deterministic: same input always produces the same bytes.
"""

import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STORIES_PATH = os.path.join(HERE, "stories.json")
OUT_PATH = os.path.join(ROOT, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
MARGIN_X = 42
CONTENT_W = PAGE_W - 2 * MARGIN_X

PAPER = (247, 243, 232)
INK = (22, 22, 22)
SOFT_INK = (70, 70, 70)
RULE = (150, 145, 130)
ACCENT = (139, 26, 26)
STORM = (52, 92, 128)
PANEL_BG = (238, 233, 219)
PANEL_EDGE = (180, 172, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(filename, size):
    path = os.path.join(FONT_DIR, filename)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_BOLD = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: load_font("DejaVuSerif.ttf", s)
SANS = lambda s: load_font("DejaVuSans.ttf", s)
SANS_BOLD = lambda s: load_font("DejaVuSans-Bold.ttf", s)


def wrap_lines(draw, text, font, max_width):
    """Split text into lines that fit max_width, measured with the font."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, text, font, fill, max_width, leading, max_lines=None):
    """Draw wrapped text starting at (x, y); return the y after the last line.

    When max_lines is set, keep at most that many lines and end the last
    one with an ellipsis when text is cut off.
    """
    lines = wrap_lines(draw, text, font, max_width)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip() + " ..."
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_spiral(draw, cx, cy, max_r, color):
    """Draw a cyclone swirl as an Archimedean spiral plus a calm eye."""
    points = []
    steps = 360
    for i in range(steps + 1):
        angle = math.radians(i * 2)
        r = max_r * i / steps
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.line(points, fill=color, width=4, joint="curve")
    draw.ellipse(
        [cx - 12, cy - 12, cx + 12, cy + 12],
        outline=color,
        width=3,
    )
    draw.ellipse(
        [cx - 5, cy - 5, cx + 5, cy + 5],
        fill=color,
    )


def draw_lead(draw, data, x, y, width):
    """Lead story on the left, cyclone art on the right. Returns bottom y."""
    lead = data["lead"]
    art_w = 300
    text_w = width - art_w - 28

    kicker_font = SANS_BOLD(20)
    head_font = SERIF_BOLD(34)
    body_font = SANS(18)

    draw.text((x, y), lead["kicker"], font=kicker_font, fill=ACCENT)
    y += 28
    y = draw_wrapped(draw, x, y, lead["headline"], head_font, INK, text_w, 42)
    y += 6
    y = draw_wrapped(draw, x, y, lead["body"], body_font, SOFT_INK, text_w, 24, max_lines=2)

    art_x = x + text_w + 28
    art_cx = art_x + art_w // 2
    art_cy = y - 150
    draw_spiral(draw, art_cx, art_cy, 120, STORM)
    caption = SANS(16)
    label = "Cyclone Akvan, Bay of Bengal"
    tw = draw.textlength(label, font=caption)
    draw.text((art_cx - tw / 2, art_cy + 132), label, font=caption, fill=SOFT_INK)
    return y


def draw_story(draw, story, x, y, width):
    """One secondary story: kicker, headline, body. Returns bottom y."""
    kicker_font = SANS_BOLD(16)
    head_font = SERIF_BOLD(22)
    body_font = SANS(17)

    draw.text((x, y), story["kicker"], font=kicker_font, fill=ACCENT)
    y += 22
    y = draw_wrapped(draw, x, y, story["headline"], head_font, INK, width, 27)
    y += 4
    y = draw_wrapped(draw, x, y, story["body"], body_font, SOFT_INK, width, 20, max_lines=2)
    return y


def draw_briefs(draw, briefs, x, y, width):
    """A short list of one-line briefs under an IN BRIEF header."""
    header_font = SANS_BOLD(18)
    item_font = SANS(18)
    draw.text((x, y), "IN BRIEF", font=header_font, fill=INK)
    y += 26
    for item in briefs:
        draw.text((x, y), "\u2022", font=item_font, fill=ACCENT)
        y = draw_wrapped(draw, x + 20, y, item, item_font, SOFT_INK, width - 20, 20)
        y += 2
    return y


def draw_markets(draw, markets, x, y, width):
    """Boxed markets strip: one cell per market, label above its figure."""
    box_h = 78
    draw.rectangle([x, y, x + width, y + box_h], fill=PANEL_BG, outline=PANEL_EDGE, width=2)
    header_font = SANS_BOLD(16)
    label_font = SANS(15)
    figure_font = SANS_BOLD(22)

    draw.text((x + 14, y + 8), "MARKETS", font=header_font, fill=INK)
    cell_w = width // len(markets)
    for i, market in enumerate(markets):
        cx = x + i * cell_w + cell_w // 2
        label = market["label"]
        figure = market["text"]
        lw = draw.textlength(label, font=label_font)
        fw = draw.textlength(figure, font=figure_font)
        draw.text((cx - lw / 2, y + 30), label, font=label_font, fill=SOFT_INK)
        draw.text((cx - fw / 2, y + 48), figure, font=figure_font, fill=INK)
    return y + box_h


def build():
    with open(STORIES_PATH, encoding="utf-8") as handle:
        data = json.load(handle)

    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)

    y = 24
    mast_font = SERIF_BOLD(54)
    title = data["paper"]
    tw = draw.textlength(title, font=mast_font)
    draw.text(((PAGE_W - tw) / 2, y), title, font=mast_font, fill=INK)
    y += 66

    draw.line([(MARGIN_X, y), (PAGE_W - MARGIN_X, y)], fill=RULE, width=2)
    y += 10
    meta_font = SANS(19)
    date_text = data["date"]
    tag_text = data["tagline"]
    draw.text((MARGIN_X, y), date_text, font=meta_font, fill=SOFT_INK)
    tag_w = draw.textlength(tag_text, font=meta_font)
    draw.text((PAGE_W - MARGIN_X - tag_w, y), tag_text, font=meta_font, fill=SOFT_INK)
    y += 30
    draw.line([(MARGIN_X, y), (PAGE_W - MARGIN_X, y)], fill=INK, width=3)
    y += 16

    y = draw_lead(draw, data, MARGIN_X, y, CONTENT_W)
    y += 12
    draw.line([(MARGIN_X, y), (PAGE_W - MARGIN_X, y)], fill=RULE, width=2)
    y += 12

    col_w = (CONTENT_W - 24) // 2
    left_x = MARGIN_X
    right_x = MARGIN_X + col_w + 24
    stories = data["stories"]
    left_y = y
    right_y = y
    for i, story in enumerate(stories):
        if i % 2 == 0:
            left_y = draw_story(draw, story, left_x, left_y, col_w)
            left_y += 12
        else:
            right_y = draw_story(draw, story, right_x, right_y, col_w)
            right_y += 12
    y = max(left_y, right_y) + 4
    draw.line([(MARGIN_X, y), (PAGE_W - MARGIN_X, y)], fill=RULE, width=2)
    y += 10

    y = draw_briefs(draw, data["briefs"], MARGIN_X, y, CONTENT_W)
    y += 8

    y = draw_markets(draw, data["markets"], MARGIN_X, y, CONTENT_W)
    y += 14

    foot_font = SANS(13)
    foot = "THE DAILY GLOBE  |  Friday, 20 November 2026  |  Sources: ICJ, Reuters, market data at close"
    fw = draw.textlength(foot, font=foot_font)
    draw.text(((PAGE_W - fw) / 2, PAGE_H - 30), foot, font=foot_font, fill=SOFT_INK)

    page.save(OUT_PATH, "PNG")
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    build()
