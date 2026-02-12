import streamlit as st
import random

@st.dialog("🧠 Разминка")
def show_warmup():
    if "w_a" not in st.session_state:
        st.session_state.w_a = random.randint(11, 99)
        st.session_state.w_b = random.randint(11, 99)
    
    a, b = st.session_state.w_a, st.session_state.w_b
    st.write(f"Реши в уме: **{a} + {b}**")
    
    val = st.text_input("Результат:", key="w_val")
    if st.button("Проверить"):
        if val == str(a + b):
            st.success("Верно! Ты в форме.")
            del st.session_state.w_a
            del st.session_state.w_b
        else:
            st.error("Ошибка. Попробуй еще раз.")
