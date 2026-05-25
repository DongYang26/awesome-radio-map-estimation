"""Tests for scripts/propose.py — focus on schema-valid stub generation.

Regression guard for the weekly auto-update failure where a candidate with no
arxiv/pdf/doi produced `links.arxiv: ''`, which violates the schema's
`format: uri` + `^https?://` constraints and broke `update-papers.yml`.
"""

import json
from pathlib import Path

import jsonschema
import yaml

from propose import build_stub  # conftest.py puts scripts/ on sys.path

REPO = Path(__file__).resolve().parents[1]
PAPER_SCHEMA = json.loads((REPO / "schema" / "paper.schema.json").read_text())


def _build_and_validate(candidate: dict) -> dict:
    _paper_id, text = build_stub(candidate)
    assert "arxiv: ''" not in text, "must not emit an empty arxiv placeholder"
    data = yaml.safe_load(text)
    jsonschema.validate(
        data, PAPER_SCHEMA, format_checker=jsonschema.FormatChecker()
    )
    return data


def test_stub_without_any_links_is_schema_valid():
    """A candidate with no arxiv/pdf/doi must omit links, not write arxiv: ''."""
    cand = {
        "arxiv_id": None,
        "title": "Spectrum Cartography Using Adaptive Multi-Kernels",
        "authors": ["A. Researcher"],
        "year": 2025,
        "venue": "IEEE Trans.",
        "abstract": "A spectrum cartography method using adaptive multi-kernels.",
        "citations": 0,
        "links": {"arxiv": None, "pdf": None, "doi": None},
    }
    data = _build_and_validate(cand)
    assert "arxiv" not in (data.get("links") or {})


def test_stub_with_valid_arxiv_keeps_it():
    cand = {
        "arxiv_id": "2505.12345",
        "title": "Some Radio Map Paper",
        "authors": ["B. Author"],
        "year": 2025,
        "abstract": "Deep learning radio map estimation.",
        "citations": 3,
        "links": {"arxiv": "https://arxiv.org/abs/2505.12345", "pdf": None, "doi": None},
    }
    data = _build_and_validate(cand)
    assert data["links"]["arxiv"] == "https://arxiv.org/abs/2505.12345"


def test_stub_drops_malformed_arxiv_but_keeps_bare_doi():
    cand = {
        "arxiv_id": None,
        "title": "Malformed Link Paper",
        "authors": ["C. Author"],
        "year": 2024,
        "abstract": "x",
        "citations": 0,
        # bare arxiv id (no scheme) is malformed for the schema; bare DOI is allowed
        "links": {"arxiv": "2505.99999", "pdf": "", "doi": "10.1109/FOO.2024.123"},
    }
    data = _build_and_validate(cand)
    links = data.get("links") or {}
    assert "arxiv" not in links
    assert links.get("doi") == "10.1109/FOO.2024.123"
