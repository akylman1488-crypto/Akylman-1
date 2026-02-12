import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
        
        html, body, [class*="st-"] {
            font-family: 'Google Sans', sans-serif;
            background-color: #ffffff;
        }

        /* Центрирование имени ИИ */
        .main-header {
            text-align: center;
            font-size: 42px;
            font-weight: 700;
            color: #1f1f1f;
            margin-bottom: 20px;
        }

        .stApp { background-color: #ffffff; }
        [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #e3e3e3; }
        .stChatInput { border-radius: 28px !important; border: 1px solid #747775 !important; }
        [data-testid="stChatMessageAvatarAssistant"] {
            background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570);
            border-radius: 50%;
        }
        </style>
    """, unsafe_allow_html=True)
