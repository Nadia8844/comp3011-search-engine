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

class TestCrawlerURLValidation:
    """Tests for URL validation logic."""

    def setup_method(self):
        self.crawler = Crawler("https://quotes.toscrape.com/")

    def test_valid_url_accepted(self):
        assert self.crawler._is_valid_url("https://quotes.toscrape.com/page/2/") is True

    def test_external_url_rejected(self):
        assert self.crawler._is_valid_url("https://google.com") is False

    def test_already_visited_rejected(self):
        self.crawler.visited.add("https://quotes.toscrape.com/page/2/")
        assert self.crawler._is_valid_url("https://quotes.toscrape.com/page/2/") is False


class TestCrawlerLinkExtraction:
    """Tests for link extraction from HTML"""

    def setup_method(self):
        self.crawler = Crawler("https://quotes.toscrape.com/")

    def test_extracts_internal_links(self):
        from bs4 import BeautifulSoup
        html = make_html(links=["/page/2/", "/author/Einstein"])
        soup = BeautifulSoup(html, "html.parser")
        links = self.crawler._extract_links(soup, "https://quotes.toscrape.com/")
        assert "https://quotes.toscrape.com/page/2/" in links
        assert "https://quotes.toscrape.com/author/Einstein" in links

    def test_ignores_external_links(self):
        from bs4 import BeautifulSoup
        html = make_html(links=["https://google.com"])
        soup = BeautifulSoup(html, "html.parser")
        links = self.crawler._extract_links(soup, "https://quotes.toscrape.com/")
        assert links == []

    def test_strips_fragments(self):
        from bs4 import BeautifulSoup
        html = make_html(links=["/page/2/#section"])
        soup = BeautifulSoup(html, "html.parser")
        links = self.crawler._extract_links(soup, "https://quotes.toscrape.com/")
        assert "https://quotes.toscrape.com/page/2/" in links

class TestCrawlerCrawlLoop:
    """Tests for the main crawl loop using mocked HTTP requests"""

    def setup_method(self):
        self.crawler = Crawler("https://quotes.toscrape.com/", politeness=0)

    @patch("src.crawler.time.sleep")
    @patch("src.crawler.requests.get")
    def test_crawl_returns_pages(self, mock_get, mock_sleep):
        mock_response = MagicMock()
        mock_response.text = make_html(text="some quote text")
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        pages = self.crawler.crawl()
        assert len(pages) > 0

    @patch("src.crawler.time.sleep")
    @patch("src.crawler.requests.get")
    def test_crawl_respects_politeness(self, mock_get, mock_sleep):
        mock_response = MagicMock()
        mock_response.text = make_html()
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        crawler = Crawler("https://quotes.toscrape.com/", politeness=6)
        crawler.crawl()
        mock_sleep.assert_called_with(6)

    @patch("src.crawler.time.sleep")
    @patch("src.crawler.requests.get")
    def test_crawl_handles_failed_request(self, mock_get, mock_sleep):
        import requests
        mock_get.side_effect = requests.RequestException("connection error")
        pages = self.crawler.crawl()
        assert isinstance(pages, dict)

    @patch("src.crawler.time.sleep")
    @patch("src.crawler.requests.get")
    def test_crawl_does_not_visit_same_url_twice(self, mock_get, mock_sleep):
        mock_response = MagicMock()
        mock_response.text = make_html()
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        self.crawler.crawl()
        urls_fetched = [call[0][0] for call in mock_get.call_args_list]
        assert len(urls_fetched) == len(set(urls_fetched))

    @patch("src.crawler.time.sleep")
    @patch("src.crawler.requests.get")
    def test_extract_text_removes_script_tags(self, mock_get, mock_sleep):
        from bs4 import BeautifulSoup
        html = "<html><body><script>alert()</script><p>clean text</p></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        crawler = Crawler("https://quotes.toscrape.com/")
        text = crawler._extract_text(soup)
        assert "alert" not in text
        assert "clean" in text

    @patch("src.crawler.time.sleep")
    @patch("src.crawler.requests.get")
    def test_duplicate_url_in_queue_skipped(self, mock_get, mock_sleep):
        mock_response = MagicMock()
        mock_response.text = "<html><body>text</body></html>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        crawler = Crawler("https://quotes.toscrape.com/", politeness=0)
        crawler.visited.add("https://quotes.toscrape.com/")
        crawler.crawl()
        mock_get.assert_not_called()