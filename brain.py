from groq import Groq
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_ai_response(prompt, subject, file_context, web_info, messages):
    sys_prompt = f"""Ты — Akylman AI, эксперт по {subject}. 
    Контекст файла: {file_context}
    Данные из сети: {web_info}
    Объясняй глубоко и понятно.
    Тебя создал Исанур."""

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": sys_prompt}] + messages,
        stream=True
    )
    return stream
