import streamlit as st
from brain import get_ai_response

def show_quiz_tool(subject):
    st.markdown("### 📝 Генератор интерактивных тестов")
    topic = st.text_input("Тема теста:", key="q_topic")
    
    if st.button("Создать тест"):
        if topic:
            with st.spinner("Создаю вопросы..."):
                prompt = f"Создай 3 вопроса по теме {topic}. Формат: Вопрос | Вариант А | Вариант Б | Вариант В | Ответ"
                st.session_state.quiz_data = get_ai_response(prompt, subject)
    
    if "quiz_data" in st.session_state:
        st.info("Ответь на вопросы ниже:")
        st.markdown(st.session_state.quiz_data)
        st.text_input("Твои ответы (например: 1А, 2Б...))
        if st.button("Проверить"):
            st.success("Ответы отправлены на проверку!")
