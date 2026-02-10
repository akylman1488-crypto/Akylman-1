import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from pypdf import PdfReader
from datetime import datetime

st.set_page_config(page_title="Akylman AI", page_icon="🧠", layout="centered")

if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("API key not found.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

def search_web(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            if results:
                return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except:
        pass
    return ""

def get_opener():
    h = datetime.now().hour
    if 5 <= h < 12: return "Доброе утро. Я готов слушать."
    elif 12 <= h < 18: return "Добрый день. Акылман на связи."
    else: return "Добрый вечер."

def generate_response(messages, model, context_file):
    last_user_msg = messages[-1]["content"]
    web_data = search_web(last_user_msg)
    
    system_prompt = (
        "Ты — Akylman. Мудрый, спокойный и проницательный. "
        "Ты ВСЕГДА используешь актуальные данные из интернета, если они предоставлены. "
        "Ты самообучаешься на основе текущего диалога: анализируй стиль пользователя и его факты. "
    )
    
    if context_file:
        system_prompt += f"\n\n[FILE]: {context_file}"
    if web_data:
        system_prompt += f"\n\n[WEB]: {web_data}"

    all_msgs = [{"role": "system", "content": system_prompt}]
    all_msgs.extend([{"role": m["role"], "content": m["content"]} for m in messages])

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=all_msgs,
            temperature=0.6
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {e}"

with st.sidebar:
    st.title("🧠 Akylman")
    
    if st.button("➕ Новый чат", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    password = st.text_input("Доступ", type="password", placeholder="Введите пароль...")
    
    models = {
        "Быстрая ⚡": "llama-3.1-8b-instant",
        "Думающая 🤔": "llama-3.3-70b-versatile"
    }
    
    if password == "1234":
        if not st.session_state.access_granted:
            st.session_state.access_granted = True
            st.balloons()
        models["Pro 🔥"] = "llama-3.3-70b-versatile"
        models["Plus 💎"] = "mixtral-8x7b-32768"
        st.success("Пароль верен")
    
    selected_name = st.selectbox("Выбор модели:", list(models.keys()))
    selected_model = models[selected_name]

    st.markdown("---")
    uploaded_file = st.file_uploader("Документ (PDF/TXT)", type=["pdf", "txt"])

st.markdown("<h1 style='text-align: center;'>Akylman</h1>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": get_opener()})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Напиши Акылману..."):
    file_text = ""
    if uploaded_file:
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                file_text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
            else:
                file_text = uploaded_file.read().decode("utf-8")
        except:
            pass

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Акылман ищет ответы..."):
            res = generate_response(st.session_state.messages, selected_model, file_text)
            st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})
