"""
Research interface.

For this submission, I gathered evidence in a directed, interactive research
pass -- AI-assisted web search, with every claim checked against its source
before it went in the file -- and saved the results to
data/<subject>_evidence.json. That file is the ground truth the rest of the
pipeline runs on: nothing downstream invents or paraphrases a fact that
isn't in that file with a source attached.

For production use as an actual weekly/on-demand tool, this module is where
you'd wire a live backend. Two ways to do that with what's documented for
this environment:

  1. Anthropic API + server-side web search tool (see anthropic_api_in_artifacts
     in this environment's own docs): call /v1/messages with
     tools=[{"type": "web_search_20250305", "name": "web_search"}] and a
     prompt that asks the model to return ONLY a JSON array of
     {claim_text, source_domain, source_url} triples -- no prose, no
     synthesis, so the verification rules in verify.py (not the search
     model) are what decide the label.

  2. A conventional search API (SerpAPI, Bing, etc.) fanned out per claim
     type (bio pages, news, primary-source pages like the company's own
     "About" page or a regulator filing), with the same JSON contract.

Either way, the contract this pipeline depends on is fixed:
    fetch_claims(subject_name: str) -> list[dict]
    each dict: {"text": str, "sources": [{"domain": str, "url": str}], ...}

This keeps the verification logic (the part that actually matters for fact
integrity) independent of which search backend is behind it.
"""
import json
from pathlib import Path
from typing import List, Dict


def fetch_claims_from_evidence_file(path: str) -> List[Dict]:
    """Load a pre-researched evidence file. This is what this submission uses."""
    data = json.loads(Path(path).read_text())
    return data["claims"], data["subject"]


def fetch_claims_live(subject_name: str) -> List[Dict]:
    """Placeholder for a live backend (see module docstring). Not wired up in
    this submission because the build environment has no outbound network --
    the interface and the verification rules are the real deliverable."""
    raise NotImplementedError(
        "Wire this to the Anthropic API web_search tool or a search API per "
        "the contract described in this module's docstring."
    )
