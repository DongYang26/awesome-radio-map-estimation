#!/usr/bin/env python3
"""Validate all YAML data sources against their JSON schemas plus cross-file integrity.

Run from the repo root:

    python scripts/validate.py

Exit code 0 if every check passes, non-zero otherwise. Each failure prints a
precise per-file / per-error message.

Schema validation uses jsonschema with the Draft 2020-12 validator and a
``FormatChecker`` so ``format: uri`` and ``format: date`` are actually enforced.

Cross-file integrity checks (not expressible in JSON Schema):
  (a) each paper file's stem equals its ``id``;
  (b) no duplicate ``id`` values across paper files;
  (c) every referential id resolves:
        - reading-path ``steps[].paper_id``        -> an existing paper id
        - datasets ``datasets[].papers_using[]``   -> an existing paper id
        - datasets ``datasets[].benchmark[].paper_id`` -> an existing paper id
        - papers ``datasets[]`` entries            -> an existing dataset id
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

# --- robust import of the shared loader -----------------------------------
# Works whether invoked as `python scripts/validate.py` from the repo root or
# from inside scripts/. The scripts/ directory is added to sys.path so the
# `lib` package resolves.
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lib.loader import (  # noqa: E402
    DATA_DIR,
    REPO_ROOT,
    load_datasets,
    load_papers,
    load_reading_path,
    load_taxonomy,
)

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover - environment guard
    print("ERROR: the 'jsonschema' package is required. Install with:", file=sys.stderr)
    print("    pip install jsonschema", file=sys.stderr)
    sys.exit(2)

SCHEMA_DIR = REPO_ROOT / "schema"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_schema(name: str) -> dict:
    """Load a JSON schema file from schema/ by filename."""
    path = SCHEMA_DIR / name
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _validator(schema: dict) -> Draft202012Validator:
    """Build a Draft 2020-12 validator with the format checker enabled."""
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _error_location(error) -> str:
    """Render a jsonschema ValidationError's path as a readable dotted location."""
    if not error.absolute_path:
        return "<root>"
    parts = [str(p) for p in error.absolute_path]
    return ".".join(parts)


def _validate_instance(label: str, instance: object, schema: dict,
                        errors: list[str]) -> bool:
    """Validate one instance against a schema; append messages, return ok flag."""
    validator = _validator(schema)
    found = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
    if not found:
        return True
    for err in found:
        errors.append(f"{label}: at '{_error_location(err)}': {err.message}")
    return False


# ---------------------------------------------------------------------------
# Schema-validation passes
# ---------------------------------------------------------------------------

def validate_papers(papers: list[dict], errors: list[str]) -> None:
    """Validate every paper dict against schema/paper.schema.json."""
    schema = _load_schema("paper.schema.json")
    for paper in papers:
        stem = paper.get("_stem", "<unknown>")
        label = f"data/papers/{stem}.yml"
        # The loader injects a private "_stem" key; strip it so the closed
        # schema (additionalProperties: false) does not reject it.
        instance = {k: v for k, v in paper.items() if k != "_stem"}
        _validate_instance(label, instance, schema, errors)


def validate_taxonomy(taxonomy: dict, errors: list[str]) -> None:
    """Validate data/taxonomy.yml against schema/taxonomy.schema.json."""
    schema = _load_schema("taxonomy.schema.json")
    _validate_instance("data/taxonomy.yml", taxonomy, schema, errors)


def validate_datasets(datasets: dict, errors: list[str]) -> None:
    """Validate data/datasets.yml against schema/datasets.schema.json."""
    schema = _load_schema("datasets.schema.json")
    _validate_instance("data/datasets.yml", datasets, schema, errors)


def validate_reading_path(reading_path: dict, errors: list[str]) -> None:
    """Validate data/reading-path.yml against schema/reading-path.schema.json."""
    schema = _load_schema("reading-path.schema.json")
    _validate_instance("data/reading-path.yml", reading_path, schema, errors)


def validate_institutions(institutions: dict, errors: list[str]) -> None:
    """Validate data/institutions.yml against schema/institutions.schema.json."""
    schema = _load_schema("institutions.schema.json")
    _validate_instance("data/institutions.yml", institutions, schema, errors)


def load_institutions() -> dict:
    """Load data/institutions.yml; return an empty catalog if the file is absent.

    The institutions catalog powers the Academic Atlas. It is optional in that
    the corpus can validate without it, but any ``first_affiliation`` on a
    paper must resolve to an entry here — see ``check_references``.
    """
    path = DATA_DIR / "institutions.yml"
    if not path.exists():
        return {"institutions": []}
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data if isinstance(data, dict) else {"institutions": []}


# ---------------------------------------------------------------------------
# Cross-file integrity passes
# ---------------------------------------------------------------------------

def check_paper_ids(papers: list[dict], errors: list[str]) -> set[str]:
    """Check id == filename stem and uniqueness of ids; return the set of ids.

    The returned set contains every id seen (even duplicates collapse to one
    entry) so downstream reference checks can resolve against it.
    """
    seen: dict[str, str] = {}
    ids: set[str] = set()
    for paper in papers:
        stem = paper.get("_stem", "<unknown>")
        label = f"data/papers/{stem}.yml"
        pid = paper.get("id")
        if pid is None:
            # Missing id is already reported by schema validation; skip here.
            continue
        if not isinstance(pid, str):
            continue  # malformed type already reported by schema validation
        # (a) stem must equal id
        if pid != stem:
            errors.append(
                f"{label}: filename stem '{stem}' does not match id '{pid}' "
                f"(the file must be named '{pid}.yml')"
            )
        # (b) no duplicate ids
        if pid in seen:
            errors.append(
                f"{label}: duplicate id '{pid}' — also defined in '{seen[pid]}'"
            )
        else:
            seen[pid] = label
        ids.add(pid)
    return ids


def check_references(papers: list[dict], datasets: dict, reading_path: dict,
                     paper_ids: set[str], errors: list[str],
                     institutions: dict | None = None) -> None:
    """Check that every cross-file id reference resolves to an existing entity.

    If *institutions* is provided, also verifies that every paper's
    ``first_affiliation`` (when set) resolves to an institution ``id``.
    Pass ``None`` (or an empty catalog) and the check is still performed —
    a broken reference to a missing catalog is still a broken reference.
    """
    dataset_list = datasets.get("datasets") or []
    dataset_ids: set[str] = {
        d.get("id") for d in dataset_list
        if isinstance(d, dict) and isinstance(d.get("id"), str)
    }

    # (c1) reading-path steps[].paper_id -> paper id
    for step in reading_path.get("steps") or []:
        if not isinstance(step, dict):
            continue
        pid = step.get("paper_id")
        order = step.get("order", "?")
        if isinstance(pid, str) and pid not in paper_ids:
            errors.append(
                f"data/reading-path.yml: step order={order} references "
                f"unknown paper_id '{pid}'"
            )

    # (c2) datasets[].papers_using[] and datasets[].benchmark[].paper_id -> paper id
    for ds in dataset_list:
        if not isinstance(ds, dict):
            continue
        did = ds.get("id", "<unknown>")
        for pid in ds.get("papers_using") or []:
            if isinstance(pid, str) and pid not in paper_ids:
                errors.append(
                    f"data/datasets.yml: dataset '{did}' papers_using lists "
                    f"unknown paper id '{pid}'"
                )
        for row in ds.get("benchmark") or []:
            if not isinstance(row, dict):
                continue
            pid = row.get("paper_id")
            if isinstance(pid, str) and pid not in paper_ids:
                errors.append(
                    f"data/datasets.yml: dataset '{did}' benchmark row references "
                    f"unknown paper_id '{pid}'"
                )

    # (c3) papers[].datasets[] -> dataset id
    for paper in papers:
        stem = paper.get("_stem", "<unknown>")
        label = f"data/papers/{stem}.yml"
        for did in paper.get("datasets") or []:
            if isinstance(did, str) and did not in dataset_ids:
                errors.append(
                    f"{label}: datasets[] references unknown dataset id '{did}'"
                )

    # (c4) papers[].first_affiliation -> institutions[].id
    inst_ids: set[str] = set()
    if isinstance(institutions, dict):
        for inst in institutions.get("institutions") or []:
            if isinstance(inst, dict) and isinstance(inst.get("id"), str):
                inst_ids.add(inst["id"])
    for paper in papers:
        stem = paper.get("_stem", "<unknown>")
        label = f"data/papers/{stem}.yml"
        fa = paper.get("first_affiliation")
        if isinstance(fa, str) and fa not in inst_ids:
            errors.append(
                f"{label}: first_affiliation references unknown institution id '{fa}'"
            )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """Run all validation passes; return a process exit code."""
    errors: list[str] = []

    # Loading itself can raise on malformed YAML — surface that as a failure.
    try:
        papers = load_papers()
        taxonomy = load_taxonomy()
        datasets = load_datasets()
        reading_path = load_reading_path()
        institutions = load_institutions()
    except (ValueError, FileNotFoundError) as exc:
        print(f"FAIL: could not load data: {exc}", file=sys.stderr)
        return 1

    # Schema validation
    validate_papers(papers, errors)
    validate_taxonomy(taxonomy, errors)
    validate_datasets(datasets, errors)
    validate_reading_path(reading_path, errors)
    validate_institutions(institutions, errors)

    # Cross-file integrity
    paper_ids = check_paper_ids(papers, errors)
    check_references(papers, datasets, reading_path, paper_ids, errors, institutions)

    if errors:
        print(f"FAIL: {len(errors)} validation error(s):", file=sys.stderr)
        for msg in errors:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    n_datasets = len(datasets.get("datasets") or [])
    n_steps = len(reading_path.get("steps") or [])
    n_insts = len(institutions.get("institutions") or [])
    print(
        f"OK: {len(papers)} paper(s), taxonomy, "
        f"{n_datasets} dataset(s), {n_steps} reading-path step(s), "
        f"{n_insts} institution(s) — all valid."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
