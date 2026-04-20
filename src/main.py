from crawler import Crawler
from indexer import Indexer
from search import Searcher

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

        if command == "build":
            crawler = Crawler("https://quotes.toscrape.com/")
            pages = crawler.crawl()
            indexer.build(pages)
            indexer.save(INDEX_PATH)
            searcher = Searcher(indexer.index)
            print(f"Built index with {len(indexer.index)} terms from {len(pages)} pages.")

        elif command == "load":
            indexer.load(INDEX_PATH)
            searcher = Searcher(indexer.index)
            print(f"Index ready with {len(indexer.index)} terms.")

        elif command == "print":
            if not args:
                print("Usage: print <word>")
            elif searcher is None:
                print("No index loaded. Run 'build' or 'load' first.")
            else:
                searcher.print_word(args[0])

        elif command == "find":
            if not args:
                print("Usage: find <word> [word2 ...]")
            elif searcher is None:
                print("No index loaded. Run 'build' or 'load' first.")
            else:
                results = searcher.find(args)
                if results:
                    print(f"\nFound {len(results)} page(s):\n")
                    for url, score in results:
                        print(f"  {url}  (score: {score:.4f})")

        elif command == "exit":
            print("Exiting.")
            break

        else:
            print(f"Unknown command: '{command}'. Try build, load, print, find, or exit.")

if __name__ == "__main__":
    run_shell()