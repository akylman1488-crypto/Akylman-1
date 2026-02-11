import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from pypdf import PdfReader
from docx import Document

st.set_page_config(page_title="Akylman AI Pro", page_icon="🎓", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages = []

def extract_text(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        return "".join([page.extract_text() for page in reader.pages])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return file.read().decode("utf-8")

def search_web(query):
    try:
        with DDGS() as ddgs:
            return "\n".join([r['body'] for r in ddgs.text(query, max_results=3)])
    except: return ""

with st.sidebar:
    st.title("📚 Учебный центр")
    subject = st.selectbox(
        "Выберите предмет:",
        ["Mathematics", "Physics", "Biology", "History", "ICT", "English"]
    )
    
    st.divider()
    uploaded_file = st.file_uploader("Загрузить учебный материал", type=['pdf', 'txt', 'docx'])
    
    if st.button("🗑 Очистить чат", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title(f"Akylman AI: {subject}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Задай вопрос по предмету..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        context = ""
        if uploaded_file:
            context += f"\nКонтекст из файла: {extract_text(uploaded_file)}"
        
        web_info = search_web(f"{subject} {prompt}")
        
        sys_prompt = f""" Ты эксперт по предмету {subject}. 
        Используй свои глубокие знания и предоставленный контекст для помощи ученику.
        Контекст файла: {context}
        Данные из сети: {web_info}
        Отвечай четко и по делу.
        Ты всегда начинаешь диалог первым.
        твой создатель Исанур, ты не упоминаешь его при каждом удобном случае, и ты создан в президентцком лицее АКЫЛМАН.
        """

        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_res += chunk.choices[0].delta.content
                placeholder.markdown(full_res + "▌")
        
        placeholder.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
