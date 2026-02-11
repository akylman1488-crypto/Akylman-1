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
import streamlit as st

def apply_dynamic_theme(subject):
    from config import THEMES
    theme = THEMES.get(subject, THEMES["Mathematics"])
    
    st.markdown(f"""
        <style>
        /* Плавный переход для всего приложения */
        .stApp {{
            background: {theme['grad']};
            transition: background 0.8s ease-in-out;
        }}
        
        /* Стилизация сайдбара */
        [data-testid="stSidebar"] {{
            background-color: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            transition: all 0.8s ease-in-out;
        }}

        /* Плавные кнопки */
        .stButton>button {{
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.1);
            color: white;
            border-radius: 12px;
            transition: 0.3s;
        }}
        
        .stButton>button:hover {{
            border: 1px solid white;
            background: rgba(255,255,255,0.2);
            box-shadow: 0 0 15px {theme['color']};
        }}
        </style>
    """, unsafe_allow_html=True)
