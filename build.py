#!/usr/bin/env python3
"""Render index.html from projects.json. Run after editing the JSON."""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
data = json.loads((ROOT / "projects.json").read_text())
GH = "https://github.com/lyhjeremy/"
PAGES = "https://lyhjeremy.github.io/"
e = html.escape

def table(projects):
    rows = []
    for slug, name, blurb in projects:
        rows.append(
            f'<tr><td><strong><a href="{GH}{slug}">{e(name)}</a></strong></td>'
            f'<td>{e(blurb)}</td>'
            f'<td class="links"><a href="{PAGES}{slug}/">Live</a>'
            f'<a href="{PAGES}{slug}/overview/">Writeup</a></td></tr>')
    return ('<div class="table-scroll"><table class="projects">'
            '<thead><tr><th>Project</th><th>Methods</th><th>Links</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')

sections = []
for s in data["sections"]:
    lede = f'<p class="section-lede">{e(s["lede"])}</p>' if s.get("lede") else ""
    sections.append(f'<h2 id="{s["id"]}">{e(s["title"])}</h2>{lede}{table(s["projects"])}')
n = sum(len(s["projects"]) for s in data["sections"])

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
<header class="masthead">
  <p class="meta">lyhjeremy.github.io</p>
  <nav aria-label="Page">
    <a href="#featured">Projects</a>
    <a href="#experience">Experience</a>
    <a href="#contact">Contact</a>
    <button class="btn theme-toggle" type="button" id="theme-toggle" hidden aria-pressed="false">Light mode</button>
  </nav>
</header>

<main id="main">
<h1>Jeremy Lee</h1>
<p class="lede">Data scientist and UCLA Anderson MSBA. Formerly Chief Strategy Officer; now focused on applied analytics and machine learning. I turn ambiguous business problems into models and decision tools.</p>
<p>Design and copy on every site here follow <a href="https://github.com/lyhjeremy/lyhjeremy/blob/main/DESIGN_STANDARDS.md">these standards</a>. The source for this page is at <a href="{GH}lyhjeremy.github.io">lyhjeremy/lyhjeremy.github.io</a>.</p>
<pre class="cmd">npx lyhjeremy</pre>
<p class="pre-cap">Run that in a terminal for the interactive version of this page.</p>

<h2 id="skills">What I work with</h2>
<dl class="skills">
  <dt>Modeling</dt><dd>scikit-learn, PyTorch, XGBoost, regression / classification / clustering, time series, neural networks, causal inference, survival analysis, A/B testing</dd>
  <dt>Optimization</dt><dd>Gurobi, LP / IP / QP / non-convex programming, branch-and-bound, LP duality, gradient descent, simulation, Monte Carlo</dd>
  <dt>GenAI</dt><dd>LLM prompting, RAG, embeddings, vector databases, fine-tuning, OpenAI / Anthropic APIs, NLP</dd>
  <dt>Agents and orchestration</dt><dd>LangChain, LangGraph, agentic workflows, tool use, retrieval pipelines, multi-step reasoning</dd>
  <dt>Data and tools</dt><dd>Python, R, SQL, Snowflake, Airflow, Spark / PySpark, Tableau, Power BI, Excel, Git, GCS, Jupyter</dd>
  <dt>Deployment and apps</dt><dd>GitHub Pages, Streamlit, interactive dashboards, desktop apps, live demos, reproducible pipelines</dd>
</dl>

{"".join(sections)}

<h2 id="experience">Experience and education</h2>
<ul>
  <li><b>Co-founder and Chief Strategy Officer</b>, Casual Ace Learning Centre: grew enrollment 5.2x to over 1,000 students across six centers.</li>
  <li><b>MSBA</b>, UCLA Anderson. Graduate analytics coursework, Georgia Tech. <b>BBA</b> (Accounting and Finance), University of Hong Kong.</li>
</ul>

<h2 id="outside">Outside the terminal</h2>
<p>14 marathons, Berlin personal best of 2:48. WSET Level 3 in wine.</p>

<h2 id="contact">Contact</h2>
<p><a href="https://www.linkedin.com/in/jeremylyh/">LinkedIn</a> · <a href="mailto:lyhjeremy@gmail.com">Email</a> · <a href="https://github.com/lyhjeremy">GitHub</a></p>
</main>

<footer class="site-footer">
  <a href="https://github.com/lyhjeremy">github.com/lyhjeremy</a>
  <span>{n} projects listed. Fonts are self-hosted; this page makes no third-party requests and sets no analytics.</span>
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
print(f"wrote index.html with {n} projects")
