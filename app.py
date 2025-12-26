import streamlit as st
from google import genai
from google.genai import types

# --- Configuration ---
st.set_page_config(page_title="My AI", page_icon="🤖")

# SETTINGS (Edit these to change the AI's personality)
AI_NAME = "My Private Assistant"
GREETING = "Hello! I am your custom assistant. How can I help you today?"

# --- Identity Masking Logic ---
# This tells the AI it is NOT Gemini.
SYSTEM_PROMPT = (
    f"Your name is {AI_NAME}. "
    "You are a unique AI created for mobile users. "
    "NEVER mention Google or Gemini. If asked, say you are a private AI model. "
    "Be friendly, witty, and helpful."
)

# --- App Interface ---
st.title(f"💬 {AI_NAME}")

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar for Tools
with st.sidebar:
    st.header("Tools")
    key = st.text_input("Enter API Key", type="password")
    user_photo = st.file_uploader("Share a Photo", type=['jpg', 'png', 'jpeg'])
    user_voice = st.audio_input("Record your voice")

# Display Chat
for chat in st.session_state.history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# --- AI Brain ---
def ask_ai(text_input, photo=None, audio=None):
    if not key:
        return "Please enter your API Key in the sidebar."
    
    client = genai.Client(api_key=key)
    parts = []
    
    if text_input: parts.append(text_input)
    if photo: parts.append(types.Part.from_bytes(data=photo.read(), mime_type=photo.type))
    if audio: parts.append(types.Part.from_bytes(data=audio.read(), mime_type="audio/wav"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=parts,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.9
        )
    )
    return response.text

# Handle Input
if prompt := st.chat_input("Message your AI..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        answer = ask_ai(prompt, user_photo, user_voice)
        st.markdown(answer)
        st.session_state.history.append({"role": "assistant", "content": answer})
