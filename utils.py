import streamlit as st
from duckduckgo_search import DDGS
from pypdf import PdfReader
from docx import Document

def extract_text(file):
    try:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            return "".join([page.extract_text() for page in reader.pages])
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file)
            return "\n".join([p.text for p in doc.paragraphs])
        else:
            return file.read().decode("utf-8")
    except:
        return "Ошибка чтения файла."

def search_web(query):
    try:
        with DDGS() as ddgs:
            return "\n".join([r['body'] for r in ddgs.text(query, max_results=3)])
    except: return ""
