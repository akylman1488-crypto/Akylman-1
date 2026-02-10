import streamlit as st
from groq import Groq
import random
from datetime import datetime
from pypdf import PdfReader

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Akylman AI", page_icon="🧠")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

def get_opener():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "Доброе утро! Я Akylman. Готов к новым мудростям?"
    elif 12 <= hour < 18: return "Добрый день! Akylman на связи. О чем поразмышляем?"
    else: return "Добрый вечер. Давай обсудим что-нибудь важное перед сном."

def generate_response(messages, model_id, context=""):
    try:
        system_prompt = "Ты — Akylman AI, мудрый наставник. Твоя цель — помогать и направлять."
        if context:
            system_prompt += f"\nКонтекст из файла: {context}"
            
        completion = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "system", "content": system_prompt}] + 
                     [{"role": m["role"], "content": m["content"]} for m in messages],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Хм, модель {model_id} сейчас капризничает. Попробуй переключиться на 'Быструю'. (Ошибка: {str(e)})"

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.title("🧠 Akylman")
    
    if st.button("➕ Новый чат", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    
    model_options = {
        "Быстрая ⚡": "llama-3.1-8b-instant",
        "Думающая 🤔": "llama-3.3-70b-versatile"
    }
    
    password = st.text_input("Пароль доступа:", type="password")
    if password == "1234":
        if not st.session_state.access_granted:
            st.session_state.access_granted = True
            st.balloons() 
        st.success("Пароль верен! Открыты PRO-модели.")
        model_options["Версия Pro 🔥"] = "llama-3.3-70b-versatile"
        model_options["Версия Plus 💎"] = "mixtral-8x7b-32768"
    elif password:
        st.error("Пароль неверен")
        st.session_state.access_granted = False

    selected_model_name = st.selectbox("Выберите модель:", list(model_options.keys()))
    selected_model = model_options[selected_model_name]

    st.markdown("---")
    uploaded_file = st.file_uploader("📂 Загрузить документ", type=["pdf", "txt"])

st.markdown("<h1 style='text-align: center;'>Akylman</h1>", unsafe_allow_html=True)

if not st.session_state.messages:
    opener = get_opener()
    st.session_state.messages.append({"role": "assistant", "content": opener})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Напиши Акылману..."):
    file_context = ""
    if uploaded_file:
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                file_context = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            else:
                file_context = uploaded_file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Не удалось прочитать файл: {e}")

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Акылман думает..."):
            res = generate_response(st.session_state.messages, selected_model, file_context)
            st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})
