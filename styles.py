import streamlit as st

def apply_styles():
    st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)
    
def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
        
        html, body, .stMarkdown, .stText, .stButton, .stChatInput {
            font-family: 'Google Sans', sans-serif !important;
        }

        .main-header {
            text-align: center; font-size: 42px; font-weight: 700;
            background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 25px;
        }

        .stButton>button {
            border-radius: 12px;
            border: 1px solid #dadce0;
            background-color: white;
            color: #3c4043;
            padding: 15px;
            transition: 0.3s;
        }

        .stButton>button:hover {
            background-color: #f8f9fa;
            border-color: #4285f4;
        }
        
        [data-testid="stMetricValue"] { color: #4285f4; }
        </style>
    """, unsafe_allow_html=True)
