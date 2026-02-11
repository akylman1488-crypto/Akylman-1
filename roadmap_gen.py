from brain import client
from config import MODEL_NAME

def generate_roadmap(topic):
    prompt = f"Создай подробный учебный план (roadmap) для изучения темы: {topic}. Разбей на уровни от простого к сложному."
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
