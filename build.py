#!/usr/bin/env python3
"""Render index.html from projects.json. Run after editing the JSON."""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
data = json.loads((ROOT / "projects.json").read_text())
ed = data["editorial"]
GH = "https://github.com/lyhjeremy/"
PAGES = "https://lyhjeremy.github.io/"
e = html.escape
MED = "assets/shots/med/"

def links(slug, code=False):
    out = [f'<a class="chev" href="{PAGES}{slug}/">Open the site</a>',
           f'<a class="chev" href="{PAGES}{slug}/overview/">Read the writeup</a>']
    if code:
        out.append(f'<a class="chev" href="{GH}{slug}">View the code</a>')
    return "".join(out)

def tile(slug, eyebrow, headline, text, *, lead=False, stat=None, img=True, code=False, tone=""):
    cls = ("tile lead " if lead else "tile ") + tone
    h = f'<h3>{e(headline)}</h3>'
    st = f'<div class="stat">{e(stat)}</div>' if stat else ""
    media = (f'<div class="media"><a href="{PAGES}{slug}/"><img src="{MED}{slug}.jpg" '
             f'alt="{e(headline)}" loading="lazy"></a></div>') if img else ""
    return (f'<article class="{cls}"><div class="copy">'
            f'<p class="eyebrow">{e(eyebrow)}</p>{st}{h}<p>{e(text)}</p>'
            f'<div class="links">{links(slug, code)}</div></div>{media}</article>')

# featured
L = ed["lead"]
featured = tile(L["slug"], "SkillCompass", L["headline"], L["deck"], lead=True, code=True, tone="dark")
TONES = {"leeway": "blue", "world-record-half-lives": "green", "marathon-heat-tax": "orange",
         "cantonese-learner-v2": "pink", "cellar-scanner": "pink", "menu-decoder": "orange",
         "receipt-auditor": "green", "race-day-copilot": "blue",
         "marathon-pacing-decay": "purple", "love-island-lexical-analysis": "teal"}
briefs = "".join(
    tile(b["slug"], b["kicker"].split("/")[-1].strip().capitalize(), b["headline"], b["text"], tone=TONES[b["slug"]])
    for b in ed["briefs"])

# fine-tuning series
S = ed["series"]
series = "".join(
    tile(r["slug"], r["name"], r["short"], r["note"][0].upper() + r["note"][1:] + ".", stat=r["stat"], tone=TONES[r["slug"]])
    for r in S["rows"])

# data stories + numbers
ST = ed["stories"]
m = ST["main"]
stories_main = tile(m["slug"], "Wine Score Inflation", m["headline"], m["text"], lead=True, tone="dark-purple")
NAMES = {slug: name for sec in data["sections"] for slug, name, _ in sec["projects"]}
stories_side = "".join(
    tile(x["slug"], NAMES[x["slug"]], x["headline"], x["text"], tone=TONES[x["slug"]]) for x in ST["side"])
STAT_TONES = ["blue", "green", "orange", "purple", "pink"]
stats = "".join(
    f'<a class="{STAT_TONES[i % 5]}" href="{PAGES}{t["slug"]}/"><span class="v">{e(t["stat"])}</span>'
    f'<span class="l">{e(t["label"])}</span></a>' for i, t in enumerate(ed["numbers"]["tiles"]))

# index
def thumb(slug):
    p = ROOT / "assets/shots/thumbs" / f"{slug}.png"
    return f'<img src="assets/shots/thumbs/{slug}.png" alt="" loading="lazy" width="56" height="38">' if p.exists() else ""
GROUP_TONES = {"featured": "blue", "applied-ai": "orange", "genai": "purple", "running": "green",
               "language": "pink", "consumer": "teal", "tools": "blue"}
groups = "".join(
    f'<div class="group {GROUP_TONES.get(s["id"], "")}"><h3>{e(s["title"])} <span>({len(s["projects"])})</span></h3><ul>'
    + "".join(
        f'<li>{thumb(slug)}<span class="t"><a href="{GH}{slug}">{e(name)}</a></span>'
        f'<span class="go"><a href="{PAGES}{slug}/">Site</a><a href="{PAGES}{slug}/overview/">Writeup</a></span></li>'
        for slug, name, _ in s["projects"])
    + '</ul></div>' for s in data["sections"])
n = sum(len(s["projects"]) for s in data["sections"])

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Jeremy Lee</title>
<meta name="description" content="Data scientist and UCLA Anderson MSBA. {n} live projects across generative AI, statistical modeling and machine learning.">
<link rel="stylesheet" href="assets/site.css">
<script>
try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t);}}catch(err){{}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<nav class="nav" aria-label="Page">
  <div class="wrap">
    <a class="brand" href="{PAGES}">Jeremy Lee</a>
    <a href="#featured">Featured</a>
    <a href="#series">Fine-tuning</a>
    <a href="#stories">Data stories</a>
    <a href="#index">All projects</a>
    <a href="https://github.com/lyhjeremy">GitHub</a>
    <button type="button" id="theme-toggle" hidden aria-pressed="false">Dark</button>
  </div>
</nav>

<main id="main">
<header class="hero wrap">
  <h1>Jeremy Lee</h1>
  <p class="sub">Data scientist. UCLA Anderson MSBA.<br><b>{n} projects, all live.</b></p>
  <div class="cta">
    <a class="chev" href="#featured">See the work</a>
    <a class="chev" href="https://github.com/lyhjeremy">github.com/lyhjeremy</a>
  </div>
</header>

<section class="section wrap" id="featured">
  <div class="section-head"><h2>Featured.</h2><p>Five projects that show the range: a full-stack product, a decision tool, two data stories and a language app.</p></div>
  {featured}
  <div class="grid-2">{briefs}</div>
</section>

<div class="band"><section class="section wrap" id="series">
  <div class="section-head"><h2>The fine-tuning series.</h2><p>{e(S["intro"])}</p></div>
  <div class="grid-2">{series}</div>
</section></div>

<section class="section wrap" id="stories">
  <div class="section-head"><h2>Data stories.</h2><p>{e(ST["intro"])}</p></div>
  {stories_main}
  <div class="grid-2">{stories_side}</div>
  <div class="stats">{stats}</div>
</section>

<div class="band" style="margin-bottom:0"><section class="section wrap" id="index">
  <div class="section-head"><h2>All {n} projects.</h2><p>Grouped the way I file them. The name opens the code.</p></div>
  <div class="index">{groups}</div>
</section></div>
</main>

<footer class="footer">
  <div class="wrap">
    <div class="cols">
      <div><h4>Modeling</h4><ul><li>scikit-learn, PyTorch, XGBoost</li><li>Regression, classification, clustering</li><li>Time series, neural networks</li><li>Causal inference, survival analysis</li><li>A/B testing</li></ul></div>
      <div><h4>Optimization</h4><ul><li>Gurobi</li><li>LP / IP / QP, non-convex</li><li>Branch-and-bound, LP duality</li><li>Gradient descent</li><li>Simulation, Monte Carlo</li></ul></div>
      <div><h4>GenAI and agents</h4><ul><li>LLM prompting, RAG, embeddings</li><li>Vector databases, fine-tuning</li><li>OpenAI and Anthropic APIs</li><li>LangChain, LangGraph</li><li>Tool use, retrieval pipelines</li></ul></div>
      <div><h4>Data and deployment</h4><ul><li>Python, R, SQL</li><li>Snowflake, Airflow, Spark</li><li>Tableau, Power BI</li><li>Git, GitHub Pages, Streamlit</li></ul></div>
    </div>
    <div class="about" style="padding:20px 0;border-bottom:1px solid var(--line)">
      <p>Co-founder and Chief Strategy Officer at Casual Ace Learning Centre: grew enrollment 5.2x to over 1,000 students across six centers. MSBA, UCLA Anderson; BBA, University of Hong Kong. 14 marathons, Berlin personal best 2:48. WSET Level 3 in wine.</p>
      <p><a href="https://www.linkedin.com/in/jeremylyh/">LinkedIn</a> · <a href="mailto:lyhjeremy@gmail.com">Email</a> · <a href="https://github.com/lyhjeremy">GitHub</a> · Terminal version: <code>npx lyhjeremy</code></p>
    </div>
    <div class="legal">
      <span>Screenshots are captures of the live sites. No analytics, no third-party requests.</span>
      <span><a href="{GH}lyhjeremy.github.io">Source for this page</a></span>
    </div>
  </div>
</footer>

<script>
(function(){{
  var root=document.documentElement,btn=document.getElementById("theme-toggle");
  if(!btn)return;
  function current(){{return root.getAttribute("data-theme")==="dark"?"dark":"light";}}
  function render(){{var dark=current()==="dark";btn.textContent=dark?"Light":"Dark";btn.setAttribute("aria-pressed",dark?"true":"false");}}
  btn.hidden=false;render();
  btn.addEventListener("click",function(){{
    var next=current()==="light"?"dark":"light";
    root.setAttribute("data-theme",next);
    try{{localStorage.setItem("theme",next);}}catch(err){{}}
    render();
  }});
}})();
</script>
</body>
</html>
'''
(ROOT / "index.html").write_text(page)
print(f"wrote index.html, {n} projects")
