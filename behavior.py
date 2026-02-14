import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from brain import get_ai_response, get_quiz_json
from behavior import get_opener, adjust_tone
from config import TELEGRAM_TOKEN, SUBJECTS

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

user_data = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Используем твой get_opener() из behavior.py
    greeting = get_opener()
    kb = [[types.KeyboardButton(text=subj)] for subj in SUBJECTS.keys()]
    kb.append([types.KeyboardButton(text="📝 Пройти тест")])
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"{greeting}\n\nЯ Акылман. Выбери предмет или начни тест:", reply_markup=keyboard)

@dp.message(F.text == "📝 Пройти тест")
async def start_quiz(message: types.Message):
    await message.answer("Напиши тему для теста (например: 'История кочевников'):")
    user_data[message.from_user.id] = "waiting_topic"

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    state = user_data.get(user_id)

    # Логика тестов как у Gemini
    if state == "waiting_topic":
        await message.answer("⏳ Создаю интерактивный тест...")
        questions = get_quiz_json(message.text, "General")
        if questions:
            for q in questions:
                options = q['options']
                # Отправляем настоящий опрос Telegram
                await bot.send_poll(
                    chat_id=message.chat.id,
                    question=q['question'],
                    options=options,
                    is_anonymous=False,
                    type='quiz',
                    correct_option_id=options.index(q['answer']),
                    explanation="Акылман: " + q.get('explanation', 'Учись прилежно!')
                )
            user_data[user_id] = None
        return

    # Обычный чат
    subj = user_data.get(user_id, "General")
    raw_response = get_ai_response(message.text, subj)
    
    # Применяем твой adjust_tone() из behavior.py
    final_response = adjust_tone(raw_response, subj)
    
    await message.answer(final_response, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
