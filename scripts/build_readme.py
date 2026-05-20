#!/usr/bin/env python3
"""Regenerate the auto-generated sections of README.md from the YAML corpus.

Run from the repo root:

    python scripts/build_readme.py

Only the content between each ``<!-- AUTO:X START -->`` / ``<!-- AUTO:X END -->``
marker pair is rewritten, for X in: badges, stats, taxonomy, papers, datasets.
Everything outside the markers (the hand-written intro, scope table, contributing
and license sections) is preserved byte-for-byte.

The generator is deterministic and idempotent: running it twice produces a
byte-identical file. ``deploy.yml`` pairs this with a ``git diff --quiet`` guard
so unchanged data yields no commit.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# --- robust import of the shared loader + stats ---------------------------
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lib.loader import (  # noqa: E402
    REPO_ROOT,
    load_datasets,
    load_papers,
    load_taxonomy,
)
from stats import compute_stats  # noqa: E402

README_PATH = REPO_ROOT / "README.md"

# GitHub Pages / repo coordinates used for badges.
GH_OWNER = "DongYang26"
GH_REPO = "awesome-radio-map-estimation"

# Section keys, in the order they appear in README.md.
SECTION_KEYS = ["badges", "stats", "taxonomy", "papers", "datasets"]

# Human-readable labels for the four subfield enum values, used as headings in
# the papers section. Order here defines the section order.
SUBFIELD_LABELS: dict[str, str] = {
    "REM": "Radio Environment Maps (REM)",
    "spectrum-cartography": "Spectrum Cartography",
    "pathloss-prediction": "Pathloss Prediction",
    "CKM": "Channel Knowledge Maps (CKM)",
}


# ---------------------------------------------------------------------------
# Marker handling
# ---------------------------------------------------------------------------

def _marker_pattern(key: str) -> re.Pattern:
    """Build a regex that captures the content between a marker pair.

    Group 1 = the opening marker line, group 2 = the inner content, group 3 =
    the closing marker line. The inner content is replaced; the markers are
    kept verbatim so the file structure is preserved.
    """
    start = re.escape(f"<!-- AUTO:{key} START -->")
    end = re.escape(f"<!-- AUTO:{key} END -->")
    return re.compile(
        rf"({start})(.*?)({end})",
        re.DOTALL,
    )


def replace_section(text: str, key: str, body: str) -> str:
    """Replace the inner content of one AUTO:key marker pair with ``body``.

    The body is wrapped in surrounding newlines so the markers always sit on
    their own lines, which keeps the output stable and idempotent. The matched
    marker lines (groups 1 and 3) are spliced back verbatim — the function
    builds the replacement string directly rather than relying on regex
    backreferences, so a body containing characters like '\\1' cannot corrupt
    the output.
    """
    pattern = _marker_pattern(key)
    if not pattern.search(text):
        raise ValueError(
            f"README.md is missing the '<!-- AUTO:{key} START/END -->' marker pair"
        )

    def _sub(match: re.Match) -> str:
        open_marker, _old, close_marker = match.group(1), match.group(2), match.group(3)
        if body:
            return f"{open_marker}\n{body}\n{close_marker}"
        return f"{open_marker}\n{close_marker}"

    return pattern.sub(_sub, text, count=1)


# ---------------------------------------------------------------------------
# Section renderers — each returns the inner markdown body (no markers)
# ---------------------------------------------------------------------------

def render_badges(papers: list[dict]) -> str:
    """Render shields.io badges: CI, GitHub Pages, license, paper count."""
    repo = f"{GH_OWNER}/{GH_REPO}"
    pages_url = f"https://{GH_OWNER.lower()}.github.io/{GH_REPO}/"
    n = len(papers)
    badges = [
        f"[![CI](https://github.com/{repo}/actions/workflows/validate.yml/"
        f"badge.svg)](https://github.com/{repo}/actions/workflows/validate.yml)",
        f"[![Deploy](https://github.com/{repo}/actions/workflows/deploy.yml/"
        f"badge.svg)](https://github.com/{repo}/actions/workflows/deploy.yml)",
        f"[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-"
        f"brightgreen)]({pages_url})",
        "[![Code License: MIT](https://img.shields.io/badge/Code%20License-"
        "MIT-blue.svg)](LICENSE)",
        "[![Data License: CC-BY-4.0](https://img.shields.io/badge/"
        "Data%20License-CC--BY--4.0-blue.svg)](LICENSE-DATA)",
        f"![Papers](https://img.shields.io/badge/papers-{n}-informational)",
    ]
    return "\n".join(badges)


def render_stats(papers: list[dict]) -> str:
    """Render a compact summary line from the aggregated statistics."""
    stats = compute_stats(papers)
    totals = stats["totals"]
    years = stats["papers_per_year"]
    subfields = stats["subfield_distribution"]

    parts = [
        f"**{totals['papers']}** papers",
        f"**{totals['subfields']}** subfields",
        f"**{totals['milestones']}** milestone papers",
    ]
    line1 = " · ".join(parts)

    if years:
        year_keys = sorted(int(y) for y in years)
        span = f"{year_keys[0]}–{year_keys[-1]}"
    else:
        span = "n/a"

    subfield_bits = ", ".join(
        f"{SUBFIELD_LABELS.get(k, k)}: {subfields[k]}"
        for k in sorted(subfields)
    )

    line2 = f"Coverage spans **{span}**."
    line3 = f"By subfield — {subfield_bits}." if subfield_bits else ""

    lines = [line1, "", line2]
    if line3:
        lines.append(line3)
    return "\n".join(lines)


def _render_taxonomy_nodes(nodes: list, depth: int, out: list[str]) -> None:
    """Recursively render taxonomy nodes as a nested markdown list."""
    indent = "  " * depth
    for node in nodes:
        if not isinstance(node, dict):
            continue
        label = node.get("label", node.get("id", "?"))
        description = node.get("description")
        if description:
            out.append(f"{indent}- **{label}** — {description}")
        else:
            out.append(f"{indent}- **{label}**")
        children = node.get("children") or []
        if children:
            _render_taxonomy_nodes(children, depth + 1, out)


def render_taxonomy(taxonomy: dict) -> str:
    """Render the taxonomy tree as a nested markdown list."""
    nodes = taxonomy.get("taxonomy") or []
    out: list[str] = []
    _render_taxonomy_nodes(nodes, 0, out)
    if not out:
        return "_No taxonomy defined._"
    return "\n".join(out)


def _paper_link(paper: dict) -> str | None:
    """Pick the best canonical link for a paper, or None if it has no link."""
    links = paper.get("links") or {}
    for key in ("arxiv", "project_page", "pdf", "code"):
        value = links.get(key)
        if value:
            return value
    doi = links.get("doi")
    if doi:
        return f"https://doi.org/{doi}"
    return None


def _format_authors(authors: list) -> str:
    """Format an author list compactly: first three names, then 'et al.'."""
    names = [a for a in (authors or []) if isinstance(a, str)]
    if not names:
        return "Unknown"
    if len(names) <= 3:
        return ", ".join(names)
    return ", ".join(names[:3]) + " et al."


def _paper_line(paper: dict) -> str:
    """Render one paper as a markdown list item."""
    title = paper.get("title", "Untitled")
    year = paper.get("year", "")
    authors = _format_authors(paper.get("authors"))
    link = _paper_link(paper)
    milestone = " ⭐" if paper.get("is_milestone") is True else ""
    if link:
        head = f"[{title}]({link})"
    else:
        head = title
    return f"- {head} — {authors}, {year}{milestone}"


def render_papers(papers: list[dict]) -> str:
    """Render papers grouped by subfield, each as a markdown list item.

    Within each subfield papers are ordered newest-first, then by id, so the
    output is deterministic.
    """
    blocks: list[str] = []
    for subfield, heading in SUBFIELD_LABELS.items():
        group = [p for p in papers if p.get("subfield") == subfield]
        group.sort(key=lambda p: (-(p.get("year") or 0), p.get("id") or ""))
        blocks.append(f"### {heading}")
        blocks.append("")
        if group:
            blocks.extend(_paper_line(p) for p in group)
        else:
            blocks.append("_No papers in this subfield yet._")
        blocks.append("")
    # Drop the trailing blank line so the body has no trailing newline; the
    # marker wrapper adds the surrounding newlines.
    while blocks and blocks[-1] == "":
        blocks.pop()
    return "\n".join(blocks)


def render_datasets(datasets: dict) -> str:
    """Render the dataset catalog as a markdown table."""
    rows = datasets.get("datasets") or []
    if not rows:
        return "_No datasets catalogued yet._"

    out = [
        "| Dataset | Description | Papers using |",
        "|---------|-------------|--------------|",
    ]
    for ds in sorted(rows, key=lambda d: d.get("id") or ""):
        if not isinstance(ds, dict):
            continue
        name = ds.get("name", ds.get("id", "?"))
        link = ds.get("link")
        # Collapse any internal whitespace/newlines so the table cell stays
        # on one line.
        description = " ".join((ds.get("description") or "").split())
        n_papers = len(ds.get("papers_using") or [])
        name_cell = f"[{name}]({link})" if link else name
        out.append(f"| {name_cell} | {description} | {n_papers} |")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_readme(text: str, papers: list[dict], taxonomy: dict,
                 datasets: dict) -> str:
    """Return README text with all AUTO sections regenerated from the corpus."""
    bodies: dict[str, str] = {
        "badges": render_badges(papers),
        "stats": render_stats(papers),
        "taxonomy": render_taxonomy(taxonomy),
        "papers": render_papers(papers),
        "datasets": render_datasets(datasets),
    }
    for key in SECTION_KEYS:
        text = replace_section(text, key, bodies[key])
    return text


def main() -> int:
    """Load the corpus, regenerate README.md in place, report what changed."""
    papers = load_papers()
    taxonomy = load_taxonomy()
    datasets = load_datasets()

    original = README_PATH.read_text(encoding="utf-8")
    updated = build_readme(original, papers, taxonomy, datasets)

    if updated == original:
        print("OK: README.md already up to date (no change).")
        return 0

    README_PATH.write_text(updated, encoding="utf-8")
    print(f"OK: regenerated README.md ({len(papers)} papers).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
