import streamlit as st

st.set_page_config(
    page_title="Akylman Ultra Pro", 
    layout="wide",
    page_icon="🎓"
)

try:
    from config import SUBJECTS
    from styles import apply_styles, apply_dynamic_theme
    from brain import get_ai_response
    from data_manager import download_chat_button
    from roadmap_gen import generate_roadmap
    from timer_module import study_timer
    from debate_logic import get_debate_response
    from image_gen import generate_image_ui
    # Заглушки для библиотек, которых пока может не быть
    # from scholar_search import search_educational
    # from analyzer import display_metrics
except ImportError as e:
    st.error(f"Ошибка импорта: {e}")
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

    try:
        generate_image_ui()
    except:
        st.info("Генератор картинок временно недоступен")
        
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

                    response = get_ai_response(
                        prompt, 
                        subject, 
                        "", 
                        "", 
                        st.session_state.messages
                    )
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            except Exception as e:
                st.error(f"Ошибка в мозге: {e}")

if st.session_state.messages:
    st.divider()
    col1, col2 = st.columns([1, 4])
    with col1:
        download_chat_button(st.session_state.messages)
    with col2:
        if st.button("🗺 Создать Roadmap"):
            with st.spinner("Рисую план обучения..."):
                try:
                    roadmap = generate_roadmap(subject)
                    st.markdown(roadmap)
                except:
                    st.error("Ошибка Roadmap")
