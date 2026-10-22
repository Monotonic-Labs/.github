"""Render the Monotonic Labs logo, org avatar, and profile banners (dark + light) to SVG and 2x PNG."""

from pathlib import Path

import resvg_py

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT.parent / "profile" / "assets"
SOCIAL = ROOT / "social"

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
    """The full 512x512 logo tile: gradient lettering on near-black, with a halo
    ring that marks the dot as a plotted point.

    `prefix` keeps gradient ids unique when embedded.
    """
    x0, y0, x1, y1 = GLYPH_BOX
    k = GLYPH_SIZE / max(x1 - x0, y1 - y0)
    paint = f"url(#{prefix}Ink)"
    line = (f'fill="none" stroke="{paint}" stroke-width="{STROKE}" '
            'stroke-linecap="round" stroke-linejoin="round"')
    # Halo sized in tile pixels (14px gap, 5px ring), converted to glyph space.
    halo_r = STROKE / 2 + 14 / k
    # Center on the visible extent, which the halo pushes up and to the right.
    halo_outer = halo_r + 2.5 / k
    cx = (x0 + max(x1, 440 + halo_outer)) / 2
    cy = (min(y0, 100 - halo_outer) + y1) / 2
    return f"""\
  <defs>
    <linearGradient id="{prefix}Ink" gradientUnits="userSpaceOnUse" x1="{x0}" y1="{y1}" x2="{x1}" y2="{y0}">{stops()}</linearGradient>
  </defs>
  <rect width="512" height="512" fill="#0b0b10"/>
  <g transform="translate(256 256) scale({k:.4f}) translate({-cx} {-cy})">
    <path d="M104 372V220L170 306L236 220V372" {line}/>
    <path d="M276 160H380M328 160V312" {line}/>
    <circle cx="440" cy="100" r="{STROKE / 2}" fill="{paint}"/>
    <circle cx="440" cy="100" r="{halo_r:.2f}" fill="none" stroke="#0A84FF" stroke-opacity="0.55" stroke-width="{5 / k:.2f}"/>
  </g>
"""


def avatar() -> str:
    # Full bleed: GitHub rounds the corners itself and shows one avatar for both themes.
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">\n{logo("logo")}</svg>\n'


def banner(t: dict, width: int = 1280, height: int = 320) -> str:
    """The 1280x320 banner design. A different canvas size scales the design to
    the full width and centers it vertically, with the background and grid
    filling the whole canvas."""
    s = width / 1280
    oy = (height - 320 * s) / 2
    cell = 40 * s
    return f"""\
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="accent" gradientUnits="userSpaceOnUse" x1="600" y1="0" x2="1220" y2="0">
      <stop offset="0" stop-color="#FF9500" stop-opacity="0"/>
      <stop offset="0.25" stop-color="#FF9500" stop-opacity="0.75"/>
      <stop offset="0.5" stop-color="#FF2D55"/>
      <stop offset="0.75" stop-color="#AF52DE"/>
      <stop offset="1" stop-color="#0A84FF"/>
    </linearGradient>
    <pattern id="grid" width="{cell:g}" height="{cell:g}" patternUnits="userSpaceOnUse">
      <path d="M{cell:g} 0H0V{cell:g}" fill="none" stroke="{t['grid']}" stroke-opacity="{t['grid_opacity']}" stroke-width="{s:g}"/>
    </pattern>
    <linearGradient id="gridFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0.3" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#fff" stop-opacity="1"/>
    </linearGradient>
    <mask id="gridMask">
      <rect width="{width}" height="{height}" fill="url(#gridFade)"/>
    </mask>
  </defs>

  <rect width="{width}" height="{height}" fill="{t['bg']}"/>
  <rect width="{width}" height="{height}" fill="url(#grid)" mask="url(#gridMask)"/>
  <g transform="translate(0 {oy:g}) scale({s:g})">

  <!-- Monotonic (non-decreasing) step function -->
  <path d="M600 272H700V252H770V238H830V204H900V192H960V156H1020V126H1080V102H1140V68H1220"
        fill="none" stroke="url(#accent)" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="900" cy="192" r="3.5" fill="#FF2D55"/>
  <circle cx="1020" cy="126" r="3.5" fill="#AF52DE"/>
  <circle cx="1140" cy="68" r="3.5" fill="#5E7BF0"/>
  <circle cx="1220" cy="68" r="6" fill="#0A84FF"/>

  <!-- Wordmark -->
  <text x="96" y="182" font-family="Inter, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="64" letter-spacing="-1.5" fill="{t['text']}">
    <tspan font-weight="700">Monotonic</tspan><tspan font-weight="300" fill="{t['text_muted']}" dx="18">Labs</tspan>
  </text>
  </g>
</svg>
"""


def render(svg: str, name: str, zoom: float, out: Path = OUT) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.svg").write_text(svg)
    png = resvg_py.svg_to_bytes(svg_string=svg, font_dirs=[str(FONTS)], zoom=zoom)
    (out / f"{name}.png").write_bytes(bytes(png))
    print(f"wrote {name}.svg / {name}.png")


def main() -> None:
    for name, theme in THEMES.items():
        render(banner(theme), f"banner-{name}", zoom=2.0)
        # X (Twitter) header: exactly 1500x500. The profile picture overlaps the
        # bottom-left corner, which the banner layout already leaves clear.
        render(banner(theme, 1500, 500), f"x-header-{name}", zoom=1.0, out=SOCIAL)
    render(avatar(), "avatar", zoom=2.0)


if __name__ == "__main__":
    main()
