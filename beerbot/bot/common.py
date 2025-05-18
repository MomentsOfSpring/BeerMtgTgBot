from telebot import types
from bot_instance import bot

# Константы
VLADOSTAS = 3
vlada_responded = False

# Установка значения по умолчанию для Влады
def set_default_vladostas():
    global VLADOSTAS, vlada_responded
    if not vlada_responded:
        VLADOSTAS = 3
        print("VLADA не ответил в течение 30 минут, VLADOSTAS установлен в 3")

# Отправка кнопок бронирования
def send_reservation_buttons(chat_id, message_id=None):
    markup = types.InlineKeyboardMarkup()
    btn_book = types.InlineKeyboardButton("Забронировать", callback_data='book_table')
    btn_not_come = types.InlineKeyboardButton("Мы не придем", callback_data='not_come')
    markup.add(btn_book, btn_not_come)
    
    if message_id is not None:
        # Если передан message_id, редактируем существующее сообщение
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Выберите действие:",
            reply_markup=markup
        )
    else:
        # Иначе отправляем новое сообщение
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup) 