import asyncio
from aiogram import Bot, Dispatcher, types, F
from config import TELEGRAM_TOKEN, SUBJECTS
from brain import get_ai_response
from behavior import get_opener, adjust_tone # Твои уникальные функции

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    # Используем твой уникальный генератор приветствий
    greeting = get_opener() 
    kb = [[types.KeyboardButton(text=s)] for s in SUBJECTS.keys()]
    markup = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"{greeting}\nЯ Akylman. Выбери режим:", reply_markup=markup)

@dp.message()
async def chat_handler(message: types.Message):
    # Читаем твою базу знаний из файла
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        memory = f.read()

    # Получаем ответ, учитывая твой контекст
    response = get_ai_response(message.text, context=memory)
    
    # Применяем твой уникальный фильтр тона из behavior.py
    final_text = adjust_tone(response, "Just Friend")
    
    await message.answer(final_text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
