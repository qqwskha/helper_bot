# src/config.py
API_TOKEN = '7905777515:AAEteXO0eCzYSjwFhDRymP1ZfZ2stn59Lw8'
PAYMENT_PROVIDER_TOKEN = '381764678:TEST:110185'
ADMIN_ID = 344101641
FEEDBACK_CHANNEL_ID = -1002344913874

# Структура данных для дисциплин, вариантов и номеров практических работ
import json

with open("works_config.json", "r", encoding="utf-8") as file:
    PRACTICAL_WORKS = json.load(file)
