from brain import client
from config import MODEL_NAME

def get_debate_response(user_input, subject, messages):
    debate_sys_prompt = f"""Ты — мастер дебатов и критического мышления. 
    Твоя задача по предмету {subject} — НЕ соглашаться с пользователем.
    Если пользователь утверждает что-то, найди контраргумент. 
    Ставь под сомнение его логику, проси доказательства и приводи альтернативные точки зрения. 
    Будь вежливым, но непоколебимым оппонентом. Твои ответы должны быть короткими и острыми."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": debate_sys_prompt}] + messages,
        stream=True
    )
    return response
