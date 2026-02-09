import streamlit as st
import google.generativeai as genai
import random
from datetime import datetime

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-pro"
SYSTEM_PROMPT = "Ты — Akylman AI, мудрый наставник. Ты всегда начинаешь диалог первым. Ты человечный, ироничный и умный."

genai.configure(api_key=GOOGLE_API_KEY)
def get_opener():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро! Я Акылман. Готов к новым свершениям сегодня?"
    elif 12 <= hour < 18:
        return "Добрый день! Акылман на связи. Нужна помощь или просто беседа?"
    else:
        return "Добрый вечер. Как прошел день? Давай обсудим что-нибудь важное."

def generate_response(messages):
    model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=SYSTEM_PROMPT)
    formatted_history = []
    for msg in messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        formatted_history.append({"role": role, "parts": [msg["content"]]})
    
    chat = model.start_chat(history=formatted_history)
    try:
        response = chat.send_message(messages[-1]["content"])
        return response.text
    except Exception as e:
        return f"Ошибка: {str(e)}"

st.set_page_config(page_title="Akylman AI 2.0", page_icon="🧠")
st.title("Akylman AI")

if "messages" not in st.session_state:
    st.session_state.messages = []
    opener = get_opener()
    st.session_state.messages.append({"role": "assistant", "content": opener})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Напиши мне..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        res = generate_response(st.session_state.messages)
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})
