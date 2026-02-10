import streamlit as st
from groq import Groq
from supabase import create_client
from duckduckgo_search import DDGS
from pypdf import PdfReader
from datetime import datetime

st.set_page_config(page_title="Akylman AI", page_icon="🧠")

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user" not in st.session_state:
    st.session_state.user = None
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

def load_history(user_id):
    res = supabase.table("chat_history").select("*").eq("user_id", user_id).order("created_at").execute()
    return [{"role": r["role"], "content": r["content"]} for r in res.data]

def save_message(user_id, role, content):
    supabase.table("chat_history").insert({"user_id": user_id, "role": role, "content": content}).execute()

def search_web(query):
    try:
        with DDGS() as ddgs:
            res = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([f"- {r['title']}: {r['body']}" for r in res]) if res else ""
    except: return ""

def generate_response(messages, model, context_file, user_name):
    web_data = search_web(messages[-1]["content"])
    system_prompt = f"Ты — Akylman. Твой собеседник: {user_name}. Ты самообучаешься и используешь интернет."
    if context_file: system_prompt += f"\n\n[FILE]: {context_file}"
    if web_data: system_prompt += f"\n\n[WEB]: {web_data}"
    
    all_msgs = [{"role": "system", "content": system_prompt}] + messages
    try:
        comp = client.chat.completions.create(model=model, messages=all_msgs, temperature=0.7)
        return comp.choices[0].message.content
    except Exception as e: return f"Ошибка: {e}"

if not st.session_state.user:
    st.title("Вход в Akylman AI")
    email = st.text_input("Email")
    pwd = st.text_input("Пароль", type="password")
    col1, col2 = st.columns(2)
    
    if col1.button("Войти"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
            st.session_state.user = res.user
            st.rerun()
        except: st.error("Неверный логин или пароль")
        
    if col2.button("Регистрация"):
        try:
            res = supabase.auth.sign_up({"email": email, "password": pwd})
            st.success("Проверьте почту для подтверждения!")
        except: st.error("Ошибка регистрации")
    st.stop()

user = st.session_state.user
if "messages" not in st.session_state:
    st.session_state.messages = load_history(user.id)

with st.sidebar:
    st.title("🧠 Akylman")
    st.write(f"Юзер: {user.email}")
    if st.button("➕ Новый чат", use_container_width=True):
        supabase.table("chat_history").delete().eq("user_id", user.id).execute()
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    unlock = st.text_input("Доступ", type="password")
    models = {"Быстрая ⚡": "llama-3.1-8b-instant", "Думающая 🤔": "llama-3.3-70b-versatile"}
    if unlock == "1234":
        if not st.session_state.access_granted:
            st.session_state.access_granted = True
            st.balloons()
        models.update({"Pro 🔥": "llama-3.3-70b-versatile", "Plus 💎": "mixtral-8x7b-32768"})
    
    sel_model = models[st.selectbox("Модель:", list(models.keys()))]
    up_file = st.file_uploader("Файл (PDF/TXT)", type=["pdf", "txt"])
    if st.button("Выход"):
        st.session_state.user = None
        st.rerun()

st.markdown("<h1 style='text-align: center;'>Akylman</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Напиши Акылману..."):
    f_text = ""
    if up_file:
        try:
            reader = PdfReader(up_file)
            f_text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
        except: pass

    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(user.id, "user", prompt)
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("..."):
            ans = generate_response(st.session_state.messages, sel_model, f_text, user.email)
            st.markdown(ans)
            save_message(user.id, "assistant", ans)
    st.session_state.messages.append({"role": "assistant", "content": ans})
