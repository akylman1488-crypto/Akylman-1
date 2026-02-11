import streamlit as st
import time

def study_timer():
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None

    if st.button("⏱ Запустить таймер на 25 мин"):
        st.session_state.start_time = time.time()
        st.success("Таймер запущен!")

    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, 1500 - int(elapsed))
        st.sidebar.write(f"Осталось: {remaining // 60}:{remaining % 60:02d}")
