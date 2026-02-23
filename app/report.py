def generate_markdown_report(question, claims):

    md = f"# Research Report\n\n"
    md += f"## Research Question\n{question}\n\n"
    md += f"## Findings\n\n"

    for i, c in enumerate(claims, 1):
        md += f"### Claim {i}\n"
        md += f"- **Claim:** {c['claim']}\n"
        md += f"- **Evidence (verbatim snippet):** {c['evidence_snippet']}\n"
        md += f"- **Source URL:** {c['url']}\n\n"

        md += f"**Credibility Analysis:**\n"
        md += f"- Base Credibility: {c.get('base_credibility', 'N/A')}\n"
        md += f"- Agreement Bonus: {c.get('agreement_bonus', 'N/A')}\n"
        md += f"- Final Credibility: {c.get('final_credibility', 'N/A')}\n"
        md += f"- Final Confidence: {c.get('final_confidence', 'N/A')}\n\n"

        md += "---\n\n"

    return md