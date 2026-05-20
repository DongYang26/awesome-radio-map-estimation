## PR checklist — adding a paper

Thank you for contributing! Please verify every item before requesting review.

- [ ] This PR adds **exactly one** new file under `data/papers/` (one paper per PR).
- [ ] The filename matches the `id` field exactly (e.g. `data/papers/2210.12345.yml` has `id: "2210.12345"`).
- [ ] All **required fields** are present: `id`, `title`, `authors`, `year`, `subfield`, `method_family`, `task`, `input_modality`, `environment`, `dimensionality`, `supervision`, `added_date`.
- [ ] Every **enum field** uses an exact value from [`schema/README.md`](../schema/README.md) (CI will fail on unknown values).
- [ ] The classification (`subfield`, `method_family`, `task`, etc.) is **justified** — if the choice is non-obvious, add a brief comment above the relevant line in the YAML explaining the reasoning.
- [ ] `python scripts/validate.py` passes locally (or CI passes on this PR).
- [ ] I did **not** hand-edit `README.md` (the paper list and statistics sections are generated automatically and my edits would be overwritten).
- [ ] I did **not** hand-edit `site/src/data/stats.json` or `site/src/lib/types.ts` (both are generated artifacts).
