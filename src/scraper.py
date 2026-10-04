"""Jumia Nigeria smartphone listing scraper.

The scraper stores raw listing-level fields. Cleaning and business logic live
in cleaning.py so extraction and transformation remain separate and testable.
"""

from __future__ import annotations

import argparse
import logging
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://www.jumia.com.ng/android-phones/?page={page}"
ROOT_URL = "https://www.jumia.com.ng"
LOGGER = logging.getLogger(__name__)


def build_session() -> requests.Session:
    """Create a retry-enabled HTTP session with a browser-like user agent."""
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/151.0 Safari/537.36"
            )
        }
    )
    return session


def _text(node) -> str | None:
    return node.get_text(" ", strip=True) if node else None


def parse_card(card) -> dict:
    """Extract raw fields from one Jumia product card."""
    name = _text(card.select_one("h3.name"))
    price = _text(card.select_one("div.prc"))
    old_price = _text(card.select_one("div.old"))
    rating = _text(card.select_one("div.stars._s"))

    review_node = card.select_one("div.rev")
    review_text = _text(review_node)
    review_count = None
    if review_text:
        match = re.search(r"\(([\d,]+)\)", review_text)
        if match:
            review_count = match.group(1).replace(",", "")

    official = bool(card.select_one(".bdg._mall"))

    link_node = card.select_one("a.core[href]") or card.select_one('a[href*=".html"]')
    href = link_node.get("href") if link_node else None
    product_url = urljoin(ROOT_URL, href) if href else None

    return {
        "phone_name": name,
        "price": price,
        "old_price": old_price,
        "rating": rating,
        "review_count": review_count,
        "official_store": "Yes" if official else "No",
        "product_url": product_url,
    }


def scrape(max_pages: int = 50, delay: float = 1.0) -> pd.DataFrame:
    """Scrape listing pages until max_pages or an empty page is reached."""
    session = build_session()
    rows: list[dict] = []
    scraped_at = datetime.now(timezone.utc).isoformat()

    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page=page)
        LOGGER.info("Scraping page %s", page)

        response = session.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        cards = soup.select("article.prd")
        if not cards:
            LOGGER.info("No product cards found on page %s; stopping.", page)
            break

        for card in cards:
            row = parse_card(card)
            row["source_page"] = page
            row["scraped_at_utc"] = scraped_at
            rows.append(row)

        time.sleep(delay)

    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=50)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--output", default="data/raw/jumia_phones_latest.csv")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    df = scrape(max_pages=args.pages, delay=args.delay)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    LOGGER.info("Saved %s rows to %s", len(df), output)


if __name__ == "__main__":
    main()
