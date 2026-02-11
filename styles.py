import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatInput {
        border-top: 1px solid #30363d;
    }
    h1 {
        color: #00ffcc;
        text-shadow: 2px 2px 4px #000000;
    }
    </style>
    """, unsafe_allow_html=True)
