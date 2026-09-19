"""
Gap detection.

This is intentionally semi-automated. The rules below flag *candidates* --
patterns that reliably indicate a narrative gap worth a human writing one
sentence about. Picking the final three and phrasing them for a client is
left to a person, on purpose: "which gaps matter most to THIS client this
quarter" is a judgement call, not something a scoring function should own.
"""
from typing import List
from .claims import Claim, Verdict


def candidate_gaps(claims: List[Claim], verdicts: List[Verdict]) -> List[str]:
    verdict_by_id = {v.claim_id: v for v in verdicts}
    candidates = []

    contradicted_groups = {c.contradiction_group for c in claims
                            if c.contradiction_group and verdict_by_id[c.id].label == "unverified"
                            and "Contradicted" in verdict_by_id[c.id].reason}
    if contradicted_groups:
        candidates.append(
            "Self-reported operating footprint numbers (sector count, country count, "
            "headcount) conflict across the subject's own bio pages -- no single "
            "current figure can be published without picking one arbitrarily."
        )

    unverified_superlatives = [c for c in claims
                                if c.superlative and verdict_by_id[c.id].label != "verified"]
    if len(unverified_superlatives) >= 2:
        candidates.append(
            "Several of the subject's most repeated claims to distinction ('first', "
            "'largest') are unsourced beyond the subject's own bio text -- widely "
            "repeated, never independently ranked or confirmed."
        )

    single_source_credentials = [c for c in claims
                                  if c.self_sourced_only and not c.superlative
                                  and verdict_by_id[c.id].label == "partially_verified"]
    if single_source_credentials:
        candidates.append(
            "Core biographical credentials appear in only one indexed source, with "
            "other bios describing the same fact more vaguely -- no primary-source "
            "(institutional) confirmation was found in a single research pass."
        )

    return candidates
