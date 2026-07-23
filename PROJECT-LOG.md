# Inkstruct — Project Log

## Day 1 — Discovery & Requirements
- Ran an interview-style discovery session to find the right capstone project given a 1 hr/day time budget.
- Landed on Inkstruct: an AI writing assistant that turns scattered notes into a structured outline and full first draft, using the Claude API.
- Defined explicit in-scope and out-of-scope features to protect against scope creep.
- Deliverables: PRD, Implementation Blueprint (Days 2–10), Pitch Deck.

## Day 2 — Technical Design
- Reviewed and confirmed Day 1 deliverables as source of truth — no redesign needed.
- Created GitHub repository (`Abhay-2727/inkstruct`) and cloned it locally.
- Finalized tech stack: Python + Streamlit, Anthropic Claude API, SQLite, python-docx/pypdf for parsing, python-docx/fpdf2 for export, Streamlit Community Cloud for hosting.
- Designed full system architecture: component diagram, data flow, request lifecycle, AI interaction pattern.
- Designed database schema (single `documents` table) and validated it against every PRD requirement.
- Designed the internal module "API" (function contracts between app.py and app/ modules) since the app has no REST layer.
- Designed the full user flow and low-fidelity wireframes for the single-page UI.
- Finalized the project folder structure.
- Updated the Implementation Blueprint with a Day 2 addendum reflecting the docs/ folder and this log.
- Deliverables: ARCHITECTURE.md, SCHEMA.md, API.md, UI-WIREFRAMES.md, PROJECT-STRUCTURE.md.
- **Status:** On track. No scope changes. Day 3 can begin implementation immediately.

## Day 3 — Project Setup & Foundation
- Verified Python 3.12.0, created and activated a virtual environment, installed all dependencies (Streamlit, Anthropic SDK, python-docx, pypdf, fpdf2).
- Hit and resolved a Windows Application Control policy blocking `pip.exe`/`streamlit.exe` — fixed by using `python -m pip`/`python -m streamlit` for all commands going forward.
- Set up `.streamlit/secrets.toml` for the Claude API key; caught and fixed a near-miss where the secrets file was briefly staged for a Git commit before `.gitignore` was corrected — no secret was ever pushed.
- Built a working "Hello World" `app.py` proving the full Streamlit → Python → API chain runs end-to-end.
- Discovered the Anthropic Console account has insufficient credit balance, blocking real API calls. Added a `MOCK_MODE` flag to keep development unblocked; flagged as an open item to resolve before real AI output can be verified.
- Scaffolded the full `app/` package (`ai.py`, `file_parser.py`, `storage.py`, `export.py`, `__init__.py`) matching API.md exactly.
- Verified local folder structure fully matches PROJECT-STRUCTURE.md; moved Day 2 docs into `docs/` and `PROJECT-LOG.md` into the project root.
- Committed and pushed all foundation work to GitHub.
- Deliverables: SETUP.md, ENVIRONMENT.md, updated PROJECT-STRUCTURE.md, DAY3-SUMMARY.md. Blueprint updated with a Day 3 addendum.
- **Status:** On track. One open item (API credits) carried into Day 4 — does not block structural implementation but must be resolved before AI output can be truly verified.
