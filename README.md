# HTML Title Extractor

Extract the page title (`<title>` tag) from a list of URLs.

## Requirements

- Python 3 (standard library only — no extra packages)

## Usage

```bash
python3 main.py https://example.com https://www.python.org
python3 main.py --file urls.txt
```

Options:

- `urls` — one or more URLs to fetch (bare hostnames get `https://` added)
- `--file, -f FILE` — file with one URL per line
- `--timeout SECONDS` — request timeout (default: 10)

## Example

```bash
$ python3 main.py https://example.com https://www.python.org
https://example.com -> Example Domain
https://www.python.org -> Welcome to Python.org
```

Pages with no `<title>` tag, HTTP errors, and network failures are
reported as `ERROR` with a reason instead of crashing.
