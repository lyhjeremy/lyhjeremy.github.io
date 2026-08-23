# lyhjeremy.github.io

Portfolio landing page at [lyhjeremy.github.io](https://lyhjeremy.github.io/). Plain HTML and CSS, no build step beyond one script, no third-party requests.

## Editing

- `projects.json` holds the grouped project list (slug, display name, one-line summary) plus the `editorial` block: the lead story, the briefs rail and the fine-tuning series rows, each with its headline and deck. Links are derived from the slug: code at `github.com/lyhjeremy/<slug>`, live at `lyhjeremy.github.io/<slug>/`, writeup at `.../<slug>/overview/`.
- `build.py` renders `index.html` from the JSON. Run `python3 build.py` after any edit, then commit both files.
- The colophon (skills, about, contact) is inline in `build.py`.
- `assets/shots/` holds screenshots captured from the live project sites with headless Chrome; retake one with:
  `chrome --headless=new --window-size=1100,800 --force-device-scale-factor=2 --screenshot=assets/shots/<slug>.png https://lyhjeremy.github.io/<slug>/` then `sips -Z 1600 assets/shots/<slug>.png`. If a site will not render headless (Leeway's map, for example), take a screenshot from its writeup instead: the images under `https://lyhjeremy.github.io/<slug>/overview/` are real captures.

## Theme

`assets/ledger/ledger.css` is the unmodified Ledger house stylesheet. `assets/site.css` loads after it and sets the dark palette on bare `:root`, so every visitor sees dark regardless of OS setting. Light is opt-in through `[data-theme="light"]`, toggled by the button in the header and remembered in `localStorage`.

Three sanctioned bends from DESIGN_STANDARDS.md apply to this one site, agreed 2026-08-23 and marked with `ledger-allow` comments in the CSS: dark-first `:root` (inverting section 2 rule 5), 120ms color-only transitions on interactive states, and a 2px corner radius on panels and controls. The palette, fonts and everything else follow the standard. Section accents: oxide marks generative AI and agents, pine marks statistics and analysis.

## Check

`python3 ../../_ai-projects-tooling/ledger/designcheck.py .` from this directory runs the house design checker.
