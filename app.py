import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from pypdf import PdfReader
from datetime import datetime
from streamlit_google_auth import Authenticate

st.set_page_config(page_title="Akylman AI", page_icon="🧠", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name='akylman_auth',
    cookie_key='akylman_secret_key',
    cookie_expiry_days=30,
)

authenticator.check_authenticity()

if not st.session_state.get('connected'):
    st.markdown("<h1 style='text-align: center;'>Akylman AI</h1>", unsafe_allow_html=True)
    st.info("Пожалуйста, войдите, чтобы начать обучение.")
    authenticator.login()
    st.stop()

user_info = st.session_state.get('user_info')
user_name = user_info.get('name')

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def search_web(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            if results:
                return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except:
        pass
    return ""

def generate_response(messages, model, context_file):
    last_query = messages[-1]["content"]
    web_data = search_web(last_query)
    
    system_prompt = (
        f"Ты — Akylman. Твой собеседник: {user_name}. "
        "Ты самообучаешься на основе этого диалога. "
        "Всегда используй актуальные данные из интернета, если они предоставлены."
    )
    
    if context_file: system_prompt += f"\n\n[FILE]: {context_file}"
    if web_data: system_prompt += f"\n\n[WEB]: {web_data}"

    all_msgs = [{"role": "system", "content": system_prompt}]
    all_msgs.extend([{"role": m["role"], "content": m["content"]} for m in messages])

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=all_msgs,
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {e}"

with st.sidebar:
    st.title(f"🧠 Akylman")
    st.write(f"Пользователь: **{user_name}**")
    
    if st.button("➕ Новый чат", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    pwd = st.text_input("Доступ", type="password", placeholder="Код...")
    
    models = {
        "Быстрая ⚡": "llama-3.1-8b-instant",
        "Думающая 🤔": "llama-3.3-70b-versatile"
    }
    
    if pwd == "1234":
        if not st.session_state.access_granted:
            st.session_state.access_granted = True
            st.balloons()
        models["Pro 🔥"] = "llama-3.3-70b-versatile"
        st.success("Pro-режим активен")
    
    sel_model = st.selectbox("Модель:", list(models.keys()))
    active_model = models[sel_model]

    st.markdown("---")
    up_file = st.file_uploader("Документ (PDF/TXT)", type=["pdf", "txt"])
    
    if st.button("Выйти из системы"):
        authenticator.logout()

st.markdown("<h1 style='text-align: center;'>Akylman</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Спроси что-нибудь..."):
    f_text = ""
    if up_file:
        try:
            if up_file.type == "application/pdf":
                reader = PdfReader(up_file)
                f_text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
            else:
                f_text = up_file.read().decode("utf-8")
        except: pass

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Акылман думает..."):
            ans = generate_response(st.session_state.messages, active_model, f_text)
            st.markdown(ans)
    st.session_state.messages.append({"role": "assistant", "content": ans})
