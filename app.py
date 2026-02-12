import streamlit as st
from config import SUBJECTS
from styles import apply_styles
from brain import get_ai_response
from warmup import show_warmup

st.set_page_config(page_title="Akylman Ultra", layout="wide")
apply_styles()

if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.title("✨ Akylman")
    subject = st.selectbox("Урок:", list(SUBJECTS.keys()))
    
    st.markdown('<div class="warmup-card"><b>🧠 Ежедневная разминка</b><br>Нажми для теста</div>', unsafe_allow_html=True)
    if st.button("Начать разминку"):
        show_warmup()
    
    st.divider()
    uploaded_file = st.file_uploader("📂 Загрузить материалы")
    if st.button("🗑 Очистить"):
        st.session_state.messages = []
        st.rerun()

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Спроси что-нибудь..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = get_ai_response(prompt, subject, history=st.session_state.messages)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
