# bot.py
import asyncio
from aiogram import Bot, Dispatcher, types, F
from behavior import get_opener, adjust_tone # Подключаем твои наработки
from brain import get_ai_response
from config import TELEGRAM_TOKEN, SUBJECTS

# ... в функции обработки сообщений ...
@dp.message()
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    subj = user_subjects.get(user_id, "General")
    
    # Получаем ответ от ИИ
    response = get_ai_response(message.text, subj)
    
    # Применяем твой фильтр тона из behavior.py
    final_text = adjust_tone(response, subj)
    
    await message.answer(final_text)
