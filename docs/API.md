# Inkstruct — API Design

Version 1.0 | Day 2 Deliverable

## A Note on "API" for This Project

Inkstruct is a single-process Streamlit app with no separate backend server, so there are no HTTP REST endpoints in v1.0 — there is no client making network requests to our own server the way a typical web app would. This is consistent with the PRD and the Day 2 tech stack (Streamlit = frontend + backend in one process).

What v1.0 *does* have is a set of **internal module functions** that act as the seams between the UI layer (`app.py`) and the logic layers (`ai.py`, `file_parser.py`, `storage.py`, `export.py`). These function signatures serve the same purpose an API spec normally would: they are the contract Day 4 onward will implement against, so this document defines them with the same rigor (purpose, inputs, outputs, validation, errors) as REST endpoints would get.

If a future version adds multi-user support or a mobile client, these same functions are the natural place to wrap in a real REST/GraphQL layer — the boundaries are already drawn correctly.

---

## Module: `ai.py`

### `generate_outline(text: str) -> str`
- **Purpose:** Send raw notes to Claude and receive a structured outline.
- **Request (function input):** `text` — non-empty string, the extracted user notes.
- **Response (function output):** Markdown-formatted string: numbered headings with sub-bullets.
- **Validation:** Caller (`app.py`) must ensure `text` is non-empty and at least ~20 characters before calling.
- **Authentication:** Claude API key read from `st.secrets["ANTHROPIC_API_KEY"]` inside the function — not passed as a parameter.
- **Error cases:** Raises an exception on API failure (timeout, auth error, rate limit) — caller wraps in try/except and shows `st.error(...)`.

### `generate_draft(outline: str, original_text: str) -> str`
- **Purpose:** Expand a structured outline into a full first draft.
- **Request:** `outline` (string, must be non-empty, normally the output of `generate_outline`), `original_text` (string, the original notes, used as source material for details).
- **Response:** Plain prose string, following the outline's structure.
- **Validation:** Caller ensures `outline` exists (i.e. outline step has already run) before this is callable — UI hides the button otherwise.
- **Authentication:** Same as above.
- **Error cases:** Same pattern — raises on failure, caught and surfaced as `st.error(...)`.

---

### `extract_text(file) -> str`
- **Purpose:** Routes an uploaded file to the correct extractor based on its filename extension.
- **Request:** `file` — a Streamlit `UploadedFile` object.
- **Response:** Extracted plain text string.
- **Error cases:** Raises `ValueError` for unsupported extensions (defensive — Streamlit's uploader already restricts selectable types).
- **Used by:** `app.py`, as the single entry point into file parsing.

## Module: `file_parser.py`

### `extract_text_from_txt(file) -> str`
- **Purpose:** Decode an uploaded `.txt` file into plain text.
- **Request:** `file` — a Streamlit `UploadedFile` object.
- **Response:** UTF-8 decoded string.
- **Validation:** None required beyond file type check (done by `st.file_uploader`'s `type=` restriction).
- **Error cases:** Raises `UnicodeDecodeError` on malformed encoding — caller catches and shows a friendly error.

### `extract_text_from_docx(file) -> str`
- **Purpose:** Extract plain text from an uploaded `.docx` file.
- **Request:** `file` — Streamlit `UploadedFile` object.
- **Response:** String of all paragraph text, newline-joined.
- **Validation:** None beyond file type.
- **Error cases:** Raises on corrupted/invalid `.docx` — caller catches, shows "Could not read this file."

### `extract_text_from_pdf(file) -> str`
- **Purpose:** Extract plain text from an uploaded `.pdf` file.
- **Request:** `file` — Streamlit `UploadedFile` object.
- **Response:** String of all page text, newline-joined.
- **Validation:** None beyond file type.
- **Error cases:** Raises on corrupted or scanned/image-only PDFs (no text layer) — caller catches, shows friendly error. Scanned PDFs are explicitly out of scope (PRD).

---

## Module: `storage.py`

### `init_db() -> None`
- **Purpose:** Create the SQLite file and `documents` table if they don't already exist.
- **Request:** None.
- **Response:** None.
- **Called:** Once, at app startup.

### `save_document(title: str, input_text: str, outline: str, draft: str, tags: str) -> int`
- **Purpose:** Persist a completed session.
- **Request:** All fields required except `tags` (nullable). `tags` is a comma-separated string.
- **Response:** The new row's `id` (int).
- **Validation:** `title`, `input_text`, `outline`, `draft` must be non-empty strings.
- **Error cases:** Raises on DB write failure (disk full, locked file) — rare, but caught and surfaced.

### `get_all_documents() -> list[dict]`
- **Purpose:** Retrieve all saved sessions for the history sidebar, most recent first.
- **Request:** None.
- **Response:** List of dicts, one per row, all columns included.

### `search_documents(keyword: str) -> list[dict]`
- **Purpose:** Keyword search across title, input, and draft.
- **Request:** `keyword` — non-empty string.
- **Response:** List of matching document dicts.
- **Validation:** Empty keyword returns all documents (same as `get_all_documents()`), not an error.

### `filter_by_tag(tag: str) -> list[dict]`
- **Purpose:** Return documents containing the given tag.
- **Request:** `tag` — non-empty string.
- **Response:** List of matching document dicts.

### `get_document(doc_id: int) -> dict | None`
- **Purpose:** Retrieve one full saved session by id, for reloading into the main view.
- **Request:** `doc_id` — integer.
- **Response:** Dict of all fields, or `None` if not found.
- **Error cases:** Returns `None` rather than raising if id doesn't exist — caller shows "Document not found" if needed.

---

## Module: `export.py`

### `export_to_docx(text: str, title: str) -> BytesIO`
- **Purpose:** Generate a downloadable Word file from text.
- **Request:** `text` (string, the outline or draft content), `title` (string, used as the document heading and suggested filename).
- **Response:** `BytesIO` buffer, ready to hand to `st.download_button`.
- **Error cases:** Should not raise under normal use; wrapped in try/except defensively.

### `export_to_pdf(text: str, title: str) -> BytesIO`
- **Purpose:** Generate a downloadable PDF from text.
- **Request:** Same as above.
- **Response:** `BytesIO` buffer.
- **Error cases:** May raise on unsupported characters — caller catches and shows a fallback message; consider `errors='replace'` encoding as a safeguard.

---

## Summary Table

| Function | Module | Trigger |
|---|---|---|
| `generate_outline` | ai.py | "Generate Outline" button |
| `generate_draft` | ai.py | "Generate Full Draft" button |
| `extract_text_from_txt/docx/pdf` | file_parser.py | File upload |
| `init_db` | storage.py | App startup |
| `save_document` | storage.py | After draft generation (auto) |
| `get_all_documents` | storage.py | Sidebar render |
| `search_documents` | storage.py | Search box input |
| `filter_by_tag` | storage.py | Tag filter selection |
| `get_document` | storage.py | Clicking a history item |
| `export_to_docx` / `export_to_pdf` | export.py | Download buttons |

This table is the full v1.0 function surface — Day 3 onward implements exactly these signatures, nothing more.
