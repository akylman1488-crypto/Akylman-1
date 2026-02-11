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
with h_col:
    st.markdown("# Akylman AI")

with a_col:
    if st.session_state.user:
        st.success(f"👤 {st.session_state.user}")
        if st.button("Выйти", use_container_width=True):
            st.session_state.user = None
            st.session_state.messages = []
            st.rerun()
    else:
        if st.button("Вход / Регистрация", use_container_width=True):
            st.session_state.show_auth = not st.session_state.get("show_auth", False)

if not st.session_state.user and st.session_state.get("show_auth"):
    with st.container(border=True):
        login_in = st.text_input("Логин")
        pwd_in = st.text_input("Пароль", type="password")
        c1, c2 = st.columns(2)
        
        try:
            df = conn.read()
            for col in ['login', 'password', 'history']:
                if col not in df.columns:
                    df[col] = ""
        except:
            st.error("Ошибка подключения к таблице!")
            st.stop()

        if c1.button("Войти", use_container_width=True):
            user_row = df[(df['login'].astype(str) == str(login_in)) & (df['password'].astype(str) == str(pwd_in))]
            if not user_row.empty:
                st.session_state.user = login_in
                hist = user_row.iloc[0]['history']
                try: st.session_state.messages = eval(hist) if hist else []
                except: st.session_state.messages = []
                st.session_state.show_auth = False
                st.rerun()
            else: st.error("Неверные данные")

        if c2.button("Регистрация", use_container_width=True):
            if login_in and pwd_in:
                if str(login_in) not in df['login'].astype(str).values:
                    new_u = pd.DataFrame([{"login": str(login_in), "password": str(pwd_in), "history": "[]"}])
                    conn.update(data=pd.concat([df, new_u], ignore_index=True))
                    st.success(f"Юзер {login_in} создан! Теперь войдите.")
                else: st.warning("Логин занят")

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

    access_pwd = st.text_input("Код доступа (Pro/Plus)", type="password")
    
    models = {
        "Быстрая ⚡": "llama-3.1-8b-instant",
        "Думающая 🤔": "llama-3.3-70b-versatile"
    }
    
    if access_pwd == "1234":
        if not st.session_state.access_granted:
            st.balloons() # САЛЮТЫ!
            st.session_state.access_granted = True
        st.success("Доступ открыт!")
        models.update({
            "Pro 🔥": "llama-3.3-70b-versatile",
            "Plus 💎": "mixtral-8x7b-32768"
        })
    
    sel_model = models[st.selectbox("Модель:", list(models.keys()))]
    st.info("🌐 Поиск в интернете: ВСЕГДА")
    up_file = st.file_uploader("Добавить контекст (PDF/TXT)", type=["pdf", "txt"])

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Напиши Акылману..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Акылман ищет в сети..."):
            web_data = search_web(prompt)
            sys_prompt = f"Ты Akylman. Юзер: {st.session_state.user or 'Гость'}. Информация из сети: {web_data}"
            
            resp = client.chat.completions.create(
                model=sel_model,
                messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages
            )
            ans = resp.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
            
            if st.session_state.user:
                df = conn.read()
                df.loc[df['login'].astype(str) == str(st.session_state.user), 'history'] = str(st.session_state.messages)
                conn.update(data=df)
