import streamlit as st
import pandas as pd

# 1. Настройка страницы (ВСЕГДА ПЕРВАЯ)
st.set_page_config(page_title="Akylman Gemini", layout="wide", page_icon="✨")

# 2. Безопасный импорт
try:
    from config import SUBJECTS
    from styles import apply_styles
    from brain import get_ai_response
    from data_manager import download_chat_button
    from visualizer import create_chart       # Функция графиков
    # from quiz_gen import generate_quiz      # Раскомментируй, если есть файл
    from utils import extract_text            # Для чтения файлов
except ImportError as e:
    st.error(f"⚠️ Ошибка импорта: {e}")
    st.stop()

# 3. Инициализация переменных
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_subject" not in st.session_state:
    st.session_state.current_subject = "Just Friend"

# 4. Сайдбар
with st.sidebar:
    st.title("✨ Akylman")
    
    # Выбор предмета
    selected_subject_key = st.selectbox(
        "Выбор режима:", 
        list(SUBJECTS.keys()),
        index=0
    )
    
    # ЛОГИКА: Если предмет изменился -> чистим чат
    if selected_subject_key != st.session_state.current_subject:
        st.session_state.messages = []
        st.session_state.current_subject = selected_subject_key
        st.rerun() # Перезагрузка страницы
        
    st.markdown(f"**Текущий урок:** {SUBJECTS[selected_subject_key]}")
    
    st.divider()
    
    # Загрузка файлов
    uploaded_file = st.file_uploader("📂 Загрузить файл (PDF/TXT)", type=["pdf", "txt", "csv"])
    
    st.divider()
    
    # Дополнительные функции
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 График"):
            st.session_state.show_chart = True
    with col2:
        if st.button("📝 Тест"):
            # generate_quiz(selected_subject_key) # Если есть функция
            st.info("Генерация теста...")

    st.divider()
    
    if st.button("🗑 Очистить чат"):
        st.session_state.messages = []
        st.rerun()

# 5. Основной интерфейс
apply_styles()

# Заголовок
st.header(SUBJECTS[selected_subject_key])

# Если нажали кнопку графика (пример)
if st.session_state.get("show_chart"):
    with st.expander("Конструктор графиков", expanded=True):
        st.write("Загрузите CSV или введите данные для построения графика")
        # Тут вызов create_chart() из visualizer.py
        if st.button("Закрыть"):
            st.session_state.show_chart = False
            st.rerun()

# Вывод сообщений
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 6. Обработка ввода
if prompt := st.chat_input("Введите сообщение..."):
    # Сохраняем и показываем вопрос
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Получаем ответ от ИИ
    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            try:
                # Обработка файла
                file_text = ""
                if uploaded_file:
                    # Простая проверка типа файла
                    if uploaded_file.name.endswith(".csv"):
                        st.info("CSV файл загружен для анализа данных.")
                        file_text = "Пользователь загрузил CSV таблицу."
                    else:
                        file_text = extract_text(uploaded_file)

                # УМНЫЙ ВЫЗОВ ФУНКЦИИ (Работает и с Plus, и с обычной версией)
                try:
                    # Пробуем вызвать как Plus (5 аргументов)
                    response = get_ai_response(
                        prompt, 
                        selected_subject_key, 
                        file_text, 
                        "", # web_info пока пусто
                        st.session_state.messages
                    )
                except TypeError:
                    # Если ошибка - вызываем старую версию (2 аргумента)
                    response = get_ai_response(prompt, selected_subject_key)
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            except Exception as e:
                st.error(f"Ошибка: {e}")
