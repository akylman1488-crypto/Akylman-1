import streamlit as st
from brain import get_quiz_json

def show_quiz_tool(subject):
    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = "setup"
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.questions = []
        st.session_state.answered = False

    if st.session_state.quiz_state == "setup":
        st.markdown("### 📝 Создание нового теста")
        topic = st.text_input("Введи тему:")
        if st.button("Начать тест") and topic:
            with st.spinner("Генерирую вопросы..."):
                qs = get_quiz_json(topic, subject)
                if qs:
                    st.session_state.questions = qs
                    st.session_state.quiz_state = "playing"
                    st.rerun()

    elif st.session_state.quiz_state == "playing":
        q_idx = st.session_state.current_q
        q_total = len(st.session_state.questions)
        q = st.session_state.questions[q_idx]

        st.progress((q_idx) / q_total)
        st.write(f"Вопрос {q_idx + 1} из {q_total}")
        st.subheader(q["question"])

        for opt in q["options"]:
            if st.button(opt, use_container_width=True, disabled=st.session_state.answered):
                st.session_state.answered = True
                if opt == q["answer"]:
                    st.session_state.score += 1
                    st.success("✅ Верно!")
                else:
                    st.error(f"❌ Ошибка. Правильно: {q['answer']}")
        
        if st.session_state.answered:
            if st.button("Дальше" if q_idx + 1 < q_total else "Показать результат"):
                if q_idx + 1 < q_total:
                    st.session_state.current_q += 1
                    st.session_state.answered = False
                else:
                    st.session_state.quiz_state = "results"
                st.rerun()

    elif st.session_state.quiz_state == "results":
        st.balloons()
        st.markdown("### 🏆 Тест завершен!")
        score = st.session_state.score
        total = len(st.session_state.questions)
        accuracy = int((score / total) * 100)
        
        col1, col2 = st.columns(2)
        col1.metric("Счет", f"{score}/{total}")
        col2.metric("Точность", f"{accuracy}%")
        
        if st.button("Заново"):
            st.session_state.quiz_state = "setup"
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()
