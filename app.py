import streamlit as st

st.set_page_config(
    page_title="Gemini Style Akylman", 
    layout="wide",
    page_icon="✨"
)

try:
    from config import SUBJECTS
    from styles import apply_styles
    from brain import get_ai_response
    from data_manager import download_chat_button
except ImportError as e:
    st.error(f"Ошибка импорта: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

apply_styles()

with st.sidebar:
    st.title("Akylman")
    subject = st.selectbox("Предмет", list(SUBJECTS.keys()))
    if st.button("Новый чат"):
        st.session_state.messages = []
        st.rerun()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Введите запрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = get_ai_response(prompt, subject)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if st.session_state.messages:
    download_chat_button(st.session_state.messages)
