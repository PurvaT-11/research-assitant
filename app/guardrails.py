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

def is_research_question(q):
    q = q.lower()

    research_indicators = [
        "how", "why", "impact", "effect", "risk", "benefit",
        "consequence", "outcome", "evidence", "study",
        "analysis", "real world", "long term"
    ]

    return any(word in q for word in research_indicators)