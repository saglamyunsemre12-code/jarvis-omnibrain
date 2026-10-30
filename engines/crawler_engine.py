#!/usr/bin/env python3
"""
JARVIS Crawler Engine — Semantic Web Extraction & Research Engine
Inspired by Crawl4AI & Deep Research methodologies.
Converts any web article/documentation URL into clean, high-signal Markdown.
"""

import urllib.request
import urllib.parse
import re
import json

def fetch_and_clean_markdown(url, max_length=4000):
    """Fetches a URL and extracts clean article text without heavy headless browser bloat."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # 1. Extract Title
        title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Web Document"

        # 2. Strip scripts, styles, header, footer, nav
        cleaned = re.sub(r"<(script|style|nav|header|footer|aside)[^>]*>.*?</\1>", "", html, flags=re.IGNORECASE | re.DOTALL)
        
        # 3. Convert headers and paragraphs
        cleaned = re.sub(r"<h1[^>]*>(.*?)</h1>", r"\n# \1\n", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"<h2[^>]*>(.*?)</h2>", r"\n## \1\n", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"<h3[^>]*>(.*?)</h3>", r"\n### \1\n", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"<p[^>]*>(.*?)</p>", r"\n\1\n", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"<li[^>]*>(.*?)</li>", r"\n* \1", cleaned, flags=re.IGNORECASE)

        # 4. Remove all remaining tags
        text = re.sub(r"<[^>]+>", " ", cleaned)
        # Normalize whitespace
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text).strip()

        # Truncate to maximum signal length
        if len(text) > max_length:
            text = text[:max_length] + "\n\n[...Metin bağlam sınırı için sıkıştırıldı...]"

        return {
            "status": "SUCCESS",
            "url": url,
            "title": title,
            "word_count": len(text.split()),
            "markdown": text
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e), "url": url}

if __name__ == "__main__":
    res = fetch_and_clean_markdown("https://example.com")
    print(json.dumps(res, indent=2))
