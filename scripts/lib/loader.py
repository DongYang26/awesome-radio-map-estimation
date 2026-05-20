"""Shared data loader for Hot_Papers_Finding.

Resolves paths from __file__ so it works regardless of the current working
directory — safe to import from scripts/ subdirectories or run directly.
"""

from pathlib import Path
import glob
import yaml

# ---------------------------------------------------------------------------
# Path constants — resolved from this file's location, NOT from cwd
# ---------------------------------------------------------------------------
REPO_ROOT: Path = Path(__file__).resolve().parents[2]
DATA_DIR: Path = REPO_ROOT / "data"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _safe_load(path: Path) -> object:
    """Load a YAML file with yaml.safe_load; raise a clear error on failure."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        raise ValueError(f"Failed to parse YAML file '{path}': {exc}") from exc


# ---------------------------------------------------------------------------
# Public loaders
# ---------------------------------------------------------------------------

def load_papers() -> list[dict]:
    """Load every data/papers/*.yml and return a list of dicts.

    Each dict has an extra ``_stem`` key set to the filename stem (without
    extension), useful for the id == stem check in validate.py.

    The list is sorted deterministically by the ``id`` field (falling back to
    ``_stem`` when ``id`` is absent so the sort never raises).
    """
    pattern = str(DATA_DIR / "papers" / "*.yml")
    paths = sorted(glob.glob(pattern))  # sort paths for reproducible order before id-sort
    papers: list[dict] = []
    for p in paths:
        path = Path(p)
        data = _safe_load(path)
        if not isinstance(data, dict):
            raise ValueError(f"Expected a YAML mapping in '{path}', got {type(data).__name__}")
        data["_stem"] = path.stem
        papers.append(data)
    # Stable sort by id; fall back to _stem when id is missing
    papers.sort(key=lambda d: (d.get("id") or d["_stem"]))
    return papers


def load_taxonomy() -> dict:
    """Load data/taxonomy.yml and return the parsed dict."""
    path = DATA_DIR / "taxonomy.yml"
    data = _safe_load(path)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in '{path}', got {type(data).__name__}")
    return data


def load_datasets() -> dict:
    """Load data/datasets.yml; return {\"datasets\": []} if the file is absent."""
    path = DATA_DIR / "datasets.yml"
    if not path.exists():
        return {"datasets": []}
    data = _safe_load(path)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in '{path}', got {type(data).__name__}")
    return data


def load_reading_path() -> dict:
    """Load data/reading-path.yml; return {\"steps\": []} if the file is absent."""
    path = DATA_DIR / "reading-path.yml"
    if not path.exists():
        return {"steps": []}
    data = _safe_load(path)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in '{path}', got {type(data).__name__}")
    return data


def load_all() -> dict:
    """Load and return all data sources as a single dict."""
    return {
        "papers": load_papers(),
        "taxonomy": load_taxonomy(),
        "datasets": load_datasets(),
        "reading_path": load_reading_path(),
    }


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    data = load_all()

    papers = data["papers"]
    taxonomy = data["taxonomy"]
    datasets = data["datasets"]
    reading_path = data["reading_path"]

    taxonomy_nodes = taxonomy.get("taxonomy", [])
    # Count all nodes (top-level + children at every depth)
    def _count_nodes(nodes: list) -> int:
        total = 0
        for node in nodes:
            total += 1
            total += _count_nodes(node.get("children", []))
        return total

    node_count = _count_nodes(taxonomy_nodes)

    print(f"REPO_ROOT      : {REPO_ROOT}")
    print(f"papers         : {len(papers)}")
    print(f"taxonomy nodes : {node_count}")
    print(f"datasets       : {len(datasets.get('datasets', []))}")
    print(f"reading steps  : {len(reading_path.get('steps', []))}")
