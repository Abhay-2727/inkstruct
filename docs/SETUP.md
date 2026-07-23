# Inkstruct — Setup Guide

Version 1.0 | Day 3 Deliverable

This is the complete, from-scratch guide to get Inkstruct running locally on Windows. Follow in order.

## 1. Prerequisites

| Tool | Minimum Version | Check with |
|---|---|---|
| Python | 3.9+ (we're using 3.12.0) | `python --version` |
| Git | Any recent version | `git --version` |
| A code editor | VS Code recommended | — |

## 2. Clone the Repository

```
cd Desktop
git clone https://github.com/Abhay-2727/inkstruct.git
cd inkstruct
```

## 3. Create and Activate a Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal prompt once active.

## 4. Install Dependencies

```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` contains:
```
streamlit
anthropic
python-docx
pypdf
fpdf2
```

## 5. Configure Your Claude API Key

1. Ensure `.streamlit/secrets.toml` exists (create the folder/file if missing).
2. Add your key:
   ```
   ANTHROPIC_API_KEY = "your-key-here"
   ```
3. Confirm `.gitignore` includes `.streamlit/secrets.toml` **before** your first `git add .` — this file must never be committed.

## 6. Run the App

```
python -m streamlit run app.py
```

Opens automatically at `http://localhost:8501`. If not, copy the URL shown in the terminal into your browser.

## 7. Verify It Works

Click **"Test Claude Connection"** in the app. You should see either:
- A real Claude response (if API credits are available), or
- A clearly labeled mock response (if running in `MOCK_MODE`, see Known Issues below)

---

## Known Issues & Workarounds (discovered Day 3)

### Issue 1: Windows Application Control policy blocks `.exe` files
**Symptom:** Errors like `Program 'pip.exe' failed to run: An Application Control policy has blocked this file` or the same for `streamlit.exe`.

**Cause:** A Windows security policy (Smart App Control or managed-device policy) blocks certain executables from running directly, even legitimate ones.

**Fix:** Always run these tools through Python instead of as standalone executables:
```
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
Never use the bare `pip` or `streamlit` commands on this machine — use the `python -m` form everywhere in this project.

### Issue 2: "Your credit balance is too low to access the Anthropic API"
**Symptom:** A 400 error from the Claude API when testing the connection, even with a correctly configured key.

**Cause:** The Anthropic Console account has $0 available credit. The Claude API is metered/paid separately from any Claude.ai subscription.

**Workaround (current):** `app.py` includes a `MOCK_MODE = True` flag. While true, the app returns a clearly labeled placeholder response instead of calling the real API — this lets development continue on everything except real AI output.

**To resume real API calls:** Add credit at https://console.anthropic.com under Plans & Billing, then set `MOCK_MODE = False` in `app.py`.

## 8. Git Workflow Reminder

Always create/verify `.gitignore` **before** your first `git add .` in a new project — a file that's already been staged once before being ignored will keep showing as tracked until explicitly removed from Git's index.
