import streamlit as st

@st.dialog("🔥 Быстрая разминка")
def show_warmup():
    st.write("Реши задачу: сколько будет $2^{10}$?")
    answer = st.text_input("Твой ответ:")
    if st.button("Проверить"):
        if answer == "1024":
            st.success("Гениально!")
        else:
            st.error("Попробуй еще раз.")
