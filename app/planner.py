
import os
from openai import OpenAI
from config.prompts import RESEARCH_SYSTEM_PROMPT, PLANNER_PROMPT
from dotenv import load_dotenv


def generate_plan(question):
    base = question.strip()

    return {
        "queries": [
            # Academic sources
            f"{base} research paper",
            f"{base} peer reviewed study",
            f"{base} site:arxiv.org {base}",
            
            # Technical evaluation
            f"{base} empirical evaluation",
            f"{base} benchmark results",
            
            # Risks & critiques
            f"{base} risks limitations challenges",
            f"{base} ethical concerns bias privacy",
            
            # Industry + applied
            f"{base} industry analysis",
            f"{base} case study",

            f"{base} evaluation metrics performance generalization",
            f"{base} distribution shift benchmark study",
        ]
    }