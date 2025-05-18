from telebot import types
import os
import logging

from bot_instance import bot
from common import send_reservation_buttons
from config import INVITE, BOSS, PHOTOS, RULES_FILE
from polls import create_poll, unpin_polls_and_say_hi, generate_report

# Логирование
logger = logging.getLogger(__name__)


# Обработка команды /invite
def invite_link(message):
    bot.send_message(message.chat.id, f'Ссылка приглашение:\n {INVITE}')

# Обработка команды /rules
def beer_rules(message):
    media = []
    logger.info(f"Текущая директория: {os.getcwd()}")
    logger.info(f"Пути к фотографиям: {PHOTOS}")
    
    # Обработка фотографий
    for path in PHOTOS:
        logger.info(f"Пытаемся открыть файл: {path}")
        if not os.path.exists(path):
            logger.error(f"Файл не существует: {path}")
            continue
        try:
            with open(path, 'rb') as photos:
                media.append(types.InputMediaPhoto(photos.read()))
        except Exception as e:
            logger.error(f"Ошибка при открытии файла {path}: {e}")
            continue
           
    # Обработка медиагруппы
    if media:
        bot.send_message(message.chat.id, "Ща всё узнаешь.")
        try:
            bot.send_media_group(message.chat.id, media)
        except Exception as e:
            logger.error(f"Ошибка при отправке медиагруппы: {e}")
            bot.send_message(message.chat.id, "Произошла ошибка при отправке изображений")
    
    # Обработка текста правил
    try:
        with open(RULES_FILE, 'r', encoding='utf-8') as t:
            rules_text = t.read()
        bot.send_message(message.chat.id, rules_text)
    except Exception as e:
        logger.error(f"Ошибка при чтении файла правил: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при чтении правил")


# Обработка нового участника
def greet_new_members(message):
    chat_id = message.chat.id
    for new_user in message.new_chat_members:
        user_id = new_user.id
        try:
            bot.restrict_chat_member(
                chat_id,
                user_id,
                permissions=types.ChatPermissions(can_send_messages=False)
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("Да", callback_data=f"beer_yes_{user_id}"),
                types.InlineKeyboardButton("Нет", callback_data=f"beer_no_{user_id}")
            )
            bot.send_message(
                chat_id,
                f"Привет, {new_user.first_name}! Ты любишь пиво?",
                reply_markup=markup
            )
        except Exception as e:
            print(f"Ошибка при ограничении прав нового участника {user_id}: {e}")

# Обработка команды /help
def help_command(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em>information</em>:', parse_mode='html')

# Обработка команды /info
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Ну привет, {message.from_user.first_name} {message.from_user.last_name or ""}..')
    elif "cedh" in message.text.lower() or "цедх" in message.text.lower() or "цдх" in message.text.lower():
        bot.reply_to(message, f"Ни слова про CEDH в этом чате!")
    elif "стас" in message.text.lower():
        bot.reply_to(message, f"Блинб, Стас.... 🤤 ")
    elif "миша" in message.text.lower():
        bot.reply_to(message, f'Блинб, Миша.... 🤤 ')
    elif "пацаны" in message.text.lower():
        bot.reply_to(message, f'Ты где здесь пацанов увидел, ПАЦАН?')
    elif (("бот крутой" in message.text.lower()
          or "крутой бот" in message.text.lower()
          or "классный бот" in message.text.lower()
          or "бот классный" in message.text.lower())
          or "хороший бот" in message.text.lower()
          or "бот хороший" in message.text.lower()):
        bot.reply_to(message, "Спасибо, бро! Обнял, поцеловал (не по-гейски)!")
    elif "говно" in message.text.lower():
        bot.reply_to(message, "Сам говно!")

# Обработка команды /pollnow
def manual_poll(message):
    create_poll(bot)
    bot.send_message(message.chat.id, "Опрос запущен вручную.")


# Обработка команды /gameon
def manual_gameon(message):
    unpin_polls_and_say_hi(bot)
    bot.send_message(message.chat.id, "Оповещение запущено вручную.")


# Обработка команды /pollres
def manual_poll_results(message):
    report, tables = generate_report(bot)
    if report is None:
        bot.send_message(BOSS, "Нет данных для подсчета результатов.")
        return
    try:
        bot.send_message(BOSS, report)
        send_reservation_buttons(BOSS)
        bot.send_message(message.chat.id, "Голосование завершено вручную.\nВсем проголосовавшим летит плотная респектуля.\nРезультаты опроса отправлены Боссу.")
    except Exception as e:
        print(f"Ошибка при отправке результатов Боссу: {e}")
        bot.send_message(message.chat.id, "Не удалось отправить сообщение Боссу.")