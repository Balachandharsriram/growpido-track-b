# Track B — Prospect to Diagnostic

Subject picked: **Badr Jafar**, CEO of Crescent Enterprises (Sharjah, UAE) — public LinkedIn
presence, president of Crescent Petroleum, chairman of Gulftainer and Pearl Petroleum.

## What this is

A small, deliberately boring verification pipeline. Given a set of claims about a person and
the sources they came from, it labels each one **verified / partially verified / unverified**
using fixed rules — not a language model's judgment call on the fly — and it never lets an
unverified claim reach the output as a bare fact.

The interesting finding wasn't a scandal. It's that the subject's *own* bio pages disagree with
each other on basic numbers (sector count, country count, headcount for Crescent Enterprises),
and two of his most-repeated superlatives ("first independent petroleum company in the Middle
East," "largest privately-owned container port operator in the world") turn out to be one
sentence copied across many bio-aggregator sites, not independently confirmed anywhere. That's
a more realistic finding for this kind of work than "found something scandalous" — and it's
exactly the class of error Growpido's brief says costs the most (25/100 on fact integrity).

## Run it

```
python3 run_example.py
```

Reads `data/badr_jafar_evidence.json`, applies the rules in `pipeline/verify.py`, writes
`output/diagnostic.html`, and prints the human-review queue to stdout.

## How the pieces fit

- `pipeline/claims.py` — data model. A `Claim` carries its sources; nothing else.
- `pipeline/verify.py` — the actual judgment. Five rules, applied in a fixed order, documented
  in the module docstring. Contradiction detection is automatic (numeric fingerprint comparison
  within a `contradiction_group`); superlative detection is a flag set at data-entry time, not
  inferred from wording, because inferring "is this a superlative" from free text is exactly the
  kind of soft judgment that shouldn't be load-bearing for a fact-integrity gate.
- `pipeline/gaps.py` — rule-based *candidates* for narrative gaps. Deliberately not fully
  automated — see the module docstring for why.
- `pipeline/research.py` — the interface the rest of the pipeline depends on
  (`fetch_claims(subject) -> [{text, sources}]`), with notes on how to wire it to a live backend
  (Anthropic API + web search tool, or a conventional search API). Not wired to a live backend in
  this submission because the build environment has no outbound network access — the evidence
  file was gathered in an interactive research pass instead, with every claim's source URL kept.
- `pipeline/diagnostic.py` — pure templating. Every sentence in the output traces to a `Claim`
  object; the renderer does not write or paraphrase claim text itself.
- `data/badr_jafar_evidence.json` — the actual evidence: 14 claims, each with its source domains
  and URLs, gathered from public sources only (Wikipedia, WEF, Milken Institute, Khaleej Times,
  Entrepreneur, MEI, trade press on Khor Mor/Pearl Petroleum, and the subject's own
  bio-aggregator pages). No LinkedIn scraping, no login-walled content, no outreach.

## Human gate and failure handling

Nothing with a `publishable=False` verdict (unverified, or contradicted) reaches the diagnostic
as a stated fact — it's rendered explicitly as "unverified — held," with the reason shown, and
listed separately in the human-review queue printed by `run_example.py`. A person decides what
happens next: drop it, attribute it to the subject rather than stating it as fact, or go find a
primary source. The pipeline has no path that publishes a claim automatically; "partially
verified" claims are shown *with* their caveat attached, never smoothed into plain prose.

If the live research backend (not wired up here) returns nothing, times out, or is rate-limited,
`fetch_claims_live` raises rather than falling back to guessing — a missing claim is a gap to
flag, not a blank to fill from the model's general knowledge. That failure mode was a deliberate
design choice, not an oversight: for this client, "we found nothing" is a safe answer and
"we made something up" is not.

## What I'd fix next

See the honest paragraph in the submission email. Short version: gap detection is rule-based and
coarse — it flags *patterns* (contradiction, unsupported superlative, single-source credential)
but a person still picks and phrases the final three gaps. Given more time I'd add: a second
verification pass that checks whether a "primary source" (the company's own official site, a
regulator filing, a university registrar) exists for each claim rather than just counting
distinct third-party domains, since right now two independent *republications* of the same
underlying press release would still count as two domains.
