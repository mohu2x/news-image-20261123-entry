#!/usr/bin/env python3
"""Render the 23 November 2026 newspaper front page to asset.png."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
MARGIN = 54
RIGHT = SIZE - MARGIN
WIDTH = RIGHT - MARGIN
PAPER = "#f7f3ea"
INK = "#141414"
RED = "#b22028"
AMBER = "#ffcb5b"
FONT_DIR = Path("/usr/share/fonts/truetype/noto")
SERIF_BLACK = "NotoSerifDisplay-Black"
SERIF_BOLD = "NotoSerifDisplay-Bold"
SANS = "NotoSansDisplay-Regular"
SANS_BOLD = "NotoSansDisplay-Bold"
SANS_SEMIBOLD = "NotoSansDisplay-SemiBold"

SHORT_ITEMS = (
    (
        "TECHNOLOGY · NVIDIA",
        "Jensen Huang is CEO again",
        "Nvidia reinstated its founder under pressure from Trump, "
        "after a scandal engulfed the chip giant.",
    ),
    (
        "MIDDLE EAST · IRAN",
        "Tehran vows to defy US blockade",
        'Iran says it will use "all its tools" against the blockade; '
        "Trump is inclined to strike if no deal comes.",
    ),
    (
        "ASIA · INDONESIA",
        "Factory fire kills at least 24",
        "A blaze tore through a sweets factory; "
        "about 30 people are still missing in the ruins.",
    ),
    (
        "MARKETS · BITCOIN",
        "Bitcoin rebounds to $61,000",
        "It bounced off a two-year low after its second-longest "
        "losing streak on record.",
    ),
)


def font(face, size):
    return ImageFont.truetype(str(FONT_DIR / f"{face}.ttf"), size)


def text_right(draw, value, face):
    return draw.textbbox((0, 0), value, font=face, anchor="ls")[2]


def text_block(draw, x, baseline, value, face, width, line_height, color=INK):
    words = iter(value.split())
    line = next(words)
    for word in words:
        candidate = f"{line} {word}"
        if text_right(draw, candidate, face) <= width:
            line = candidate
        else:
            draw.text((x, baseline), line, font=face, fill=color, anchor="ls")
            baseline += line_height
            line = word
    draw.text((x, baseline), line, font=face, fill=color, anchor="ls")


def rule(draw, y, thickness=1):
    draw.rectangle((MARGIN, y, RIGHT - 1, y + thickness - 1), fill=INK)


def render():
    page = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(page)

    rule(draw, 54, 4)
    draw.text((MARGIN, 85), "THE WORLD IN ONE IMAGE", font=font(SANS_BOLD, 20),
              fill=RED, anchor="ls")
    draw.text((RIGHT, 85), "MONDAY · 23 NOVEMBER 2026", font=font(SANS_SEMIBOLD, 20),
              fill=INK, anchor="rs")
    title = "The Day the World Could Not Agree"
    nameplate = font(SANS_SEMIBOLD, 32)
    letter_spacing = 2.5
    advances = [draw.textlength(letter, font=nameplate) for letter in title]
    title_width = sum(advances) + (len(title) - 1) * letter_spacing
    x = (SIZE - title_width) / 2
    for letter, advance in zip(title, advances):
        draw.text((x, 139), letter, font=nameplate, fill=INK, anchor="ls")
        x += advance + letter_spacing
    rule(draw, 165, 6)

    lead_kicker = font(SANS_BOLD, 20)
    draw.text((MARGIN, 204), "CLIMATE · COP31 SUMMIT, TÜRKIYE", font=lead_kicker,
              fill=RED, anchor="ls")
    text_block(
        draw, MARGIN, 259,
        "COP31 ends without a deal after the longest climate summit on record",
        font(SERIF_BLACK, 48), WIDTH, 51,
    )
    text_block(
        draw, MARGIN, 351,
        "Nations split over phasing out fossil fuels and adaptation finance, "
        "and the record-breaking talks closed in disarray — what diplomats "
        "called climate diplomacy's darkest moment.",
        font(SANS, 25), 690, 31,
    )
    rule(draw, 444, 2)

    draw.text((MARGIN, 480), "WAR AT SEA · MEDITERRANEAN", font=lead_kicker,
              fill=RED, anchor="ls")
    headline = "Ukraine sinks a Russian warship off Libya"
    # Supersample the fine serifs, leaving room around the ink for Lanczos.
    scale = 4
    padding = 3
    face = font(SERIF_BLACK, 36 * scale)
    left, top, right, bottom = face.getbbox(headline, anchor="ls")
    left = left // scale - padding
    top = top // scale - padding
    right = (right + scale - 1) // scale + padding
    bottom = (bottom + scale - 1) // scale + padding
    mask_width, mask_height = right - left, bottom - top
    mask = Image.new("L", (mask_width * scale, mask_height * scale))
    ImageDraw.Draw(mask).text((-left * scale, -top * scale), headline,
                              font=face, fill=255, anchor="ls")
    mask = mask.resize((mask_width, mask_height), Image.Resampling.LANCZOS)
    draw.bitmap((MARGIN + left, 532 + top), mask, fill=INK)
    text_block(
        draw, MARGIN, 569,
        'Naval drones struck Russian ships in Benghazi port. President Zelenskyy '
        'hailed an "exemplary operation" — and the Ukraine war reached the Mediterranean.',
        font(SANS, 24), WIDTH, 29,
    )
    rule(draw, 624, 2)

    grid_kicker = font(SANS_BOLD, 17)
    grid_headline = font(SERIF_BOLD, 26)
    grid_body = font(SANS, 18)
    column_gap = 30
    column_width = (WIDTH - column_gap) // 2
    draw.line((SIZE // 2, 641, SIZE // 2, 900), fill=INK)
    rule(draw, 770)
    for index, (kicker, headline, body) in enumerate(SHORT_ITEMS):
        row, column = divmod(index, 2)
        x = MARGIN + column * (column_width + column_gap)
        baseline = 658 + row * 142
        draw.text((x, baseline), kicker, font=grid_kicker, fill=RED, anchor="ls")
        draw.text((x, baseline + 33), headline, font=grid_headline, fill=INK, anchor="ls")
        text_block(draw, x, baseline + 69, body, grid_body, column_width, 23)

    draw.rectangle((0, 917, SIZE - 1, SIZE - 1), fill=INK)
    draw.text((MARGIN, 942), "ALSO ON MONDAY", font=font(SANS_BOLD, 17),
              fill=AMBER, anchor="ls")
    ticker_lines = (
        'BepiColombo reaches Mercury after eight years · AI "proof" of the Riemann '
        'hypothesis sparks debate',
        'Russian strikes kill 15 near Kyiv · Democrats seal biggest US House '
        'majority since 1992',
    )
    ticker_face = font(SANS_SEMIBOLD, 19)
    for index, line in enumerate(ticker_lines):
        draw.text((MARGIN, 968 + index * 30), line, font=ticker_face,
                  fill="#ffffff", anchor="ls")
    return page


if __name__ == "__main__":
    render().save(Path(__file__).with_name("asset.png"), optimize=True)
