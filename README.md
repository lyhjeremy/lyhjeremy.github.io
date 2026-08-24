# lyhjeremy.github.io

Portfolio landing page at [lyhjeremy.github.io](https://lyhjeremy.github.io/). Plain HTML and CSS, one build script, no third-party requests, no analytics.

## Editing

- `projects.json` holds the grouped project list (slug, display name, one-line summary) plus the `editorial` block: the lead project, four featured briefs, the fine-tuning series rows, the data stories and the numbers strip. Links are derived from the slug: code at `github.com/lyhjeremy/<slug>`, site at `lyhjeremy.github.io/<slug>/`, writeup at `.../<slug>/overview/`.
- `build.py` renders `index.html` from the JSON. Run `python3 build.py` after any edit, then commit both files.
- The footer (skills, about, contact) is inline in `build.py`.

## Images

`assets/shots/<slug>.png` are 1600px captures of each live project site, taken with headless Chrome:

    chrome --headless=new --window-size=1100,800 --force-device-scale-factor=2 --screenshot=assets/shots/<slug>.png https://lyhjeremy.github.io/<slug>/
    sips -Z 1600 assets/shots/<slug>.png

If a site will not render headless (Leeway's map, for example), use a screenshot from its writeup: the images under `https://lyhjeremy.github.io/<slug>/overview/` are real captures. Derived sizes used by the page: `assets/shots/med/` (16:10 tile images, JPEG) and `assets/shots/thumbs/` (144x96 index thumbs). The crop code is in the git history of this README's commit; regenerate with PIL if a source changes.

## Styling

The page follows apple.com conventions: system sans (SF on Apple devices, Helvetica/Arial elsewhere), black and near-black surfaces, one blue accent, rounded tiles, chevron links. Dark is the default for every visitor; light is opt-in through the nav toggle and remembered in `localStorage`. All colors are CSS custom properties on `:root` and `:root[data-theme="light"]` in `assets/site.css`.

This site is a deliberate exception to `DESIGN_STANDARDS.md` (decided 2026-08-23). Do not run `designcheck.py` against it.
