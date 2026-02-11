import streamlit as st
from config import SUBJECTS
from styles import apply_styles
from utils import extract_text, search_web
from brain import get_ai_response
from data_manager import download_chat_button

st.set_page_config(page_title="Akylman AI Pro", layout="wide")

apply_styles()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("🎓 Akylman Hub")
    subject = st.selectbox("Выберите предмет:", list(SUBJECTS.keys()))
    uploaded_file = st.file_uploader("Загрузить файл", type=['pdf', 'txt', 'docx'])
    
    if st.button("🗑 Очистить чат", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    download_chat_button()

st.title(f"{SUBJECTS[subject]} {subject}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Спроси меня..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        f_txt = extract_text(uploaded_file) if uploaded_file else ""
        w_txt = search_web(f"{subject} {prompt}")
        
        response_stream = get_ai_response(prompt, subject, f_txt, w_txt, st.session_state.messages)
        
        for chunk in response_stream:
            if chunk.choices[0].delta.content:
                full_res += chunk.choices[0].delta.content
                placeholder.markdown(full_res + "▌")
        
        placeholder.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
