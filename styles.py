import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&display=swap');
        html, body, [class*="st-"] { font-family: 'Google Sans', sans-serif; background-color: #ffffff; color: #1f1f1f; }
        [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #e3e3e3; }
        .stChatInput { border-radius: 28px !important; border: 1px solid #747775 !important; }
        .stChatMessage { background-color: transparent !important; border: none !important; }
        [data-testid="stChatMessageAvatarAssistant"] { background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570); border-radius: 50%; }
        .warmup-card { background: #e8f0fe; padding: 15px; border-radius: 12px; border: 1px solid #1967d2; margin-bottom: 10px; cursor: pointer; }
        </style>
    """, unsafe_allow_html=True)
