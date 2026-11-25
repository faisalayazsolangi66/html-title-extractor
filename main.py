#!/usr/bin/env python3
"""Extract the <title> of a web page for a list of URLs.

Usage:
    python3 main.py https://example.com https://www.python.org
    python3 main.py --file urls.txt
"""
import argparse
import html
import re
import sys
import urllib.error
import urllib.request

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")


def fetch_title(url, timeout):
    """Return (title or None, error message or None) for one URL."""
    request = urllib.request.Request(
        url, headers={"User-Agent": "html-title-extractor/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(1_000_000)  # title is near the top; cap read
            charset = response.headers.get_content_charset() or "utf-8"
            text = raw.decode(charset, errors="replace")
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code} {exc.reason}"
    except urllib.error.URLError as exc:
        return None, str(exc.reason)
    except (TimeoutError, ValueError, UnicodeError) as exc:
        return None, str(exc)
    match = TITLE_RE.search(text)
    if not match:
        return None, "no <title> tag found"
    title = html.unescape(TAG_RE.sub("", match.group(1)))
    return " ".join(title.split()), None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Extract the page title from a list of URLs.")
    parser.add_argument("urls", nargs="*", help="URL(s) to fetch")
    parser.add_argument("--file", "-f", help="file with one URL per line")
    parser.add_argument("--timeout", type=float, default=10,
                        help="request timeout in seconds (default: 10)")
    args = parser.parse_args(argv)

    urls = list(args.urls)
    if args.file:
        with open(args.file, encoding="utf-8") as handle:
            urls.extend(line.strip() for line in handle if line.strip())
    if not urls:
        parser.error("no URLs given (pass URLs or --file)")
    urls = [u if "://" in u else "https://" + u for u in urls]

    failures = 0
    for url in urls:
        title, error = fetch_title(url, args.timeout)
        if error:
            print(f"{url} -> ERROR: {error}")
            failures += 1
        else:
            print(f"{url} -> {title}")
    return 1 if failures == len(urls) else 0


if __name__ == "__main__":
    raise SystemExit(main())
