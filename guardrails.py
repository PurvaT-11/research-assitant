DISALLOWED = [
    "tell me a joke",
    "ignore previous instructions",
    "write a poem",
    "hack",
]

def validate_prompt(prompt: str) -> bool:
    if len(prompt.strip()) < 20:
        return False
    
    lower = prompt.lower()
    for pattern in DISALLOWED:
        if pattern in lower:
            return False
    
    return True

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def is_research_question(question: str) -> bool:
    prompt = f"""
    Determine whether the following question requires multi-source research 
    and evidence synthesis.

    Respond with ONLY true or false.

    Question: {question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.choices[0].message.content.strip().lower()

    return answer == "true"