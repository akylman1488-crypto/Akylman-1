from brain import client
from config import MODEL_NAME

def quick_translate(text, target_lang="Russian"):
    if not text: return ""
    prompt = f"Translate this text to {target_lang}: {text}"
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
