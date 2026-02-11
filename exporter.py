import streamlit as st

def export_to_markdown(content):
    st.download_button(
        label="📄 Сохранить конспект (.md)",
        data=content,
        file_name="akylman_notes.md",
        mime="text/markdown",
        use_container_width=True
    )
