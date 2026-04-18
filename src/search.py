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