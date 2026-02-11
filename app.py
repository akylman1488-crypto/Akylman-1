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
from debate_logic import get_debate_response
from analyzer import display_metrics
from quiz_gen import generate_quiz
from exporter import export_to_markdown
from stats_dashboard import show_stats, update_stat
from styles import apply_dynamic_theme

with st.sidebar:
    subject = st.selectbox("Предмет:", list(SUBJECTS.keys()))
    apply_dynamic_theme(subject)

st.set_page_config(page_title="Akylman Ultra Pro", layout="wide")
apply_styles()

if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.title("🚀 Akylman Ultra")
    subject = st.selectbox("Предмет:", list(SUBJECTS.keys()))
    
    debate_mode = st.toggle("🔥 Режим дебатов")
    
    study_timer()
    st.divider()
    
    uploaded_file = st.file_uploader("Файл:", type=['pdf', 'txt', 'docx'])
    f_txt = extract_text(uploaded_file) if uploaded_file else ""
    display_metrics(f_txt)
    
    if st.button("📝 Создать квиз"):
        st.session_state.messages.append({"role": "assistant", "content": generate_quiz(f_txt)})
        
    if st.button("🗺 План обучения"):
        st.session_state.messages.append({"role": "assistant", "content": generate_roadmap(subject)})
    
    if st.button("📊 График"):
        create_chart("line")
        
    st.divider()
    download_chat_button()
    show_stats()
    
    if st.button("🗑 Очистить"):
        st.session_state.messages = []
        st.rerun()

st.title(f"{'⚖️' if debate_mode else SUBJECTS[subject]} {subject}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Спроси, нарисуй или начни дебаты..."):
    update_stats(subject)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        w_txt = search_web(f"{subject} {prompt}")
        
        if debate_mode:
            stream = get_debate_response(prompt, subject, st.session_state.messages)
        else:
            stream = get_ai_response(prompt, subject, f_txt, w_txt, st.session_state.messages)
            
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_res += chunk.choices[0].delta.content
                placeholder.markdown(full_res + "▌")
        
        placeholder.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
