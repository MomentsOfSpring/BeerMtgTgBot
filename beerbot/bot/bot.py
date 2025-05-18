import threading
import signal
import sys
import logging

from bot_instance import bot
from bot_scheduler import scheduler
from handlers import register_handlers

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def signal_handler(sig, frame):
    logger.info('Завершение работы бота...')
    bot.stop_polling()
    sys.exit(0)


# Значит жить можно.
if __name__ == '__main__':
    # Регистрируем обработчики команд
    register_handlers()
    
    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        logger.info('Запуск планировщика...')
        # Запускаем планировщик в отдельном потоке
        scheduler_thread = threading.Thread(target=scheduler, daemon=True)
        scheduler_thread.start()
        
        logger.info('Бот запущен...')
        bot.polling(none_stop=True, interval=1, timeout=60)
    except Exception as e:
        logger.error(f'Ошибка при запуске бота: {e}', exc_info=True)
        sys.exit(1)