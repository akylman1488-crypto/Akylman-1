import streamlit as st
from groq import Groq
from streamlit_gsheets import GSheetsConnection
from duckduckgo_search import DDGS

st.set_page_config(page_title="Akylman AI", page_icon="🧠", layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages = []
if "user" not in st.session_state: st.session_state.user = None

def search_web(query):
    try:
        with DDGS() as ddgs:
            res = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([f"- {r['title']}: {r['body']}" for r in res]) if res else ""
    except: return ""

h_col, a_col = st.columns([8, 2])
with h_col: st.title("Akylman AI")
with a_col:
    if st.session_state.user:
        st.write(f"👤 {st.session_state.user}")
        if st.button("Выйти"):
            st.session_state.user = None
            st.session_state.messages = []
            st.rerun()
    else:
        if st.button("Вход / Регистрация", use_container_width=True):
            st.session_state.show_auth = True

if not st.session_state.user and st.session_state.get("show_auth"):
    with st.expander("Авторизация", expanded=True):
        login = st.text_input("Логин")
        pwd = st.text_input("Пароль", type="password")
        c1, c2 = st.columns(2)

        df = conn.read()
        
        if c1.button("Войти"):
            user_data = df[(df['login'] == login) & (df['password'] == pwd)]
            if not user_data.empty:
                st.session_state.user = login
                history_raw = user_data.iloc[0]['history']
                st.session_state.messages = eval(history_raw) if history_raw else []
                st.session_state.show_auth = False
                st.rerun()
            else: st.error("Ошибка")
            
        if c2.button("Создать"):
            if login not in df['login'].values:
                new_row = {"login": login, "password": pwd, "history": "[]"}
                st.success("Создано! Войдите.")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Напиши Акылману..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        web = search_web(prompt)
        sys = f"Ты — Akylman. Юзер: {st.session_state.user or 'Гость'}. Интернет: {web}"
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"system","content":sys}] + st.session_state.messages
        ).choices[0].message.content
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

        if st.session_state.user:
            pass
