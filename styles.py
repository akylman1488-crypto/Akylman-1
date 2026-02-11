import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    .stChatMessage {
        background-color: #F0F2F6;
        border-radius: 15px;
        color: #000000;
    }
    h1, h2, h3, p, span, label {
        color: #000000 !important;
    }
    .stChatInputContainer {
        background-color: #FFFFFF;
    }
    .stSidebar {
        background-color: #F8F9FB;
    }
    </style>
    """, unsafe_allow_html=True)
