import pytest
from src.search import Searcher


SAMPLE_INDEX = {
    "good": {
        "https://quotes.toscrape.com/": {"freq": 3, "positions": [2, 10, 15]},
        "https://quotes.toscrape.com/page/2/": {"freq": 1, "positions": [5]},
    },
    "friends": {
        "https://quotes.toscrape.com/": {"freq": 2, "positions": [4, 20]},
    },
    "life": {
        "https://quotes.toscrape.com/": {"freq": 1, "positions": [8]},
        "https://quotes.toscrape.com/page/2/": {"freq": 4, "positions": [1, 6, 9, 12]},
        "https://quotes.toscrape.com/page/3/": {"freq": 2, "positions": [3, 7]},
    },
}


class TestSearcherInit:
    """Tests for Searcher initialisation"""

    def test_index_stored(self):
        searcher = Searcher(SAMPLE_INDEX)
        assert searcher.index == SAMPLE_INDEX

    def test_total_docs_correct(self):
        searcher = Searcher(SAMPLE_INDEX)
        assert searcher.total_docs == 3

class TestSearcherFind:
    """Tests for the find method"""

    def setup_method(self):
        self.searcher = Searcher(SAMPLE_INDEX)

    def test_single_word_returns_results(self):
        results = self.searcher.find(["good"])
        urls = [url for url, score in results]
        assert "https://quotes.toscrape.com/" in urls

    def test_missing_word_returns_empty(self):
        results = self.searcher.find(["nonexistentword"])
        assert results == []

    def test_multi_word_returns_intersection(self):
        results = self.searcher.find(["good", "friends"])
        urls = [url for url, score in results]
        assert "https://quotes.toscrape.com/" in urls
        assert "https://quotes.toscrape.com/page/2/" not in urls

    def test_no_intersection_returns_empty(self):
        results = self.searcher.find(["friends", "life"])
        assert results == []

    def test_results_sorted_by_score(self):
        results = self.searcher.find(["life"])
        scores = [score for url, score in results]
        assert scores == sorted(scores, reverse=True)

    def test_case_insensitive_query(self):
        results_lower = self.searcher.find(["good"])
        results_upper = self.searcher.find(["GOOD"])
        assert results_lower == results_upper

    def test_empty_query_returns_empty(self):
        results = self.searcher.find([])
        assert results == []