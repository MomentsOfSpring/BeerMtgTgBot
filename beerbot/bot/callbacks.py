from telebot import types
from config import MAGIC_CHAT_ID, BOSS, BARTENDER, VLADA
from utils import declension_tables
import threading
from bot_instance import bot
from commands import beer_rules
from common import VLADOSTAS, vlada_responded, set_default_vladostas, send_reservation_buttons
from polls import generate_report


# Обработка нажатий на кнопки
def callback_message(callback):
    global VLADOSTAS, vlada_responded
    data = callback.data
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    
    # Обработка нажатий на кнопки от Влады
    if data in ['two_stas', 'one_stas'] and callback.from_user.id == VLADA:
        if not vlada_responded:
            VLADOSTAS = 3 if data == 'two_stas' else 2
            vlada_responded = True
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="Спасибо, я передам"
            )
        else:
            bot.answer_callback_query(callback.id, "Ответ уже учтён, спасибо!")
        return

    # Обработка нажатий на кнопки от нового пользователя
    if data.startswith("beer_"):
        parts = data.split("_")
        if len(parts) != 3:
            bot.answer_callback_query(callback.id, "Некорректные данные!", show_alert=True)
            return
        action = parts[1]
        try:
            user_id_from_button = int(parts[2])
        except ValueError:
            bot.answer_callback_query(callback.id, "Некорректный user_id!", show_alert=True)
            return

        if callback.from_user.id != user_id_from_button:
            bot.answer_callback_query(callback.id, "Остальных не спрашивали!", show_alert=True)
            return

        bot.answer_callback_query(callback.id)


        # Обработка нажатия на кнопки любви к пиву
        if action == "yes":
            bot.restrict_chat_member(
                chat_id,
                user_id_from_button,
                permissions=types.ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )
            bot.edit_message_text(
                "Добро пожаловать домой!",
                chat_id,
                message_id
            )
            full_name = f"{callback.from_user.first_name or ''} {callback.from_user.last_name or ''}".strip()
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('📜 Правила группы', callback_data='RULES'))
            welcome_text = (
                f"Добро пожаловать, {full_name}! 🎉\n\n"
                f"Ознакомься с правилами группы, чтобы не получить по щам!"
            )
            bot.send_message(chat_id, welcome_text, reply_markup=markup)
            
        # Обработка нажатия на кнопки не любви к пиву
        elif action == "no":
            bot.edit_message_text(
                "У нас таких не любят..",
                chat_id,
                message_id
            )
            bot.kick_chat_member(chat_id, user_id_from_button)
        return
    
        
    # Обработка нажатия на кнопку "Правила группы"
    elif data == 'RULES':
        beer_rules(callback.message)
        
    # Обработка нажатия на кнопку "Забронировать стол"
    elif data == 'book_table':
        report, tables = generate_report(bot)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Стол забронирован! 🪑"
        )
        try:
            bot.send_message(MAGIC_CHAT_ID, f"Босс забронировал кабак!")
            bot.send_message(BOSS, 'Отлично, фиксируем столы.')
            bot.send_message(BARTENDER, f"Привет, маги сегодня придут к 19:00, резервируем {declension_tables(tables)}")
        except Exception as e:
            print(f"Ошибка при отправке результата брони: {e}")
    elif data == 'not_come':
        markup = types.InlineKeyboardMarkup()
        back_btn = types.InlineKeyboardButton("Назад", callback_data='back_to_menu')
        sure_btn = types.InlineKeyboardButton("Точно не придем", callback_data='sure_not_come')
        markup.add(sure_btn, back_btn)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Вы уверены, что не придете?",
            reply_markup=markup
        )
    # Обработка нажатия на кнопку "Назад"
    elif data == 'back_to_menu':
        send_reservation_buttons(chat_id, message_id)
    # Обработка нажатия на кнопку "Точно не придем"
    elif data == 'sure_not_come':
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Очень жаль. Магии сегодня не будет. 😢"
        )
        try:
            bot.send_message(MAGIC_CHAT_ID, "Сегодня магии не будет. Никто не придет 😢")
            bot.send_message(BARTENDER, "Привет, к сожалению, на этой неделе маги не придут, сегодня без брони")
        except Exception as e:
            print(f"Ошибка при отправке 'не придем' бармену: {e}")