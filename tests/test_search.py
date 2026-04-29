import pytest
from src.search import Searcher

PHRASE_INDEX = {
    "good": {
        "https://quotes.toscrape.com/": {"freq": 2, "positions": [3, 10]},
        "https://quotes.toscrape.com/page/2/": {"freq": 1, "positions": [5]},
    },
    "friends": {
        "https://quotes.toscrape.com/": {"freq": 2, "positions": [4, 20]},
        "https://quotes.toscrape.com/page/2/": {"freq": 1, "positions": [7]},
    },
}

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
        results = self.searcher.find(["friends", "nonexistentword"])
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

class TestSearcherPrintWord:
    """Tests for the print_word method"""

    def setup_method(self):
        self.searcher = Searcher(SAMPLE_INDEX)

    def test_existing_word_prints(self, capsys):
        self.searcher.print_word("good")
        captured = capsys.readouterr()
        assert "good" in captured.out
        assert "2" in captured.out

    def test_missing_word_prints_message(self, capsys):
        self.searcher.print_word("nonexistentword")
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_case_insensitive_print(self, capsys):
        self.searcher.print_word("GOOD")
        captured = capsys.readouterr()
        assert "good" in captured.out

    def test_shows_frequency(self, capsys):
        self.searcher.print_word("good")
        captured = capsys.readouterr()
        assert "freq" in captured.out or "frequency" in captured.out

    def test_shows_positions(self, capsys):
        self.searcher.print_word("good")
        captured = capsys.readouterr()
        assert "positions" in captured.out

    def test_tfidf_returns_zero_for_missing_url(self):
        score = self.searcher._tfidf("good", "https://quotes.toscrape.com/nonexistent/")
        assert score == 0.0

class TestSearcherPhrase:
    """Tests for phrase search using positional data."""

    def setup_method(self):
        self.searcher = Searcher(PHRASE_INDEX)

    def test_phrase_match_found(self):
        results = self.searcher.find_phrase(["good", "friends"])
        urls = [url for url, score in results]
        assert "https://quotes.toscrape.com/" in urls

    def test_phrase_match_excludes_non_consecutive(self):
        results = self.searcher.find_phrase(["good", "friends"])
        urls = [url for url, score in results]
        assert "https://quotes.toscrape.com/page/2/" not in urls

    def test_phrase_missing_word_returns_empty(self):
        results = self.searcher.find_phrase(["good", "nonexistent"])
        assert results == []

    def test_phrase_case_insensitive(self):
        results = self.searcher.find_phrase(["GOOD", "FRIENDS"])
        urls = [url for url, score in results]
        assert "https://quotes.toscrape.com/" in urls

    def test_phrase_single_word(self):
        results = self.searcher.find_phrase(["good"])
        assert len(results) > 0

    def test_phrase_no_match_returns_empty(self):
        results = self.searcher.find_phrase(["friends", "good"])
        assert results == []