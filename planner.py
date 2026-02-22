
import os
from openai import OpenAI
from prompts import RESEARCH_SYSTEM_PROMPT, PLANNER_PROMPT
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_plan(research_question: str):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": RESEARCH_SYSTEM_PROMPT},
            {"role": "user", "content": PLANNER_PROMPT + "\n\nQuestion:\n" + research_question}
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content