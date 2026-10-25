import re
import requests
from bs4 import BeautifulSoup

try:
    from src.utils import save_to_json
except ImportError:
    from utils import save_to_json

URL = "https://en.wikipedia.org/wiki/Web_scraping"
OUTPUT_FILE = "extracted_wikipedia_data.json"


def fetch_wikipedia_page(url: str = URL) -> str:
    """Download the HTML of the page and return it as text."""
    headers = {"User-Agent": "Mozilla/5.0 (student DS lab)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def extract_title(soup: BeautifulSoup) -> str:
    heading = soup.find("h1", id="firstHeading")
    return heading.get_text(strip=True) if heading else ""


def extract_first_sentence(soup: BeautifulSoup) -> str:
    for p in soup.find_all("p"):
        text = p.get_text(" ", strip=True)
        if not text:
            continue
        text = re.sub(r"\[\d+\]", "", text)         # remove [1] citations
        text = re.sub(r"\s+([,.;])", r"\1", text)   # fix spaces before punctuation
        return re.split(r"(?<=[.!?])\s", text.strip())[0]
    return ""


def main() -> None:
    html = fetch_wikipedia_page()
    soup = BeautifulSoup(html, "html.parser")
    data = {
        "title": extract_title(soup),
        "first_sentence": extract_first_sentence(soup),
    }
    save_to_json(data, OUTPUT_FILE)


if __name__ == "__main__":
    main()