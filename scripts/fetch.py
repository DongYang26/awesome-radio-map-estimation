#!/usr/bin/env python3
"""Fetch candidate papers from arXiv and Semantic Scholar.

Queries the four subfield keyword groups defined in the project spec:
  - REM          (Radio Environment Map / Radio Map Estimation)
  - Spectrum-Cartography
  - Pathloss
  - CKM          (Channel Knowledge Map)

Each group is searched on both arXiv and Semantic Scholar.  Results are
date-windowed to the last N days (default: 30).  A polite sleep is applied
between every API call.

Output is JSON — a list of raw candidate dicts — written to stdout or to a
file with ``-o / --output``.

Usage:
    python scripts/fetch.py [--days 30] [--max-per-query 50] [-o candidates.json]
    python scripts/fetch.py --help
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

# Make `scripts/lib` importable when called as `python scripts/fetch.py`
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lib.sources import fetch_arxiv, fetch_s2  # noqa: E402

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Keyword groups (from spec §Automation)
# ---------------------------------------------------------------------------

KEYWORD_GROUPS: dict[str, list[str]] = {
    "REM": [
        "radio environment map estimation",
        "radio map estimation deep learning",
        "radio propagation map neural network",
        "RSS map reconstruction",
    ],
    "spectrum-cartography": [
        "spectrum cartography",
        "spectrum map estimation",
        "power spectral density map",
        "radio frequency map",
        "spectrum sensing map",
    ],
    "pathloss": [
        "pathloss map prediction",
        "path loss prediction machine learning",
        "propagation loss map neural network",
        "coverage map prediction deep learning",
    ],
    "CKM": [
        "channel knowledge map",
        "channel map construction",
        "channel gain map estimation",
        "environment-aware channel prediction",
    ],
}

# Inter-query sleep (seconds) — polite pacing beyond the per-source sleep
_INTER_QUERY_SLEEP = 1.0


# ---------------------------------------------------------------------------
# Core fetch logic
# ---------------------------------------------------------------------------

def fetch_all(
    days: int = 30,
    max_per_query: int = 50,
    s2_api_key: str | None = None,
    rate_limit_sleep_arxiv: float = 3.0,
    rate_limit_sleep_s2: float = 1.0,
) -> list[dict]:
    """Run all keyword groups on both APIs and return a flat list of candidates.

    Candidates from different queries may overlap; ``dedup.py`` handles de-
    duplication against the existing corpus.  Intra-fetch near-duplicates
    (same arXiv id seen in two queries) are collapsed here by arXiv id so the
    output list is already deduplicated by arXiv id.
    """
    all_candidates: list[dict] = []
    seen_arxiv_ids: set[str] = set()

    for group_name, queries in KEYWORD_GROUPS.items():
        logger.info("=== Group: %s ===", group_name)
        for query in queries:
            # arXiv
            logger.info("  arXiv: %s", query)
            arxiv_results = fetch_arxiv(
                query,
                max_results=max_per_query,
                days=days,
                rate_limit_sleep=rate_limit_sleep_arxiv,
            )
            for c in arxiv_results:
                aid = c.get("arxiv_id")
                if aid and aid in seen_arxiv_ids:
                    continue
                c["_group"] = group_name
                all_candidates.append(c)
                if aid:
                    seen_arxiv_ids.add(aid)

            time.sleep(_INTER_QUERY_SLEEP)

            # Semantic Scholar
            logger.info("  S2: %s", query)
            s2_results = fetch_s2(
                query,
                limit=max_per_query,
                rate_limit_sleep=rate_limit_sleep_s2,
                s2_api_key=s2_api_key,
            )
            for c in s2_results:
                aid = c.get("arxiv_id")
                if aid and aid in seen_arxiv_ids:
                    continue
                c["_group"] = group_name
                all_candidates.append(c)
                if aid:
                    seen_arxiv_ids.add(aid)

            time.sleep(_INTER_QUERY_SLEEP)

    logger.info("Total raw candidates after intra-fetch dedup: %d", len(all_candidates))
    return all_candidates


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Fetch candidate papers from arXiv and Semantic Scholar "
            "using the four RME subfield keyword groups."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--days",
        type=int,
        default=30,
        metavar="N",
        help="Include papers submitted within the last N days.",
    )
    p.add_argument(
        "--max-per-query",
        type=int,
        default=50,
        metavar="N",
        help="Maximum results per query per API.",
    )
    p.add_argument(
        "-o", "--output",
        default=None,
        metavar="FILE",
        help="Write JSON output to FILE instead of stdout.",
    )
    p.add_argument(
        "--s2-api-key",
        default=None,
        metavar="KEY",
        help=(
            "Semantic Scholar API key for higher rate limits. "
            "Falls back to the S2_API_KEY environment variable."
        ),
    )
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    s2_key = args.s2_api_key or os.environ.get("S2_API_KEY")

    candidates = fetch_all(
        days=args.days,
        max_per_query=args.max_per_query,
        s2_api_key=s2_key,
    )

    output = json.dumps(candidates, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Wrote {len(candidates)} candidates to {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
