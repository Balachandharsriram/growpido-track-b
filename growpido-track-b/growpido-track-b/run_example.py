"""
Run the full pipeline on the researched evidence for Badr Jafar (CEO,
Crescent Enterprises) and regenerate the diagnostic.

    python run_example.py

Reproduces output/diagnostic.html and prints the human-review queue --
everything the rules could not independently verify, which a person must
sign off before it goes anywhere near a client deliverable.
"""
from pathlib import Path
from pipeline.claims import Claim, Source
from pipeline.research import fetch_claims_from_evidence_file
from pipeline.verify import run as verify_run
from pipeline.gaps import candidate_gaps
from pipeline.diagnostic import render

EVIDENCE_PATH = "data/badr_jafar_evidence.json"
OUTPUT_PATH = "output/diagnostic.html"


def build_claims(raw_claims):
    claims = []
    for rc in raw_claims:
        claims.append(Claim(
            id=rc["id"],
            text=rc["text"],
            sources=[Source(**s) for s in rc["sources"]],
            self_sourced_only=rc.get("self_sourced_only", False),
            numeric_claim=rc.get("numeric_claim", False),
            superlative=rc.get("superlative", False),
            note=rc.get("note"),
            contradiction_group=rc.get("contradiction_group"),
        ))
    return claims


def main():
    raw_claims, subject = fetch_claims_from_evidence_file(EVIDENCE_PATH)
    claims = build_claims(raw_claims)
    verdicts = verify_run(claims)
    gaps = candidate_gaps(claims, verdicts)[:3]

    html = render(subject, claims, verdicts, gaps)
    Path(OUTPUT_PATH).write_text(html)

    held = [v for v in verdicts if not v.publishable]
    print(f"Diagnostic written to {OUTPUT_PATH}")
    print(f"\n{len(verdicts)} claims processed: "
          f"{sum(1 for v in verdicts if v.label=='verified')} verified, "
          f"{sum(1 for v in verdicts if v.label=='partially_verified')} partially verified, "
          f"{sum(1 for v in verdicts if v.label=='unverified')} unverified.")
    print(f"\n--- HUMAN REVIEW QUEUE ({len(held)} items held, nothing here auto-publishes) ---")
    for v in held:
        print(f"  [{v.claim_id}] {v.label}: {v.reason}")


if __name__ == "__main__":
    main()
