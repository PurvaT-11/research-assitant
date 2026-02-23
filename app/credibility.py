# credibility.py

from urllib.parse import urlparse

ACADEMIC = [
    "arxiv.org",
    "nature.com",
    "science.org",
    "acm.org",
    "ieee.org",
    "sciencedirect.com",
    "proceedings.mlr.press",
]

INDUSTRY_DOMAINS = [
    "openai.com",
    "google.com",
    "microsoft.com",
    "anthropic.com",
    "meta.com"
]

FORUM_DOMAINS = [
    "reddit.com",
    "stackoverflow.com",
    "quora.com",
    "medium.com"
]


def score_credibility(url: str) -> float:
    url_lower = url.lower()
    parsed = urlparse(url)
    domain = parsed.netloc

    score = 0.5  # base

    # academic journal boost
    if any(d in url_lower for d in ACADEMIC):
        score += 0.35

    #  .edu or .gov boost
    if domain.endswith(".edu") or domain.endswith(".gov"):
        score += 0.25

    # Industry research boost
    if any(d in url_lower for d in INDUSTRY_DOMAINS):
        score += 0.2

    # PDF boost (most likely a paper)
    if url_lower.endswith(".pdf"):
        score += 0.15

    # Forum penalty
    if any(d in url_lower for d in FORUM_DOMAINS):
        score -= 0.25

    # Clamp between 0 and 1
    return round(max(0.1, min(score, 1.0)), 3)

import re

import re

def tokenize(text):
    return set(re.findall(r"[a-zA-Z]+", text.lower()))

def agreement_bonus(claim, all_claims):
    words_current = tokenize(claim["claim"])
    similar = 0

    for c in all_claims:
        if c["claim"] != claim["claim"]:
            words_other = tokenize(c["claim"])
            overlap = len(words_current & words_other)

            if overlap >= 4:
                similar += 1

    return min(similar * 0.05, 0.15)