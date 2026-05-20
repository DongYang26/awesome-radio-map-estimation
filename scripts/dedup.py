#!/usr/bin/env python3
"""Deduplicate candidate papers against the existing corpus in data/papers/.

Reads a JSON list of candidate dicts (from ``fetch.py``) and drops any
candidate that is already present in the corpus, using two checks:

  1. **Exact arXiv-id match** — candidate ``arxiv_id`` equals any existing
     paper's ``id`` (the schema mandates the arXiv id as the ``id`` field).
  2. **Fuzzy title match** — ``difflib.SequenceMatcher`` ratio >= 0.9 between
     the candidate title and any existing paper title (case-insensitive,
     whitespace-normalised).  This catches the same paper submitted under a
     slightly different title, or a preprint-vs-published discrepancy.

Candidates that pass both checks are written to stdout (or a file) as a JSON
array — the input for ``propose.py``.

Usage:
    python scripts/dedup.py candidates.json [-o new_candidates.json]
    python scripts/fetch.py | python scripts/dedup.py -
    python scripts/dedup.py --help
"""

from __future__ import annotations

import argparse
import difflib
import json
import logging
import sys
from pathlib import Path

# Make `scripts/lib` importable when called as `python scripts/dedup.py`
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lib.loader import load_papers  # noqa: E402

logger = logging.getLogger(__name__)

# Fuzzy-title match threshold: SequenceMatcher ratio must be >= this to be
# considered a duplicate.
FUZZY_TITLE_THRESHOLD = 0.9


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _normalise_title(title: str) -> str:
    """Lowercase and collapse whitespace for consistent comparison."""
    return " ".join(title.lower().split())


def _is_fuzzy_duplicate(candidate_title: str, existing_titles: list[str]) -> bool:
    """Return True if *candidate_title* fuzzy-matches any title in *existing_titles*."""
    norm_candidate = _normalise_title(candidate_title)
    for existing in existing_titles:
        ratio = difflib.SequenceMatcher(
            None, norm_candidate, existing, autojunk=False
        ).ratio()
        if ratio >= FUZZY_TITLE_THRESHOLD:
            return True
    return False


# ---------------------------------------------------------------------------
# Core dedup logic
# ---------------------------------------------------------------------------

def build_corpus_index(papers: list[dict]) -> tuple[set[str], list[str]]:
    """Build lookup structures from the loaded corpus.

    Returns:
        A tuple of:
        - ``arxiv_ids``: set of existing arXiv ids (from the paper ``id`` field).
        - ``norm_titles``: list of normalised existing titles.
    """
    arxiv_ids: set[str] = set()
    norm_titles: list[str] = []

    for paper in papers:
        pid = paper.get("id")
        if isinstance(pid, str) and pid:
            arxiv_ids.add(pid)
        title = paper.get("title")
        if isinstance(title, str) and title:
            norm_titles.append(_normalise_title(title))

    return arxiv_ids, norm_titles


def deduplicate(
    candidates: list[dict],
    papers: list[dict] | None = None,
) -> list[dict]:
    """Filter *candidates* to only those not already present in the corpus.

    Args:
        candidates: List of candidate dicts (as returned by ``fetch.py``).
        papers:     Pre-loaded corpus papers.  If ``None``, ``load_papers()``
                    is called automatically.

    Returns:
        A list of candidates that are genuinely new.
    """
    if papers is None:
        papers = load_papers()

    arxiv_ids, norm_titles = build_corpus_index(papers)

    new_candidates: list[dict] = []
    for c in candidates:
        aid = c.get("arxiv_id")
        title = c.get("title") or ""

        # 1. Exact arXiv-id match
        if aid and aid in arxiv_ids:
            logger.debug("DROP (exact id match): %s — %s", aid, title)
            continue

        # 2. Fuzzy title match
        if title and _is_fuzzy_duplicate(title, norm_titles):
            logger.debug("DROP (fuzzy title match): %s", title)
            continue

        new_candidates.append(c)
        # Add to in-memory index so within-batch duplicates are also caught
        if aid:
            arxiv_ids.add(aid)
        if title:
            norm_titles.append(_normalise_title(title))

    logger.info(
        "Dedup: %d candidates in, %d new (dropped %d duplicates)",
        len(candidates),
        len(new_candidates),
        len(candidates) - len(new_candidates),
    )
    return new_candidates


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Drop candidate papers already present in data/papers/. "
            "Reads a JSON list from a file or stdin ('-')."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "input",
        nargs="?",
        default="-",
        metavar="FILE",
        help="JSON candidates file from fetch.py, or '-' to read from stdin.",
    )
    p.add_argument(
        "-o", "--output",
        default=None,
        metavar="FILE",
        help="Write filtered JSON to FILE instead of stdout.",
    )
    p.add_argument(
        "--fuzzy-threshold",
        type=float,
        default=FUZZY_TITLE_THRESHOLD,
        metavar="RATIO",
        help=(
            "SequenceMatcher ratio threshold for fuzzy title dedup "
            "(0.0–1.0; default: %(default)s)."
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

    # Allow overriding the threshold from CLI
    global FUZZY_TITLE_THRESHOLD  # noqa: PLW0603
    FUZZY_TITLE_THRESHOLD = args.fuzzy_threshold

    # Read candidates
    try:
        if args.input == "-":
            raw = sys.stdin.read()
        else:
            raw = Path(args.input).read_text(encoding="utf-8")
        candidates: list[dict] = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR reading candidates: {exc}", file=sys.stderr)
        return 1

    if not isinstance(candidates, list):
        print("ERROR: expected a JSON array of candidates", file=sys.stderr)
        return 1

    # Load existing corpus and deduplicate
    try:
        papers = load_papers()
    except (ValueError, FileNotFoundError) as exc:
        print(f"ERROR loading corpus: {exc}", file=sys.stderr)
        return 1

    new_candidates = deduplicate(candidates, papers=papers)

    output = json.dumps(new_candidates, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(
            f"Wrote {len(new_candidates)} new candidates to {args.output}",
            file=sys.stderr,
        )
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
