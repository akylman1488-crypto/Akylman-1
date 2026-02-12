from groq import Groq
from config import GROQ_API_KEY, MODELS

client = Groq(api_key=GROQ_API_KEY)

def get_ai_response(prompt, subject, context="", history=[]):
    messages = [{"role": "system", "content": f"Ты Akylman, эксперт в {subject}. Отвечай человечно, глубоко, но без лишней воды. Контекст: {context}"}]
    for m in history[-5:]:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": prompt})
    
    completion = client.chat.completions.create(model=MODELS["Fast"], messages=messages, temperature=0.6)
    return completion.choices[0].message.content
