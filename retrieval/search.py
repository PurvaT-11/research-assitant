# search.py

import os
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str, max_results: int = 5):
    results = tavily.search(
        query=query,
        max_results=max_results,
        search_depth="advanced"
    )

    return results["results"]