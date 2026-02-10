import streamlit as st
from groq import Groq
from supabase import create_client
from duckduckgo_search import DDGS
from pypdf import PdfReader

st.set_page_config(page_title="Akylman AI", page_icon="🧠", layout="wide")

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user" not in st.session_state:
    session = supabase.auth.get_session()
    st.session_state.user = session.user if session else None

if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

def load_history(user_id):
    try:
        res = supabase.table("chat_history").select("*").eq("user_id", user_id).order("created_at").execute()
        return [{"role": r["role"], "content": r["content"]} for r in res.data]
    except: return []

def save_msg(user_id, role, content):
    supabase.table("chat_history").insert({"user_id": user_id, "role": role, "content": content}).execute()

def search_web(query):
    try:
        with DDGS() as ddgs:
            res = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([f"- {r['title']}: {r['body']}" for r in res]) if res else ""
    except: return ""

def generate_response(messages, model, context_file, user_email):
    web_data = search_web(messages[-1]["content"])
    system_prompt = f"Ты — Akylman. Юзер: {user_email}. Ты самообучаешься на истории и всегда используешь интернет."
    if context_file: system_prompt += f"\n\n[FILE]: {context_file}"
    if web_data: system_prompt += f"\n\n[WEB]: {web_data}"
    all_msgs = [{"role": "system", "content": system_prompt}] + messages
    comp = client.chat.completions.create(model=model, messages=all_msgs, temperature=0.7)
    return comp.choices[0].message.content

# --- ВЕРХНЯЯ ПАНЕЛЬ ---
header_col, auth_col = st.columns([8, 2])
with header_col:
    st.title("Akylman AI")

with auth_col:
    if st.session_state.user:
        if st.button("Выйти", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
    else:
        if st.button("Вход / Рега", use_container_width=True):
            st.session_state.show_auth = True

if not st.session_state.user:
    st.info("Войдите, чтобы Akylman запомнил вас.")
    email = st.text_input("Email")
    pwd = st.text_input("Пароль", type="password")
    c1, c2 = st.columns(2)
    
    if c1.button("Войти"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
            st.session_state.user = res.user
            st.rerun()
        except: st.error("Ошибка входа")
        
    if c2.button("Регистрация"):
        try:
            supabase.auth.sign_up({"email": email, "password": pwd})
            st.success("Готово! Если подтверждение почты включено — проверьте email.")
        except: st.error("Ошибка регистрации")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = load_history(st.session_state.user.id)

with st.sidebar:
    st.title("⚙️ Настройки")
    if st.button("➕ Новый чат", use_container_width=True):
        supabase.table("chat_history").delete().eq("user_id", st.session_state.user.id).execute()
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    code = st.text_input("Код доступа", type="password")
    models = {"Быстрая": "llama-3.1-8b-instant", "Думающая": "llama-3.3-70b-versatile"}
    if code == "1234":
        if not st.session_state.access_granted:
            st.session_state.access_granted = True
            st.balloons()
        models.update({"Pro": "llama-3.3-70b-versatile"})
    
    sel_model = models[st.selectbox("Модель:", list(models.keys()))]
    up_file = st.file_uploader("Загрузить файл", type=["pdf", "txt"])

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Напиши Акылману..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_msg(st.session_state.user.id, "user", prompt)
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            f_text = ""
            if up_file:
                try:
                    reader = PdfReader(up_file)
                    f_text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
                except: pass
            
            ans = generate_response(st.session_state.messages, sel_model, f_text, st.session_state.user.email)
            st.markdown(ans)
            save_msg(st.session_state.user.id, "assistant", ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
