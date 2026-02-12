import streamlit as st
from config import SUBJECTS
from styles import apply_styles
from brain import get_ai_response
from utils import extract_text
from warmup import show_warmup
from quiz_gen import show_quiz_tool

# Настройка страницы ДОЛЖНА быть первой строчкой
st.set_page_config(page_title="Akylman Ultra Pro", layout="wide", page_icon="🎓")

apply_styles()

# Инициализация сессии
if "messages" not in st.session_state: st.session_state.messages = []
if "tool_mode" not in st.session_state: st.session_state.tool_mode = "Chat"

# --- БОКОВАЯ ПАНЕЛЬ (Один блок, без дублей) ---
with st.sidebar:
    st.markdown("## ✨ Akylman Меню")
    subject = st.selectbox("Выберите урок:", list(SUBJECTS.keys()), key="sb_subject")
    
    st.divider()
    st.markdown("### 🧠 Активности")
    if st.button("🔥 Начать разминку", use_container_width=True, key="sb_warmup"):
        show_warmup()
    
    if st.button("📝 Тестовые вопросы", use_container_width=True, key="sb_quiz"):
        st.session_state.tool_mode = "Quiz"
        
    if st.button("💬 Вернуться в чат", use_container_width=True, key="sb_chat"):
        st.session_state.tool_mode = "Chat"

    st.divider()
    uploaded_file = st.file_uploader("📂 Материалы (PDF/DOCX)", type=['pdf', 'docx'], key="sb_file")
    
    if st.button("🗑 Очистить историю", key="sb_clear"):
        st.session_state.messages = []
        st.rerun()

# --- ЦЕНТРАЛЬНАЯ ЧАСТЬ (Ваш заголовок) ---
st.markdown(f'<div class="main-header">✨ Akylman: {subject}</div>', unsafe_allow_html=True)

if st.session_state.tool_mode == "Quiz":
    show_quiz_tool(subject)
else:
    # Отображение сообщений
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Ввод
    if prompt := st.chat_input("Спроси Akylman..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            context = extract_text(uploaded_file) if uploaded_file else ""
            # Теперь вызов сработает, так как в brain.py есть значения по умолчанию
            response = get_ai_response(prompt, subject, history=st.session_state.messages, context=context)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
