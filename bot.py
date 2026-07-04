import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

TOKEN = "8832873611:AAERZVR-1dopD5PvZdmC0wN2rrWA6fPBFM8"
ADMIN_ID = 5889477300  # сюда свой Telegram ID

PROMO = "Forzze228689"

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage)


class UserState(StatesGroup):
    promo = State()
    gameid = State()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать!\n\nВведите промокод:"
    )
    bot.set_state(message.from_user.id, UserState.promo, message.chat.id)


@bot.message_handler(state=UserState.promo)
def promo(message):
    if message.text.strip() == PROMO:
        bot.send_message(
            message.chat.id,
            "✅ Промокод принят!\n\nТеперь отправьте ваш игровой ID Standoff 2."
        )
        bot.set_state(message.from_user.id, UserState.gameid, message.chat.id)
    else:
        bot.send_message(
            message.chat.id,
            "❌ Неверный промокод.\nПопробуйте ещё раз."
        )


@bot.message_handler(state=UserState.gameid)
def gameid(message):
    username = message.from_user.username
    if username:
        username = "@" + username
    else:
        username = "Без username"

    text = f"""
🔔 Новая заявка

👤 Пользователь: {username}
🆔 Telegram ID: {message.from_user.id}
🎮 Игровой ID: {message.text}
"""

    bot.send_message(ADMIN_ID, text)
    bot.send_message(
        message.chat.id,
        "✅ Заявка отправлена администрации.\nОжидайте выдачи."
    )
    bot.delete_state(message.from_user.id, message.chat.id)


print("Bot started...")
bot.infinity_polling(skip_pending=True)
