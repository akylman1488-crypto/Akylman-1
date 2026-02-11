import streamlit as st
from groq import Groq
from supabase import create_client
from duckduckgo_search import DDGS

st.set_page_config(page_title="Akylman AI", page_icon="🧠", layout="wide")

try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Ошибка секретов!")
    st.stop()

if "user" not in st.session_state: st.session_state.user = None
if "messages" not in st.session_state: st.session_state.messages = []

def search_web(query):
    try:
        with DDGS() as ddgs:
            res = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([r['body'] for r in res])
    except: return ""

with st.sidebar:
    st.title("⚙️ Меню")
    if st.button("🗑 Новый чат", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    code = st.text_input("Код доступа (1234)", type="password")
    models = {"Быстрая ⚡": "llama-3.1-8b-instant", "Мощная 💎": "llama-3.3-70b-versatile"}
    if code == "1234":
        st.success("Pro режим!")
    sel_model = models[st.selectbox("Модель:", list(models.keys()))]

col_h, col_a = st.columns([7, 3])
with col_h: st.title("Akylman AI")

with col_a:
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
    with st.container(border=True):
        u_email = st.text_input("Email")
        u_pass = st.text_input("Пароль", type="password")
        c1, c2 = st.columns(2)
        
        if c1.button("Войти", use_container_width=True):
            try:
                res = supabase.auth.sign_in_with_password({"email": u_email, "password": u_pass})
                st.session_state.user = u_email
                st.rerun()
            except: st.error("Неверный логин/пароль")

        if c2.button("Регистрация", use_container_width=True):
            try:
                supabase.auth.sign_up({"email": u_email, "password": u_pass})
                st.info("Аккаунт создан! Теперь нажмите Войти.")
            except: st.error("Ошибка регистрации")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Напиши мне..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        web_info = search_web(prompt)
        sys_msg = f"Ты Akylman. Инфо из сети: {web_info}"
        full_res = ""
        placeholder = st.empty()
        
        try:
            stream = client.chat.completions.create(
                model=sel_model,
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                stream=True
            )
            
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_res += content
                    placeholder.markdown(full_res + "▌")
            
            placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"Ошибка: {e}")
