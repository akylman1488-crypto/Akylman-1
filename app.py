import streamlit as st
from groq import Groq
from streamlit_gsheets import GSheetsConnection
from duckduckgo_search import DDGS
import pandas as pd

st.set_page_config(page_title="Akylman AI", page_icon="🧠", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
conn = st.connection("gsheets", type=GSheetsConnection)

if "user" not in st.session_state: st.session_state.user = None
if "messages" not in st.session_state: st.session_state.messages = []

def search_web(query):
    try:
        with DDGS() as ddgs:
            res = [r for r in ddgs.text(query, max_results=2)]
            return "\n".join([f"{r['title']}: {r['body']}" for r in res])
    except: return ""

header_col, auth_col = st.columns([8, 2])
with header_col:
    st.markdown("# Akylman AI")

with auth_col:
    if st.session_state.user:
        st.write(f"👤 **{st.session_state.user}**")
        if st.button("Выйти", use_container_width=True):
            st.session_state.user = None
            st.session_state.messages = []
            st.rerun()
    else:
        if st.button("Вход / Регистрация", use_container_width=True):
            st.session_state.show_auth = not st.session_state.get("show_auth", False)

if not st.session_state.user and st.session_state.get("show_auth"):
    with st.container(border=True):
        login = st.text_input("Логин (любое слово)")
        pwd = st.text_input("Пароль", type="password")
        c1, c2 = st.columns(2)

        try:
            df = conn.read()
        except Exception as e:
            st.error("Ошибка подключения к таблице. Проверьте Secrets!")
            st.stop()
            
        if c1.button("Войти", use_container_width=True):
            user_row = df[(df['login'].astype(str) == str(login)) & (df['password'].astype(str) == str(pwd))]
            if not user_row.empty:
                st.session_state.user = login
                hist_raw = user_row.iloc[0]['history']
                try:
                    st.session_state.messages = eval(hist_raw) if (isinstance(hist_raw, str) and hist_raw != "") else []
                except:
                    st.session_state.messages = []
                st.session_state.show_auth = False
                st.rerun()
            else:
                st.error("Неверный логин или пароль")

        if c2.button("Регистрация", use_container_width=True):
            if login and pwd:
                if str(login) not in df['login'].astype(str).values:
                    new_user = pd.DataFrame([{"login": str(login), "password": str(pwd), "history": "[]"}])
                    updated_df = pd.concat([df, new_user], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("Аккаунт создан! Нажмите 'Войти'")
                else:
                    st.warning("Этот логин уже занят")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Напиши Акылману..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Акылман думает..."):
            web_info = search_web(prompt)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": f"Ты Akylman. Юзер: {st.session_state.user or 'Гость'}. Интернет: {web_info}"}] + st.session_state.messages
            )
            ans = response.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
            
            if st.session_state.user:
                df = conn.read()
                df.loc[df['login'].astype(str) == str(st.session_state.user), 'history'] = str(st.session_state.messages)
                conn.update(data=df)
