import streamlit as st
import json

def save_chat_to_json():
    if st.session_state.messages:
        chat_data = json.dumps(st.session_state.messages, ensure_ascii=False, indent=2)
        return chat_data
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
