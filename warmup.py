import streamlit as st
import random

@st.dialog("🧠 Разминка для мозга")
def show_warmup():
    if "w_a" not in st.session_state:
        st.session_state.w_a = random.randint(10, 50)
        st.session_state.w_b = random.randint(10, 50)
    
    a, b = st.session_state.w_a, st.session_state.w_b
    st.write(f"Сколько будет: **{a} + {b}**?")
    
    ans = st.text_input("Введите ответ:", key="w_input")
    
    if st.button("Проверить"):
        if ans == str(a + b):
            st.success("🎯 Верно! Вы молодец.")
            # Чистим для следующего раза
            del st.session_state.w_a
            del st.session_state.w_b
            st.balloons()
        else:
            st.error("❌ Не совсем так. Попробуйте еще раз!")
