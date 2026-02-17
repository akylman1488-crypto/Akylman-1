import json
import os
from groq import Groq
from config import GROQ_API_KEY, PROMPTS

def get_ai_response(prompt, subject="General", context=""):
    p_lower = prompt.lower()
    who_list = ["кто тебя создал", "кто твой создатель", "чей ты проект", "кто твой автор"]
    
    if any(q in p_lower for q in who_list):
        return "Меня создал Исанур! 😎 Я — уникальный ИИ-проект, разработанный им лично."

client = Groq(api_key=GROQ_API_KEY)

def get_quiz_json(topic, subject):
    prompt = f"""
    Создай тест на тему '{topic}' по предмету '{subject}'.
    Верни ТОЛЬКО JSON формат (список из 3 объектов).
    Каждый объект: {{"question": "текст", "options": ["А", "Б", "В", "Г"], "answer": "правильный текст"}}
    Никакого лишнего текста, только чистый JSON.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        data = json.loads(completion.choices[0].message.content)
        return data.get("questions", data) if isinstance(data, dict) else data
    except:
        return None

def get_ai_response(prompt, subject, history=None, context=""):
    if history is None: history = []
        
    system_msg = PROMPTS.get(subject, PROMPTS.get("General", "You are Akylman"))
    
    messages = [{"role": "system", "content": f"{system_msg}\nContext: {context}"}]
    
    for msg in history[-5:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    messages.append({"role": "user", "content": prompt})
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.6
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {e}"

