import streamlit as st
from app.file_parser import extract_text

st.set_page_config(page_title="Inkstruct", page_icon="📝")

st.title("Inkstruct")
st.caption("From scattered notes to structured writing.")

MOCK_MODE = True  # Set to False once Claude API credits are available

# ---------- INPUT SECTION ----------
st.subheader("1. Add your notes")

input_mode = st.radio("Choose input method:", ["Paste Text", "Upload File"], horizontal=True)

extracted_text = ""
error_message = ""

if input_mode == "Paste Text":
    pasted_text = st.text_area("Paste your notes here:", height=200, placeholder="Paste messy notes, research, or ideas...")
    extracted_text = pasted_text.strip()

else:
    uploaded_file = st.file_uploader("Upload a .txt, .docx, or .pdf file", type=["txt", "docx", "pdf"])
    if uploaded_file is not None:
        try:
            extracted_text = extract_text(uploaded_file).strip()
        except Exception as e:
            error_message = f"Could not read this file: {e}"

# ---------- VALIDATION + PREVIEW ----------
if error_message:
    st.error(error_message)
elif extracted_text and len(extracted_text) < 20:
    st.warning("This looks too short to generate a useful outline. Please add more content.")
elif extracted_text:
    st.subheader("2. Preview")
    st.text_area("Extracted text (read-only):", value=extracted_text, height=200, disabled=True)
    st.success(f"Ready — {len(extracted_text)} characters extracted.")
else:
    st.info("Paste text or upload a file to get started.")

# ---------- TEMP: Claude connection test (kept from Day 3, will be replaced Day 5) ----------
st.divider()
st.caption("Diagnostic: Claude API connection test (temporary, removed once outline generation is built)")

if st.button("Test Claude Connection"):
    with st.spinner("Talking to Claude..."):
        try:
            if MOCK_MODE:
                st.warning("Running in MOCK MODE — no real API call made (no credits yet).")
                st.success("Mock connection successful!")
                st.write("Hello! This is a placeholder response standing in for Claude.")
            else:
                from anthropic import Anthropic
                client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=100,
                    messages=[{"role": "user", "content": "Say hello in one short sentence."}]
                )
                st.success("Connected to Claude successfully!")
                st.write(response.content[0].text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")