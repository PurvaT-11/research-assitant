# agent.py

import json
from collections import defaultdict
from app.planner import generate_plan
from retrieval.search import search_web
from app.extractor import extract_claims
from app.credibility import score_credibility
from app.report import generate_markdown_report
from app.guardrails import validate_prompt
from app.guardrails import is_research_question



def agreement_bonus(current_claim, all_claims):
    similar = 0
    words_current = set(current_claim["claim"].lower().split())

    for c in all_claims:
        words_other = set(c["claim"].lower().split())
        overlap = len(words_current & words_other)

        if overlap > 5:
            similar += 1

    return min(similar * 0.03, 0.15)

def refine_queries(question: str):
    """
    Generate more focused academic-style queries.
    """

    refined = [
        f"{question} peer reviewed study",
        f"{question} systematic review",
        f"{question} academic research paper",
    ]

    return refined[:2]  # keep small for speed

def run_agent(question: str):

    # ------------------------
    # Guardrails
    # ------------------------
    if not validate_prompt(question):
        raise ValueError("Invalid research prompt.")

    if not is_research_question(question):
        raise ValueError("This agent is designed for research questions only.")

    trace = {
        "question": question,
        "plan": {},
        "search_results": [],
        "claims": []
    }

    plan = generate_plan(question)
    trace["plan"] = plan

    all_claims = []

    # ------------------------
    # Main Search Loop (1 extraction per query)
    # ------------------------
    for query in plan["queries"]:

        results = search_web(query)

        trace["search_results"].append({
            "query": query,
            "results": results
        })

        # Combine top 4 results before extraction
        combined_content = "\n\n".join(
            r.get("content", "")[:800] for r in results[:4]
        )

        extracted_json = extract_claims(combined_content, question)
        try:
            extracted = json.loads(extracted_json)
        except json.JSONDecodeError:
            print("JSON parsing failed. Skipping result.")
            continue

        for claim in extracted.get("claims", []):

            matched_url = None
            for r in results[:4]:
                if claim["evidence_snippet"] in r.get("content", ""):
                    matched_url = r.get("url", "")
                    break

            if not matched_url:
                continue

            base_credibility = score_credibility(matched_url)
            model_confidence = claim.get("confidence", 0.5)
            bonus = agreement_bonus(claim, all_claims)

            final_credibility = round(
                min(1.0, base_credibility + bonus),
                3
            )

            final_confidence = round(
                model_confidence * final_credibility,
                3
            )

            claim.update({
                "url": matched_url,
                "base_credibility": base_credibility,
                "agreement_bonus": bonus,
                "final_credibility": final_credibility,
                "final_confidence": final_confidence
            })

            all_claims.append(claim)

    # ------------------------
    # Filter + Deduplicate + Rank
    # ------------------------
    all_claims = [
        c for c in all_claims
        if c["final_credibility"] >= 0.6
    ]

    all_claims = deduplicate_claims(all_claims)
    all_claims = limit_per_source(all_claims, max_per_source=2)

    all_claims = sorted(
        all_claims,
        key=lambda x: x["final_confidence"],
        reverse=True
    )[:10]

    trace["claims"] = all_claims

    # ------------------------
    # Final Metrics
    # ------------------------
    if all_claims:
        trace["avg_credibility"] = round(
            sum(c["final_credibility"] for c in all_claims) / len(all_claims),
            3
        )
    else:
        trace["avg_credibility"] = 0.0

    report_md = generate_markdown_report(question, all_claims)

    return report_md, trace

def needs_more_research(claims):
    if len(claims) < 5:
        return True
    
    avg_cred = sum(c["final_credibility"] for c in claims) / len(claims)
    if avg_cred < 0.6:
        return True
    
    return False

def deduplicate_claims(claims):
    unique = []

    for c in claims:
        is_duplicate = False

        words_current = set(c["claim"].lower().split())

        for u in unique:
            words_other = set(u["claim"].lower().split())
            overlap = len(words_current & words_other)

            if overlap > 6:
                is_duplicate = True
                break

        if not is_duplicate:
            unique.append(c)

    return unique



def limit_per_source(claims, max_per_source=2):
    counts = defaultdict(int)
    filtered = []

    for c in claims:
        if counts[c["url"]] < max_per_source:
            filtered.append(c)
            counts[c["url"]] += 1

    return filtered


# A domain refinement module (domain_policy.py) exists for future
# domain-aware credibility thresholds and query adaptation.
# It is intentionally not wired into run_agent() yet to keep
# the current system minimal and deterministic.