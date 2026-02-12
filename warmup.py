import streamlit as st
import random

@st.dialog("🧠 Ежедневная разминка")
def show_warmup():
    if "warmup_a" not in st.session_state:
        st.session_state.warmup_a = random.randint(10, 50)
        st.session_state.warmup_b = random.randint(10, 50)
    
    a, b = st.session_state.warmup_a, st.session_state.warmup_b
    st.write(f"Реши пример, чтобы активировать мозг:")
    st.subheader(f"{a} + {b} = ?")
    
    user_ans = st.text_input("Твой ответ", key="warmup_input")
    
    if st.button("Проверить"):
        if user_ans == str(a + b):
            st.success("🎉 Правильно! Ты готов к учебе.")
            # Сброс для следующего раза
            del st.session_state.warmup_a
            del st.session_state.warmup_b
        else:
            st.error("Попробуй еще раз!")
