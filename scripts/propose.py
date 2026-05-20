#!/usr/bin/env python3
"""Propose candidate YAML stubs for genuinely-new papers.

Reads a JSON list of deduplicated candidate dicts (from ``dedup.py``) and
writes one ``data/papers/<id>.yml`` stub per candidate.

Every *judgement* field (subfield, method_family, method_detail, task,
input_modality, environment, dimensionality, supervision, is_milestone, tldr,
tags) is filled with a heuristic guess derived from keyword matching and is
marked with a ``# TODO: maintainer verify`` YAML comment.  Factual fields
(title, authors, year, venue, abstract, citations, links) are written as-is.

The stubs are schema-shaped so ``validate.py`` can check them.  Note that
heuristically-guessed enum values are chosen from the schema's allowed set, so
they will not trigger enum-validation failures, but maintainer review is still
required to confirm correctness.

Usage:
    python scripts/propose.py new_candidates.json [--output-dir data/papers]
    python scripts/dedup.py candidates.json | python scripts/propose.py -
    python scripts/propose.py --help
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from datetime import date
from pathlib import Path

import yaml

# Make `scripts/lib` importable when called as `python scripts/propose.py`
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lib.loader import REPO_ROOT, load_papers  # noqa: E402

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "papers"

# ---------------------------------------------------------------------------
# Heuristic classification tables
# ---------------------------------------------------------------------------
# Each entry is (compiled regex, value).  The first matching pattern wins.

_SUBFIELD_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bckm\b|channel knowledge map|channel map", re.I), "CKM"),
    (re.compile(r"spectrum cartograph|spectrum map|spectral map|spectrum occupan|power spectral density map", re.I), "spectrum-cartography"),
    (re.compile(r"path[\s-]?loss|propagation loss|coverage map|coverage prediction", re.I), "pathloss-prediction"),
    (re.compile(r"radio environment map|radio map|rem\b|signal map|rss map|radio propagation map", re.I), "REM"),
]

_METHOD_FAMILY_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bray[\s-]trac|site-specific|electromagnetic simulat", re.I), "model-based"),
    (re.compile(r"\bkriging\b|interpolat|idw\b|inverse distance", re.I), "interpolation"),
    (re.compile(r"neural|deep learn|cnn|gnn|transformer|gan\b|generative|diffusion|autoencoder|machine learn|data-driven|learning-based", re.I), "learning-based"),
]

_METHOD_DETAIL_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bdiffusion model|score-based|denoising diffusion", re.I), "Diffusion"),
    (re.compile(r"\btransformer|attention mechanism|self-attention|bert|vit\b", re.I), "Transformer"),
    (re.compile(r"\bgnn\b|graph neural|graph convolution", re.I), "GNN"),
    (re.compile(r"\bgan\b|generative adversarial", re.I), "GAN"),
    (re.compile(r"\binr\b|implicit neural|neural radiance|nerf", re.I), "INR"),
    (re.compile(r"\bautoencoder|auto-encoder|vae\b|variational", re.I), "autoencoder"),
    (re.compile(r"\brnn\b|lstm\b|recurrent", re.I), "RNN"),
    (re.compile(r"\bcnn\b|convolutional|unet|u-net|resnet|convnet", re.I), "CNN"),
    (re.compile(r"\bmatrix.completion|matrix factori|low rank", re.I), "matrix-completion"),
    (re.compile(r"\bgaussian process|kriging", re.I), "Gaussian-process"),
    (re.compile(r"\bkriging\b", re.I), "Kriging"),
    (re.compile(r"\bidw\b|inverse distance", re.I), "IDW"),
    (re.compile(r"\bray[\s-]trac", re.I), "ray-tracing"),
]

_TASK_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"spectrum occupan|spectrum sensing", re.I), "spectrum-occupancy"),
    (re.compile(r"spectrum cartograph|spectrum map", re.I), "spectrum-cartography"),
    (re.compile(r"channel gain|channel map|channel knowledge", re.I), "channel-gain-prediction"),
    (re.compile(r"path[\s-]?loss|propagation loss", re.I), "pathloss-prediction"),
    (re.compile(r"coverage map|coverage prediction", re.I), "coverage-prediction"),
    (re.compile(r"radio environment map|rem\b|rss map|radio map", re.I), "REM-construction"),
    (re.compile(r"signal strength|rssi|received signal|signal level", re.I), "signal-strength-estimation"),
]

_INPUT_MODALITY_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"building map|environment map|city map|urban map|floorplan|3d map|geographic", re.I), "environment-map"),
    (re.compile(r"sparse measurement|crowdsource|drive test|sample point", re.I), "sparse-measurements"),
]

_ENVIRONMENT_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bindoor\b|indoor environment|indoor propagat", re.I), "indoor"),
    (re.compile(r"\boutdoor\b|urban|suburban|rural|city|street", re.I), "outdoor"),
]

_SUPERVISION_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"self-supervised|self supervised|contrastive|pretext task", re.I), "self-supervised"),
    (re.compile(r"semi-supervised|semi supervised", re.I), "semi-supervised"),
    (re.compile(r"unsupervised|clustering|anomaly detect", re.I), "unsupervised"),
]


# ---------------------------------------------------------------------------
# Heuristic helpers
# ---------------------------------------------------------------------------

def _search_text(candidate: dict) -> str:
    """Concatenate title + abstract for keyword scanning."""
    title = candidate.get("title") or ""
    abstract = candidate.get("abstract") or ""
    return f"{title} {abstract}"


def _guess_subfield(text: str) -> str:
    for pattern, value in _SUBFIELD_RULES:
        if pattern.search(text):
            return value
    return "REM"  # safe default for this domain


def _guess_method_family(text: str) -> str:
    for pattern, value in _METHOD_FAMILY_RULES:
        if pattern.search(text):
            return value
    return "learning-based"  # most common in recent literature


def _guess_method_details(text: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for pattern, value in _METHOD_DETAIL_RULES:
        if value not in seen and pattern.search(text):
            found.append(value)
            seen.add(value)
    return found or ["other"]


def _guess_tasks(text: str, subfield: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for pattern, value in _TASK_RULES:
        if value not in seen and pattern.search(text):
            found.append(value)
            seen.add(value)
    if not found:
        # Fall back to a task consistent with the subfield guess
        fallback_map = {
            "REM": "REM-construction",
            "spectrum-cartography": "spectrum-cartography",
            "pathloss-prediction": "pathloss-prediction",
            "CKM": "channel-gain-prediction",
        }
        found.append(fallback_map.get(subfield, "other"))
    return found


def _guess_input_modality(text: str) -> str:
    for pattern, value in _INPUT_MODALITY_RULES:
        if pattern.search(text):
            return value
    return "sparse-measurements"


def _guess_environment(text: str) -> str:
    results: set[str] = set()
    for pattern, value in _ENVIRONMENT_RULES:
        if pattern.search(text):
            results.add(value)
    if "indoor" in results and "outdoor" in results:
        return "both"
    if results:
        return next(iter(results))
    return "outdoor"  # most common in the field


def _guess_supervision(text: str) -> str:
    for pattern, value in _SUPERVISION_RULES:
        if pattern.search(text):
            return value
    return "supervised"


def _guess_dimensionality(text: str) -> str:
    if re.search(r"\b3d\b|three-dimensional|3-d|height|altitude|floor", text, re.I):
        return "3D"
    return "2D"


def _slugify_title(title: str) -> str:
    """Derive a filename-safe slug from a paper title."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:60] or "unknown-paper"


def _sanitise_id(arxiv_id: str | None, title: str) -> str:
    """Derive a filename-safe id from arXiv id or a slugified title.

    The ``arxiv_id`` is attacker-controllable (it comes from third-party
    arXiv/Semantic Scholar APIs), so it is charset-filtered and rejected if it
    could traverse the filesystem; the title slug is used as a safe fallback.
    The result always matches the schema id pattern ``^[a-z0-9._-]+$``.
    """
    if arxiv_id:
        cleaned = re.sub(r"[^a-z0-9._-]", "", arxiv_id.strip().lower())
        if cleaned and cleaned not in (".", "..") and "/" not in cleaned:
            return cleaned
    return _slugify_title(title)


# ---------------------------------------------------------------------------
# YAML stub builder
# ---------------------------------------------------------------------------

# Mapping from field name to inline TODO comment
_TODO = "  # TODO: maintainer verify"


def _yaml_str(value: str, indent: int = 0) -> str:
    """Render a YAML scalar string, quoting via the library emitter.

    Delegating to ``yaml.safe_dump`` ensures every case that requires quoting
    (leading indicator characters such as ``-?@&*!|>%#``, leading/trailing
    whitespace, and YAML-reserved words like ``true``/``null``/numbers) is
    handled correctly and the round-trip is loss-free.
    """
    emitted = yaml.safe_dump(
        value, default_flow_style=True, allow_unicode=True, width=float("inf")
    ).rstrip()
    # safe_dump appends a "..." document-end marker for bare scalars; drop it.
    if emitted.endswith("..."):
        emitted = emitted[:-3].rstrip()
    prefix = " " * indent
    return f"{prefix}{emitted}"


def build_stub(candidate: dict) -> tuple[str, str]:
    """Build a YAML stub string for *candidate*.

    Returns:
        A tuple of ``(paper_id, yaml_text)``.
    """
    arxiv_id = candidate.get("arxiv_id")
    title = candidate.get("title") or "Unknown Title"
    authors: list[str] = candidate.get("authors") or []
    year = candidate.get("year")
    venue = candidate.get("venue") or ""
    abstract = candidate.get("abstract") or ""
    citations = candidate.get("citations") or 0
    links: dict = candidate.get("links") or {}

    paper_id = _sanitise_id(arxiv_id, title)

    text = _search_text(candidate)
    subfield = _guess_subfield(text)
    method_family = _guess_method_family(text)
    method_details = _guess_method_details(text)
    tasks = _guess_tasks(text, subfield)
    input_modality = _guess_input_modality(text)
    environment = _guess_environment(text)
    dimensionality = _guess_dimensionality(text)
    supervision = _guess_supervision(text)

    today = date.today().isoformat()

    lines: list[str] = []

    def w(line: str = "") -> None:
        lines.append(line)

    # --- Factual fields (no TODO) ---
    w(f"id: {_yaml_str(paper_id)}")
    w(f"title: {_yaml_str(title)}")
    w("authors:")
    for author in authors:
        w(f"  - {_yaml_str(author)}")
    if not authors:
        w("  - Unknown  # TODO: maintainer verify")
    w(f"year: {year if year is not None else 0}  # TODO: maintainer verify" if year is None else f"year: {year}")
    if venue:
        w(f"venue: {_yaml_str(venue)}")
    if abstract:
        # Emit the abstract as a single quoted scalar via the YAML emitter.
        # (Splitting on ". " would silently drop sentence-ending periods.)
        w(f"abstract: {_yaml_str(abstract)}")
    w(f"tldr: ''  {_TODO}")

    # links
    w("links:")
    arxiv_url = links.get("arxiv")
    pdf_url = links.get("pdf")
    doi = links.get("doi")
    if arxiv_url:
        w(f"  arxiv: {_yaml_str(arxiv_url)}")
    if pdf_url:
        w(f"  pdf: {_yaml_str(pdf_url)}")
    if doi:
        w(f"  doi: {_yaml_str(doi)}")
    if not (arxiv_url or pdf_url or doi):
        w("  arxiv: ''  # TODO: maintainer verify")

    # --- Judgement fields (all marked TODO) ---
    w(f"subfield: {_yaml_str(subfield)}{_TODO}")
    w(f"method_family: {_yaml_str(method_family)}{_TODO}")
    w("method_detail:")
    for md in method_details:
        w(f"  - {_yaml_str(md)}{_TODO}")
    w("task:")
    for t in tasks:
        w(f"  - {_yaml_str(t)}{_TODO}")
    w(f"input_modality: {_yaml_str(input_modality)}{_TODO}")
    w(f"environment: {_yaml_str(environment)}{_TODO}")
    w(f"dimensionality: {_yaml_str(dimensionality)}{_TODO}")
    w(f"supervision: {_yaml_str(supervision)}{_TODO}")

    # Optional fields
    if isinstance(citations, int) and citations > 0:
        w(f"citations: {citations}")
    w(f"is_milestone: false{_TODO}")
    w(f"tags: []{_TODO}")
    w(f"added_date: '{today}'")

    return paper_id, "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Core propose logic
# ---------------------------------------------------------------------------

def propose(
    candidates: list[dict],
    output_dir: Path,
    overwrite: bool = False,
) -> list[Path]:
    """Write one YAML stub per candidate into *output_dir*.

    Args:
        candidates:  List of new-candidate dicts (already deduped by ``dedup.py``).
        output_dir:  Directory to write stubs into (created if absent).
        overwrite:   If ``True``, overwrite existing files.  Default is to skip.

    Returns:
        List of paths written.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    resolved_output_dir = output_dir.resolve()

    for candidate in candidates:
        paper_id, yaml_text = build_stub(candidate)
        out_path = output_dir / f"{paper_id}.yml"

        # Defence-in-depth: confirm the resolved stub path stays inside
        # output_dir. _sanitise_id already filters traversal sequences, but a
        # containment check guarantees an attacker-controlled id cannot escape.
        resolved_out = out_path.resolve()
        if resolved_output_dir not in resolved_out.parents:
            raise ValueError(
                f"refusing to write outside output dir: {resolved_out} "
                f"(output dir: {resolved_output_dir})"
            )

        if out_path.exists() and not overwrite:
            logger.warning("SKIP (already exists): %s", out_path)
            continue

        out_path.write_text(yaml_text, encoding="utf-8")
        logger.info("WROTE: %s", out_path)
        written.append(out_path)

    return written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Emit candidate data/papers/<id>.yml stubs with heuristic "
            "pre-classification, all judgement fields marked "
            "'# TODO: maintainer verify'."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "input",
        nargs="?",
        default="-",
        metavar="FILE",
        help="JSON new-candidates file from dedup.py, or '-' to read stdin.",
    )
    p.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        metavar="DIR",
        help="Directory to write stub YAML files into.",
    )
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing stub files (default: skip).",
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

    output_dir = Path(args.output_dir)
    written = propose(candidates, output_dir=output_dir, overwrite=args.overwrite)

    print(
        f"Proposed {len(written)} stub(s) in {output_dir}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
