#!/usr/bin/env python3
"""Aggregate the paper corpus into site/src/data/stats.json.

Run from the repo root:

    python scripts/stats.py

Reads every data/papers/*.yml via the shared loader, computes summary
statistics, and writes them as deterministic JSON to site/src/data/stats.json
(creating the directory if needed). The Astro trends page hard-depends on this
file; build_readme.py reuses ``compute_stats`` for the README stat line.

Output shape::

    {
      "papers_per_year":          { "<year>": <count>, ... },
      "method_family_by_year":    { "<year>": { "<family>": <count>, ... }, ... },
      "subfield_distribution":    { "<subfield>": <count>, ... },
      "method_family_distribution": { "<family>": <count>, ... },
      "totals": {
        "papers":    <int>,
        "milestones":<int>,
        "subfields": <int>
      }
    }
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# --- robust import of the shared loader -----------------------------------
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lib.loader import REPO_ROOT, load_papers  # noqa: E402

STATS_PATH = REPO_ROOT / "site" / "src" / "data" / "stats.json"


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def compute_stats(papers: list[dict]) -> dict:
    """Aggregate a list of paper dicts into the stats structure.

    All counters are built with plain dicts and the result is fully sorted so
    repeated runs over the same corpus produce a byte-identical JSON file.
    """
    papers_per_year: dict[str, int] = {}
    method_family_by_year: dict[str, dict[str, int]] = {}
    subfield_distribution: dict[str, int] = {}
    method_family_distribution: dict[str, int] = {}
    milestone_count = 0

    for paper in papers:
        year = paper.get("year")
        family = paper.get("method_family")
        subfield = paper.get("subfield")

        if isinstance(year, int):
            ykey = str(year)
            papers_per_year[ykey] = papers_per_year.get(ykey, 0) + 1
            if family:
                by_fam = method_family_by_year.setdefault(ykey, {})
                by_fam[family] = by_fam.get(family, 0) + 1

        if subfield:
            subfield_distribution[subfield] = subfield_distribution.get(subfield, 0) + 1

        if family:
            method_family_distribution[family] = (
                method_family_distribution.get(family, 0) + 1
            )

        if paper.get("is_milestone") is True:
            milestone_count += 1

    def _sorted(d: dict) -> dict:
        return {k: d[k] for k in sorted(d)}

    return {
        "papers_per_year": _sorted(papers_per_year),
        "method_family_by_year": {
            year: _sorted(method_family_by_year[year])
            for year in sorted(method_family_by_year)
        },
        "subfield_distribution": _sorted(subfield_distribution),
        "method_family_distribution": _sorted(method_family_distribution),
        "totals": {
            "papers": len(papers),
            "milestones": milestone_count,
            "subfields": len(subfield_distribution),
        },
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """Compute stats from the corpus and write site/src/data/stats.json."""
    papers = load_papers()
    stats = compute_stats(papers)

    os.makedirs(STATS_PATH.parent, exist_ok=True)
    # Trailing newline + sorted keys keep the file diff-friendly and stable.
    with open(STATS_PATH, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print(
        f"OK: wrote {STATS_PATH.relative_to(REPO_ROOT)} "
        f"({stats['totals']['papers']} papers, "
        f"{stats['totals']['milestones']} milestones, "
        f"{stats['totals']['subfields']} subfields)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
