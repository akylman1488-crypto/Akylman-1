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

h_col, a_col = st.columns([8, 2])
with h_col: st.markdown("# Akylman AI")
with a_col:
    if st.session_state.user:
        st.success(f"👤 {st.session_state.user}")
        if st.button("Выйти"):
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
        except:
            st.error("Ошибка таблицы! Проверьте Secrets.")
            st.stop()
            
        if c1.button("Войти", use_container_width=True):
            user_row = df[(df['login'].astype(str) == str(login)) & (df['password'].astype(str) == str(pwd))]
            if not user_row.empty:
                st.session_state.user = login
                hist_raw = user_row.iloc[0]['history']
                try: st.session_state.messages = eval(hist_raw) if hist_raw else []
                except: st.session_state.messages = []
                st.session_state.show_auth = False
                st.rerun()
            else: st.error("Неверный логин или пароль")

        if c2.button("Регистрация", use_container_width=True):
            if login and pwd and str(login) not in df['login'].astype(str).values:
                new_u = pd.DataFrame([{"login": str(login), "password": str(pwd), "history": "[]"}])
                conn.update(data=pd.concat([df, new_u], ignore_index=True))
                st.success(f"Аккаунт {login} создан! Теперь войдите.")

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
    # Поле пароля доступа с салютами
    access_code = st.text_input("Код доступа (Pro/Plus)", type="password")
    models = {"Быстрая ⚡": "llama-3.1-8b-instant", "Думающая 🤔": "llama-3.3-70b-versatile"}
    
    if access_code == "1234": # Твой код
        if not st.session_state.access_granted:
            st.balloons()
            st.session_state.access_granted = True
        st.success("Доступ открыт!")
        models.update({"Pro 🔥": "llama-3.3-70b-versatile", "Plus 💎": "mixtral-8x7b-32768"})
    
    sel_model = models[st.selectbox("Модель:", list(models.keys()))]
    st.info("🌐 Поиск в интернете всегда включен")
    up_file = st.file_uploader("Документ (PDF/TXT)", type=["pdf", "txt"])

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Напиши Акылману..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Акылман ищет в актуальном времени..."):
            web_info = search_web(prompt)
            sys_prompt = f"Ты Akylman. Юзер: {st.session_state.user or 'Гость'}. Актуальные данные: {web_info}"
            
            response = client.chat.completions.create(
                model=sel_model,
                messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages
            )
            ans = response.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
            
            if st.session_state.user:
                df = conn.read()
                df.loc[df['login'].astype(str) == str(st.session_state.user), 'history'] = str(st.session_state.messages)
                conn.update(data=df)
