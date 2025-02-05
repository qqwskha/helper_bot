from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значений переменных
API_TOKEN = os.getenv("API_TOKEN")
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
FEEDBACK_CHANNEL_ID = int(os.getenv("FEEDBACK_CHANNEL_ID"))

# Структура данных для дисциплин, вариантов и номеров практических работ
import json

with open("works_config.json", "r", encoding="utf-8") as file:
    PRACTICAL_WORKS = json.load(file)
