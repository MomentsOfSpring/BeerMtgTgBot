import os
import logging

logger = logging.getLogger(__name__)

def get_project_root():
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    logger.info(f"Путь к корню проекта: {project_root}")
    return project_root

# MAIN INFO:
# TOKEN = "YOUR_BOT_TOKEN" #(from @botfather)
MAGIC_CHAT_ID = 1 #YOUR_GROUP_CHAT_ID

# ADDITIONAL INFO
# INVITE = "YOUR_INVITE_LINK"

# FILES:
RULES_FILE = os.path.join(get_project_root(), 'beerbot', 'text', 'rules.txt')
PHOTOS = [
    os.path.join(get_project_root(), 'beerbot', 'img', 'brackets.jpeg'),
    os.path.join(get_project_root(), 'beerbot', 'img', 'changers.jpeg')
]

# Проверяем существование файлов при импорте
for photo in PHOTOS:
    if not os.path.exists(photo):
        logger.error(f"Файл не существует: {photo}")
    else:
        logger.info(f"Файл существует: {photo}")

if not os.path.exists(RULES_FILE):
    logger.error(f"Файл правил не существует: {RULES_FILE}")
else:
    logger.info(f"Файл правил существует: {RULES_FILE}")

# PERSONS:
VLADA = 111111111
STAS = 222222222
BOSS = 123456789
BARTENDER = 987654321

# Специальная константа для Влады и Стаса
VLADOSTAS = 2
