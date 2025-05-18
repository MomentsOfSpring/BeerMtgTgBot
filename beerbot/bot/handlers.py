from bot_instance import bot
from commands import (
    invite_link, beer_rules, greet_new_members, help_command,
    info, manual_poll, manual_gameon, manual_poll_results
)
from callbacks import callback_message
from polls import handle_poll_answer

def register_handlers():
    # Регистрация обработчиков команд
    # Обработчик команды /start
    bot.message_handler(commands=['start'])(help_command)
    # Обработчик команды /help
    bot.message_handler(commands=['help'])(help_command)
    # Обработчик команды /invite
    bot.message_handler(commands=['invite'])(invite_link)
    # Обработчик команды /rules
    bot.message_handler(commands=['rules'])(beer_rules)
    # Обработчик команды /pollnow
    bot.message_handler(commands=['pollnow'])(manual_poll)
    # Обработчик команды /gameon
    bot.message_handler(commands=['gameon'])(manual_gameon)
    # Обработчик команды /pollres
    bot.message_handler(commands=['pollres'])(manual_poll_results)
    
    # Обработчик новых участников
    bot.message_handler(content_types=['new_chat_members'])(greet_new_members)
    
    # Обработчик текстовых сообщений
    bot.message_handler(content_types=['text'])(info)
    
    # Обработчик callback-запросов
    bot.callback_query_handler(func=lambda call: True)(callback_message)
    
    # Обработчик ответов на опрос
    bot.poll_answer_handler(func=lambda poll_answer: True)(handle_poll_answer) 