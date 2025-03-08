import telebot
from openai import OpenAI
import os
import time


# Твои ключи
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(commands=['chatid'])
def send_chat_id(message):
    bot.reply_to(message, f"ID этой группы:{message.chat.id}")

@bot.message_handler(func=lambda message: message.text.lower().startswith('чат'))
def respond(message):
    try:
        user_request = message.text[3:].strip()  # Убираем слово "чат"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Отвечай только на русском языке."},
                {"role": "user", "content": user_request}
            ]
        )
        bot.send_message(message.chat.id, response.choices[0].message.content)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

while True:
    try:
        bot.polling(none_stop=True, interval=1, timeout=20)
    except Exception as e:
        print(f"Ошибка: {e}. Перезапуск через 5 секунд.")
        time.sleep(5)

