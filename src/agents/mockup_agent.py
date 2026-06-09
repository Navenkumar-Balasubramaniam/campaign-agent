import base64
import hashlib
import urllib.request
from io import BytesIO
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


_ALCOHOL_KEYWORDS = {
    "beer", "wine", "spirits", "alcohol", "lager", "ale",
    "whiskey", "whisky", "vodka", "gin", "rum", "cocktail",
    "liquor", "brew", "cider", "champagne", "prosecco",
}

_PALETTES = [
    # 0 — navy / electric blue
    {"bg": (15, 23, 42), "panel": (10, 15, 30),
     "accent": (96, 165, 250), "text": (255, 255, 255),
     "subtext": (186, 210, 250), "cta_text": (10, 15, 30)},
    # 1 — charcoal / coral
    {"bg": (30, 27, 27), "panel": (20, 18, 18),
     "accent": (239, 100, 78), "text": (255, 255, 255),
     "subtext": (220, 210, 210), "cta_text": (255, 255, 255)},
    # 2 — forest / cream
    {"bg": (20, 52, 36), "panel": (12, 35, 24),
     "accent": (250, 235, 195), "text": (255, 255, 255),
     "subtext": (200, 230, 210), "cta_text": (12, 35, 24)},
    # 3 — midnight / sky
    {"bg": (10, 10, 35), "panel": (5, 5, 22),
     "accent": (56, 189, 248), "text": (255, 255, 255),
     "subtext": (186, 230, 253), "cta_text": (5, 5, 22)},
    # 4 — warm black / amber
    {"bg": (24, 18, 10), "panel": (15, 10, 5),
     "accent": (251, 191, 36), "text": (255, 255, 255),
     "subtext": (240, 220, 180), "cta_text": (15, 10, 5)},
]

_image_cache = {}


def _brand_seed(brand: str) -> int:
    return int(hashlib.md5(brand.encode()).hexdigest(), 16) % 900


def _pick_palette(brand: str) -> dict:
    return _PALETTES[sum(ord(c) for c in brand) % len(_PALETTES)]


def _fetch_image(url: str):
    if url in _image_cache:
        return _image_cache[url]
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            img = Image.open(BytesIO(resp.read())).convert("RGBA")
            _image_cache[url] = img
            return img
    except Exception:
        return None


def _photo_url(seed: int, w: int, h: int) -> str:
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


def _fit_cover(img: Image.Image, w: int, h: int) -> Image.Image:
    src_w, src_h = img.size
    scale = max(w / src_w, h / src_h)
    nw, nh = int(src_w * scale), int(src_h * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - w) // 2, (nh - h) // 2
    return img.crop((left, top, left + w, top + h))


def _dark_overlay(w: int, h: int, a_top: int = 0, a_bottom: int = 210):
    """Black gradient overlay — paste using itself as mask."""
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(h):
        a = int(a_top + (a_bottom - a_top) * y / h)
        d.rectangle([0, y, w, y + 1], fill=(0, 0, 0, a))
    return overlay


def _is_alcohol(product: str) -> bool:
    return any(kw in product.lower() for kw in _ALCOHOL_KEYWORDS)


class MockupAgent:
    def generate(self, brief, copy, strategy):
        headlines = copy["headlines"]
        primary_texts = copy["primary_texts"]
        palette = _pick_palette(brief.brand)
        seed = _brand_seed(brief.brand)
        legal = (
            "Enjoy responsibly. Legal drinking age only."
            if _is_alcohol(brief.product)
            else "Terms and conditions apply."
        )

        formats = [
            ("A", "Feed Ad",    (1080, 1080), "feed",    seed),
            ("B", "Story Ad",   (1080, 1920), "story",   seed + 1),
            ("C", "Product Ad", (1080, 1080), "product", seed + 2),
        ]

        assets = []
        for idx, (variant, label, size, layout, pseed) in enumerate(formats):
            headline = headlines[idx % len(headlines)]
            body = primary_texts[idx % len(primary_texts)]
            url = self._render(
                brief, label, size, layout,
                headline, body, palette, pseed, legal,
            )
            assets.append({
                "variant": variant,
                "format": f"{brief.channel} {label}",
                "headline": headline,
                "body": body,
                "image_data_url": url,
                "design_notes": (
                    "Draft layout for academic demo. "
                    "Replace with brand-approved photography for production."
                ),
            })

        return {
            "generation_note": (
                "Mock creative assets are draft layouts only. "
                "They are not official brand assets."
            ),
            "assets": assets,
        }

    # ------------------------------------------------------------------ #

    def _render(
        self, brief, label, size, layout,
        headline, body, palette, pseed, legal,
    ):
        w, h = size
        photo = _fetch_image(_photo_url(pseed, w, h))
        canvas = Image.new("RGB", (w, h), palette["bg"])

        if layout == "feed":
            self._draw_feed(
                canvas, brief, label, size,
                headline, body, palette, photo, legal,
            )
        elif layout == "story":
            self._draw_story(
                canvas, brief, label, size,
                headline, body, palette, photo, legal,
            )
        else:
            self._draw_product(
                canvas, brief, label, size,
                headline, body, palette, photo, legal,
            )

        buf = BytesIO()
        canvas.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(
            buf.getvalue()
        ).decode("ascii")

    # ------------------------------------------------------------------ #
    # Layout A — Feed (1080×1080): full-bleed photo + text bottom third  #
    # ------------------------------------------------------------------ #

    def _draw_feed(
        self, canvas, brief, label, size,
        headline, body, palette, photo, legal,
    ):
        w, h = size
        pad = 64

        if photo:
            bg = _fit_cover(photo.convert("RGB"), w, h)
            canvas.paste(bg, (0, 0))
            ov = _dark_overlay(w, h, a_top=0, a_bottom=220)
            canvas.paste(ov, (0, 0), ov)
        else:
            d0 = ImageDraw.Draw(canvas)
            d0.rectangle([0, 0, w, h], fill=palette["panel"])

        draw = ImageDraw.Draw(canvas)

        # Brand badge
        b_font = self._font(44, bold=True)
        badge_txt = brief.brand.upper()
        bw = self._tw(badge_txt, b_font) + 48
        draw.rounded_rectangle(
            [pad, 52, pad + bw, 52 + 64], radius=12, fill=palette["accent"]
        )
        draw.text(
            (pad + 24, 64), badge_txt,
            fill=palette["cta_text"], font=b_font,
        )
        draw.text(
            (pad, 132),
            f"{brief.channel.upper()} · {label.upper()}",
            fill=(180, 180, 180), font=self._font(24),
        )

        # Text block pinned to bottom
        hl_sz = 76
        bd_sz = 32
        cta_h = 84
        hl_lines = wrap(headline, width=20)
        bd_lines = wrap(body, width=44)[:2]
        total = (
            len(hl_lines) * int(hl_sz * 1.15) + 20
            + len(bd_lines) * int(bd_sz * 1.35) + 28
            + cta_h + 16 + 32
        )
        y = max(h // 2, h - total - pad)

        for line in hl_lines:
            draw.text(
                (pad, y), line, fill=palette["text"],
                font=self._font(hl_sz, bold=True),
            )
            y += int(hl_sz * 1.15)

        y += 20
        for line in bd_lines:
            draw.text(
                (pad, y), line, fill=(220, 220, 220),
                font=self._font(bd_sz),
            )
            y += int(bd_sz * 1.35)

        y += 28
        cf = self._font(32, bold=True)
        bw2 = max(260, self._tw(brief.cta.upper(), cf) + 80)
        draw.rounded_rectangle(
            [pad, y, pad + bw2, y + cta_h], radius=20, fill=palette["accent"]
        )
        draw.text(
            (pad + 36, y + (cta_h - 32) // 2),
            brief.cta.upper(), fill=palette["cta_text"], font=cf,
        )
        draw.text(
            (pad, y + cta_h + 12), legal,
            fill=(150, 150, 150), font=self._font(20),
        )

    # ------------------------------------------------------------------ #
    # Layout B — Story (1080×1920): photo top, headline spans split,     #
    #            dark panel + body + CTA bottom                           #
    # ------------------------------------------------------------------ #

    def _draw_story(
        self, canvas, brief, label, size,
        headline, body, palette, photo, legal,
    ):
        w, h = size
        pad = 72
        split = int(h * 0.52)

        # Photo (top portion)
        if photo:
            ph = _fit_cover(photo.convert("RGB"), w, split)
            canvas.paste(ph, (0, 0))
            # Light dark at top for brand readability
            top_ov = _dark_overlay(w, split, a_top=160, a_bottom=20)
            canvas.paste(top_ov, (0, 0), top_ov)
        else:
            d0 = ImageDraw.Draw(canvas)
            d0.rectangle([0, 0, w, split], fill=palette["panel"])

        draw = ImageDraw.Draw(canvas)

        # Brand name top-left
        draw.text(
            (pad, 64), brief.brand.upper(),
            fill=palette["accent"], font=self._font(52, bold=True),
        )
        draw.text(
            (pad, 132),
            f"{brief.channel.upper()} · STORY",
            fill=(190, 190, 190), font=self._font(26),
        )

        # Dark panel (bottom half)
        draw.rectangle([0, split, w, h], fill=palette["panel"])
        draw.rectangle(
            [pad, split, w - pad, split + 4], fill=palette["accent"]
        )

        # Headline — starts 80px above split so it bridges photo/panel
        hl_sz = 88
        hl_lines = wrap(headline, width=17)
        hl_total = len(hl_lines) * int(hl_sz * 1.12)
        y = max(split // 3, split - 80 - hl_total)

        for line in hl_lines:
            # Drop shadow for legibility over photo
            draw.text(
                (pad + 3, y + 3), line,
                fill=(0, 0, 0), font=self._font(hl_sz, bold=True),
            )
            draw.text(
                (pad, y), line,
                fill=palette["text"], font=self._font(hl_sz, bold=True),
            )
            y += int(hl_sz * 1.12)

        # Body in dark panel
        y = split + 40
        bd_sz = 36
        for line in wrap(body, width=34)[:3]:
            draw.text(
                (pad, y), line,
                fill=palette["subtext"], font=self._font(bd_sz),
            )
            y += int(bd_sz * 1.35)

        y += 28
        cf = self._font(34, bold=True)
        bw = max(280, self._tw(brief.cta.upper(), cf) + 80)
        cta_h = 90
        draw.rounded_rectangle(
            [pad, y, pad + bw, y + cta_h], radius=22, fill=palette["accent"]
        )
        draw.text(
            (pad + 36, y + (cta_h - 34) // 2),
            brief.cta.upper(), fill=palette["cta_text"], font=cf,
        )
        draw.text(
            (pad, h - 50), legal,
            fill=(130, 130, 130), font=self._font(22),
        )

    # ------------------------------------------------------------------ #
    # Layout C — Product (1080×1080): accent sidebar, photo + text panel #
    # ------------------------------------------------------------------ #

    def _draw_product(
        self, canvas, brief, label, size,
        headline, body, palette, photo, legal,
    ):
        w, h = size
        pad = 56
        sidebar_w = int(w * 0.12)
        cx = sidebar_w + pad          # content left edge
        pzone_w = w - sidebar_w
        pzone_h = int(h * 0.52)

        draw = ImageDraw.Draw(canvas)

        # Accent sidebar
        draw.rectangle([0, 0, sidebar_w, h], fill=palette["accent"])

        # Photo zone (right of sidebar, top 52%)
        if photo:
            ph = _fit_cover(photo.convert("RGB"), pzone_w, pzone_h)
            canvas.paste(ph, (sidebar_w, 0))
            fade = _dark_overlay(pzone_w, pzone_h, a_top=0, a_bottom=150)
            canvas.paste(fade, (sidebar_w, 0), fade)
        else:
            draw.rectangle(
                [sidebar_w, 0, w, pzone_h], fill=palette["panel"]
            )

        draw = ImageDraw.Draw(canvas)

        # Brand + label on photo
        draw.text(
            (cx, 52), brief.brand.upper(),
            fill=palette["accent"], font=self._font(54, bold=True),
        )
        draw.text(
            (cx, 122),
            f"{brief.channel.upper()} · {label.upper()}",
            fill=(190, 190, 190), font=self._font(26),
        )

        # Text panel
        draw.rectangle([sidebar_w, pzone_h, w, h], fill=palette["bg"])
        draw.rectangle(
            [cx, pzone_h, w - pad, pzone_h + 4], fill=palette["accent"]
        )

        y = pzone_h + 36
        hl_sz = 68
        for line in wrap(headline, width=22):
            draw.text(
                (cx, y), line, fill=palette["text"],
                font=self._font(hl_sz, bold=True),
            )
            y += int(hl_sz * 1.1)

        y += 16
        bd_sz = 30
        for line in wrap(body, width=46)[:3]:
            draw.text(
                (cx, y), line,
                fill=palette["subtext"], font=self._font(bd_sz),
            )
            y += int(bd_sz * 1.35)

        y += 20
        cf = self._font(30, bold=True)
        bw = max(240, self._tw(brief.cta.upper(), cf) + 80)
        cta_h = 74
        draw.rounded_rectangle(
            [cx, y, cx + bw, y + cta_h], radius=18, fill=palette["accent"]
        )
        draw.text(
            (cx + 32, y + (cta_h - 30) // 2),
            brief.cta.upper(), fill=palette["cta_text"], font=cf,
        )
        draw.text(
            (cx, h - 40), legal,
            fill=(130, 130, 130), font=self._font(20),
        )

    # ------------------------------------------------------------------ #

    def _tw(self, text: str, font) -> int:
        try:
            bbox = font.getbbox(text)
            return bbox[2] - bbox[0]
        except Exception:
            return len(text) * 18

    def _font(self, size: int, bold: bool = False):
        candidates = [
            "C:/Windows/Fonts/arialbd.ttf"
            if bold else "C:/Windows/Fonts/arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
            if bold else
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial Bold.ttf"
            if bold else "/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/liberation/"
            "LiberationSans-Bold.ttf"
            if bold else
            "/usr/share/fonts/truetype/liberation/"
            "LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold else
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        for path in candidates:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
        try:
            return ImageFont.load_default(size=size)
        except TypeError:
            return ImageFont.load_default()
