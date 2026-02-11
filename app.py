import streamlit as st
from config import SUBJECTS
from styles import apply_styles
from utils import extract_text, search_web
from brain import get_ai_response
from data_manager import download_chat_button
from visualizer import create_chart
from translator import quick_translate
from roadmap_gen import generate_roadmap
from scholar_search import search_educational
from timer_module import study_timer

st.set_page_config(page_title="Akylman Ultra", layout="wide")
apply_styles()

if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.title("🚀 Akylman Ultra")
    subject = st.selectbox("Предмет:", list(SUBJECTS.keys()))
    uploaded_file = st.file_uploader("Файл:", type=['pdf', 'txt', 'docx'])
    
    study_timer()
    
    if st.button("🗺 Создать план обучения"):
        plan = generate_roadmap(subject)
        st.session_state.messages.append({"role": "assistant", "content": plan})
    
    if st.button("📊 Построить график"):
        create_chart("line")
    
    download_chat_button()

st.title(f"{SUBJECTS[subject]} {subject}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Спроси или попроси найти научную статью..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        f_txt = extract_text(uploaded_file) if uploaded_file else ""
        web_txt = search_web(f"{subject} {prompt}")
        
        stream = get_ai_response(prompt, subject, f_txt, web_txt, st.session_state.messages)
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_res += chunk.choices[0].delta.content
                placeholder.markdown(full_res + "▌")
        
        placeholder.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
