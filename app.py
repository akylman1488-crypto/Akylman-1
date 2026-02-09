import streamlit as st
from groq import Groq
import random
from datetime import datetime

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MODEL_NAME = "llama-3.3-70b-versatile"
SYSTEM_PROMPT = "Ты — Akylman AI, мудрый наставник. Ты всегда начинаешь диалог первым. Ты человечный, ироничный и умный. Отвечай на языке пользователя."

client = Groq(api_key=GROQ_API_KEY)

def get_opener():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро! Я Акылман. Готов к новым свершениям сегодня?"
    elif 12 <= hour < 18:
        return "Добрый день! Акылман на связи. Нужна помощь или просто беседа?"
    else:
        return "Добрый вечер. Как прошел день? Давай обсудим что-нибудь важное."

def generate_response(messages):
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + 
                     [{"role": m["role"], "content": m["content"]} for m in messages],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Ой, мои мысли запутались... Давай еще раз? (Ошибка: {str(e)})"

st.set_page_config(page_title="Akylman AI 2.0", page_icon="🧠")
st.title("Akylman AI (Powered by Groq)")

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
