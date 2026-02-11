import streamlit as st
from config import SUBJECTS
from styles import apply_styles
from utils import extract_text, search_web
from brain import get_ai_response
from data_manager import download_chat_button
from analyzer import display_metrics
from quiz_gen import generate_quiz
from exporter import export_to_markdown
from stats_dashboard import show_stats, update_stats

st.set_page_config(page_title="Akylman Pro", layout="wide")
apply_styles()

if "messages" not in st.session_state: st.session_state.messages = []
if "last_response" not in st.session_state: st.session_state.last_response = ""

with st.sidebar:
    st.title("🎓 Akylman")
    subject = st.selectbox("Предмет:", list(SUBJECTS.keys()))
    uploaded_file = st.file_uploader("Файл:", type=['pdf', 'txt', 'docx'])
    
    f_txt = extract_text(uploaded_file) if uploaded_file else ""
    display_metrics(f_txt)
    
    if st.button("📝 Создать тест по файлу"):
        st.session_state.messages.append({"role": "assistant", "content": generate_quiz(f_txt)})
    
    export_to_markdown(st.session_state.last_response)
    download_chat_button()
    show_stats()
    
    if st.button("🗑 Очистить"):
        st.session_state.messages = []
        st.rerun()

st.title(f"{SUBJECTS[subject]} {subject}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Спроси меня..."):
    update_stats(subject)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        w_txt = search_web(f"{subject} {prompt}")
        
        stream = get_ai_response(prompt, subject, f_txt, w_txt, st.session_state.messages)
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_res += chunk.choices[0].delta.content
                placeholder.markdown(full_res + "▌")
        placeholder.markdown(full_res)
        st.session_state.last_response = full_res
        st.session_state.messages.append({"role": "assistant", "content": full_res})
