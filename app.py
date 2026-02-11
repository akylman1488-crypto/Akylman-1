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
            return "\n".join([f"{r['title']}: {r['body']}" for r in res])
    except: return ""

with st.sidebar:
    st.title("⚙️ Меню")
    
    if st.button("🗑 Новый чат", use_container_width=True):
        st.session_state.messages = []
        if st.session_state.user:
            try:
                df = conn.read()
                df.loc[df['login'].astype(str) == str(st.session_state.user), 'history'] = "[]"
                conn.update(data=df)
            except: pass
        st.rerun()
        
    st.divider()
    
    access_code = st.text_input("Код доступа (Pro)", type="password")
    
    models = {
        "Быстрая ⚡": "llama-3.1-8b-instant",
        "Думающая 🤔": "llama-3.3-70b-versatile"
    }
    
    if access_code == "1234":
        if not st.session_state.access_granted:
            st.balloons()
            st.session_state.access_granted = True
        
        models.update({
            "Pro 🔥": "llama-3.3-70b-versatile",
            "Plus 💎": "mixtral-8x7b-32768"
        })
        st.success("Pro режим активирован!")
    
    sel_model = models[st.selectbox("Модель:", list(models.keys()))]
    st.info("🌐 Интернет: Всегда включен")
    st.file_uploader("Загрузить файл", type=["pdf", "txt"])

h_col, a_col = st.columns([7, 3])
with h_col:
    st.markdown("# Akylman AI")

with a_col:
    if st.session_state.user:
        st.success(f"👤 Вы вошли как: **{st.session_state.user}**")
        if st.button("Выйти", use_container_width=True):
            st.session_state.user = None
            st.session_state.messages = []
            st.rerun()
    else:
        if st.button("Вход / Регистрация", use_container_width=True):
            st.session_state.show_auth = not st.session_state.get("show_auth", False)

if not st.session_state.user and st.session_state.get("show_auth"):
    with st.container(border=True):
        login = st.text_input("Логин")
        pwd = st.text_input("Пароль", type="password")
        c1, c2 = st.columns(2)
        
        try:
            df = conn.read()
            if df.empty or 'login' not in df.columns:
                df = pd.DataFrame(columns=['login', 'password', 'history'])
        except:
            df = pd.DataFrame(columns=['login', 'password', 'history'])
            
        if c1.button("Войти", use_container_width=True):
            user_row = df[(df['login'].astype(str) == str(login)) & (df['password'].astype(str) == str(pwd))]
            if not user_row.empty:
                st.session_state.user = login
                hist = user_row.iloc[0]['history']
                try: st.session_state.messages = eval(hist) if hist else []
                except: st.session_state.messages = []
                st.session_state.show_auth = False
                st.rerun()
            else: st.error("Ошибка входа")

        if c2.button("Регистрация", use_container_width=True):
            if login and pwd:
                if str(login) not in df['login'].astype(str).values:
                    new_user = pd.DataFrame([{"login": str(login), "password": str(pwd), "history": "[]"}])
                    df = pd.concat([df, new_user], ignore_index=True)
                    conn.update(data=df)
                    st.success("Готово! Нажмите Войти.")
                else: st.warning("Логин занят")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        web_res = search_web(prompt)
        sys = f"Ты Akylman. Юзер: {st.session_state.user or 'Гость'}. Интернет: {web_res}"
        
        try:
            stream = client.chat.completions.create(
                model=sel_model,
                messages=[{"role": "system", "content": sys}] + st.session_state.messages,
                stream=True
            )
            resp = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": resp})
            
            if st.session_state.user:
                df = conn.read()
                df.loc[df['login'].astype(str) == str(st.session_state.user), 'history'] = str(st.session_state.messages)
                conn.update(data=df)
        except Exception as e:
            st.error(f"Ошибка модели: {e}")
