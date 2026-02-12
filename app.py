import streamlit as st

st.set_page_config(page_title="Akylman Ultra", layout="wide")

from config import SUBJECTS
from styles import apply_styles
from brain import get_ai_response
from utils import extract_text
from warmup import show_warmup
from quiz_gen import show_quiz_tool

apply_styles()

if "messages" not in st.session_state: st.session_state.messages = []
if "tool_mode" not in st.session_state: st.session_state.tool_mode = "Chat"

with st.sidebar:
    st.title("✨ Akylman")
    subject = st.selectbox("Урок:", list(SUBJECTS.keys()), key="sub_select")
    
    st.divider()
    if st.button("🧠 Разминка", use_container_width=True, key="btn_warmup"):
        show_warmup()
    
    if st.button("📝 Создать тест", use_container_width=True, key="btn_quiz"):
        st.session_state.tool_mode = "Quiz"
    
    if st.button("💬 Чат", use_container_width=True, key="btn_chat"):
        st.session_state.tool_mode = "Chat"

    st.divider()
    uploaded_file = st.file_uploader("📂 Файлы", type=['pdf', 'docx'], key="f_up")
    
    if st.button("🗑 Очистить", key="btn_clear"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div class="main-header">✨ Akylman</div>', unsafe_allow_html=True)

if st.session_state.tool_mode == "Quiz":
    show_quiz_tool(subject)
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Спроси Akylman..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            ctx = extract_text(uploaded_file) if uploaded_file else ""
            resp = get_ai_response(prompt, subject, st.session_state.messages, ctx)
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp})
