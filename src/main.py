from src.crawler import Crawler
from src.indexer import Indexer
from src.search import Searcher

INDEX_PATH = "data/index.json"


def run_shell(searcher: Searcher = None) -> None:
    """Run an interactive command-line shell for the search tool"""
    print("\nSearch Engine ready. Commands: build, load, print <word>, find <query>, exit\n")

    indexer = Indexer()

    while True:
        try:
            raw = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not raw:
            continue

        parts = raw.split()
        command = parts[0].lower()
        args = parts[1:]