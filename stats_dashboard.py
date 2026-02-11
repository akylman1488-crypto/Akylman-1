import streamlit as st
import pandas as pd

def show_stats():
    if "history_stats" not in st.session_state:
        st.session_state.history_stats = []
    
    if st.session_state.history_stats:
        df = pd.DataFrame(st.session_state.history_stats)
        st.sidebar.write("📊 Твоя активность:")
        st.sidebar.bar_chart(df['subject'].value_counts())

def update_stats(subject):
    if "history_stats" not in st.session_state:
        st.session_state.history_stats = []
    st.session_state.history_stats.append({"subject": subject})
