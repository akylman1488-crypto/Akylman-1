import streamlit as st
from groq import Groq
import random
from datetime import datetime
from pypdf import PdfReader
import io

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Akylman AI 3.0", page_icon="🧠")

if "sessions" not in st.session_state:
    st.session_state.sessions = {"Чат 1": []}
if "current_session" not in st.session_state:
    st.session_state.current_session = "Чат 1"

def get_opener():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "Доброе утро! Я Акылман. Готов к новым задачам?"
    elif 12 <= hour < 18: return "Добрый день! Акылман на связи. Что обсудим?"
    else: return "Добрый вечер. Есть интересные мысли на ночь глядя?"

def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        return " ".join([page.extract_text() for page in reader.pages])
    else:
        return uploaded_file.read().decode("utf-8")

def generate_response(messages, context=""):
    system_msg = "Ты — Akylman AI, мудрый наставник. Ты человечный и умный."
    if context:
        system_msg += f"\nКонтекст из файла: {context}"
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}] + 
                     [{"role": m["role"], "content": m["content"]} for m in messages],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {str(e)}"

with st.sidebar:
    st.title("🧠 Akylman AI")
    
    if st.button("➕ Новый чат", use_container_width=True):
        new_id = f"Чат {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[new_id] = []
        st.session_state.current_session = new_id
        st.rerun()

    st.subheader("Ваши чаты")
    for session_id in list(st.session_state.sessions.keys()):
        if st.button(session_id, use_container_width=True):
            st.session_state.current_session = session_id
            st.rerun()

    st.markdown("---")
    uploaded_file = st.file_uploader("📂 Загрузить файл (PDF/TXT)", type=["pdf", "txt"])
    
    if st.button("🗑️ Удалить текущий чат", use_container_width=True):
        if len(st.session_state.sessions) > 1:
            del st.session_state.sessions[st.session_state.current_session]
            st.session_state.current_session = list(st.session_state.sessions.keys())[0]
            st.rerun()

st.title(st.session_state.current_session)

current_messages = st.session_state.sessions[st.session_state.current_session]

if not current_messages:
    opener = get_opener()
    current_messages.append({"role": "assistant", "content": opener})

for msg in current_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Спроси Акылмана..."):
    file_context = ""
    if uploaded_file:
        with st.spinner("Читаю файл..."):
            file_context = extract_text(uploaded_file)
    
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = generate_response(current_messages, file_context)
        st.markdown(response)
    current_messages.append({"role": "assistant", "content": response})
