#!/usr/bin/env python3
"""Generate the project card SVGs used in README.md (assets/cards/*.svg).

Edit PROJECTS below, then run: python3 scripts/gen_project_cards.py
"""
import os
import textwrap
from xml.sax.saxutils import escape

PROJECTS = [
    ("dijkstra", "Dijkstra Visualizer", "Simulation", "ALGORITHMIC_GRAPH",
     ["Python", "Manim", "NumPy"],
     "Mathematical visualization suite animating pathfinding convergence bounds and visual state tables using Manim.",
     "https://github.com/Anubisx404/Dijkstra-Algorithm-Visualization"),
    ("fourier", "Fourier Transform Suite", "Physics", "COMPUTATIONAL_PHYSICS",
     ["C++20", "Zig", "x86-64 MASM"],
     "High-performance decimation-in-time radix-2 FFT suite comparing native butterfly computations across C++20, Zig, and x86-64 Assembly.",
     "https://github.com/Anubisx404/Fourier-Transform"),
    ("fleetpulse", "FleetPulse Transit", "Full-Stack", "DISTRIBUTED_TELEMETRY",
     [".NET 10", "Svelte 5", "PostgreSQL"],
     "Full-scale telemetry aggregator tracking transit assets, maintenance, and live operational alerts through PostgreSQL and SignalR.",
     None),
    ("fluxsync", "FluxSync Energy", "Cross-Platform", "SIMULATED_LOGISTICS",
     ["Flutter", ".NET 10", "TimescaleDB"],
     "Energy flow tracker managing time-series telemetry streams through TimescaleDB and Redis caching structures.",
     None),
    ("grace-boutique", "Grace Boutique", "Full-Stack", "SECURE_ECOMMERCE",
     [".NET 10", "SvelteKit", "Flutter", "GraphQL"],
     "Microservices network featuring vector semantic search pipelines and secure try-on system integration.",
     "https://github.com/Anubisx404/Grace_Boutique"),
    ("svelterender", "SvelteRender SSR", "Backend", "ISOLATED_SANDBOX",
     [".NET 10", "Svelte Compiler", "Bun"],
     "High-speed SSR engine executing Svelte compilations inside isolated Bun-powered execution environments.",
     None),
    ("pageui", "Page.Ui Engine", "Backend", "COMPILATION_SANDBOX",
     [".NET 10", "GraphQL", "SignalR", "Docker"],
     "Active interface compiler running isolated compilation networks for generated reactive elements.",
     "https://github.com/page-ui/Backend_Department"),
    ("mirox", "Mirox Editor", "Desktop", "CROSS_PLATFORM_UI",
     [".NET 10", "Avalonia UI", "ReactiveUI"],
     "Cross-platform Markdown editor and viewer structured around MVVM, ReactiveUI, and Markdig rendering.",
     "https://github.com/Anubisx404/Mirox"),
    ("extent", "Extent", "Developer Tooling", "OBSERVABILITY_BOOTSTRAP",
     ["Go", "OpenTelemetry", "Docker", "Grafana"],
     "Repo-aware CLI that generates and verifies reviewable OpenTelemetry instrumentation and a local LGTM observability stack.",
     "https://github.com/Anubisx404/Extent"),
    ("eduscan", "EduScan Pro", "Education", "AI_LEARNING",
     ["Flutter", "Node.js", "OCR", "GraphQL"],
     "Cross-platform study scanner and organizer with OCR, flashcards, adaptive tutoring, and collaborative learning workflows.",
     "https://github.com/MuonByte/Education_Manager"),
    ("virtual-try-on", "Virtual Try-On Platform", "AI Platform", "VIRTUAL_TRY_ON",
     [".NET 10", "Flutter", "MinIO", "BFL FLUX VTO"],
     "Provider-neutral virtual try-on service with secure object storage, background workers, and production-oriented deployment controls.",
     None),
]

MONO = "'Fira Code', 'Cascadia Code', Consolas, 'Courier New', monospace"
SANS = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Space Grotesk', sans-serif"
W, H = 480, 290
PAD = 32
MONO_CHAR = 0.6  # approx monospace glyph width as a fraction of font size

# Small equation per card, in the spirit of the header banner's corner formulas.
FORMULAS = {
    "dijkstra": "d(v) = min(d(v), d(u) + w(u,v))",
    "fourier": "X_k = Σ x_n·e^(-2πikn/N)",
    "fleetpulse": "Δt = t_rx − t_tx",
    "fluxsync": "P(t) = V(t)·I(t)",
    "grace-boutique": "cos θ = (a·b) / (‖a‖‖b‖)",
    "svelterender": "T_ssr = T_compile + T_render",
    "pageui": "f: AST → DOM",
    "mirox": "V = f(VM(M))",
    "extent": "span = ⟨trace_id, t₀, t₁⟩",
    "eduscan": "P(recall) = e^(−t/S)",
    "virtual-try-on": "I_out = G(I_person, I_garment)",
}


def emblem(cx, cy):
    """Rotating orbital globe with a pulse ring, mirroring the header's right-hand globe."""
    return f"""  <g>
    <circle cx="{cx}" cy="{cy}" r="52" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
    <circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1" stroke-dasharray="6,3"/>
    <circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="rgba(255,255,255,0.35)" stroke-width="1" stroke-dasharray="2,2"/>
    <circle cx="{cx}" cy="{cy}" r="0" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="1">
      <animate attributeName="r" values="0;52" dur="6s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values="0.6;0" dur="6s" repeatCount="indefinite"/>
    </circle>
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="30s" repeatCount="indefinite"/>
      <ellipse cx="{cx}" cy="{cy}" rx="40" ry="13" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="0.8"/>
      <ellipse cx="{cx}" cy="{cy}" rx="40" ry="26" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="0.8" stroke-dasharray="4,4"/>
      <ellipse cx="{cx}" cy="{cy}" rx="13" ry="40" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="0.8"/>
      <ellipse cx="{cx}" cy="{cy}" rx="26" ry="40" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="0.8" stroke-dasharray="4,4"/>
      <line x1="{cx - 48}" y1="{cy}" x2="{cx + 48}" y2="{cy}" stroke="rgba(255,255,255,0.2)" stroke-width="0.6"/>
      <line x1="{cx}" y1="{cy - 48}" x2="{cx}" y2="{cy + 48}" stroke="rgba(255,255,255,0.2)" stroke-width="0.6"/>
    </g>
    <path d="M {cx - 5} {cy} L {cx + 5} {cy} M {cx} {cy - 5} L {cx} {cy + 5}" stroke="#ffffff" stroke-width="1" filter="url(#crt-glow)"/>
  </g>"""


def card(index, slug, name, domain, tag, stack, desc, url):
    status = "[STATUS: PUBLIC ↗]" if url else "[STATUS: PRIVATE]"
    lines = textwrap.wrap(desc, 56)
    title_size = min(24, round(290 / (len(name) * 0.6), 1))  # keep long titles clear of the globe
    desc_svg = "\n".join(
        f'    <tspan x="{PAD}" dy="{0 if i == 0 else 19}">{escape(l)}</tspan>'
        for i, l in enumerate(lines)
    )

    chips, x = [], PAD
    for tech in stack:
        w = len(tech) * 11 * MONO_CHAR + 16
        chips.append(
            f'  <rect x="{x:.1f}" y="{H - 74}" width="{w:.1f}" height="22" '
            f'fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.3)" stroke-width="0.8"/>\n'
            f'  <text x="{x + w / 2:.1f}" y="{H - 59}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="11" fill="rgba(255,255,255,0.85)">{escape(tech)}</text>'
        )
        x += w + 8

    L, T, R, B = 16, 16, W - 16, H - 16  # inner frame
    ticks = " ".join(
        f"M {px - 4} {py} L {px + 4} {py} M {px} {py - 4} L {px} {py + 4}"
        for px in (L, R) for py in (T, B)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="0.5"/>
      <circle cx="0" cy="0" r="1" fill="rgba(255,255,255,0.15)"/>
    </pattern>
    <filter id="crt-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="1.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="#000000"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <path d="M {L} {T} L {R} {T} L {R} {B} L {L} {B} Z" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <path d="{ticks}" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>

  <line x1="{L + 4}" y1="{T}" x2="{R - 4}" y2="{T}" stroke="rgba(255,255,255,0.25)" stroke-width="1">
    <animate attributeName="y1" values="{T};{B};{T}" dur="10s" repeatCount="indefinite"/>
    <animate attributeName="y2" values="{T};{B};{T}" dur="10s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values="0.05;0.4;0.05" dur="10s" repeatCount="indefinite"/>
  </line>

{emblem(W - 84, 84)}

  <text x="{PAD}" y="44" font-family="{MONO}" font-size="10" fill="rgba(255,255,255,0.35)">[0x{index:02X} // {escape(domain.upper())}]</text>
  <text x="{PAD}" y="80" font-family="{SANS}" font-size="{title_size}" font-weight="900" fill="#ffffff" letter-spacing="1" filter="url(#crt-glow)">{escape(name)}</text>
  <text x="{PAD}" y="102" font-family="{MONO}" font-size="11" font-weight="bold" fill="rgba(255,255,255,0.55)" letter-spacing="2">{escape(tag)}</text>
  <line x1="{PAD}" y1="118" x2="{W - PAD}" y2="118" stroke="rgba(255,255,255,0.2)" stroke-width="1" stroke-dasharray="3,6"/>

  <text x="{PAD}" y="142" font-family="{SANS}" font-size="13.5" fill="rgba(255,255,255,0.75)">
{desc_svg}
  </text>

{chr(10).join(chips)}

  <g font-family="{MONO}" font-size="10" fill="rgba(255,255,255,0.25)">
    <text x="{PAD}" y="{H - 28}">{escape(FORMULAS.get(slug, ""))}</text>
    <text x="{W - PAD}" y="{H - 28}" text-anchor="end">{status}</text>
  </g>
</svg>
"""


def main():
    out = os.path.join(os.path.dirname(__file__), "..", "assets", "cards")
    os.makedirs(out, exist_ok=True)
    for i, (slug, *rest) in enumerate(PROJECTS, 1):
        with open(os.path.join(out, f"{slug}.svg"), "w", encoding="utf-8") as f:
            f.write(card(i, slug, *rest))


if __name__ == "__main__":
    main()
