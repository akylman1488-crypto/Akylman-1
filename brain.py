from groq import Groq
from config import GROQ_API_KEY, PROMPTS

client = Groq(api_key=GROQ_API_KEY)

def get_ai_response(prompt, subject, context="", history=[]):
    system_instruction = PROMPTS.get(subject, PROMPTS["General"])
    
    messages = [{"role": "system", "content": f"{system_instruction}\nКонтекст: {context}"}]
    
    # Добавляем историю для памяти
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
        return f"⚠️ Ошибка ИИ: {str(e)}"
