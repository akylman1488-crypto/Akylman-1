import streamlit as st
from groq import Groq
import random
from datetime import datetime
from pypdf import PdfReader

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Akylman AI 3.0", page_icon="🧠")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

def get_opener():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "Доброе утро! Я Akylman. Готов к работе?"
    elif 12 <= hour < 18: return "Добрый день! Akylman на связи. Что нового?"
    else: return "Добрый вечер. Давай обсудим что-нибудь важное."

def generate_response(messages, model_id):
    try:
        completion = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "system", "content": "Ты — Akylman AI, мудрый наставник."}] + 
                     [{"role": m["role"], "content": m["content"]} for m in messages],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {str(e)}"

with st.sidebar:
    st.title("🧠 Akylman")
    
    if st.button("➕ Новый чат", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    model_options = {
        "Быстрая ⚡": "llama3-8b-8192",
        "Думающая 🤔": "llama-3.3-70b-versatile"
    }

    password = st.text_input("Введи пароль доступа:", type="password")
    if password:
            if not st.session_state.access_granted:
                st.session_state.access_granted = True
                st.success("Пароль верен!")
                st.balloons() 
            
            model_options["Версия Про 🔥"] = "llama-3.1-70b-specdec"
            model_options["Версия Плюс 💎"] = "mixtral-8x7b-32768"
        else:
            st.error("Пароль неверен")
            st.session_state.access_granted = False

    selected_model_name = st.selectbox("Выберите модель:", list(model_options.keys()))
    selected_model = model_options[selected_model_name]

    st.markdown("---")
    uploaded_file = st.file_uploader("📂 Анализ файлов", type=["pdf", "txt"])

st.markdown("<h1 style='text-align: center;'>Akylman</h1>", unsafe_allow_html=True)

if not st.session_state.messages:
    opener = get_opener()
    st.session_state.messages.append({"role": "assistant", "content": opener})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Спроси Akylman..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Размышляю..."):
            res = generate_response(st.session_state.messages, selected_model)
            st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})
