"""Tests for scripts/dedup.py.

All tests are self-contained and use in-memory fixtures — no real network
calls, no filesystem writes to data/papers/.

Scenarios covered:
  1. Exact arXiv-id duplicate is dropped.
  2. Fuzzy-title duplicate (ratio >= 0.9) is dropped.
  3. A genuinely new paper (different id AND non-similar title) is kept.
  4. A within-batch duplicate (same arXiv id appearing twice in the candidate
     list) is collapsed to one entry.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure scripts/ is importable (conftest.py also does this, but belt-and-braces)
REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from dedup import FUZZY_TITLE_THRESHOLD, build_corpus_index, deduplicate  # noqa: E402

# ---------------------------------------------------------------------------
# Corpus fixtures
# ---------------------------------------------------------------------------

# Minimal paper dicts that mimic what load_papers() returns (with _stem key).
CORPUS_PAPERS: list[dict] = [
    {
        "id": "1911.09002",
        "title": "RadioUNet: Fast Radio Map Estimation With Convolutional Neural Networks",
        "_stem": "1911.09002",
    },
    {
        "id": "2211.10527",
        "title": "PMNet: Robust Pathloss Map Prediction via Supervised Learning",
        "_stem": "2211.10527",
    },
    {
        "id": "good-paper",
        "title": "A Well-Formed Radio Map Estimation Paper",
        "_stem": "good-paper",
    },
]

# ---------------------------------------------------------------------------
# Candidate fixtures
# ---------------------------------------------------------------------------

# Exact arXiv-id match — same id as an existing corpus paper.
CANDIDATE_EXACT_ID_DUP: dict = {
    "arxiv_id": "1911.09002",
    "title": "RadioUNet: Fast Radio Map Estimation With Convolutional Neural Networks",
    "authors": ["Ron Levie"],
    "year": 2019,
    "abstract": "RadioUNet proposes a U-Net architecture ...",
    "venue": "IEEE TWC",
    "citations": 418,
    "links": {"arxiv": "https://arxiv.org/abs/1911.09002"},
}

# Fuzzy-title duplicate — id is different, but the title is almost identical
# (a single word changed), so SequenceMatcher ratio will be >= 0.9.
CANDIDATE_FUZZY_TITLE_DUP: dict = {
    "arxiv_id": "9999.99999",  # not in corpus
    # Title differs only in "Fast" -> "Quick" — high similarity ratio
    "title": "RadioUNet: Quick Radio Map Estimation With Convolutional Neural Networks",
    "authors": ["Ron Levie"],
    "year": 2019,
    "abstract": "Very similar paper ...",
    "venue": "IEEE TWC",
    "citations": 10,
    "links": {"arxiv": "https://arxiv.org/abs/9999.99999"},
}

# Genuinely new paper — different arXiv id AND dissimilar title.
CANDIDATE_NEW: dict = {
    "arxiv_id": "2312.00001",
    "title": "A Novel Diffusion-Based Approach to 3D Channel Knowledge Map Construction",
    "authors": ["Jane Doe", "John Smith"],
    "year": 2023,
    "abstract": "We propose a diffusion model for CKM construction ...",
    "venue": "IEEE GLOBECOM",
    "citations": 5,
    "links": {"arxiv": "https://arxiv.org/abs/2312.00001"},
}

# No arXiv id at all — must still be deduped by title when titles match.
CANDIDATE_NO_ID_TITLE_DUP: dict = {
    "arxiv_id": None,
    "title": "PMNet: Robust Pathloss Map Prediction via Supervised Learning",
    "authors": ["Ju-Hyung Lee"],
    "year": 2022,
    "abstract": "Same title, no id ...",
    "venue": "IEEE GLOBECOM",
    "citations": 31,
    "links": {},
}

# Within-batch duplicate — same arXiv id as CANDIDATE_NEW appears twice.
CANDIDATE_NEW_DUP_IN_BATCH: dict = {
    "arxiv_id": "2312.00001",
    "title": "A Novel Diffusion-Based Approach to 3D Channel Knowledge Map Construction",
    "authors": ["Jane Doe"],
    "year": 2023,
    "abstract": "Duplicate of the new paper in the same batch.",
    "venue": "",
    "citations": 0,
    "links": {},
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestBuildCorpusIndex:
    """Unit tests for the build_corpus_index helper."""

    def test_extracts_arxiv_ids(self):
        arxiv_ids, _ = build_corpus_index(CORPUS_PAPERS)
        assert "1911.09002" in arxiv_ids
        assert "2211.10527" in arxiv_ids
        assert "good-paper" in arxiv_ids

    def test_extracts_titles(self):
        _, norm_titles = build_corpus_index(CORPUS_PAPERS)
        assert len(norm_titles) == 3
        # Titles are normalised to lowercase
        assert any("radiounet" in t for t in norm_titles)

    def test_empty_corpus(self):
        arxiv_ids, norm_titles = build_corpus_index([])
        assert arxiv_ids == set()
        assert norm_titles == []


class TestDeduplicateExactId:
    """Exact arXiv-id match drops the candidate."""

    def test_exact_id_is_dropped(self):
        result = deduplicate([CANDIDATE_EXACT_ID_DUP], papers=CORPUS_PAPERS)
        assert result == [], (
            "A candidate whose arxiv_id matches an existing paper id should be dropped."
        )

    def test_exact_id_not_in_result(self):
        result = deduplicate(
            [CANDIDATE_EXACT_ID_DUP, CANDIDATE_NEW], papers=CORPUS_PAPERS
        )
        ids = [c.get("arxiv_id") for c in result]
        assert "1911.09002" not in ids
        assert "2312.00001" in ids


class TestDeduplicateFuzzyTitle:
    """Fuzzy title match drops near-identical papers regardless of id."""

    def test_fuzzy_title_dup_is_dropped(self):
        result = deduplicate([CANDIDATE_FUZZY_TITLE_DUP], papers=CORPUS_PAPERS)
        assert result == [], (
            "A candidate with a near-identical title (ratio >= 0.9) should be dropped."
        )

    def test_no_id_title_dup_is_dropped(self):
        result = deduplicate([CANDIDATE_NO_ID_TITLE_DUP], papers=CORPUS_PAPERS)
        assert result == [], (
            "A candidate with no arXiv id but a matching title should be dropped."
        )

    def test_genuinely_different_title_is_kept(self):
        result = deduplicate([CANDIDATE_NEW], papers=CORPUS_PAPERS)
        assert len(result) == 1
        assert result[0]["arxiv_id"] == "2312.00001"


class TestDeduplicateNewPaper:
    """A genuinely new paper passes through unchanged."""

    def test_new_paper_kept(self):
        result = deduplicate([CANDIDATE_NEW], papers=CORPUS_PAPERS)
        assert len(result) == 1

    def test_new_paper_dict_unchanged(self):
        result = deduplicate([CANDIDATE_NEW], papers=CORPUS_PAPERS)
        assert result[0]["title"] == CANDIDATE_NEW["title"]
        assert result[0]["arxiv_id"] == CANDIDATE_NEW["arxiv_id"]

    def test_empty_candidates_returns_empty(self):
        result = deduplicate([], papers=CORPUS_PAPERS)
        assert result == []

    def test_empty_corpus_keeps_all_unique(self):
        candidates = [CANDIDATE_NEW, CANDIDATE_EXACT_ID_DUP]
        result = deduplicate(candidates, papers=[])
        # Both have different arxiv_ids, so both are kept
        assert len(result) == 2


class TestDeduplicateWithinBatch:
    """Within-batch duplicates (same arxiv_id appearing twice) collapse to one."""

    def test_within_batch_dedup(self):
        candidates = [CANDIDATE_NEW, CANDIDATE_NEW_DUP_IN_BATCH]
        result = deduplicate(candidates, papers=CORPUS_PAPERS)
        assert len(result) == 1, (
            "The same arXiv id appearing twice in the input should be collapsed to one."
        )
        assert result[0]["arxiv_id"] == "2312.00001"


class TestDeduplicateMixed:
    """Mixed batch: some duplicates, some new — only new ones survive."""

    def test_mixed_batch(self):
        candidates = [
            CANDIDATE_EXACT_ID_DUP,   # exact id dup   -> dropped
            CANDIDATE_FUZZY_TITLE_DUP, # fuzzy title dup -> dropped
            CANDIDATE_NEW,             # new             -> kept
        ]
        result = deduplicate(candidates, papers=CORPUS_PAPERS)
        assert len(result) == 1
        assert result[0]["arxiv_id"] == "2312.00001"

    def test_all_duplicates_returns_empty(self):
        candidates = [CANDIDATE_EXACT_ID_DUP, CANDIDATE_FUZZY_TITLE_DUP]
        result = deduplicate(candidates, papers=CORPUS_PAPERS)
        assert result == []
