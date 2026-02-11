import streamlit as st
import json

def save_chat_to_json():
    if "messages" in st.session_state and st.session_state.messages:
        return json.dumps(st.session_state.messages, ensure_ascii=False, indent=2)
    return None

def download_chat_button():
    chat_json = save_chat_to_json()
    if chat_json:
        st.download_button(
            label="📥 Скачать историю чата",
            data=chat_json,
            file_name="akylman_chat_history.json",
            mime="application/json",
            use_container_width=True
        )
