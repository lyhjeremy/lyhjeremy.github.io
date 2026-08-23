# lyhjeremy.github.io

Portfolio landing page at [lyhjeremy.github.io](https://lyhjeremy.github.io/). Plain HTML and CSS, no build step beyond one script, no third-party requests.

## Editing

- `projects.json` holds the grouped project list (slug, display name, one-line method summary). Links are derived from the slug: code at `github.com/lyhjeremy/<slug>`, live at `lyhjeremy.github.io/<slug>/`, writeup at `.../<slug>/overview/`.
- `build.py` renders `index.html` from the JSON. Run `python3 build.py` after any edit, then commit both files.
- The bio, skills and contact sections are inline in `build.py`.

## Theme

`assets/ledger/ledger.css` is the unmodified Ledger house stylesheet. `assets/site.css` loads after it and sets the dark palette on bare `:root`, so every visitor sees dark regardless of OS setting. Light is opt-in through `[data-theme="light"]`, toggled by the button in the header and remembered in `localStorage`. This deliberately inverts rule 5 of DESIGN_STANDARDS.md section 2 for this one site; the color values themselves are the measured Ledger sets.

## Check

`python3 ../../_ai-projects-tooling/ledger/designcheck.py .` from this directory runs the house design checker.
