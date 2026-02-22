# agent.py

import json
from planner import generate_plan
from search import search_web
from extractor import extract_claims
from credibility import score_credibility
from report import generate_markdown_report
from guardrails import validate_prompt
from guardrails import is_research_question
from domain_policy import classify_domain, get_credibility_threshold


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

    # ------------------------
    # Planning
    # ------------------------
    plan_json = generate_plan(question)
    plan = json.loads(plan_json)
    trace["plan"] = plan

    all_claims = []

    # ------------------------
    # Initial Search Loop
    # ------------------------
    for query in plan["queries"]:
        results = search_web(query)

        trace["search_results"].append({
            "query": query,
            "results": results
        })

        for result in results[:2]:  # limit for speed
            content = result.get("content", "")
            url = result.get("url", "")

            extracted_json = extract_claims(content[:2000], question)
            extracted = json.loads(extracted_json)

            for claim in extracted["claims"]:

                if claim["evidence_snippet"] not in content:
                    continue

                base_credibility = score_credibility(url)
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

                claim["url"] = url
                claim["base_credibility"] = base_credibility
                claim["agreement_bonus"] = bonus
                claim["final_credibility"] = final_credibility
                claim["final_confidence"] = final_confidence

                all_claims.append(claim)

    # ------------------------
    # Filter + Deduplicate + Rank
    # ------------------------
    all_claims = [
        c for c in all_claims
        if c["final_credibility"] >= 0.6
    ]

    all_claims = deduplicate_claims(all_claims)

    all_claims = sorted(
        all_claims,
        key=lambda x: x["final_confidence"],
        reverse=True
    )[:12]

    trace["claims"] = all_claims

    # ------------------------
    # Refinement Step (One Retry)
    # ------------------------
    if needs_more_research(all_claims):
        print("🔁 Low quality evidence detected — refining search...")

        refined_queries = refine_queries(question)

        for query in refined_queries:
            results = search_web(query)

            trace["search_results"].append({
                "query": f"REFINED: {query}",
                "results": results
            })

            for result in results[:2]:
                content = result.get("content", "")
                url = result.get("url", "")

                extracted_json = extract_claims(content[:2000], question)
                extracted = json.loads(extracted_json)

                for claim in extracted["claims"]:

                    if claim["evidence_snippet"] not in content:
                        continue

                    base_credibility = score_credibility(url)
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

                    claim["url"] = url
                    claim["base_credibility"] = base_credibility
                    claim["agreement_bonus"] = bonus
                    claim["final_credibility"] = final_credibility
                    claim["final_confidence"] = final_confidence

                    all_claims.append(claim)

        # Re-filter and re-rank after refinement
        all_claims = [
            c for c in all_claims
            if c["final_credibility"] >= 0.6
        ]

        all_claims = deduplicate_claims(all_claims)

        all_claims = sorted(
            all_claims,
            key=lambda x: x["final_confidence"],
            reverse=True
        )[:12]

        trace["claims"] = all_claims

    # ------------------------
    # Final Metrics
    # ------------------------
    if all_claims:
        avg_credibility = round(
            sum(c["final_credibility"] for c in all_claims) / len(all_claims),
            3
        )
    else:
        avg_credibility = 0.0

    trace["avg_credibility"] = avg_credibility

    # ------------------------
    # Report Generation
    # ------------------------
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