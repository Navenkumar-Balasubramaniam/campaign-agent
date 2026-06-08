import base64
import urllib.request
from io import BytesIO
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


_PRODUCT_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/b/bc/Estrella2014.jpg"
)
_LIFESTYLE_URL = (
    "https://images.unsplash.com/photo-1575037614876-c38a4d44f5b8"
    "?w=1080&q=80"
)

_image_cache = {}


def _fetch_image(url):
    if url in _image_cache:
        return _image_cache[url]
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            img = Image.open(BytesIO(resp.read())).convert("RGBA")
            _image_cache[url] = img
            return img
    except Exception:
        return None


def _fit_cover(img, target_w, target_h):
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def _gradient_overlay(width, height, alpha_top=0, alpha_bottom=200):
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(height):
        a = int(alpha_top + (alpha_bottom - alpha_top) * y / height)
        d.rectangle([0, y, width, y + 1], fill=(0, 0, 0, a))
    return overlay


class MockupAgent:
    def generate(self, brief, copy, strategy):
        headlines = copy["headlines"]
        primary_texts = copy["primary_texts"]

        product_img = _fetch_image(_PRODUCT_URL)
        lifestyle_img = _fetch_image(_LIFESTYLE_URL)

        formats = [
            ("A", "Instagram Feed Ad",
             (1080, 1080), "lifestyle", lifestyle_img),
            ("B", "Instagram Story Ad",
             (1080, 1600), "lifestyle", lifestyle_img),
            ("C", "Retargeting Product Ad",
             (1080, 1080), "product", product_img),
        ]

        assets = []
        for idx, (variant, ad_format, size, layout, photo) in enumerate(
            formats
        ):
            headline = headlines[idx % len(headlines)]
            body = primary_texts[idx % len(primary_texts)]
            image_data_url = self._render(
                brief, ad_format, size, layout, headline, body, photo
            )
            assets.append({
                "variant": variant,
                "format": ad_format,
                "headline": headline,
                "body": body,
                "image_data_url": image_data_url,
                "design_notes": (
                    "Draft layout generated locally for academic demo. "
                    "Use approved brand photography for production visuals."
                ),
            })

        return {
            "generation_note": (
                "Mock creative assets generated locally in free demo mode. "
                "Not official brand assets — treat as draft layouts."
            ),
            "assets": assets,
        }

    # ------------------------------------------------------------------

    def _render(self, brief, ad_format, size, layout, headline, body, photo):
        width, height = size
        RED = (181, 18, 27)
        DARK_RED = (122, 11, 18)
        GOLD = (245, 197, 66)
        CREAM = (255, 244, 214)
        WHITE = (255, 255, 255)

        canvas = Image.new("RGB", (width, height), RED)

        if layout == "lifestyle":
            self._draw_lifestyle(
                canvas, brief, ad_format, size,
                headline, body, photo,
                RED, DARK_RED, GOLD, CREAM, WHITE,
            )
        else:
            self._draw_product(
                canvas, brief, ad_format, size,
                headline, body, photo,
                RED, DARK_RED, GOLD, CREAM, WHITE,
            )

        buf = BytesIO()
        canvas.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(
            buf.getvalue()
        ).decode("ascii")

    def _draw_lifestyle(
        self, canvas, brief, ad_format, size,
        headline, body, photo,
        RED, DARK_RED, GOLD, CREAM, WHITE,
    ):
        width, height = size
        pad = 72

        # Full-bleed background photo with dark gradient
        if photo:
            bg = _fit_cover(photo.convert("RGB"), width, height)
            canvas.paste(bg, (0, 0))
            overlay = _gradient_overlay(
                width, height, alpha_top=40, alpha_bottom=230
            )
            canvas.paste(overlay, (0, 0), overlay)
        else:
            d = ImageDraw.Draw(canvas)
            d.rectangle([0, 0, width, height], fill=RED)
            d.rectangle(
                [0, int(height * 0.65), width, height],
                fill=(30, 107, 69),
            )

        draw = ImageDraw.Draw(canvas)

        # Brand + format label
        draw.text(
            (pad, 52),
            brief.brand.upper(),
            fill=GOLD,
            font=self._font(52, bold=True),
        )
        draw.text(
            (pad, 116),
            ad_format.upper(),
            fill=CREAM,
            font=self._font(26),
        )

        # Compute bottom text block
        hl_size = 76 if height <= 1100 else 88
        body_size = 34 if height <= 1100 else 40
        body_wrap = 44 if height <= 1100 else 34
        hl_lines = wrap(headline, width=20)
        body_lines = wrap(body, width=body_wrap)[:3]

        hl_block = len(hl_lines) * int(hl_size * 1.15)
        body_block = len(body_lines) * int(body_size * 1.35)
        cta_h = 90
        legal_h = 44
        total = hl_block + 24 + body_block + 32 + cta_h + 20 + legal_h
        y = height - total - pad

        for line in hl_lines:
            draw.text(
                (pad, y), line, fill=WHITE, font=self._font(hl_size, bold=True)
            )
            y += int(hl_size * 1.15)

        y += 24
        for line in body_lines:
            draw.text(
                (pad, y), line, fill=CREAM, font=self._font(body_size)
            )
            y += int(body_size * 1.35)

        y += 32
        cta_font = self._font(32, bold=True)
        btn_w = max(
            280,
            self._text_width(brief.cta.upper(), cta_font) + 80,
        )
        draw.rounded_rectangle(
            [pad, y, pad + btn_w, y + cta_h], radius=20, fill=GOLD
        )
        draw.text(
            (pad + 36, y + 22),
            brief.cta.upper(),
            fill=DARK_RED,
            font=cta_font,
        )

        draw.text(
            (pad, y + cta_h + 16),
            "Enjoy responsibly. Legal drinking age only.",
            fill=CREAM,
            font=self._font(24),
        )

    def _draw_product(
        self, canvas, brief, ad_format, size,
        headline, body, photo,
        RED, DARK_RED, GOLD, CREAM, WHITE,
    ):
        width, height = size
        pad = 72
        split = int(height * 0.52)

        if photo:
            ph = _fit_cover(photo.convert("RGB"), width, split)
            canvas.paste(ph, (0, 0))
            fade = _gradient_overlay(
                width, split, alpha_top=0, alpha_bottom=130
            )
            canvas.paste(fade, (0, 0), fade)
        else:
            d = ImageDraw.Draw(canvas)
            d.rectangle([0, 0, width, split], fill=DARK_RED)

        draw = ImageDraw.Draw(canvas)

        draw.text(
            (pad, 48),
            brief.brand.upper(),
            fill=GOLD,
            font=self._font(54, bold=True),
        )
        draw.text(
            (pad, 114),
            ad_format.upper(),
            fill=CREAM,
            font=self._font(26),
        )

        # Text zone
        draw.rectangle([0, split, width, height], fill=DARK_RED)
        draw.rectangle([pad, split, width - pad, split + 4], fill=GOLD)

        y = split + 32
        hl_size = 70
        for line in wrap(headline, width=22):
            draw.text(
                (pad, y), line, fill=WHITE,
                font=self._font(hl_size, bold=True),
            )
            y += int(hl_size * 1.1)

        y += 18
        body_size = 32
        for line in wrap(body, width=44)[:3]:
            draw.text(
                (pad, y), line, fill=CREAM, font=self._font(body_size)
            )
            y += int(body_size * 1.35)

        y += 24
        cta_font = self._font(30, bold=True)
        btn_w = max(
            260,
            self._text_width(brief.cta.upper(), cta_font) + 80,
        )
        cta_h = 76
        draw.rounded_rectangle(
            [pad, y, pad + btn_w, y + cta_h], radius=18, fill=GOLD
        )
        draw.text(
            (pad + 32, y + 20),
            brief.cta.upper(),
            fill=DARK_RED,
            font=cta_font,
        )

        draw.text(
            (pad, height - 40),
            "Enjoy responsibly. Legal drinking age only.",
            fill=CREAM,
            font=self._font(22),
        )

    # ------------------------------------------------------------------

    def _text_width(self, text, font):
        try:
            bbox = font.getbbox(text)
            return bbox[2] - bbox[0]
        except Exception:
            return len(text) * 18

    def _font(self, size, bold=False):
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
