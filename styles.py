import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .main-header {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            background: linear-gradient(45deg, #4285f4, #9b72cb, #d96570);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 20px;
        }
        [data-testid="stSidebar"] { background-color: #f8f9fa; }
        .stChatInput { border-radius: 20px !important; }
        </style>
    """, unsafe_allow_html=True)
