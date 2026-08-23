#!/usr/bin/env python3
"""Render index.html from projects.json. Run after editing the JSON."""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
data = json.loads((ROOT / "projects.json").read_text())
ed = data["editorial"]
GH = "https://github.com/lyhjeremy/"
PAGES = "https://lyhjeremy.github.io/"
e = html.escape

ACCENT = {"featured": "ink", "applied-ai": "oxide", "genai": "oxide",
          "running": "pine", "language": "pine", "consumer": "pine", "tools": "ink"}

def links(slug, code=True):
    out = [f'<a href="{PAGES}{slug}/">Live</a>', f'<a href="{PAGES}{slug}/overview/">Writeup</a>']
    if code:
        out.append(f'<a href="{GH}{slug}">Code</a>')
    return "".join(out)

# lead story
L = ed["lead"]
lead = f'''<article class="lead {L["accent"]}">
<figure><img src="{L["figure"]}" alt="{e(L["figcap"])}" width="1600" height="1170">
<figcaption>{e(L["figcap"])}</figcaption></figure>
<p class="kicker">{e(L["kicker"])}</p>
<h2><a href="{PAGES}{L["slug"]}/">{e(L["headline"])}</a></h2>
<p class="deck">{e(L["deck"])}</p>
<p class="story-links">{links(L["slug"])}</p>
</article>'''

briefs = "".join(
    f'''<article class="brief {b["accent"]}">
<p class="kicker">{e(b["kicker"])}</p>
<h3><a href="{PAGES}{b["slug"]}/">{e(b["headline"])}</a></h3>
<p>{e(b["text"])}</p>
<p class="story-links">{links(b["slug"], code=False)}</p>
</article>''' for b in ed["briefs"])

# fine-tuning series
S = ed["series"]
series_rows = "".join(
    f'<tr><td><strong><a href="{GH}{r["slug"]}">{e(r["name"])}</a></strong></td>'
    f'<td class="stat">{e(r["stat"])}</td><td>{e(r["note"])}</td>'
    f'<td class="links">{links(r["slug"], code=False)}</td></tr>'
    for r in S["rows"])
series = f'''<section class="band oxide" id="series">
<div class="band-head"><span class="n">II</span><h2>{e(S["title"])}</h2></div>
<p class="band-intro">{e(S["intro"])}</p>
<div class="series-table-wrap"><table>
<thead><tr><th>Project</th><th>Result</th><th>What the number is</th><th>Links</th></tr></thead>
<tbody>{series_rows}</tbody></table></div>
</section>'''

# full index of all projects
groups = []
for s in data["sections"]:
    cls = ACCENT.get(s["id"], "ink")
    items = "".join(
        f'<li><span class="t"><a href="{GH}{slug}">{e(name)}</a></span>'
        f'<span class="go">{links(slug, code=False)}</span></li>'
        for slug, name, _ in s["projects"])
    groups.append(f'<div class="group {cls}"><h3>{e(s["title"])} '
                  f'<span class="count">({len(s["projects"])})</span></h3><ul>{items}</ul></div>')
n = sum(len(s["projects"]) for s in data["sections"])
index = f'''<section class="band ink" id="index">
<div class="band-head"><span class="n">III</span><h2>The full index</h2></div>
<p class="band-intro">All {n} projects. Every one is live; every name links to its code, Live opens the project, Writeup opens the long-form page on how it works and what it found.</p>
<div class="index">{"".join(groups)}</div>
</section>'''

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Jeremy Lee</title>
<meta name="description" content="Data scientist and UCLA Anderson MSBA. {n} live projects across generative AI, statistical modeling and machine learning.">
<link rel="stylesheet" href="assets/ledger/ledger.css">
<link rel="stylesheet" href="assets/site.css">
<script>
/* Apply a saved theme before first paint. Default is dark; nothing is stored until the
   visitor presses the toggle. */
try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t);}}catch(err){{}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="wrap">

<div class="topbar">
  <span class="left">Applied analytics and machine learning</span>
  <nav aria-label="Page">
    <a href="#series">Series</a>
    <a href="#index">Index</a>
    <a href="#colophon">About</a>
    <a class="gh-link" href="https://github.com/lyhjeremy">github.com/lyhjeremy</a>
    <button class="btn theme-toggle" type="button" id="theme-toggle" hidden aria-pressed="false">Light mode</button>
  </nav>
</div>

<header class="nameplate">
  <h1>Jeremy Lee</h1>
  <p class="dateline">Data scientist · UCLA Anderson MSBA · formerly Chief Strategy Officer · <b>{n} live projects</b></p>
</header>
<hr class="double-rule">

<main id="main">
<div class="front">
{lead}
<div class="rail">
{briefs}
</div>
</div>

{series}

{index}

<section class="colophon" id="colophon">
<div class="cols">
<div>
<h3>What I work with</h3>
<dl class="skills">
  <dt>Modeling</dt><dd>scikit-learn, PyTorch, XGBoost, regression / classification / clustering, time series, neural networks, causal inference, survival analysis, A/B testing</dd>
  <dt>Optimization</dt><dd>Gurobi, LP / IP / QP / non-convex programming, branch-and-bound, LP duality, gradient descent, simulation, Monte Carlo</dd>
  <dt>GenAI and agents</dt><dd>LLM prompting, RAG, embeddings, vector databases, fine-tuning, OpenAI / Anthropic APIs, LangChain, LangGraph, tool use, retrieval pipelines</dd>
  <dt>Data and deployment</dt><dd>Python, R, SQL, Snowflake, Airflow, Spark / PySpark, Tableau, Power BI, Git, GitHub Pages, Streamlit</dd>
</dl>
</div>
<div>
<h3>About</h3>
<p>Co-founder and Chief Strategy Officer at Casual Ace Learning Centre: grew enrollment 5.2x to over 1,000 students across six centers. MSBA, UCLA Anderson; BBA, University of Hong Kong. Outside the terminal: 14 marathons, Berlin personal best of 2:48, WSET Level 3 in wine.</p>
<p><a href="https://www.linkedin.com/in/jeremylyh/">LinkedIn</a> · <a href="mailto:lyhjeremy@gmail.com">Email</a> · <a href="https://github.com/lyhjeremy">GitHub</a></p>
<pre class="cmd">npx lyhjeremy</pre>
<p class="pre-cap">The interactive version of this page, in a terminal.</p>
</div>
</div>
</section>
</main>

<footer class="site-footer">
  <a href="https://github.com/lyhjeremy">github.com/lyhjeremy</a>
  <span>Design and copy follow <a href="https://github.com/lyhjeremy/lyhjeremy/blob/main/DESIGN_STANDARDS.md">the house standards</a>. Fonts are self-hosted; no third-party requests, no analytics. Source: <a href="{GH}lyhjeremy.github.io">lyhjeremy.github.io</a>.</span>
</footer>
</div>

<script>
(function(){{
  var root=document.documentElement,btn=document.getElementById("theme-toggle");
  if(!btn)return;
  function current(){{return root.getAttribute("data-theme")==="light"?"light":"dark";}}
  function render(){{var light=current()==="light";btn.textContent=light?"Dark mode":"Light mode";btn.setAttribute("aria-pressed",light?"true":"false");}}
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
