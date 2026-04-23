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

class TestIndexerBuild:
    """Tests for index building logic"""

    def setup_method(self):
        self.indexer = Indexer()
        self.indexer.build(SAMPLE_PAGES)

    def test_index_contains_word(self):
        assert "good" in self.indexer.index

    def test_word_frequency_correct(self):
        assert self.indexer.index["good"]["https://quotes.toscrape.com/"]["freq"] == 1
        assert self.indexer.index["good"]["https://quotes.toscrape.com/page/2/"]["freq"] == 1

    def test_positions_recorded(self):
        positions = self.indexer.index["good"]["https://quotes.toscrape.com/"]["positions"]
        assert isinstance(positions, list)
        assert len(positions) > 0

    def test_case_insensitive_indexing(self):
        assert "the" in self.indexer.index
        assert "world" in self.indexer.index

    def test_word_appears_in_multiple_pages(self):
        assert len(self.indexer.index["world"]) == 2

    def test_empty_pages_returns_empty_index(self):
        indexer = Indexer()
        indexer.build({})
        assert indexer.index == {}