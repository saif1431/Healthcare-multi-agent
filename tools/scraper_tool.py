            
import requests
from bs4 import BeautifulSoup


MAX_ARTICLE_CHARACTERS = 1500


def scrape_article(url: str) -> str:
    """Extract readable article text from a webpage URL."""
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary HTML elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        # Extract paragraph text
        paragraphs = soup.find_all("p")

        article_text = "\n".join(
            paragraph.get_text(strip=True)
            for paragraph in paragraphs
        )

        if not article_text.strip():
            return "No readable article content found."

        return article_text[:MAX_ARTICLE_CHARACTERS]

    except requests.RequestException as error:
        return f"Unable to scrape article: {error}"
