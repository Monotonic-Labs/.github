"""Render the Monotonic Labs org profile banners (dark + light) to SVG and 2x PNG."""

from pathlib import Path
from string import Template

import resvg_py

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT.parent / "profile" / "assets"

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "grid": "#e6edf3",
        "grid_opacity": "0.045",
        "accent_start": "#2dd4bf",
        "accent_end": "#60a5fa",
        "mark_bg": "#161b22",
        "mark_border": "#30363d",
        "text": "#e6edf3",
        "text_muted": "#8b949e",
    },
    "light": {
        "bg": "#ffffff",
        "grid": "#1f2328",
        "grid_opacity": "0.05",
        "accent_start": "#0d9488",
        "accent_end": "#2563eb",
        "mark_bg": "#f6f8fa",
        "mark_border": "#d1d9e0",
        "text": "#1f2328",
        "text_muted": "#59636e",
    },
}

BANNER = Template("""\
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="320" viewBox="0 0 1280 320">
  <defs>
    <linearGradient id="accent" gradientUnits="userSpaceOnUse" x1="600" y1="0" x2="1220" y2="0">
      <stop offset="0" stop-color="$accent_start" stop-opacity="0"/>
      <stop offset="0.35" stop-color="$accent_start" stop-opacity="0.55"/>
      <stop offset="1" stop-color="$accent_end"/>
    </linearGradient>
    <linearGradient id="markAccent" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="$accent_start"/>
      <stop offset="1" stop-color="$accent_end"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="$grid" stroke-opacity="$grid_opacity" stroke-width="1"/>
    </pattern>
    <linearGradient id="gridFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0.3" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#fff" stop-opacity="1"/>
    </linearGradient>
    <mask id="gridMask">
      <rect width="1280" height="320" fill="url(#gridFade)"/>
    </mask>
  </defs>

  <rect width="1280" height="320" fill="$bg"/>
  <rect width="1280" height="320" fill="url(#grid)" mask="url(#gridMask)"/>

  <!-- Monotonic (non-decreasing) step function -->
  <path d="M600 272H700V252H770V238H830V204H900V192H960V156H1020V126H1080V102H1140V68H1220"
        fill="none" stroke="url(#accent)" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
  <g fill="$accent_end">
    <circle cx="900" cy="192" r="3.5" fill-opacity="0.55"/>
    <circle cx="1020" cy="126" r="3.5" fill-opacity="0.75"/>
    <circle cx="1140" cy="68" r="3.5" fill-opacity="0.9"/>
    <circle cx="1220" cy="68" r="6"/>
  </g>

  <!-- Mark -->
  <rect x="96" y="112" width="96" height="96" rx="22" fill="$mark_bg" stroke="$mark_border" stroke-width="1.5"/>
  <path d="M116 184H138V160H158V136H174" fill="none" stroke="url(#markAccent)"
        stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="174" cy="136" r="5.5" fill="$accent_end"/>

  <!-- Wordmark -->
  <text x="224" y="182" font-family="Inter, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="64" letter-spacing="-1.5" fill="$text">
    <tspan font-weight="700">Monotonic</tspan><tspan font-weight="300" fill="$text_muted" dx="18">Labs</tspan>
  </text>
</svg>
""")


# Org avatar: the banner's mark scaled to a full-bleed square. GitHub rounds the
# corners itself and shows one avatar for both themes, so it uses a filled
# gradient that stands out on light and dark backgrounds alike.
AVATAR = Template("""\
<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="$accent_start"/>
      <stop offset="1" stop-color="$accent_end"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" fill="url(#bg)"/>
  <path d="M102 386H210V262H314V138H398" fill="none" stroke="#ffffff"
        stroke-width="40" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="398" cy="138" r="32" fill="#ffffff"/>
</svg>
""")


def render(svg: str, name: str, zoom: float) -> None:
    (OUT / f"{name}.svg").write_text(svg)
    png = resvg_py.svg_to_bytes(svg_string=svg, font_dirs=[str(FONTS)], zoom=zoom)
    (OUT / f"{name}.png").write_bytes(bytes(png))
    print(f"wrote {name}.svg / {name}.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, palette in THEMES.items():
        render(BANNER.substitute(palette), f"banner-{name}", zoom=2.0)
    render(AVATAR.substitute(THEMES["light"]), "avatar", zoom=2.0)


if __name__ == "__main__":
    main()
