import base64
from io import BytesIO
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


class MockupAgent:
    def generate(self, brief, copy, strategy):
        headlines = copy["headlines"]
        primary_texts = copy["primary_texts"]
        formats = [
            ("A", "Instagram Feed Ad", (1080, 1080), "sun"),
            ("B", "Instagram Story Ad", (1080, 1600), "park"),
            ("C", "Retargeting Product Ad", (1080, 1080), "product"),
        ]

        assets = []
        for index, (variant, ad_format, size, layout) in enumerate(formats):
            headline = headlines[index % len(headlines)]
            body = primary_texts[index % len(primary_texts)]
            image_data_url = self._render_mockup(
                brief=brief,
                strategy=strategy,
                variant=variant,
                ad_format=ad_format,
                size=size,
                layout=layout,
                headline=headline,
                body=body,
            )
            assets.append(
                {
                    "variant": variant,
                    "format": ad_format,
                    "headline": headline,
                    "body": body,
                    "image_data_url": image_data_url,
                    "design_notes": (
                        "Offline mock creative generated for academic demo. Use OpenRouter "
                        "or approved brand photography for final high-fidelity visuals."
                    ),
                }
            )

        return {
            "generation_note": (
                "These mock creative assets are generated locally in free demo mode. "
                "They are not official Estrella assets and should be treated as draft layouts."
            ),
            "assets": assets,
        }

    def _render_mockup(self, brief, strategy, variant, ad_format, size, layout, headline, body):
        width, height = size
        image = Image.new("RGB", size, "#B5121B")
        draw = ImageDraw.Draw(image)

        red = "#B5121B"
        deep_red = "#7A0B12"
        gold = "#F5C542"
        cream = "#FFF4D6"
        green = "#1E6B45"
        white = "#FFFFFF"

        draw.rectangle([0, 0, width, height], fill=red)
        draw.rectangle([0, int(height * 0.68), width, height], fill=green if layout != "product" else deep_red)

        if layout == "sun":
            draw.ellipse([width - 290, 70, width - 70, 290], fill=gold)
            draw.rectangle([0, int(height * 0.70), width, height], fill="#267A4E")
        elif layout == "park":
            draw.ellipse([width - 260, 80, width - 80, 260], fill=gold)
            for x in range(80, width, 220):
                draw.rectangle([x, int(height * 0.70), x + 26, int(height * 0.88)], fill="#6B3F1D")
                draw.ellipse([x - 52, int(height * 0.62), x + 78, int(height * 0.74)], fill="#2E8B57")
        else:
            draw.ellipse([width - 250, 90, width - 70, 270], fill=gold)

        self._draw_star(draw, 115, 120, 62, 28, gold)
        self._draw_bottle(draw, width // 2, int(height * 0.58), max(220, width // 5), cream, gold, deep_red)

        brand_font = self._font(56, bold=True)
        headline_size = 74 if height <= 1100 else 82
        body_size = 34 if height <= 1100 else 40
        headline_font = self._font(headline_size, bold=True)
        body_font = self._font(body_size)
        small_font = self._font(28)

        draw.text((200, 82), brief.brand.upper(), fill=white, font=brand_font)
        draw.text((86, int(height * 0.19)), ad_format.upper(), fill=cream, font=small_font)

        y = int(height * 0.25)
        for line in wrap(headline, width=18):
            draw.text((82, y), line, fill=white, font=headline_font)
            y += int(headline_size * 1.05)

        y += 18
        for line in wrap(body, width=38 if height <= 1100 else 30)[:4]:
            draw.text((86, y), line, fill=cream, font=body_font)
            y += int(body_size * 1.25)

        cta_text = brief.cta.upper()
        cta_y = height - 150
        draw.rounded_rectangle([82, cta_y, 82 + 320, cta_y + 78], radius=22, fill=gold)
        draw.text((112, cta_y + 21), cta_text, fill=deep_red, font=self._font(32, bold=True))

        legal = "Enjoy responsibly. Legal drinking age only."
        draw.text((82, height - 54), legal, fill=cream, font=self._font(24))

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        return f"data:image/png;base64,{encoded}"

    def _draw_bottle(self, draw, cx, cy, height, fill, gold, red):
        bottle_w = int(height * 0.22)
        bottle_h = height
        neck_w = int(bottle_w * 0.42)
        x0 = cx - bottle_w // 2
        y0 = cy - bottle_h // 2
        x1 = cx + bottle_w // 2
        y1 = cy + bottle_h // 2

        draw.rounded_rectangle([x0, y0 + 110, x1, y1], radius=40, fill="#4A2414")
        draw.rectangle([cx - neck_w // 2, y0 + 35, cx + neck_w // 2, y0 + 145], fill="#4A2414")
        draw.rectangle([cx - neck_w // 2 - 10, y0 + 25, cx + neck_w // 2 + 10, y0 + 50], fill=gold)
        draw.rounded_rectangle([x0 + 18, cy - 25, x1 - 18, cy + 110], radius=24, fill=fill)
        self._draw_star(draw, cx, cy + 16, 38, 17, red)
        draw.text((cx - 62, cy + 62), "ESTRELLA", fill=red, font=self._font(22, bold=True))

    def _draw_star(self, draw, cx, cy, outer, inner, fill):
        import math

        points = []
        for i in range(10):
            radius = outer if i % 2 == 0 else inner
            angle = math.pi / 2 + i * math.pi / 5
            points.append((cx + radius * math.cos(angle), cy - radius * math.sin(angle)))
        draw.polygon(points, fill=fill)

    def _font(self, size, bold=False):
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        ]

        for path in candidates:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue

        return ImageFont.load_default()
