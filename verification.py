
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detect_contradictions(claims):
    prompt = f"""
    Analyze these claims and identify contradictions.

    Claims:
    {claims}

    Return JSON:
    {{
      "contradictions": [
        {{
          "claim_1_index": 0,
          "claim_2_index": 2,
          "reason": ""
        }}
      ]
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content