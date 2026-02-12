import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
        
        html, body, .stMarkdown, .stText, .stButton, .stChatInput {
            font-family: 'Google Sans', sans-serif;
        }

        .main-header {
            text-align: center;
            font-size: 40px;
            font-weight: 700;
            background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }

        [data-testid="stSidebar"] { 
            background-color: #f8f9fa; 
        }
        
        .stChatInputContainer {
            padding-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
