import streamlit as st
from anthropic import Anthropic

st.set_page_config(page_title="Inkstruct", page_icon="📝")

st.title("Inkstruct")
st.caption("From scattered notes to structured writing.")

MOCK_MODE = True  # Set to False once Claude API credits are available

if st.button("Test Claude Connection"):
    with st.spinner("Talking to Claude..."):
        try:
            if MOCK_MODE:
                st.warning("Running in MOCK MODE — no real API call made (no credits yet).")
                st.success("Mock connection successful!")
                st.write("Hello! This is a placeholder response standing in for Claude.")
            else:
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