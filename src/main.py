import os
from crawler import Crawler
from indexer import Indexer
from search import Searcher

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "data", "index.json")

def run_shell(searcher: Searcher = None) -> None:
    """Run an interactive command-line shell for the search tool"""
    print("\nSearch Engine ready. Type 'help' for a list of commands.\n")

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
                print("Usage: find <word> [word2 ...]  or  find \"exact phrase\"")
            elif searcher is None:
                print("No index loaded. Run 'build' or 'load' first.")
            else:
                # detect phrase search: find "good friends"
                raw_args = raw[len("find"):].strip()
                if raw_args.startswith('"') and raw_args.endswith('"'):
                    phrase = raw_args[1:-1].split()
                    results = searcher.find_phrase(phrase)
                    mode = "phrase"
                else:
                    results = searcher.find(args)
                    mode = "AND"

                if results:
                    print(f"\nFound {len(results)} page(s) [{mode} search]:\n")
                    for url, score in results:
                        print(f"  {url}  (score: {score:.4f})")

        elif command == "exit":
            print("Exiting.")
            break

        elif command == "help":
            print("\nAvailable commands:")
            print("  build              — crawl the site and build the index")
            print("  load               — load the index from disk")
            print("  print <word>       — show index entry for a word")
            print("  find <query>       — AND search ranked by TF-IDF")
            print("  find \"<phrase>\"    — exact phrase search")
            print("  help               — show this help message")
            print("  exit               — quit the shell\n")

        else:
            print(f"Unknown command: '{command}'. Try build, load, print, find, find \"phrase\", help, or exit.")

if __name__ == "__main__":
    run_shell()