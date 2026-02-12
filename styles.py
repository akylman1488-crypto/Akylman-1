import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
        
        html, body, .stMarkdown, .stText, .stButton, .stChatInput {
            font-family: 'Google Sans', sans-serif !important;
        }

        .main-header {
            text-align: center;
            font-size: 42px;
            font-weight: 700;
            background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 25px;
        }

        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
        }

        .stChatMessage {
            border-radius: 15px;
        }
        </style>
    """, unsafe_allow_html=True)
