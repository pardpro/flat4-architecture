# Repository Language Policy

- Keep the root `README.md` bilingual, with Chinese as the primary introduction and an English summary for international readers.
- Use English for every other Git-tracked Markdown document, ADR, Skill instruction, UI metadata file, release note, and developer-facing code comment.
- Keep optional Chinese working copies under `.local/zh/`. The `.local/` directory is intentionally ignored and must never be committed.
- Treat English files under `docs/`, `references/`, and the Skill package as the canonical source. Do not maintain a second tracked Chinese documentation tree.
- Before committing documentation changes, run `python scripts/check_english_docs.py` and the repository test suite.
- Product UI localization is outside this rule when a project explicitly requires translated runtime content; document that exception before committing it.
