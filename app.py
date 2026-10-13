import os
import streamlit as st
from google import genai
from google.genai import types

# Page configuration
st.set_page_config(page_title="Class 12 AI Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Class 12 AI Project Chatbot")
st.write("An intelligent assistant powered by Google Gemini.")

# Get API key from Streamlit secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ Please add your Gemini API Key in Streamlit Cloud Secrets settings.")
    st.stop()

client = genai.Client(api_key=api_key)

# Initialize chat session state
if "chat_history" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful and educational AI assistant created for a Class 12 Artificial Intelligence project.",
            temperature=0.7,
        )
    )
    st.session_state.chat_history = []

# Display chat messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                bot_reply = response.text
                st.markdown(bot_reply)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"An error occurred: {e}")
