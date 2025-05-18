from telebot import types
import threading
from bot_instance import bot
from config import VLADA
from common import VLADOSTAS, vlada_responded, set_default_vladostas
# Почему эта функция в отдельном файле? Потому что.

# Запрос у Влады количества Стасов
def ask_vlada_for_stas():
    global vlada_responded
    vlada_responded = False
    markup = types.InlineKeyboardMarkup()
    btn_two_stas = types.InlineKeyboardButton("Два Стаса", callback_data='two_stas')
    btn_one_stas = types.InlineKeyboardButton("Один Стас", callback_data='one_stas')
    markup.add(btn_two_stas, btn_one_stas)
    try:
        bot.send_message(VLADA, "Привет! Сколько Стасов возьмешь с собой на магию?", reply_markup=markup)
        threading.Timer(1800, set_default_vladostas).start()
    except Exception as e:
        print(f"Ошибка при отправке запроса VLADA: {e}") 