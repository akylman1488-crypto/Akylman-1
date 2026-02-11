import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&display=swap');

        html, body, [class*="st-"] {
            font-family: 'Google Sans', sans-serif;
        }

        .stApp {
            background-color: #ffffff;
        }

        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
            border-right: 1px solid #e3e3e3;
        }

        .stChatMessage {
            background-color: transparent !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }

        [data-testid="stChatMessageAvatarUser"] {
            background-color: #5f6368 !important;
        }

        [data-testid="stChatMessageAvatarAssistant"] {
            background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570);
        }

        .stChatInputContainer {
            padding-bottom: 2rem;
            background-color: transparent !important;
        }

        .stChatInput {
            border-radius: 28px !important;
            border: 1px solid #747775 !important;
            padding: 10px 20px !important;
        }

        .stButton>button {
            border-radius: 20px;
            text-transform: none;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

def apply_dynamic_theme(subject):
    pass
