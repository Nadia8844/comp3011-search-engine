import requests
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


class Crawler:
    """Crawls all pages of a target website and returns their text content2"""

    def __init__(self, seed_url: str, politeness: int = 6):
        self.seed_url = seed_url
        self.politeness = politeness
        self.domain = urlparse(seed_url).netloc
        self.visited = set()
        self.pages = {}

    def _is_valid_url(self, url: str) -> bool:
        """Check the URL belongs to the same domain and hasn't been visited."""
        parsed = urlparse(url)
        return (
            parsed.netloc == self.domain
            and url not in self.visited
        )

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> list:
        """Extract all valid links from a page."""
        links = []
        for tag in soup.find_all("a", href=True):
            full_url = urljoin(base_url, tag["href"])
            full_url = full_url.split("#")[0]  # strip fragments
            if self._is_valid_url(full_url):
                links.append(full_url)
        return links

    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract clean visible text from a page."""
        for tag in soup(["script", "style", "meta"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)