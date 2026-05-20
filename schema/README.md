# Data Schema Reference

Every file under `data/` is validated in CI against a JSON Schema in this
directory (`scripts/validate.py`). This document is the human-readable field
reference; the machine-readable contracts are the `*.schema.json` files.

There are four schemas:

| Schema file | Validates |
|-------------|-----------|
| `paper.schema.json` | each `data/papers/<id>.yml` |
| `datasets.schema.json` | `data/datasets.yml` |
| `taxonomy.schema.json` | `data/taxonomy.yml` |
| `reading-path.schema.json` | `data/reading-path.yml` |

All schemas are JSON Schema **draft 2020-12** and use `additionalProperties: false`
— an unknown or misspelled key fails CI.

---

## `paper.schema.json` — a single paper

One YAML file per paper in `data/papers/`. The filename stem **must equal** the
`id` field (e.g. `data/papers/2210.12345.yml` has `id: "2210.12345"`).

### Required fields

| Field | Type | Meaning |
|-------|------|---------|
| `id` | string | arXiv id or kebab-case slug; lowercase, matches `^[a-z0-9._-]+$`; equals the filename stem |
| `title` | string | Paper title (≥ 4 chars) |
| `authors` | string[] | Author names, ≥ 1 |
| `year` | integer | Publication year, 1990–2100 |
| `subfield` | enum | One of: `REM`, `spectrum-cartography`, `pathloss-prediction`, `CKM` |
| `method_family` | enum | One of: `interpolation`, `model-based`, `learning-based` |
| `task` | enum[] | ≥ 1 of: `signal-strength-estimation`, `coverage-prediction`, `spectrum-occupancy`, `pathloss-prediction`, `channel-gain-prediction`, `spectrum-cartography`, `REM-construction`, `other` |
| `input_modality` | enum | One of: `sparse-measurements`, `environment-map`, `both` |
| `environment` | enum | One of: `indoor`, `outdoor`, `both` |
| `dimensionality` | enum | One of: `2D`, `3D` |
| `supervision` | enum | One of: `supervised`, `self-supervised`, `unsupervised`, `semi-supervised`, `n/a` |
| `added_date` | string | Date added, ISO `YYYY-MM-DD` |

### Optional fields

| Field | Type | Meaning |
|-------|------|---------|
| `venue` | string | Conference / journal |
| `abstract` | string | Paper abstract |
| `tldr` | string | One-sentence human summary (≤ 280 chars) |
| `links` | object | `arxiv`, `pdf`, `code`, `project_page` (URIs), `doi` (string) |
| `method_detail` | enum[] | Any of: `Kriging`, `IDW`, `matrix-completion`, `ray-tracing`, `CNN`, `GAN`, `Transformer`, `INR`, `Diffusion`, `GNN`, `RNN`, `autoencoder`, `Gaussian-process`, `other` |
| `datasets` | string[] | Dataset ids; each must exist in `data/datasets.yml` |
| `citations` | integer | Semantic Scholar citation count (≥ 0) |
| `is_milestone` | boolean | Highlight on the evolution timeline (default `false`) |
| `tags` | string[] | Free-form tags |

`method_detail` and `task` are **arrays** — a paper may combine, e.g., a CNN and
a Transformer, or address both coverage and signal-strength estimation. Use the
`"other"` enum value when no listed value fits rather than inventing a new one.

---

## `datasets.schema.json` — the dataset catalog

`data/datasets.yml` is `{ datasets: [ ... ] }`. Each entry:

| Field | Type | Meaning |
|-------|------|---------|
| `id` | string | kebab-case identifier (referenced by papers' `datasets[]`) |
| `name` | string | Display name |
| `description` | string | What the dataset contains |
| `link` | string (uri) | Project / download URL |
| `papers_using` | string[] | Paper ids that use the dataset |
| `benchmark` | object[] | Optional leaderboard rows `{paper_id, metric, value}` |

## `taxonomy.schema.json` — the classification tree

`data/taxonomy.yml` is `{ taxonomy: [ <node>, ... ] }`. A node is recursive:

| Field | Type | Meaning |
|-------|------|---------|
| `id` | string | Node identifier |
| `label` | string | Display label |
| `description` | string | Optional one-line description |
| `children` | node[] | Optional child nodes |

## `reading-path.schema.json` — the newcomer reading path

`data/reading-path.yml` is `{ steps: [ ... ] }`. Each step:

| Field | Type | Meaning |
|-------|------|---------|
| `order` | integer | Step number (≥ 1) |
| `paper_id` | string | A paper `id` from `data/papers/` |
| `why` | string | Why this paper, at this point in the path |
