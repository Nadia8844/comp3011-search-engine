import pytest
from unittest.mock import patch, MagicMock
from src.crawler import Crawler


def make_html(links=None, text="Hello world"):
    """Helper to build a minimal HTML page for testing"""
    link_tags = "".join(f'<a href="{l}">link</a>' for l in (links or []))
    return f"<html><body><p>{text}</p>{link_tags}</body></html>"


class TestCrawlerInit:
    """Tests for Crawler initialisation"""

    def test_seed_url_stored(self):
        crawler = Crawler("https://quotes.toscrape.com/")
        assert crawler.seed_url == "https://quotes.toscrape.com/"

    def test_default_politeness(self):
        crawler = Crawler("https://quotes.toscrape.com/")
        assert crawler.politeness == 6

    def test_custom_politeness(self):
        crawler = Crawler("https://quotes.toscrape.com/", politeness=1)
        assert crawler.politeness == 1

    def test_domain_extracted(self):
        crawler = Crawler("https://quotes.toscrape.com/")
        assert crawler.domain == "quotes.toscrape.com"

    def test_visited_starts_empty(self):
        crawler = Crawler("https://quotes.toscrape.com/")
        assert crawler.visited == set()