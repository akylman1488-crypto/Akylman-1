import streamlit as st
from utils import extract_text, search_web
from brain import get_ai_response
from styles import apply_styles         
from config import SUBJECTS, PROMPTS    
from data_manager import download_chat_button 

# Применяем стили
apply_styles()

with st.sidebar:
    subject = st.selectbox("Предмет:", list(SUBJECTS.keys()))
    download_chat_button() 

st.set_page_config(page_title="Akylman AI Pro", layout="wide")

if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.title("🎓 Akylman Hub")
    subject = st.selectbox("Предмет:", ["Mathematics", "Physics", "Biology", "History", "ICT", "English"])
    uploaded_file = st.file_uploader("Загрузить файл", type=['pdf', 'txt', 'docx'])
    if st.button("🗑 Очистить"):
        st.session_state.messages = []
        st.rerun()

st.title(f"Akylman: {subject}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Спроси меня..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        file_txt = extract_text(uploaded_file) if uploaded_file else ""
        web_txt = search_web(f"{subject} {prompt}")
        
        response_stream = get_ai_response(prompt, subject, file_txt, web_txt, st.session_state.messages)
        
        for chunk in response_stream:
            if chunk.choices[0].delta.content:
                full_res += chunk.choices[0].delta.content
                placeholder.markdown(full_res + "▌")
        
        placeholder.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
