import random
from datetime import datetime

def get_opener():
    hour = datetime.now().hour
    
    morning = ["Доброе утро! Я Акылман. Готов к новым свершениям сегодня?", "Привет! Утро — время мудрости. О чем хочешь поговорить?"]
    day = ["Добрый день! Как твои дела? У меня есть пара идей, если тебе интересно.", "Привет! Акылман на связи. Нужна помощь или просто беседа?"]
    evening = ["Добрый вечер. Как прошел день? Давай обсудим что-нибудь важное.", "Привет! Вечер — время итогов. Что полезного мы сегодня сделали?"]

    if 5 <= hour < 12:
        return random.choice(morning)
    elif 12 <= hour < 18:
        return random.choice(day)
    else:
        return random.choice(evening)
