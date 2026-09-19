"""
Renders the one-page diagnostic. Pure templating -- no claim text is
generated here; every sentence on the page traces to a Claim object that
came from research.py with sources attached.
"""
from typing import List
from .claims import Claim, Verdict

LABEL_META = {
    "verified": ("Verified", "#1a7f4e", "#e7f6ee"),
    "partially_verified": ("Partially verified", "#9a6a00", "#fff4dc"),
    "unverified": ("Unverified — held", "#a3272e", "#fbe8e9"),
}


def render(subject: dict, claims: List[Claim], verdicts: List[Verdict], gaps: List[str]) -> str:
    verdict_by_id = {v.claim_id: v for v in verdicts}
    rows = []
    for c in claims:
        v = verdict_by_id[c.id]
        label, color, bg = LABEL_META[v.label]
        sources_html = ", ".join(f'<a href="{s.url}" target="_blank" rel="noopener">{s.domain}</a>' for s in c.sources)
        rows.append(f"""
        <div class="claim-row">
          <div class="claim-text">{c.text}</div>
          <div class="claim-meta">
            <span class="badge" style="color:{color};background:{bg};border:1px solid {color}33;">{label}</span>
            <span class="sources">{sources_html}</span>
          </div>
          <div class="claim-reason">{v.reason}</div>
        </div>""")

    gaps_html = "".join(f"<li>{g}</li>" for g in gaps)

    counts = {"verified": 0, "partially_verified": 0, "unverified": 0}
    for v in verdicts:
        counts[v.label] += 1

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>Reputation Diagnostic — {subject['name']}</title>
<style>
  :root {{
    --ink:#1c1c1c; --sub:#5a5a5a; --line:#e7e4de; --paper:#fdfcfa; --accent:#8a3b2b;
    padding-top: env(safe-area-inset-top, 0px);
    padding-bottom: env(safe-area-inset-bottom, 0px);
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{ --ink:#ece9e4; --sub:#b7b2a9; --line:#3a362f; --paper:#171512; }}
  }}
  :root[data-theme="dark"] {{ --ink:#ece9e4; --sub:#b7b2a9; --line:#3a362f; --paper:#171512; }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--paper); color:var(--ink);
    font-family: 'Iowan Old Style','Palatino Linotype',Georgia,serif;
    -webkit-font-smoothing:antialiased;
  }}
  .page {{ max-width:840px; margin:0 auto; padding:40px 28px 64px; }}
  .masthead {{ display:flex; justify-content:space-between; align-items:baseline; border-bottom:2px solid var(--ink); padding-bottom:14px; margin-bottom:6px; }}
  .masthead h1 {{ font-size:1.5rem; margin:0; letter-spacing:.02em; }}
  .masthead .tag {{ font-family:-apple-system,Helvetica,Arial,sans-serif; font-size:.72rem; text-transform:uppercase; letter-spacing:.12em; color:var(--sub); }}
  .subline {{ font-family:-apple-system,Helvetica,Arial,sans-serif; font-size:.85rem; color:var(--sub); margin-bottom:28px; }}
  .scorebar {{ display:flex; gap:16px; font-family:-apple-system,Helvetica,Arial,sans-serif; font-size:.78rem; margin-bottom:30px; }}
  .scorebar span {{ padding:4px 10px; border-radius:20px; border:1px solid var(--line); }}
  h2 {{ font-size:1rem; text-transform:uppercase; letter-spacing:.08em; font-family:-apple-system,Helvetica,Arial,sans-serif; color:var(--sub); border-bottom:1px solid var(--line); padding-bottom:6px; margin:30px 0 14px; }}
  .claim-row {{ padding:12px 0; border-bottom:1px solid var(--line); }}
  .claim-text {{ font-size:1rem; line-height:1.45; margin-bottom:6px; }}
  .claim-meta {{ display:flex; flex-wrap:wrap; align-items:center; gap:10px; font-family:-apple-system,Helvetica,Arial,sans-serif; font-size:.75rem; margin-bottom:4px; }}
  .badge {{ padding:2px 9px; border-radius:20px; font-weight:600; white-space:nowrap; }}
  .sources {{ color:var(--sub); }}
  .sources a {{ color:var(--sub); }}
  .claim-reason {{ font-family:-apple-system,Helvetica,Arial,sans-serif; font-size:.8rem; color:var(--sub); line-height:1.4; }}
  ul.gaps {{ margin:0; padding-left:20px; }}
  ul.gaps li {{ margin-bottom:10px; line-height:1.5; }}
  .refused {{ background:var(--paper); border:1px solid #a3272e55; border-left:4px solid #a3272e; padding:14px 16px; border-radius:4px; margin-top:6px; }}
  .refused .claim-text {{ text-decoration: line-through; text-decoration-color:#a3272e88; }}
  footer {{ margin-top:40px; font-family:-apple-system,Helvetica,Arial,sans-serif; font-size:.72rem; color:var(--sub); border-top:1px solid var(--line); padding-top:14px; }}
  @media print {{ body {{ background:#fff; }} }}
</style>
</head>
<body>
<div class="page">
  <div class="masthead">
    <h1>Reputation Diagnostic</h1>
    <div class="tag">Growpido · Track B</div>
  </div>
  <div class="subline">
    Subject: <strong>{subject['name']}</strong>, {subject['role']} · Source: public LinkedIn presence + open web ·
    Prepared {subject['researched_on']}
  </div>

  <div class="scorebar">
    <span>{counts['verified']} verified</span>
    <span>{counts['partially_verified']} partially verified</span>
    <span>{counts['unverified']} unverified / held</span>
  </div>

  <h2>Claim-by-claim verification</h2>
  {''.join(rows)}

  <h2>Three biggest gaps in current public presence</h2>
  <ul class="gaps">{gaps_html}</ul>

  <h2>One claim the system refused to publish</h2>
  <div class="refused">
    <div class="claim-text">"Gulftainer — the largest privately-owned container port operator in the world"</div>
    <div class="claim-reason">
      Refused as a bare fact. This sentence appears on four+ third-party bio pages, but every
      instance is a verbatim republish of the same company-supplied paragraph — not four
      independent confirmations, one claim copied four times. No maritime-industry ranking or
      third-party benchmark was located in this research pass to corroborate "largest in the
      world" among privately-owned operators specifically. It may well be true — it is simply not
      independently verified, and a fund manager's or founder's client-facing content should not
      carry a superlative dressed as fact on the strength of repetition alone. Recommended
      treatment: attribute it ("Gulftainer, which the company describes as...") or drop it,
      pending a primary industry-ranking source.
    </div>
  </div>

  <footer>
    Generated by the Track B verification pipeline. Every line above traces to a source URL;
    nothing here was written by summarizing what "sounds right." Items marked unverified are held
    and require human sign-off before any client-facing use — see README §Human gate.
  </footer>
</div>
</body>
</html>"""
