# Inkstruct — Project Structure

Version 1.1 | Originally Day 2, updated Day 3 to reflect actual local state

> **Day 3 update:** Structure below now reflects the real, verified local project as of Day 3 (not just the planned target). All Day 2-planned folders/files are confirmed present and correctly placed. `venv/` added as a new root item (local Python virtual environment, excluded from Git). `app.py` now contains a working "Hello World" implementation with a `MOCK_MODE` flag — see ENVIRONMENT.md.

## 1. Full Folder Structure (target state by end of Day 7)

```
inkstruct/
├── app.py                     (Hello World implemented Day 3 — MOCK_MODE flag active)
├── requirements.txt
├── README.md
├── .gitignore
├── venv/                       (local virtual environment — not committed)
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml          (local only — never committed)
├── app/
│   ├── __init__.py
│   ├── ai.py
│   ├── file_parser.py
│   ├── storage.py
│   └── export.py
├── docs/
│   ├── PRD.md (or .docx)
│   ├── ARCHITECTURE.md
│   ├── SCHEMA.md
│   ├── API.md
│   ├── UI-WIREFRAMES.md
│   ├── PROJECT-STRUCTURE.md
│   └── IMPLEMENTATION-BLUEPRINT.md
├── inkstruct.db               (auto-created at runtime — not committed)
└── PROJECT-LOG.md
```

## 2. What Each Item Is Responsible For

| Path | Responsibility |
|---|---|
| `app.py` | Entry point. Streamlit page config, layout, session_state orchestration. Calls into `app/` modules but contains no business logic itself. Currently a minimal "Hello World" with a Claude connection test and `MOCK_MODE` flag (Day 3). |
| `venv/` | Local Python virtual environment — isolates project dependencies from the rest of the machine. Excluded from Git via `.gitignore`. Recreated locally by anyone cloning the repo via `python -m venv venv`. |
| `requirements.txt` | Pinned dependency list — read by both local `pip install` and Streamlit Cloud's deploy process. |
| `README.md` | Public-facing project description, deployed link, usage instructions (written Day 9). |
| `.gitignore` | Excludes `secrets.toml`, `inkstruct.db`, `__pycache__/`, virtual environment folders from Git. |
| `.streamlit/config.toml` | Theme settings (colors, font) — created Day 7. |
| `.streamlit/secrets.toml` | Local-only API key storage. Mirrored in Streamlit Cloud's Secrets manager for deployment, never committed. |
| `app/ai.py` | All Claude API interaction: `generate_outline()`, `generate_draft()`. |
| `app/file_parser.py` | All file-to-text extraction: `extract_text_from_txt/docx/pdf()`. |
| `app/storage.py` | All SQLite interaction: `init_db()`, `save_document()`, `get_all_documents()`, `search_documents()`, `filter_by_tag()`, `get_document()`. |
| `app/export.py` | All export generation: `export_to_docx()`, `export_to_pdf()`. |
| `docs/` | All planning and design deliverables from Days 1–2, kept in the repo as living documentation and for any future AI assistant picking up a fresh day's session. |
| `inkstruct.db` | Runtime-generated SQLite database file. Not committed — regenerates automatically via `init_db()` on first run. |
| `PROJECT-LOG.md` | Running day-by-day log of what was done, decisions made, and issues hit — updated at the end of every day starting today. |

## 3. Why This Structure

- **`app/` as a package, not flat files in root:** keeps `app.py` (the UI entry point) visually distinct from logic modules, and mirrors the module boundaries defined in `API.md` — each file in `app/` maps 1:1 to a section of that document.
- **No `tests/` folder yet:** testing in this project is manual (per the Blueprint's Day 9 test checklist), not automated unit tests — appropriate given the 1-hour/day time budget. If time allows later, a `tests/` folder can be added without restructuring anything else.
- **`docs/` folder in-repo:** rather than keeping planning documents only in chat history or a local drive, committing them ensures a fresh AI conversation on any future day can be pointed at the repo and immediately have full context — directly supporting the Blueprint's "fresh AI session per day" requirement.
- **Flat `app/` (no sub-packages):** four modules is small enough that further nesting (e.g. `app/services/`, `app/utils/`) would be over-engineering for this project's size and timeline.
- **Config/secrets separated into `.streamlit/`:** this is Streamlit's required convention, not a choice — `secrets.toml` and `config.toml` must live there to be auto-detected.

## 4. Where Future Code Lives (day-by-day mapping)

| Day | New/modified files |
|---|---|
| Day 3 | `app.py` (input UI), `app/file_parser.py` (new) |
| Day 4 | `app/ai.py` (new, outline function), `app.py` (outline UI) |
| Day 5 | `app/ai.py` (draft function added), `app.py` (draft UI) |
| Day 6 | `app/storage.py` (new), `app.py` (sidebar/history UI) |
| Day 7 | `.streamlit/config.toml` (new), `app/export.py` (new), `app.py` (polish + export UI) |
| Day 8 | No new files — deployment configuration only |
| Day 9 | Bug fixes across existing files, `README.md` added |
| Day 10 | Minor polish only, `PROJECT-LOG.md` finalized |

This mapping is identical to the Implementation Blueprint's daily file lists — this document and the Blueprint must always agree; if either changes, update both.
