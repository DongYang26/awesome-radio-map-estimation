"""Tests for the fetch.py relevance gate.

Regression guard for the weekly-bot firehose: the arXiv/S2 search APIs once
returned a contiguous block of ~hundreds of off-topic recent papers
(astrophysics, CV, NLP, medical, ...) that polluted the corpus. `is_relevant`
is the defense-in-depth gate that drops anything without a genuine
radio-map-domain phrase in its title/abstract before it can reach a PR.
"""

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from fetch import is_relevant  # noqa: E402

# Real RME / wireless-radio-map papers — must PASS the gate.
RELEVANT_TITLES = [
    "RadioUNet: Fast Radio Map Estimation With Convolutional Neural Networks",
    "Spectrum Cartography via Coupled Block-Term Tensor Decomposition",
    "PMNet: Robust Pathloss Map Prediction via Supervised Learning",
    "Toward Environment-Aware 6G Communications via Channel Knowledge Map",
    "Deep Learning for Path Loss Prediction in Urban Environments",
    "Coverage Map Prediction with Deep Neural Networks",
    "RSS map reconstruction from sparse measurements",
    "Power Spectral Density Map Estimation for Spectrum Sensing",
]

# Actual off-topic titles from the firehose that polluted the corpus — must be BLOCKED.
OFFTOPIC_TITLES = [
    "Depth Map Prediction from a Single Image using a Multi-Scale Deep Network",
    "LOFAR reveals the giant: A low-frequency radio continuum study of a radio galaxy",
    "Dark Energy Survey Year 3 results: Curved-sky weak lensing mass map",
    "Fluence Map Prediction with Deep Learning: A Transformer-based Approach",  # radiotherapy
    "Rethinking the work of Langlands on Eisenstein series",
    "Topological semimetals: surface transport and spin effects",
    "JWST reveals anomalously enhanced methane outgassing",
    "Few-Shot Fine-Grained Ship Classification With a Foreground-Aware Feature Map",
    "Epicure: Navigating the Emergent Geometry of Food Ingredient Embeddings",
    "A Precise Measurement of the Fermi-LAT Galactic Center Excess",
    "Gravitational waves from cosmic strings with friction",
    "Brand visibility in packaging: a deep learning approach for logo detection",
]


def test_relevant_titles_pass():
    for t in RELEVANT_TITLES:
        assert is_relevant({"title": t, "abstract": ""}), f"should KEEP: {t}"


def test_offtopic_titles_blocked():
    for t in OFFTOPIC_TITLES:
        assert not is_relevant({"title": t, "abstract": ""}), f"should DROP: {t}"


def test_relevance_can_match_in_abstract():
    c = {"title": "A Generative Model for Spatial Estimation",
         "abstract": "We reconstruct a radio map from sparse received signal strength samples."}
    assert is_relevant(c)


def test_empty_candidate_is_not_relevant():
    assert not is_relevant({"title": "", "abstract": ""})
    assert not is_relevant({})
