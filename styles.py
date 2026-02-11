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
        background-color: #000000;
    }
    .stSidebar {
        background-color: #F8F9FB;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-image: url("https://www.transparenttextures.com/patterns/cubes.png"); /* Или ссылка на орнамент */
        background-color: #0e1117;
    }
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #00ffcc;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)
