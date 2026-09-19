"""
Verification logic.

The rule set is deliberately conservative, because the cost of a false
"verified" is a client's regulatory exposure, and the cost of a false
"unverified" is just an analyst spending two more minutes checking. The
pipeline is built to fail toward caution.

Rules, applied in order:

1. CONTRADICTED -> unverified, held.
   Any claim in a contradiction_group whose numbers don't match at least
   one other claim in the same group is a contradiction. We do not average,
   round, or pick the "most common" number -- we surface the conflict and
   stop.

2. UNSOURCED SUPERLATIVE -> unverified, held.
   A superlative ("first", "largest", "only", "biggest") that is
   self-sourced-only (every citation traces back to subject/company-supplied
   text, republished by third parties without independent reporting) is not
   treated as verified no matter how many places repeat it. Repetition of
   the same original sentence is not corroboration.

3. INDEPENDENT CORROBORATION -> verified.
   Claim is not self-sourced-only AND appears via 2+ independent domains
   AND is not a bare unsourced superlative -> verified.

4. SINGLE OR SELF-SOURCED, NON-SUPERLATIVE -> partially verified, held for
   review (not blocked from the diagnostic, but must be labelled and must
   name what corroboration is missing).

5. Anything else -> unverified, held.
"""
from collections import defaultdict
from typing import Dict, List
from .claims import Claim, Verdict


def _numeric_signature(text: str) -> str:
    """Pull out the digit groups in a claim's text as a crude fingerprint
    for detecting when two claims in the same contradiction_group disagree."""
    import re
    return ",".join(re.findall(r"\d+", text))


def find_contradictions(claims: List[Claim]) -> Dict[str, List[Claim]]:
    groups: Dict[str, List[Claim]] = defaultdict(list)
    for c in claims:
        if c.contradiction_group:
            groups[c.contradiction_group].append(c)
    contradicted = {}
    for group, members in groups.items():
        signatures = {_numeric_signature(m.text) for m in members}
        if len(signatures) > 1:
            contradicted[group] = members
    return contradicted


def verify_claim(claim: Claim, contradicted_groups: Dict[str, List[Claim]]) -> Verdict:
    if claim.contradiction_group and claim.contradiction_group in contradicted_groups:
        conflicting = [c.text for c in contradicted_groups[claim.contradiction_group] if c.id != claim.id]
        return Verdict(
            claim_id=claim.id,
            label="unverified",
            reason=(
                "Contradicted by the subject's own other published bios: "
                + " | ".join(conflicting)
            ),
            publishable=False,
        )

    # Superlatives never clear straight to "verified" -- see rule 2 in the
    # module docstring. A claim to be "first" or "largest" gets at best
    # "partially verified", and only if independent reporting supports the
    # underlying substance even though the exact wording isn't an independent
    # match. If every source is self-supplied, it's held outright.
    if claim.superlative:
        if claim.self_sourced_only:
            return Verdict(
                claim_id=claim.id,
                label="unverified",
                reason=(
                    "Superlative claim whose every source traces back to the same "
                    "subject/company-supplied sentence. No independent ranking or "
                    "third-party reporting corroborates it. Repetition is not corroboration."
                ),
                publishable=False,
            )
        return Verdict(
            claim_id=claim.id,
            label="partially_verified",
            reason=(
                claim.note or
                "Directionally supported by independent reporting but the exact "
                "wording of the superlative is not an independent match."
            ),
            publishable=True,  # publishable WITH the caveat attached, never as bare fact
        )

    if not claim.self_sourced_only and claim.independent_domain_count >= 2:
        return Verdict(
            claim_id=claim.id,
            label="verified",
            reason=f"Corroborated independently across {claim.independent_domain_count} unrelated domains.",
            publishable=True,
        )

    if claim.self_sourced_only or claim.independent_domain_count < 2:
        return Verdict(
            claim_id=claim.id,
            label="partially_verified",
            reason=(claim.note or "Only a single source, or all sources trace to subject-supplied text; no independent corroboration found."),
            publishable=True,
        )

    return Verdict(claim_id=claim.id, label="unverified", reason="Did not meet any corroboration rule.", publishable=False)


def run(claims: List[Claim]) -> List[Verdict]:
    contradicted = find_contradictions(claims)
    return [verify_claim(c, contradicted) for c in claims]
