# domain_policy.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_domain(question: str) -> str:
    prompt = f"""
    Classify this question into ONE of the following categories:

    - medical
    - technical
    - policy
    - general

    Respond with ONLY the category name.

    Question: {question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip().lower()


def get_credibility_threshold(domain: str) -> float:
    """
    Domain-aware credibility threshold.
    """

    if domain == "medical":
        return 0.75

    if domain == "technical":
        return 0.6

    if domain == "policy":
        return 0.65

    return 0.6