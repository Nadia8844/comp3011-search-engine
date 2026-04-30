import math


class Searcher:
    """Handles search operations over an inverted index"""

    def __init__(self, index: dict):
        self.index = index
        self.total_docs = len(
            set(url for postings in index.values() for url in postings)
        )

    def print_word(self, word: str) -> None:
        """Print the index entry for a single word"""
        word = word.lower()

        if word not in self.index:
            print(f"'{word}' not found in index.")
            return

        postings = self.index[word]
        print(f"\nWord: '{word}' — appears in {len(postings)} page(s)\n")

        for url, stats in postings.items():
            print(f"  {url}")
            print(f"    frequency : {stats['freq']}")
            print(f"    positions : {stats['positions'][:10]}{'...' if len(stats['positions']) > 10 else ''}")

    def _tfidf(self, word: str, url: str) -> float:
        """Calculate TF-IDF score for a word in a given page."""
        postings = self.index.get(word, {})
        if url not in postings:
            return 0.0

        tf = postings[url]["freq"]
        df = len(postings)
        idf = math.log(self.total_docs / (1 + df))
        return tf * idf
    
    def _is_phrase_match(self, query: list, url: str) -> bool:
        """Check if query words appear consecutively in the given page.

        Uses stored positional data to verify exact phrase matches.
        """
        first_word = query[0]
        start_positions = self.index[first_word][url]["positions"]

        for start in start_positions:
            match = True
            for offset, word in enumerate(query[1:], start=1):
                positions = self.index[word][url]["positions"]
                if (start + offset) not in positions:
                    match = False
                    break
            if match:
                return True
        return False

    def find_phrase(self, query: list) -> list:
        """Find pages where query words appear as an exact consecutive phrase.

        First finds pages containing all terms (AND search), then filters
        to only those where the terms appear in order using positional data.
        Results are ranked by combined TF-IDF score.
        """
        query = [word.lower() for word in query]

        # get AND intersection first
        matching_urls = None
        for word in query:
            if word not in self.index:
                print(f"'{word}' not found in index.")
                return []
            urls_for_word = set(self.index[word].keys())
            if matching_urls is None:
                matching_urls = urls_for_word
            else:
                matching_urls = matching_urls & urls_for_word

        if not matching_urls:
            print("No pages found containing all query terms.")
            return []

        # filter to phrase matches only
        phrase_urls = [url for url in matching_urls if self._is_phrase_match(query, url)]

        if not phrase_urls:
            print("No pages found containing that exact phrase.")
            return []

        # rank by combined TF-IDF score
        scored = [(url, sum(self._tfidf(w, url) for w in query)) for url in phrase_urls]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def find(self, query: list) -> list:
        """Find pages containing all query terms, ranked by TF-IDF score"""
        query = [word.lower() for word in query]

        # find pages that contain every query term
        matching_urls = None
        for word in query:
            if word not in self.index:
                print(f"'{word}' not found in index.")
                return []
            urls_for_word = set(self.index[word].keys())
            if matching_urls is None:
                matching_urls = urls_for_word
            else:
                matching_urls = matching_urls & urls_for_word

        if not matching_urls:
            print("No pages found containing all query terms.")
            return []

        # rank by combined TF-IDF score
        scored = []
        for url in matching_urls:
            score = sum(self._tfidf(word, url) for word in query)
            scored.append((url, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored
    
def test_phrase_no_common_pages_returns_empty(self, capsys):
        index = {
            "hello": {"https://quotes.toscrape.com/page/1/": {"freq": 1, "positions": [0]}},
            "world": {"https://quotes.toscrape.com/page/2/": {"freq": 1, "positions": [0]}},
        }
        searcher = Searcher(index)
        results = searcher.find_phrase(["hello", "world"])
        assert results == []
        captured = capsys.readouterr()
        assert "No pages found" in captured.out