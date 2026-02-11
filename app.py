import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import pandas as pd

st.set_page_config(page_title="Akylman AI", page_icon="🧠", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def load_data():
    try:
        sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
        if "/edit" in csv_url and "gid=" not in csv_url:
            csv_url = sheet_url.replace("/edit", "/export?format=csv")
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame(columns=['login', 'password', 'history'])

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
        st.rerun()
    
    st.divider()
    access_code = st.text_input("Код доступа", type="password")
    
    models = {
        "Быстрая ⚡": "llama-3.1-8b-instant",
        "Думающая 🤔": "llama-3.3-70b-versatile"
    }
    
    if access_code == "1234":
        if not st.session_state.access_granted:
            st.balloons()
            st.session_state.access_granted = True
        models.update({"Pro 🔥": "llama-3.3-70b-versatile"})
        st.success("Pro режим!")

    sel_model = models[st.selectbox("Модель:", list(models.keys()))]
    st.info("🌐 Интернет поиск: ВКЛ")

h_col, a_col = st.columns([7, 3])
with h_col: st.markdown("# Akylman AI")

with a_col:
    if st.session_state.user:
        st.write(f"✅ **{st.session_state.user}**")
        if st.button("Выйти"):
            st.session_state.user = None
            st.session_state.messages = []
            st.rerun()
    else:
        if st.button("Вход / Регистрация"):
            st.session_state.show_auth = not st.session_state.get("show_auth", False)

if not st.session_state.user and st.session_state.get("show_auth"):
    with st.form("auth_form"):
        u_login = st.text_input("Логин")
        u_pwd = st.text_input("Пароль", type="password")
        col1, col2 = st.columns(2)
        
        df = load_data()
        
        if col1.form_submit_button("Войти"):
            user_check = df[(df['login'].astype(str) == str(u_login)) & (df['password'].astype(str) == str(u_pwd))]
            if not user_check.empty:
                st.session_state.user = u_login
                try: 
                    h = user_check.iloc[0]['history']
                    st.session_state.messages = eval(h) if isinstance(h, str) else []
                except: st.session_state.messages = []
                st.rerun()
            else: st.error("Неверный логин/пароль")
        
        if col2.form_submit_button("Регистрация"):
            st.info("Для регистрации временно напишите админу или используйте тестовый вход.")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Напиши мне..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        web_info = search_web(prompt)
        sys_msg = f"Ты Akylman. Юзер: {st.session_state.user or 'Гость'}. Инфо из сети: {web_info}"

        full_response = ""
        placeholder = st.empty()
        
        try:
            stream = client.chat.completions.create(
                model=sel_model,
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
