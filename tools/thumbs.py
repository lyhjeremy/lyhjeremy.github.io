#!/usr/bin/env python3
"""Make the card thumbnail (and optionally the wide-card image) for one project.

Usage:
  python3 tools/thumbs.py <slug> <figure-url-or-local-path> [--wide]

The image is padded to 16:10 (never cropped) on a background sampled from its
corners, then written to assets/shots/card/<slug>.jpg at 720x450; --wide also
writes assets/shots/med/<slug>.jpg at 1280x800 for the two wide cards.

Pick the figure by hand from the project's writeup at
https://lyhjeremy.github.io/<slug>/overview/ : the most interesting chart, app
screenshot or diagram, the way a good video thumbnail works. If a project has
no writeup figures, capture its live page instead:

  chrome --headless=new --window-size=1100,800 --force-device-scale-factor=2 \
      --screenshot=/tmp/<slug>.png https://lyhjeremy.github.io/<slug>/
"""
import io, pathlib, sys, urllib.request
from PIL import Image

def corner_color(im):
    px = im.load()
    cs = [px[2,2], px[im.width-3,2], px[2,im.height-3], px[im.width-3,im.height-3]]
    return tuple(sum(c[i] for c in cs)//4 for i in range(3))

def to_16x10(im, out_w):
    w, h = im.size
    bg = corner_color(im)
    if w/h > 1.6:
        H = int(w/1.6); canvas = Image.new("RGB", (w, H), bg); canvas.paste(im, (0, (H-h)//2))
    else:
        W = int(h*1.6); canvas = Image.new("RGB", (W, h), bg); canvas.paste(im, ((W-w)//2, 0))
    return canvas.resize((out_w, out_w*10//16), Image.LANCZOS)

def main():
    slug, src = sys.argv[1], sys.argv[2]
    wide = "--wide" in sys.argv
    root = pathlib.Path(__file__).resolve().parent.parent
    data = urllib.request.urlopen(src).read() if src.startswith("http") else pathlib.Path(src).read_bytes()
    im = Image.open(io.BytesIO(data)).convert("RGB")
    out = root/"assets/shots/card"/f"{slug}.jpg"
    to_16x10(im, 720).save(out, quality=84, optimize=True); print("wrote", out)
    if wide:
        out = root/"assets/shots/med"/f"{slug}.jpg"
        to_16x10(im, 1280).save(out, quality=84, optimize=True); print("wrote", out)

if __name__ == "__main__":
    main()
