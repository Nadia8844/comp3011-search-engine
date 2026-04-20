import re
from collections import defaultdict


class Indexer:
    """Builds an inverted index from crawled page content"""

    def __init__(self):
        self.index = {}

    def _tokenise(self, text: str) -> list:
        """Convert text to a list of lowercase tokens, stripping punctuation"""
        text = text.lower()
        tokens = re.findall(r'[a-z]+', text)
        return tokens
    
    def build(self, pages: dict) -> dict:
        """Build an inverted index from a dict of {url: text}

        Each entry stores the frequency and positions of a word per page
        Structure: {word: {url: {freq: int, positions: [int]}}}
        """
        self.index = {}

        for url, text in pages.items():
            tokens = self._tokenise(text)

            for position, word in enumerate(tokens):
                if word not in self.index:
                    self.index[word] = {}

                if url not in self.index[word]:
                    self.index[word][url] = {"freq": 0, "positions": []}

                self.index[word][url]["freq"] += 1
                self.index[word][url]["positions"].append(position)

        return self.index
    
    def save(self, filepath: str) -> None:
        """Save the inverted index to a JSON file"""
        import json
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.index, f, indent=2)
        print(f"Index saved to {filepath}")

def load(self, filepath: str) -> dict:
        """Load the inverted index from a JSON file"""
        import json
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.index = json.load(f)
            print(f"Index loaded from {filepath} ({len(self.index)} terms)")
        except FileNotFoundError:
            print(f"No index file found at '{filepath}'. Run 'build' first.")
        return self.index