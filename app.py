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
        results = DDGS().text(query, max_results=3)
        if results:
            return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
        return ""
    except:
        return ""

def get_opener():
    h = datetime.now().hour
    if 5 <= h < 12: return "Доброе утро. Я готов слушать."
    elif 12 <= h < 18: return "Добрый день. Акылман на связи."
    else: return "Добрый вечер."

def generate_response(messages, model, web_enabled, context_file):
    system_prompt = (
        "Ты — Akylman. Мудрый, спокойный и проницательный. "
        "Ты самообучаешься на основе текущего диалога: анализируй стиль пользователя, "
        "его предпочтения и факты, упомянутые ранее. "
        "Твоя личность адаптируется под пользователя."
    )
    
    if context_file:
        system_prompt += f"\n\n[FILE CONTEXT]:\n{context_file}"

    if web_enabled:
        last_query = messages[-1]["content"]
        web_data = search_web(last_query)
        if web_data:
            system_prompt += f"\n\n[WEB DATA]:\n{web_data}"

    all_msgs = [{"role": "system", "content": system_prompt}]
    for m in messages:
        all_msgs.append({"role": m["role"], "content": m["content"]})

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
    
    password = st.text_input("Доступ", type="password", placeholder="Введите пароль...")
    
    selected_model = "llama-3.3-70b-versatile"
    enable_web = False 
    
    if password == "1234":
        if not st.session_state.access_granted:
            st.session_state.access_granted = True
            st.balloons()
            st.toast("Доступ разрешен", icon="🔓")
        
        st.success("Пароль верен")
        st.markdown("---")
        
        selected_model = st.selectbox(
            "Выбор модели:",
            ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "llama-3.1-8b-instant"]
        )
        enable_web = st.toggle("Поиск в интернете", value=True)
        
        if st.button("Очистить чат"):
            st.session_state.messages = []
            st.rerun()
            
    elif password:
        st.error("Пароль неверен")
        st.session_state.access_granted = False

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
        with st.spinner("..."):
            res = generate_response(st.session_state.messages, selected_model, enable_web, file_text)
            st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})
