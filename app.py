import streamlit as st
from groq import Groq
from streamlit_gsheets import GSheetsConnection
from duckduckgo_search import DDGS
import pandas as pd

st.set_page_config(page_title="Akylman AI", page_icon="🧠", layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user" not in st.session_state: st.session_state.user = None
if "messages" not in st.session_state: st.session_state.messages = []

def search_web(query):
    try:
        with DDGS() as ddgs:
            res = [r for r in ddgs.text(query, max_results=2)]
            return "\n".join([f"- {r['body']}" for r in res])
    except: return ""

header_col, auth_col = st.columns([8, 2])
with header_col:
    st.title("Akylman AI")

with auth_col:
    if st.session_state.user:
        st.write(f"👤 {st.session_state.user}")
        if st.button("Выйти"):
            st.session_state.user = None
            st.session_state.messages = []
            st.rerun()
    else:
        if st.button("Вход / Регистрация", use_container_width=True):
            st.session_state.show_auth = not st.session_state.get("show_auth", False)

if not st.session_state.user and st.session_state.get("show_auth"):
    with st.container(border=True):
        login = st.text_input("Придумайте логин")
        pwd = st.text_input("Пароль", type="password")
        c1, c2 = st.columns(2)

        df = conn.read()
        
        if c1.button("Войти"):
            found = df[(df['login'] == login) & (df['password'] == str(pwd))]
            if not found.empty:
                st.session_state.user = login
                try: st.session_state.messages = eval(found.iloc[0]['history'])
                except: st.session_state.messages = []
                st.session_state.show_auth = False
                st.rerun()
            else: st.error("Неверный логин или пароль")

        if c2.button("Регистрация"):
            if login and pwd:
                if login not in df['login'].values:
                    st.info("Добавьте пользователя в таблицу вручную или используйте API")
                else: st.error("Логин занят")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Спроси Акылмана..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Акылман ищет в сети..."):
            web = search_web(prompt)
            sys_msg = f"Ты — Akylman. Юзер: {st.session_state.user or 'Гость'}. Актуальное из сети: {web}"
            
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages
            ).choices[0].message.content
            
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
