"""Pytest configuration: make scripts/ importable from the test suite.

The generation/validation scripts live in scripts/ and import the shared
loader as ``from lib.loader import ...``. Adding scripts/ to sys.path lets the
tests import validate.py, stats.py, and build_readme.py directly.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
