
import requests
from bs4 import BeautifulSoup

def scrape_url(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for tag in soup(["script", "style"]):
            tag.extract()

        text = soup.get_text(separator="\n")
        return text[:15000]  # truncate safely

    except Exception as e:
        return ""