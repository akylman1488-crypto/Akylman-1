import streamlit as st
import random

@st.dialog("🧠 Разминка")
def show_warmup():
    if "q_a" not in st.session_state:
        st.session_state.q_a = random.randint(10, 50)
        st.session_state.q_b = random.randint(10, 50)
    
    a, b = st.session_state.q_a, st.session_state.q_b
    st.write(f"Сколько будет: **{a} + {b}**?")
    
    ans = st.text_input("Ответ:", key="warmup_field")
    
    if st.button("Проверить", key="check_warmup"):
        if ans == str(a + b):
            st.success("Правильно!")
            del st.session_state.q_a
            del st.session_state.q_b
        else:
            st.error("Ошибка, попробуй еще раз.")
