from datetime import datetime, timedelta
import json
import os
from config import MAGIC_CHAT_ID, VLADA, STAS
from common import VLADOSTAS
from vlada_utils import ask_vlada_for_stas
import logging

logger = logging.getLogger(__name__)

# Получаем путь к директории, где находится файл polls.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
VOTES_FILE = os.path.join(CURRENT_DIR, 'votes.json')

def load_votes():
    """Загружает голоса из файла"""
    if os.path.exists(VOTES_FILE):
        try:
            with open(VOTES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Ошибка при загрузке голосов: {e}")
    return {}

def save_votes(votes):
    """Сохраняет голоса в файл"""
    try:
        with open(VOTES_FILE, 'w') as f:
            json.dump(votes, f)
    except Exception as e:
        logger.error(f"Ошибка при сохранении голосов: {e}")

# Получение даты следующей среды
def get_next_wednesday():
    today = datetime.now()
    days_ahead = (2 - today.weekday()) % 7  # 2 = среда
    if days_ahead == 0:
        days_ahead = 7
    return today + timedelta(days=days_ahead)


# Создание опроса
def create_poll(bot):
    wednesday_date = get_next_wednesday().strftime('%d.%m.%Y')
    poll_message = bot.send_poll(
        MAGIC_CHAT_ID,
        question=f"Магия, среда, {wednesday_date}. Придешь?",
        options=["Да", "Нет"],
        is_anonymous=False,
        allows_multiple_answers=False
    )
    try:
        bot.pin_chat_message(MAGIC_CHAT_ID, poll_message.message_id, disable_notification=True)
    except Exception as e:
        logger.error(f"Не удалось закрепить сообщение: {e}")


# Открепление опроса и отправка хорошего настроения
def unpin_polls_and_say_hi(bot):
    try:
        chat_pins = bot.get_chat(MAGIC_CHAT_ID).pinned_message
        if chat_pins:
            bot.unpin_all_chat_messages(MAGIC_CHAT_ID)
    except Exception as e:
        logger.error(f"Ошибка при откреплении: {e}")
    bot.send_message(MAGIC_CHAT_ID, "Удачной игры, господа маги 🧙‍♂️")


# Поиск активного опроса
def find_active_poll(bot):
    try:
        chat = bot.get_chat(MAGIC_CHAT_ID)
        pinned_msg = chat.pinned_message
        if pinned_msg and pinned_msg.poll:
            return pinned_msg
    except Exception as e:
        logger.error(f"Ошибка при поиске закрепленного опроса: {e}")
    return None


# Подсчет голосов за "Да"
def count_yes_votes(bot):
    poll_message = find_active_poll(bot)
    if not poll_message:
        return None, None
    poll = poll_message.poll
    return poll_message.message_id, poll.options

# Обработка ответов на опрос
def handle_poll_answer(poll_answer):
    user_id = poll_answer.user.id
    option_index = poll_answer.option_ids[0]
    vote = "Да" if option_index == 0 else "Нет"
    
    votes = load_votes()
    votes[str(user_id)] = vote
    save_votes(votes)
    
    if user_id == VLADA and vote == "Да":
        ask_vlada_for_stas()


# Генерация отчета о результатах голосования
def generate_report(bot):
    votes = load_votes()
    yes_users_ids = [int(uid) for uid, v in votes.items() if v == "Да"]
    if not yes_users_ids:
        report_text = "Никто не проголосовал 'ДА'."
        # Очищаем голоса даже если никто не проголосовал
        save_votes({})
        return report_text, 0

    # Получение списка имен магов энтузиастов и романтиков
    yes_users_names = []
    # Проверка, придут ли Влада и Стасы
    vlada_yes = VLADA in yes_users_ids
    stas_yes = STAS in yes_users_ids
    for uid in yes_users_ids:
        try:
            user = bot.get_chat_member(MAGIC_CHAT_ID, uid).user
            full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
            yes_users_names.append(full_name if full_name else str(uid))
        except Exception:
            yes_users_names.append(str(uid))

    # Подсчет количества игроков
    yes_count = len(yes_users_ids)
    if vlada_yes and stas_yes:
        players = yes_count - 2 + VLADOSTAS
    elif vlada_yes:
        players = yes_count - 1 + VLADOSTAS
    else:
        players = yes_count

    # Подсчет количества столов путем сложных математических вычислений и статистических расчетов
    tables = -(-players // 4)
    report_text = (
        f"Результаты голосования:\n\n"
        f"Придут ({players} игроков):\n"
        + "\n".join(f"- {name}" for name in yes_users_names) +
        f"\n\nКоличество столов: {tables}"
    )
    
    # Очищаем голоса после генерации отчёта
    save_votes({})
    
    return report_text, tables