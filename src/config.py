#src/config.py
from dotenv import load_dotenv
import os
import json

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значений переменных
API_TOKEN = os.getenv("API_TOKEN")
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
FEEDBACK_CHANNEL_ID = int(os.getenv("FEEDBACK_CHANNEL_ID"))

# Структура данных для дисциплин, вариантов и номеров практических работ
current_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к директории src
works_config_path = os.path.join(current_dir, "works_config.json")  # Полный путь к файлу

with open(works_config_path, "r", encoding="utf-8") as file:
    PRACTICAL_WORKS = json.load(file)
