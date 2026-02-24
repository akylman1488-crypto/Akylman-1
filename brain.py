import json
import os
from groq import Groq
from config import GROQ_API_KEY, PROMPTS
import groq
import random

# Список твоих ключей (добавь сюда столько, сколько есть)
GROQ_KEYS = [
    "",
    "gsk_key_2_ваша_строка",
    "gsk_key_3_ваша_строка"
]

def get_ai_response(prompt):
    # Копируем список ключей, чтобы пробовать их по очереди
    available_keys = GROQ_KEYS.copy()
    
    while available_keys:
        # Берем первый ключ из списка
        current_key = available_keys[0]
        
        try:
            client = groq.Client(api_key=current_key)
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
            
        except Exception as e:
            # Если ошибка 429 (лимит исчерпан)
            if "429" in str(e) or "rate_limit" in str(e).lower():
                print(f"Ключ {current_key[:10]}... исчерпан. Переключаюсь.")
                available_keys.pop(0) # Удаляем нерабочий ключ и идем на второй круг
            else:
                return f"Произошла ошибка: {e}"
    
    return "Извини, все лимиты на сегодня исчерпаны даже на запасных ключах!"

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

