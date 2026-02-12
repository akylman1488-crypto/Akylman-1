import streamlit as st
from brain import get_ai_response

def show_quiz_tool(subject):
    st.markdown("### 📝 Генератор тестов")
    topic = st.text_input("Введи тему для теста:")
    if st.button("Создать вопросы"):
        if topic:
            prompt = f"Создай 3 тестовых вопроса с вариантами ответов по теме: {topic}"
            with st.spinner("Генерирую..."):
                response = get_ai_response(prompt, subject)
                st.markdown(response)
