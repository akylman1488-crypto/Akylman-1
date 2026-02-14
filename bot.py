import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from brain import get_ai_response
from config import TELEGRAM_TOKEN, SUBJECTS

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

user_subjects = {}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    kb = [
        [types.KeyboardButton(text=s)] for s in SUBJECTS.keys()
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Привет! Я Акылман. Выбери предмет для начала обучения:", reply_markup=markup)

@dp.message(F.text.in_(SUBJECTS.keys()))
async def set_subject(message: types.Message):
    user_subjects[message.from_user.id] = message.text
    await message.answer(f"Предмет установлен: {message.text}. Теперь можешь задавать вопросы!")

@dp.message()
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    subject = user_subjects.get(user_id, "General")
    
    msg = await message.answer("🤔 Акылман думает...")
    
    response = get_ai_response(message.text, subject)
    
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=msg.message_id,
        text=response,
        parse_mode="Markdown"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
