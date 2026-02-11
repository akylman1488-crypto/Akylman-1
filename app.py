import streamlit as st
from groq import Groq
from supabase import create_client
from duckduckgo_search import DDGS

st.set_page_config(page_title="Akylman AI", page_icon="🧠", layout="wide")

if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
    st.error("Настрой Secrets в Streamlit: добавь SUPABASE_URL и SUPABASE_KEY")
    st.stop()

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user" not in st.session_state: st.session_state.user = None
if "messages" not in st.session_state: st.session_state.messages = []

def search_web(query):
    try:
        with DDGS() as ddgs:
            return "\n".join([r['body'] for r in ddgs.text(query, max_results=3)])
    except: return ""

with st.sidebar:
    st.title("⚙️ Меню")
    if st.button("🗑 Очистить чат", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    models = {"Быстрая ⚡": "llama-3.1-8b-instant", "Мощная 💎": "llama-3.3-70b-versatile"}
    sel_model = models[st.selectbox("Модель:", list(models.keys()))]

col1, col2 = st.columns([7, 3])
with col1: st.title("Akylman AI")
with col2:
    if st.session_state.user:
        st.write(f"✅ {st.session_state.user}")
        if st.button("Выйти"):
            st.session_state.user = None
            st.rerun()
    else:
        if st.button("Вход / Регистрация"):
            st.session_state.show_auth = not st.session_state.get("show_auth", False)

if not st.session_state.user and st.session_state.get("show_auth"):
    with st.container(border=True):
        u_email = st.text_input("Email (asko@ai.com)")
        u_pass = st.text_input("Пароль", type="password")
        c1, c2 = st.columns(2)
        
        if c1.button("Войти", use_container_width=True):
            try:
                supabase.auth.sign_in_with_password({"email": u_email, "password": u_pass})
                st.session_state.user = u_email
                st.rerun()
            except Exception as e: st.error(f"Ошибка: {e}")

        if c2.button("Регистрация", use_container_width=True):
            try:
                supabase.auth.sign_up({"email": u_email, "password": u_pass})
                st.success("Аккаунт создан! Нажми 'Войти'")
            except Exception as e: st.error(f"Ошибка: {e}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Напиши мне..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        stream = client.chat.completions.create(
            model=sel_model,
            messages=[{"role": "system", "content": f"Ты Akylman. Контекст: {search_web(prompt)}"}] + st.session_state.messages,
            stream=True
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                full_res += content
                placeholder.markdown(full_res + "▌")
        placeholder.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
