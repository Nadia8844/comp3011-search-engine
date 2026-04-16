import re
from collections import defaultdict


class Indexer:
    """Builds an inverted index from crawled page content."""

    def __init__(self):
        self.index = {}

    def _tokenise(self, text: str) -> list:
        """Convert text to a list of lowercase tokens, stripping punctuation."""
        text = text.lower()
        tokens = re.findall(r'[a-z]+', text)
        return tokens