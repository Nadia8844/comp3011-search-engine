import pytest
from src.indexer import Indexer


SAMPLE_PAGES = {
    "https://quotes.toscrape.com/": "The world is a good place and worth fighting for.",
    "https://quotes.toscrape.com/page/2/": "Good things come to those who wait in this world.",
}


class TestIndexerTokenise:
    """Tests for the tokeniser"""

    def setup_method(self):
        self.indexer = Indexer()

    def test_lowercase_conversion(self):
        tokens = self.indexer._tokenise("Hello World")
        assert tokens == ["hello", "world"]

    def test_strips_punctuation(self):
        tokens = self.indexer._tokenise("it's a test!")
        assert "it" in tokens
        assert "s" in tokens
        assert "test" in tokens

    def test_empty_string(self):
        tokens = self.indexer._tokenise("")
        assert tokens == []

    def test_numbers_excluded(self):
        tokens = self.indexer._tokenise("page 2 of 10")
        assert "2" not in tokens
        assert "10" not in tokens