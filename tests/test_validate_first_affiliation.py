"""Tests for validate.py's first_affiliation cross-reference check.

Regression guard: every ``first_affiliation`` value on a paper must resolve to
an ``id`` in ``data/institutions.yml``. A broken reference must fail CI.
"""

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate import check_references  # noqa: E402


def _paper(stem: str, first_aff: str | None = None) -> dict:
    p = {
        "_stem": stem,
        "id": stem,
        "title": "x",
        "authors": ["a"],
        "year": 2024,
        "subfield": "REM",
        "method_family": "learning-based",
        "task": ["other"],
        "input_modality": "sparse-measurements",
        "environment": "outdoor",
        "dimensionality": "2D",
        "supervision": "supervised",
        "added_date": "2024-01-01",
    }
    if first_aff is not None:
        p["first_affiliation"] = first_aff
    return p


def _empty_refs():
    return {"datasets": []}, {"steps": []}


def test_paper_without_first_affiliation_passes():
    """first_affiliation is optional; absence is fine."""
    papers = [_paper("a")]
    ds, rp = _empty_refs()
    insts = {"institutions": []}
    errors: list[str] = []
    check_references(papers, ds, rp, {"a"}, errors, institutions=insts)
    assert errors == []


def test_paper_with_known_first_affiliation_passes():
    papers = [_paper("a", "mit")]
    ds, rp = _empty_refs()
    insts = {
        "institutions": [
            {"id": "mit", "name": "MIT", "country": "USA", "lat": 42.36, "lon": -71.09}
        ]
    }
    errors: list[str] = []
    check_references(papers, ds, rp, {"a"}, errors, institutions=insts)
    assert errors == []


def test_paper_with_unknown_first_affiliation_fails():
    """A first_affiliation referencing an id not in institutions.yml must fail."""
    papers = [_paper("a", "nonexistent-school")]
    ds, rp = _empty_refs()
    insts = {
        "institutions": [
            {"id": "mit", "name": "MIT", "country": "USA", "lat": 42.36, "lon": -71.09}
        ]
    }
    errors: list[str] = []
    check_references(papers, ds, rp, {"a"}, errors, institutions=insts)
    assert any(
        "first_affiliation" in msg and "nonexistent-school" in msg for msg in errors
    ), errors


def test_paper_with_first_affiliation_but_no_catalog_still_fails():
    """A missing catalog must NOT silently let a ref slip through."""
    papers = [_paper("a", "mit")]
    ds, rp = _empty_refs()
    errors: list[str] = []
    check_references(papers, ds, rp, {"a"}, errors, institutions=None)
    assert any("first_affiliation" in msg and "mit" in msg for msg in errors), errors
