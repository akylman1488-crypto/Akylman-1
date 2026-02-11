import streamlit as st

def get_text_metrics(text):
    if not text:
        return None
    words = text.split()
    avg_word_len = sum(len(word) for word in words) / len(words)
    return {
        "word_count": len(words),
        "avg_word_length": round(avg_word_len, 2),
        "complexity": "High" if avg_word_len > 6 else "Medium" if avg_word_len > 4 else "Low"
    }

def display_metrics(text):
    metrics = get_text_metrics(text)
    if metrics:
        st.sidebar.metric("Слов в контексте", metrics["word_count"])
        st.sidebar.metric("Сложность материала", metrics["complexity"])
