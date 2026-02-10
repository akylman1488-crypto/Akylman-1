import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from datetime import datetime
from pypdf import PdfReader

st.set_page_config(page_title="Akylman AI: Online", page_icon="🌐")

if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Нет ключа API в секретах!")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory" not in st.session_state:
    st.session_state.memory = "Ты — Akylman, мудрый AI. Ты помогаешь пользователю."

def search_web(query):
    """Ищет информацию в DuckDuckGo"""
    try:
        results = DDGS().text(query, max_results=3)
        if results:
            context = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
            return context
        return "Ничего не найдено."
    except Exception as e:
        return f"Ошибка поиска: {e}"

def generate_response(messages, model, web_enabled, context_file=""):
    system_prompt = st.session_state.memory

    if context_file:
        system_prompt += f"\n\n[КОНТЕКСТ ИЗ ФАЙЛА]:\n{context_file}"

    last_user_msg = messages[-1]["content"]
    if web_enabled:
        with st.spinner("🔍 Ищу информацию в интернете..."):
            web_results = search_web(last_user_msg)
        system_prompt += f"\n\n[ДАННЫЕ ИЗ ИНТЕРНЕТА ПО ЗАПРОСУ '{last_user_msg}']:\n{web_results}\nИспользуй эти данные для ответа, если они актуальны."

    all_messages = [{"role": "system", "content": system_prompt}]
    for m in messages:
        all_messages.append({"role": m["role"], "content": m["content"]})

    try:
        chat_completion = client.chat.completions.create(
            messages=all_messages,
            model=model,
            temperature=0.6,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Ошибка модели: {str(e)}"

with st.sidebar:
    st.title("🌐 Akylman 4.0")

    model = st.selectbox(
        "Мозг:",
        ("llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768")
    )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        web_search = st.toggle("🌐 Интернет", value=False)
    with col2:
        if st.button("🗑️ Сброс"):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")

    with st.expander("🧠 Обучение и Память"):
        new_memory = st.text_area(
            "Чему научить Акылмана?", 
            value=st.session_state.memory,
            height=150,
            help="Напиши сюда правила, которые бот должен помнить всегда."
        )
        if new_memory != st.session_state.memory:
            st.session_state.memory = new_memory
            st.success("Обновлено!")

    uploaded_file = st.file_uploader("📂 Документы", type=["pdf", "txt"])

st.title("Akylman AI")

if not st.session_state.messages:
    hour = datetime.now().hour
    greeting = "Привет! Я на связи. Включи 'Интернет' слева, если нужны свежие данные."
    st.session_state.messages.append({"role": "assistant", "content": greeting})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Спроси что-нибудь..."):
    file_text = ""
    if uploaded_file:
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                file_text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
            else:
                file_text = uploaded_file.read().decode("utf-8")
        except:
            st.error("Ошибка чтения файла")

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = generate_response(st.session_state.messages, model, web_search, file_text)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
