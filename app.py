import streamlit as st
from groq import Groq
from streamlit_gsheets import GSheetsConnection
from duckduckgo_search import DDGS
import pandas as pd

st.set_page_config(page_title="Akylman AI", page_icon="🧠", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Ошибка настройки Secrets: {e}")
    st.stop()

if "user" not in st.session_state: st.session_state.user = None
if "messages" not in st.session_state: st.session_state.messages = []
if "access_granted" not in st.session_state: st.session_state.access_granted = False

def search_web(query):
    try:
        with DDGS() as ddgs:
            res = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([f"- {r['title']}: {r['body']}" for r in res])
    except: return "Нет доступа к интернету."

with st.sidebar:
    st.title("⚙️ Меню")
    
    if st.button("➕ Новый чат", use_container_width=True):
        st.session_state.messages = []
        if st.session_state.user:
            try:
                df = conn.read()
                df.loc[df['login'].astype(str) == str(st.session_state.user), 'history'] = "[]"
                conn.update(data=df)
            except: pass
        st.rerun()
        
    st.divider()

    pass_input = st.text_input("Код доступа (Pro)", type="password")
    
    models = {
        "Быстрая ⚡": "llama-3.1-8b-instant",
        "Думающая 🤔": "llama-3.3-70b-versatile"
    }

    if pass_input == "1234":
        if not st.session_state.access_granted:
            st.balloons()
            st.session_state.access_granted = True
        
        models.update({
            "Pro 🔥": "llama-3.3-70b-versatile",
        })
        st.success("Pro режим активирован!")
    
    selected_model = models[st.selectbox("Модель:", list(models.keys()))]
    st.caption("✅ Интернет поиск активен")
    st.file_uploader("Файл (PDF/TXT)", type=["pdf", "txt"])

col_logo, col_auth = st.columns([7, 3])
with col_logo:
    st.markdown("# Akylman AI")

with col_auth:
    if st.session_state.user:
        st.success(f"👤 **{st.session_state.user}**")
        if st.button("Выйти", key="logout_btn", use_container_width=True):
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
        b1, b2 = st.columns(2)

        try:
            df = conn.read()
            if df.empty or 'login' not in df.columns:
                df = pd.DataFrame(columns=['login', 'password', 'history'])
        except:
            df = pd.DataFrame(columns=['login', 'password', 'history'])

        if b1.button("Войти", use_container_width=True):
            mask = (df['login'].astype(str) == str(login)) & (df['password'].astype(str) == str(pwd))
            if not df[mask].empty:
                st.session_state.user = login
                hist_raw = df[mask].iloc[0]['history']
                try: st.session_state.messages = eval(hist_raw) if hist_raw else []
                except: st.session_state.messages = []
                st.session_state.show_auth = False
                st.rerun()
            else:
                st.error("Неверные данные")

        if b2.button("Регистрация", use_container_width=True):
            if login and pwd:
                if str(login) not in df['login'].astype(str).values:
                    new_user = pd.DataFrame([{"login": str(login), "password": str(pwd), "history": "[]"}])
                    try:
                        updated_df = pd.concat([df, new_user], ignore_index=True)
                        conn.update(data=updated_df)
                        st.success("Создано! Теперь войдите.")
                    except Exception as e:
                        st.error("Ошибка записи. Проверьте права 'Редактор' в таблице.")
                else:
                    st.warning("Логин занят")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        web_data = search_web(prompt)
        
        system_prompt = f"Ты Akylman. Пользователь: {st.session_state.user or 'Гость'}. Актуальная информация из интернета: {web_data}"
        
        full_history = [{"role": "system", "content": system_prompt}] + st.session_state.messages
        
        try:
            stream = client.chat.completions.create(
                model=selected_model,
                messages=full_history,
                stream=True
            )
            response_text = st.write_stream(stream)

            st.session_state.messages.append({"role": "assistant", "content": response_text})

            if st.session_state.user:
                try:
                    df = conn.read()
                    df.loc[df['login'].astype(str) == str(st.session_state.user), 'history'] = str(st.session_state.messages)
                    conn.update(data=df)
                except: pass 
                
        except Exception as e:
            st.error(f"Ошибка Groq API: {e}")
