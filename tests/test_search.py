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