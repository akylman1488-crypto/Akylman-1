import streamlit as st
import random

@st.dialog("🧠 Ежедневная разминка")
def show_warmup():
    # Генерируем числа только один раз за открытие окна
    if "w_a" not in st.session_state:
        st.session_state.w_a = random.randint(10, 50)
        st.session_state.w_b = random.randint(10, 50)
    
    a, b = st.session_state.w_a, st.session_state.w_b
    st.write(f"Реши пример, чтобы проснуться: **{a} + {b} = ?**")
    
    # Уникальный ключ key="warmup_ans_input" обязателен
    ans = st.text_input("Твой ответ:", key="warmup_ans_input")
    
    if st.button("Проверить", key="warmup_check_btn"):
        if ans == str(a + b):
            st.success("🎯 Верно! Мозг активирован.")
            # Сброс для следующего раза
            del st.session_state.w_a
            del st.session_state.w_b
        else:
            st.error("Попробуй еще раз!")
