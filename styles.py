import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&display=swap');

        /* Основной фон - белый */
        html, body, [class*="st-"] {
            font-family: 'Google Sans', sans-serif;
            background-color: #ffffff;
            color: #1f1f1f;
        }

        /* Сайдбар - светло-серый */
        [data-testid="stSidebar"] {
            background-color: #f0f4f9;
            border-right: none;
        }

        /* Убираем стандартные отступы */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        /* Сообщения чата */
        .stChatMessage {
            background-color: transparent !important;
            border: none !important;
        }

        /* Аватар пользователя */
        [data-testid="stChatMessageAvatarUser"] {
            background-color: #eceff1 !important;
            color: #000;
        }

        /* Аватар ассистента (градиент) */
        [data-testid="stChatMessageAvatarAssistant"] {
            background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570);
        }

        /* Поле ввода (закругленное) */
        .stChatInput {
            border-radius: 24px !important;
            border: 1px solid #c4c7c5 !important;
            padding: 10px 20px !important;
        }
        
        /* Кнопки в сайдбаре */
        .stButton>button {
            border-radius: 20px;
            width: 100%;
            border: 1px solid #e3e3e3;
            background: white;
            color: #444746;
        }
        .stButton>button:hover {
            background: #f0f4f9;
            border-color: #0b57d0;
            color: #0b57d0;
        }
        </style>
    """, unsafe_allow_html=True)

def apply_dynamic_theme(subject):
    pass # В стиле Gemini тема статичная (белая), меняется только контент
