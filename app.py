import streamlit as st

# 1. СТРОГО ПЕРВАЯ КОМАНДА
st.set_page_config(page_title="Akylman Ultra Pro", layout="wide", page_icon="🎓")

from config import SUBJECTS
from styles import apply_styles
from brain import get_ai_response
from utils import extract_text
from warmup import show_warmup
from quiz_gen import show_quiz_tool

apply_styles()

# Инициализация
if "messages" not in st.session_state: st.session_state.messages = []
if "tool_mode" not in st.session_state: st.session_state.tool_mode = "Chat"

# --- ЕДИНЫЙ БОКОВОЙ ПАНЕЛЬ (Fix Duplicate ID) ---
with st.sidebar:
    st.title("✨ Akylman")
    
    # Выбор предмета
    subject = st.selectbox("Урок:", list(SUBJECTS.keys()), key="main_sub_select")
    
    st.divider()
    
    # Кнопка разминки
    st.markdown("### 🧠 Активность")
    if st.button("Начать разминку", use_container_width=True, key="side_warmup"):
        show_warmup()
    
    # Кнопки инструментов
    if st.button("📝 Создать тест", use_container_width=True, key="side_quiz"):
        st.session_state.tool_mode = "Quiz"
    
    if st.button("💬 Вернуться в чат", use_container_width=True, key="side_chat"):
        st.session_state.tool_mode = "Chat"

    st.divider()
    
    uploaded_file = st.file_uploader("📂 Загрузить файлы", type=['pdf', 'docx'], key="side_file")
    
    if st.button("🗑 Очистить историю", key="side_clear"):
        st.session_state.messages = []
        st.rerun()

# --- ГЛАВНЫЙ ЭКРАН ---

# Выводим имя ИИ по центру (твоя красная зона)
st.markdown('<div class="main-header">✨ Akylman</div>', unsafe_allow_html=True)

if st.session_state.tool_mode == "Quiz":
    show_quiz_tool(subject)
else:
    # Отрисовка чата
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Поле ввода
    if prompt := st.chat_input("Спроси Akylman..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # Извлекаем текст из файла
            context_text = extract_text(uploaded_file) if uploaded_file else ""
            
            # Вызываем исправленную функцию (теперь без TypeError)
            response = get_ai_response(
                prompt=prompt, 
                subject=subject, 
                history=st.session_state.messages,
                context=context_text
            )
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
