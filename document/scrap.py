import requests
from bs4 import BeautifulSoup


def scrape_website(url: str) -> str:
    """
    Scrape a website and convert its visible content into plain text.

    Args:
        url: Website URL.

    Returns:
        str: Extracted website text.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove content that is usually not useful as page text
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Clean empty lines and extra spaces
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]


    return "\n".join(lines)




print(scrape_website("https://codeanddebug.in"))