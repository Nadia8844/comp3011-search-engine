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