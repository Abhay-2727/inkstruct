# Inkstruct — Environment Configuration

Version 1.0 | Day 3 Deliverable

## 1. Runtime

| Item | Value |
|---|---|
| Language | Python 3.12.0 |
| Package manager | pip (invoked via `python -m pip` — see Known Issues in SETUP.md) |
| Virtual environment | `venv/` (excluded from Git) |
| Web framework | Streamlit 1.60.0 |

## 2. Environment Variables / Secrets

| Name | Where it lives | Purpose | Committed to Git? |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | `.streamlit/secrets.toml` | Authenticates all Claude API calls | **No — must never be committed** |

Accessed in code via:
```python
st.secrets["ANTHROPIC_API_KEY"]
```

When deployed to Streamlit Community Cloud (Day 8), this same key must be re-entered in the app's **Secrets** section in the Cloud dashboard — `secrets.toml` is local-only and does not travel with a `git push`.

## 3. Configuration Files

| File | Purpose | Committed? |
|---|---|---|
| `requirements.txt` | Pinned dependency list, read by both local pip and Streamlit Cloud | Yes |
| `.gitignore` | Excludes `venv/`, `__pycache__/`, `.streamlit/secrets.toml`, `inkstruct.db`, `*.pyc` | Yes |
| `.streamlit/secrets.toml` | Local API key storage | **No** |
| `.streamlit/config.toml` | Theme settings (colors/fonts) | Not yet created — planned Day 7 |

## 4. Development Flags

| Flag | Location | Purpose | Current Value |
|---|---|---|---|
| `MOCK_MODE` | `app.py` | Bypasses real Claude API calls with a placeholder response, due to insufficient API credits discovered Day 3 | `True` |

**This flag must be set to `False` before real feature testing can validate actual AI output.** Until then, all outline/draft generation work (Days 4–5) can be structurally built and tested with mock data, but true output quality cannot be verified. This is tracked as an open item — see DAY3-SUMMARY.md.

## 5. Known Machine-Specific Quirks

- This development machine has a **Windows Application Control policy** that blocks direct execution of `pip.exe` and `streamlit.exe`. All commands must be run through `python -m` (e.g. `python -m streamlit run app.py`). This is documented so future days/sessions don't waste time rediscovering it.

## 6. Ports

| Service | Port | Notes |
|---|---|---|
| Streamlit local dev server | 8501 | Default, auto-assigned by `streamlit run` |
