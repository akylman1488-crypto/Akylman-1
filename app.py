import streamlit as st
from config import SUBJECTS
from styles import apply_styles, apply_dynamic_theme

# 1. Настройка страницы (ДОЛЖНА БЫТЬ ПЕРВОЙ СТРОКОЙ КОДА)
st.set_page_config(page_title="Akylman Ultra Pro", layout="wide")

# 2. Инициализация памяти
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. ЕДИНЫЙ Сайдбар
with st.sidebar:
    st.title("🎓 Akylman Ultra")
    
    # Выбор предмета
    subject = st.selectbox("Выберите предмет:", list(SUBJECTS.keys()), key="main_subject_select")
    
    # Плавная тема (наша новая фишка)
    apply_dynamic_theme(subject)
    
    st.markdown("---")
    
    # Кнопка очистки
    if st.button("🗑 Очистить историю"):
        st.session_state.messages = []
        st.rerun()

    # Сюда можно будет добавить генератор картинок позже
    # from image_gen import generate_image_ui
    # generate_image_ui()

# 4. Основной интерфейс
apply_styles()
st.title(f"{subject}")

# Отображение чата
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Поле ввода
if prompt := st.chat_input("Задай вопрос своему наставнику..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Здесь будет вызов твоей модели Llama или Gemini
    with st.chat_message("assistant"):
        st.write("Я тебя услышал! Давай разберем тему...")
