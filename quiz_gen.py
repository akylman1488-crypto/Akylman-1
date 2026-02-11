from brain import client
from config import MODEL_NAME

def generate_quiz(context):
    prompt = f"На основе этого текста создай 3 вопроса с вариантами ответов для проверки знаний: {context}"
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
