import streamlit as st
import brain
import behavior
import config

st.set_page_config(page_title="Akylman AI 2.0", page_icon="🧠")

if "messages" not in st.session_state:
    st.session_state.messages = []
    opener = behavior.get_opener()
    st.session_state.messages.append({"role": "assistant", "content": opener})

st.title("Akylman AI — Твой мудрый наставник")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Напиши Акылману..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = brain.generate_response(st.session_state.messages)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
