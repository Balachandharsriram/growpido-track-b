"""
Data model for the verification pipeline.

A Claim is one factual statement about the subject, carrying the list of
sources it was found in. Nothing here decides truth -- verify.py does that,
using only the evidence attached to the claim.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Source:
    domain: str
    url: str


@dataclass
class Claim:
    id: str
    text: str
    sources: List[Source]
    self_sourced_only: bool = False   # every source traces to subject/company-supplied bio text
    numeric_claim: bool = False
    superlative: bool = False         # "first", "largest", "only" etc.
    note: Optional[str] = None
    contradiction_group: Optional[str] = None  # claims in the same group are compared for numeric conflicts

    @property
    def independent_domain_count(self) -> int:
        return len({s.domain for s in self.sources})


@dataclass
class Verdict:
    claim_id: str
    label: str            # "verified" | "partially_verified" | "unverified"
    reason: str
    publishable: bool     # False = held for human review, never auto-published
