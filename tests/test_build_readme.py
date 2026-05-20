"""Tests for scripts/build_readme.py.

Covers the three guarantees the generator must provide:

  * Idempotency — running generation twice yields a byte-identical result.
  * Marker preservation — every ``<!-- AUTO:X START/END -->`` pair survives.
  * Hand-written regions are untouched — text outside the markers is preserved
    byte-for-byte.

The tests drive ``build_readme.build_readme`` (the pure text transform) against
a skeleton fixture and the real YAML corpus, so the repo's actual README.md is
never mutated by the suite.
"""

from __future__ import annotations

from pathlib import Path

import build_readme
from lib.loader import load_datasets, load_papers, load_taxonomy

FIXTURES = Path(__file__).resolve().parent / "fixtures"
SKELETON = FIXTURES / "readme-skeleton.md"

SECTION_KEYS = ["badges", "stats", "taxonomy", "papers", "datasets"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _corpus():
    """Load the real YAML corpus once for a test."""
    return load_papers(), load_taxonomy(), load_datasets()


def _generate(text: str) -> str:
    """Run the README generator over ``text`` using the real corpus."""
    papers, taxonomy, datasets = _corpus()
    return build_readme.build_readme(text, papers, taxonomy, datasets)


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------

def test_generation_is_idempotent():
    """Running generation twice produces byte-identical output."""
    skeleton = SKELETON.read_text(encoding="utf-8")
    once = _generate(skeleton)
    twice = _generate(once)
    assert once == twice, "second generation pass changed the output"


def test_generation_changes_placeholder_content():
    """The first generation pass actually fills the placeholder sections."""
    skeleton = SKELETON.read_text(encoding="utf-8")
    once = _generate(skeleton)
    # The skeleton's placeholder comment must be gone after generation.
    assert "<!-- placeholder -->" not in once
    assert once != skeleton


# ---------------------------------------------------------------------------
# Marker preservation
# ---------------------------------------------------------------------------

def test_all_markers_preserved():
    """Every AUTO:X START/END marker pair survives generation."""
    skeleton = SKELETON.read_text(encoding="utf-8")
    out = _generate(skeleton)
    for key in SECTION_KEYS:
        assert f"<!-- AUTO:{key} START -->" in out, f"missing {key} START marker"
        assert f"<!-- AUTO:{key} END -->" in out, f"missing {key} END marker"
        # Exactly one of each marker.
        assert out.count(f"<!-- AUTO:{key} START -->") == 1
        assert out.count(f"<!-- AUTO:{key} END -->") == 1


def test_marker_order_preserved():
    """Markers appear in the same order before and after generation."""
    skeleton = SKELETON.read_text(encoding="utf-8")
    out = _generate(skeleton)
    positions = [out.index(f"<!-- AUTO:{k} START -->") for k in SECTION_KEYS]
    assert positions == sorted(positions), "marker order changed"


# ---------------------------------------------------------------------------
# Hand-written regions untouched
# ---------------------------------------------------------------------------

def test_intro_region_untouched():
    """Text in the hand-written intro region is preserved byte-for-byte."""
    skeleton = SKELETON.read_text(encoding="utf-8")
    out = _generate(skeleton)
    # The intro sentinel and the whole header block must be present verbatim.
    intro = skeleton.split("<!-- AUTO:badges START -->")[0]
    assert out.startswith(intro), "intro region was modified"
    assert "INTRO-SENTINEL-DO-NOT-TOUCH" in out


def test_outro_region_untouched():
    """Text after the last marker is preserved byte-for-byte."""
    skeleton = SKELETON.read_text(encoding="utf-8")
    out = _generate(skeleton)
    outro = skeleton.split("<!-- AUTO:datasets END -->")[1]
    assert out.endswith(outro), "outro region was modified"
    assert "OUTRO-SENTINEL-DO-NOT-TOUCH" in out


def test_only_marked_regions_change():
    """Generation changes only the inter-marker regions, nothing else.

    Reconstructs the skeleton with every marked region blanked, does the same
    to the generated output, and asserts the two skeletons are identical — i.e.
    every byte outside the markers is untouched.
    """
    import re

    skeleton = SKELETON.read_text(encoding="utf-8")
    out = _generate(skeleton)

    def _blank_marked(text: str) -> str:
        for key in SECTION_KEYS:
            pattern = re.compile(
                rf"(<!-- AUTO:{key} START -->).*?(<!-- AUTO:{key} END -->)",
                re.DOTALL,
            )
            text = pattern.sub(r"\1\2", text)
        return text

    assert _blank_marked(skeleton) == _blank_marked(out)


# ---------------------------------------------------------------------------
# Real README idempotency
# ---------------------------------------------------------------------------

def test_real_readme_is_idempotent():
    """Generating over the repo's actual README.md twice is idempotent.

    Reads the real README.md, runs two generation passes in memory (never
    writing back), and asserts the second pass is a no-op.
    """
    real = build_readme.README_PATH.read_text(encoding="utf-8")
    once = _generate(real)
    twice = _generate(once)
    assert once == twice, "second pass over the real README changed output"
