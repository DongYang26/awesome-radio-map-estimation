"""Tests for scripts/validate.py.

Covers both halves of the validator:

  * JSON-Schema validation — a good fixture passes; bad fixtures (unknown enum
    value, missing required field) each fail.
  * Cross-file integrity — a broken cross-reference and a duplicate id each
    produce a validation error.

The tests reuse validate.py's own building blocks (``_load_schema``,
``_validate_instance``, ``check_paper_ids``, ``check_references``) so they
exercise the exact code path the CLI runs, rather than a re-implementation.
"""

from __future__ import annotations

from pathlib import Path

import yaml

import validate

FIXTURES = Path(__file__).resolve().parent / "fixtures"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> object:
    """Load a YAML fixture file."""
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _schema_errors(instance: object, schema_name: str) -> list[str]:
    """Validate an instance against a named schema; return error messages."""
    schema = validate._load_schema(schema_name)
    errors: list[str] = []
    validate._validate_instance("fixture", instance, schema, errors)
    return errors


def _as_paper(path: Path) -> dict:
    """Load a paper fixture and attach the loader's ``_stem`` key."""
    data = _load_yaml(path)
    assert isinstance(data, dict)
    data["_stem"] = path.stem
    return data


# ---------------------------------------------------------------------------
# Schema validation — good fixture passes
# ---------------------------------------------------------------------------

def test_good_paper_passes_schema():
    """A well-formed paper fixture produces zero schema errors."""
    paper = _load_yaml(FIXTURES / "good_papers" / "good-paper.yml")
    assert isinstance(paper, dict)
    errors = _schema_errors(paper, "paper.schema.json")
    assert errors == [], f"expected good paper to pass, got: {errors}"


def test_good_taxonomy_passes_schema():
    """A well-formed taxonomy fixture produces zero schema errors."""
    taxonomy = _load_yaml(FIXTURES / "cross" / "taxonomy-good.yml")
    errors = _schema_errors(taxonomy, "taxonomy.schema.json")
    assert errors == [], f"expected good taxonomy to pass, got: {errors}"


def test_good_datasets_passes_schema():
    """A well-formed datasets fixture produces zero schema errors."""
    datasets = _load_yaml(FIXTURES / "cross" / "datasets-good.yml")
    errors = _schema_errors(datasets, "datasets.schema.json")
    assert errors == [], f"expected good datasets to pass, got: {errors}"


def test_good_reading_path_passes_schema():
    """A well-formed reading-path fixture produces zero schema errors."""
    reading_path = _load_yaml(FIXTURES / "cross" / "reading-path-good.yml")
    errors = _schema_errors(reading_path, "reading-path.schema.json")
    assert errors == [], f"expected good reading-path to pass, got: {errors}"


# ---------------------------------------------------------------------------
# Schema validation — bad fixtures fail
# ---------------------------------------------------------------------------

def test_unknown_enum_value_fails():
    """A paper with an out-of-enum 'subfield' value fails schema validation."""
    paper = _load_yaml(FIXTURES / "bad_papers" / "unknown-enum.yml")
    errors = _schema_errors(paper, "paper.schema.json")
    assert errors, "expected the unknown-enum paper to fail validation"
    assert any("subfield" in e for e in errors), errors


def test_missing_required_field_fails():
    """A paper missing the required 'year' field fails schema validation."""
    paper = _load_yaml(FIXTURES / "bad_papers" / "missing-required.yml")
    errors = _schema_errors(paper, "paper.schema.json")
    assert errors, "expected the missing-required paper to fail validation"
    assert any("year" in e for e in errors), errors


def test_bad_taxonomy_node_id_fails():
    """A taxonomy node whose id breaks the kebab-case pattern fails validation."""
    taxonomy = _load_yaml(FIXTURES / "cross" / "taxonomy-bad.yml")
    errors = _schema_errors(taxonomy, "taxonomy.schema.json")
    assert errors, "expected the bad taxonomy node to fail validation"


# ---------------------------------------------------------------------------
# Cross-file integrity — duplicate id
# ---------------------------------------------------------------------------

def test_duplicate_id_fails():
    """Two paper files sharing one id produce a duplicate-id error."""
    good = _load_yaml(FIXTURES / "good_papers" / "good-paper.yml")
    assert isinstance(good, dict)
    # Two dicts with the SAME id but DIFFERENT filename stems.
    paper_a = dict(good, _stem="paper-one")
    paper_b = dict(good, _stem="paper-two")
    errors: list[str] = []
    validate.check_paper_ids([paper_a, paper_b], errors)
    assert errors, "expected a duplicate-id error"
    assert any("duplicate id" in e for e in errors), errors


def test_id_not_matching_stem_fails():
    """A paper whose id differs from its filename stem produces an error."""
    good = _load_yaml(FIXTURES / "good_papers" / "good-paper.yml")
    assert isinstance(good, dict)
    mismatched = dict(good, _stem="a-different-stem")  # id stays 'good-paper'
    errors: list[str] = []
    validate.check_paper_ids([mismatched], errors)
    assert errors, "expected an id-vs-stem mismatch error"
    assert any("does not match id" in e for e in errors), errors


# ---------------------------------------------------------------------------
# Cross-file integrity — broken references
# ---------------------------------------------------------------------------

def test_broken_dataset_paper_reference_fails():
    """A datasets papers_using id with no matching paper produces an error."""
    paper = _as_paper(FIXTURES / "good_papers" / "good-paper.yml")
    datasets = _load_yaml(FIXTURES / "cross" / "datasets-broken-ref.yml")
    reading_path = {"steps": []}
    paper_ids = {paper["id"]}
    errors: list[str] = []
    validate.check_references([paper], datasets, reading_path, paper_ids, errors)
    assert errors, "expected a broken dataset->paper reference error"
    assert any("this-paper-does-not-exist" in e for e in errors), errors


def test_broken_reading_path_reference_fails():
    """A reading-path paper_id with no matching paper produces an error."""
    paper = _as_paper(FIXTURES / "good_papers" / "good-paper.yml")
    datasets = {"datasets": []}
    reading_path = _load_yaml(FIXTURES / "cross" / "reading-path-broken-ref.yml")
    paper_ids = {paper["id"]}
    errors: list[str] = []
    validate.check_references([paper], datasets, reading_path, paper_ids, errors)
    assert errors, "expected a broken reading-path->paper reference error"
    assert any("nonexistent-paper-id" in e for e in errors), errors


def test_broken_paper_dataset_reference_fails():
    """A paper's datasets[] entry with no matching dataset produces an error."""
    paper = _as_paper(FIXTURES / "good_papers" / "good-paper.yml")
    paper["datasets"] = ["no-such-dataset"]
    datasets = {"datasets": [{"id": "real-dataset", "name": "Real",
                              "description": "x", "link": "https://e.com"}]}
    reading_path = {"steps": []}
    paper_ids = {paper["id"]}
    errors: list[str] = []
    validate.check_references([paper], datasets, reading_path, paper_ids, errors)
    assert errors, "expected a broken paper->dataset reference error"
    assert any("no-such-dataset" in e for e in errors), errors


def test_good_cross_references_pass():
    """A self-consistent mini-corpus produces zero cross-reference errors."""
    paper = _as_paper(FIXTURES / "good_papers" / "good-paper.yml")
    datasets = _load_yaml(FIXTURES / "cross" / "datasets-good.yml")
    reading_path = _load_yaml(FIXTURES / "cross" / "reading-path-good.yml")
    errors: list[str] = []
    paper_ids = validate.check_paper_ids([paper], errors)
    validate.check_references([paper], datasets, reading_path, paper_ids, errors)
    assert errors == [], f"expected a clean mini-corpus, got: {errors}"


# ---------------------------------------------------------------------------
# End-to-end: the real corpus must validate
# ---------------------------------------------------------------------------

def test_real_corpus_validates():
    """validate.main() exits 0 on the actual data/ corpus."""
    assert validate.main() == 0
