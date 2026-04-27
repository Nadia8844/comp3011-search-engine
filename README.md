# COMP3011 Search Engine Tool

A command-line search engine that crawls [quotes.toscrape.com](https://quotes.toscrape.com/), builds an inverted index, and lets you search it interactively.

## Project overview

The tool is split into four modules:

- `crawler.py` — crawls all pages of the target site, respecting a 6-second politeness window
- `indexer.py` — tokenises page text and builds an inverted index storing word frequency and positions
- `search.py` — implements the `print` and `find` commands with TF-IDF ranking
- `main.py` — provides the interactive command-line shell

## Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/Nadia8844/comp3011-search-engine.git
cd comp3011-search-engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Start the shell from inside the `src/` directory:

```bash
cd src
python main.py
```

### Commands

**build** — crawl the site and save the index to disk:
```
> build
```

**load** — load a previously built index:
```
> load
```

**print** — show index entries for a word:
```
> print nonsense
```

**find** — search for pages containing one or more words, ranked by TF-IDF:
```
> find indifference
> find good friends
```

**exit** — quit the shell:
```
> exit
```

## Testing

Run the full test suite from the project root:

```bash
pytest -v
```

Run with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

The test suite has 46 tests with 100% coverage across crawler, indexer and search modules.

## Dependencies

- `requests` — HTTP requests for crawling
- `beautifulsoup4` — HTML parsing
- `pytest` — test framework
- `pytest-cov` — coverage reporting

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## Design decisions

The inverted index stores word frequency and token positions for each page, which enables accurate multi-word search and TF-IDF ranking. The `find` command returns results sorted by combined TF-IDF score, giving higher weight to pages where query terms are more distinctive. The crawler strips script, style and meta tags before indexing to avoid noise in the index.