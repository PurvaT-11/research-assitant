
import os
from openai import OpenAI
from config.prompts import EXTRACTION_PROMPT
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_claims(content: str, research_question: str):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {
                "role": "user",
                "content": f"Research Question:\n{research_question}\n\nContent:\n{content}"
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=400
    )

    return response.choices[0].message.content