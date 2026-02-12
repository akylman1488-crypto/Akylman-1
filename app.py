import streamlit as st
from config import SUBJECTS
from styles import apply_styles
from brain import get_ai_response
from utils import extract_text
from warmup import show_warmup
from quiz_gen import show_quiz_tool

# 1. Настройка страницы должна быть ВЫШЕ всех вызовов streamlit
st.set_page_config(page_title="Akylman Ultra Pro", layout="wide", page_icon="🎓")

apply_styles()

# Инициализация сессии
if "messages" not in st.session_state: st.session_state.messages = []
if "tool_mode" not in st.session_state: st.session_state.tool_mode = "Chat"

# БОКОВАЯ ПАНЕЛЬ
with st.sidebar:
    st.title("✨ Akylman")
    
    # Выбор предмета
    subject = st.selectbox("Предмет:", list(SUBJECTS.keys()), key="main_subject_select")
    
    st.divider()
    
    # Кнопка разминки
    st.markdown("### 🧠 Разминка")
    if st.button("Начать разминку", use_container_width=True, key="warmup_btn_sidebar"):
        show_warmup()
    
    st.divider()
    
    # Управление режимами
    if st.button("📝 Создать тест", use_container_width=True, key="mode_quiz_btn"):
        st.session_state.tool_mode = "Quiz"
    if st.button("💬 Вернуться в чат", use_container_width=True, key="mode_chat_btn"):
        st.session_state.tool_mode = "Chat"
        
    st.divider()
    
    uploaded_file = st.file_uploader("📂 Загрузить учебные материалы", type=['pdf', 'docx'], key="file_uploader_sidebar")
    
    if st.button("🗑 Очистить чат", key="clear_chat_btn"):
        st.session_state.messages = []
        st.rerun()

# ЦЕНТРАЛЬНЫЙ ЗАГОЛОВОК (Исправляем пустую область с твоего скриншота)
st.markdown('<div class="main-header">✨ Akylman</div>', unsafe_allow_html=True)

# ГЛАВНАЯ ЛОГИКА
if st.session_state.tool_mode == "Quiz":
    show_quiz_tool(subject)
else:
    # Отрисовка сообщений
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Поле ввода
    if prompt := st.chat_input("Спроси Akylman о чем угодно..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # Читаем файл если он есть
            context_data = extract_text(uploaded_file) if uploaded_file else ""
            
            # Вызов функции с правильным количеством аргументов
            response = get_ai_response(
                prompt=prompt, 
                subject=subject, 
                history=st.session_state.messages,
                context=context_data
            )
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
