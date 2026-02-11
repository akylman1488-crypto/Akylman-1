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
if "access_granted" not in st.session_state: st.session_state.access_granted = False

def search_web(query):
    try:
        with DDGS() as ddgs:
            res = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([f"- {r['title']}: {r['body']}" for r in res])
    except: return ""

header_col, user_col = st.columns([7, 3])
with header_col:
    st.markdown("# Akylman AI")

with user_col:
    if st.session_state.user:
        # Если залогинен, показываем ник и кнопку выхода
        st.success(f"👤 Аккаунт: **{st.session_state.user}**")
        if st.button("Выйти", use_container_width=True):
            st.session_state.user = None
            st.session_state.messages = []
            st.rerun()
    else:
        # Если не залогинен, показываем кнопку открытия входа
        if st.button("Вход / Регистрация", use_container_width=True):
            st.session_state.show_auth = not st.session_state.get("show_auth", False)

if not st.session_state.user and st.session_state.get("show_auth"):
    with st.container(border=True):
        login_input = st.text_input("Логин")
        pwd_input = st.text_input("Пароль", type="password")
        c1, c2 = st.columns(2)
        
        try:
            df = conn.read()
        except:
            st.error("Ошибка подключения к таблице!")
            st.stop()
            
        if c1.button("Войти", use_container_width=True):
            user_row = df[(df['login'].astype(str) == str(login_input)) & (df['password'].astype(str) == str(pwd_input))]
            if not user_row.empty:
                st.session_state.user = login_input
                hist = user_row.iloc[0]['history']
                try: st.session_state.messages = eval(hist) if hist else []
                except: st.session_state.messages = []
                st.session_state.show_auth = False
                st.rerun()
            else: st.error("Неверный логин или пароль")

        if c2.button("Регистрация", use_container_width=True):
            if login_input and pwd_input:
                if str(login_input) not in df['login'].astype(str).values:
                    new_u = pd.DataFrame([{"login": str(login_input), "password": str(pwd_input), "history": "[]"}])
                    conn.update(data=pd.concat([df, new_u], ignore_index=True))
                    st.success(f"Аккаунт {login_input} создан! Теперь нажмите 'Войти'.")
                else: st.warning("Логин уже занят")

with st.sidebar:
    st.title("⚙️ Настройки")
    
    if st.button("➕ Новый чат", use_container_width=True):
        st.session_state.messages = []
        if st.session_state.user:
            df = conn.read()
            df.loc[df['login'].astype(str) == str(st.session_state.user), 'history'] = "[]"
            conn.update(data=df)
        st.rerun()
    
    st.markdown("---")

    code = st.text_input("Код доступа к Pro", type="password")

    avail_models = {
        "Быстрая ⚡": "llama-3.1-8b-instant", 
        "Думающая 🤔": "llama-3.3-70b-versatile"
    }
    
    if code == "1234": # Твой секретный код
        if not st.session_state.access_granted:
            st.balloons()
            st.session_state.access_granted = True
        avail_models.update({
            "Pro 🔥": "llama-3.3-70b-versatile", 
        })
        st.success("Доступ к Pro открыт!")
    
    sel_model = avail_models[st.selectbox("Выберите мозг:", list(avail_models.keys()))]
    st.caption("🌐 Поиск в интернете активен всегда")
    
    up_file = st.file_uploader("Добавить файл в контекст", type=["pdf", "txt"])

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Напиши Акылману..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Акылман ищет актуальную информацию..."):
            web_context = search_web(prompt)
            sys_msg = f"Ты Akylman. Юзер: {st.session_state.user or 'Гость'}. Актуальные данные из сети: {web_context}"
            
            response = client.chat.completions.create(
                model=sel_model,
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages
            )
            ans = response.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})

            if st.session_state.user:
                df = conn.read()
                df.loc[df['login'].astype(str) == str(st.session_state.user), 'history'] = str(st.session_state.messages)
                conn.update(data=df)
