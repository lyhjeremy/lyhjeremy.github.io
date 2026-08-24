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

If a site will not render headless (Leeway's map, for example), use a screenshot from its writeup: the images under `https://lyhjeremy.github.io/<slug>/overview/` are real captures. Card thumbnails in `assets/shots/card/` (720px 16:10) are the most interesting figure from each project's writeup (chart, UI shot or diagram), padded to 16:10 with a background sampled from the image corners, never cropped; `assets/shots/med/` holds 1280px versions for the two wide cards. Candidate figures come from the images under `https://lyhjeremy.github.io/<slug>/overview/`. The two projects whose writeups have no figures (epub-to-audiobook, podcastify) use a crop of their live page instead. The crop code is in the git history of this README's commit; regenerate with PIL if a source changes.

## Styling

A compact, image-first card grid in apple.com idiom: system sans (SF on Apple devices, Helvetica/Arial elsewhere), white and `#f5f5f7` bands, rounded cards that lead with the project screenshot, chevron links. Cards carry one of six tints (blue, green, orange, purple, pink, teal) mapped to project categories in `build.py` (`TONES`, `STAT_TONES`, `GROUP_TONES`); the lead tiles use a dark gradient. Light is the default for every visitor; dark is opt-in through the nav toggle and remembered in `localStorage`. All colors are CSS custom properties on `:root` and `:root[data-theme="dark"]` in `assets/site.css`.

This site is a deliberate exception to `DESIGN_STANDARDS.md` (decided 2026-08-23). Do not run `designcheck.py` against it.
