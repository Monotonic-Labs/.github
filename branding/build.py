"""Render the Monotonic Labs logo, org avatar, and profile banners (dark + light) to SVG and 2x PNG."""

from pathlib import Path

import resvg_py

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT.parent / "profile" / "assets"

# Brand gradient, bottom-left to top-right: orange, pink, purple, blue.
GRADIENT = [(0.0, "#FF9500"), (0.35, "#FF2D55"), (0.68, "#AF52DE"), (1.0, "#0A84FF")]

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "grid": "#e6edf3",
        "grid_opacity": "0.045",
        "text": "#e6edf3",
        "text_muted": "#8b949e",
    },
    "light": {
        "bg": "#ffffff",
        "grid": "#1f2328",
        "grid_opacity": "0.05",
        "text": "#1f2328",
        "text_muted": "#59636e",
    },
}

# The MT monogram on a 512 grid. M, the T crossbar, and the dot each sit one
# step higher than the last: a small monotonic sequence.
STROKE = 54
GLYPH_BOX = (104 - STROKE / 2, 100 - STROKE / 2, 440 + STROKE / 2, 372 + STROKE / 2)
GLYPH_SIZE = 330  # longest side of the glyph inside the 512 tile


def stops() -> str:
    return "".join(f'<stop offset="{offset}" stop-color="{color}"/>' for offset, color in GRADIENT)


def logo(prefix: str) -> str:
    """The full 512x512 logo tile. `prefix` keeps gradient ids unique when embedded."""
    x0, y0, x1, y1 = GLYPH_BOX
    k = GLYPH_SIZE / max(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    line = (f'fill="none" stroke="#ffffff" stroke-width="{STROKE}" '
            'stroke-linecap="round" stroke-linejoin="round"')
    return f"""\
  <defs>
    <linearGradient id="{prefix}Bg" x1="0" y1="1" x2="1" y2="0">{stops()}</linearGradient>
    <radialGradient id="{prefix}Glow" cx="0.25" cy="0.15" r="0.8">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.22"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="512" height="512" fill="url(#{prefix}Bg)"/>
  <rect width="512" height="512" fill="url(#{prefix}Glow)"/>
  <g transform="translate(256 256) scale({k:.4f}) translate({-cx} {-cy})">
    <path d="M104 372V220L170 306L236 220V372" {line}/>
    <path d="M276 160H380M328 160V312" {line}/>
    <circle cx="440" cy="100" r="{STROKE / 2}" fill="#ffffff"/>
  </g>
"""


def avatar() -> str:
    # Full bleed: GitHub rounds the corners itself and shows one avatar for both themes.
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">\n{logo("logo")}</svg>\n'


def banner(t: dict) -> str:
    return f"""\
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="320" viewBox="0 0 1280 320">
  <defs>
    <linearGradient id="accent" gradientUnits="userSpaceOnUse" x1="600" y1="0" x2="1220" y2="0">
      <stop offset="0" stop-color="#FF9500" stop-opacity="0"/>
      <stop offset="0.25" stop-color="#FF9500" stop-opacity="0.75"/>
      <stop offset="0.5" stop-color="#FF2D55"/>
      <stop offset="0.75" stop-color="#AF52DE"/>
      <stop offset="1" stop-color="#0A84FF"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{t['grid']}" stroke-opacity="{t['grid_opacity']}" stroke-width="1"/>
    </pattern>
    <linearGradient id="gridFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0.3" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#fff" stop-opacity="1"/>
    </linearGradient>
    <mask id="gridMask">
      <rect width="1280" height="320" fill="url(#gridFade)"/>
    </mask>
    <clipPath id="markClip">
      <rect x="96" y="112" width="96" height="96" rx="22"/>
    </clipPath>
  </defs>

  <rect width="1280" height="320" fill="{t['bg']}"/>
  <rect width="1280" height="320" fill="url(#grid)" mask="url(#gridMask)"/>

  <!-- Monotonic (non-decreasing) step function -->
  <path d="M600 272H700V252H770V238H830V204H900V192H960V156H1020V126H1080V102H1140V68H1220"
        fill="none" stroke="url(#accent)" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="900" cy="192" r="3.5" fill="#FF2D55"/>
  <circle cx="1020" cy="126" r="3.5" fill="#AF52DE"/>
  <circle cx="1140" cy="68" r="3.5" fill="#5E7BF0"/>
  <circle cx="1220" cy="68" r="6" fill="#0A84FF"/>

  <!-- Mark -->
  <g clip-path="url(#markClip)">
    <g transform="translate(96 112) scale({96 / 512})">
{logo("mark")}    </g>
  </g>

  <!-- Wordmark -->
  <text x="224" y="182" font-family="Inter, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="64" letter-spacing="-1.5" fill="{t['text']}">
    <tspan font-weight="700">Monotonic</tspan><tspan font-weight="300" fill="{t['text_muted']}" dx="18">Labs</tspan>
  </text>
</svg>
"""


def render(svg: str, name: str, zoom: float) -> None:
    (OUT / f"{name}.svg").write_text(svg)
    png = resvg_py.svg_to_bytes(svg_string=svg, font_dirs=[str(FONTS)], zoom=zoom)
    (OUT / f"{name}.png").write_bytes(bytes(png))
    print(f"wrote {name}.svg / {name}.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        render(banner(theme), f"banner-{name}", zoom=2.0)
    render(avatar(), "avatar", zoom=2.0)


if __name__ == "__main__":
    main()
