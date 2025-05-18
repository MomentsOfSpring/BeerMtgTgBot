from polls import create_poll, unpin_polls_and_say_hi, generate_report
from config import BOSS
from common import send_reservation_buttons
from datetime import datetime
import time
import logging
from bot_instance import bot


logger = logging.getLogger(__name__)


# Расписание триггеров
# 1. В понедельник в 10:00 создаём опрос
# 2. В среду в 18:00 отправляем результаты опроса и кнопки бронирования

def should_run_task(weekday, hour, minute):
    """Проверяет, нужно ли запустить задачу в текущий момент"""
    now = datetime.now()
    return (now.weekday() == weekday and 
            now.hour == hour and 
            now.minute == minute)


def run_monday_task():
    """Выполняет задачи понедельника"""
    try:
        logger.info("Запуск задачи понедельника: создание опроса")
        create_poll(bot)
    except Exception as e:
        logger.error(f"Ошибка при создании опроса: {e}", exc_info=True)


def run_wednesday_task():
    """Выполняет задачи среды"""
    try:
        logger.info("Запуск задачи среды: обработка результатов опроса")
        unpin_polls_and_say_hi(bot)
        report, tables = generate_report(bot)
        
        if report and tables:
            try:
                user = bot.get_chat_member(BOSS, BOSS).user
                boss_id = user.id
                bot.send_message(boss_id, report)
                send_reservation_buttons(bot, boss_id)
            except Exception as e:
                logger.error(f"Ошибка при отправке результатов боссу: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Ошибка при обработке результатов опроса: {e}", exc_info=True)


def scheduler():
    """Основной планировщик задач"""
    logger.info("Запуск планировщика задач")
    last_monday_run = None
    last_wednesday_run = None
    
    while True:
        try:
            now = datetime.now()
            
            # Проверяем задачу понедельника
            if should_run_task(0, 10, 0):
                if last_monday_run is None or (now - last_monday_run).total_seconds() > 60:
                    run_monday_task()
                    last_monday_run = now
            
            # Проверяем задачу среды
            if should_run_task(2, 18, 0):
                if last_wednesday_run is None or (now - last_wednesday_run).total_seconds() > 60:
                    run_wednesday_task()
                    last_wednesday_run = now
            
            # Сбрасываем флаги выполнения в начале нового дня
            if now.hour == 0 and now.minute == 0:
                last_monday_run = None
                last_wednesday_run = None
            
            time.sleep(10)
            
        except Exception as e:
            logger.error(f"Критическая ошибка в планировщике: {e}", exc_info=True)
            time.sleep(60)  # Увеличенная пауза при ошибке