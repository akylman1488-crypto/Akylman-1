import streamlit as st

st.set_page_config(
    page_title="Akylman Ultra Pro", 
    layout="wide",
    page_icon="🎓"
)

try:
    from config import SUBJECTS
    from styles import apply_styles, apply_dynamic_theme
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
    # from quiz_gen import generate_quiz          # Раскомментируй, если создал файл
    # from exporter import export_to_markdown     # Раскомментируй, если создал файл
    # from stats_dashboard import show_stats      # Раскомментируй, если создал файл
except ImportError as e:
    st.error(f"Ошибка импорта библиотеки: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "debate_mode" not in st.session_state:
    st.session_state.debate_mode = False

with st.sidebar:
    st.title("🎓 Akylman")

    subject = st.selectbox(
        "Предмет:", 
        list(SUBJECTS.keys()) if 'SUBJECTS' in locals() else ["General"],
        key="subject_select"
    )

    apply_dynamic_theme(subject)
    
    st.divider()

    study_timer()
    
    st.divider()
    
    st.divider()

    st.session_state.debate_mode = st.toggle("🔥 Режим дебатов", value=False)
    
    if st.button("🗑 Очистить чат"):
        st.session_state.messages = []
        st.rerun()

apply_styles()

if st.session_state.debate_mode:
    st.header(f"⚔️ Дебаты: {subject}")
else:
    st.header(f"📚 {SUBJECTS.get(subject, '')} {subject}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Задай вопрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            try:
                if st.session_state.debate_mode:
                    response = get_debate_response(prompt, subject)
                else:
                    response = get_ai_response(prompt, subject)
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            except Exception as e:
                st.error(f"Ошибка генерации: {e}")
if st.session_state.messages:
    st.divider()
    col1, col2 = st.columns([1, 4])
    with col1:
        download_chat_button(st.session_state.messages)
    with col2:
        if st.button("🗺 Создать карту знаний"):
            with st.spinner("Рисую Roadmap..."):
                roadmap = generate_roadmap(subject)
                st.markdown(roadmap)
