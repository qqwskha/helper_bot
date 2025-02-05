# src/main.py
from src.bot import TelegramBot
from src.config import API_TOKEN, PAYMENT_PROVIDER_TOKEN
from src.file_scaner import generate_json, save_to_json
import os
import json

def update_works_config():
    BASE_PATH = "../files"  # Путь к корневой папке с файлами
    OUTPUT_FILE = "works_config.json"  # Путь к выходному JSON-файлу

    # Проверяем, существует ли выходной файл
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    else:
        existing_data = {}

    # Генерируем новые данные
    new_data = generate_json(BASE_PATH)

    # Обновляем существующие данные новыми данными
    for discipline, practical_types in new_data.items():
        if discipline not in existing_data:
            existing_data[discipline] = {}
        for practical_type, variants in practical_types.items():
            if practical_type not in existing_data[discipline]:
                existing_data[discipline][practical_type] = {}
            for variant, data in variants.items():
                existing_data[discipline][practical_type][variant] = data

    # Сохраняем обновленные данные в JSON-файл
    save_to_json(existing_data, OUTPUT_FILE)
    print(f"JSON-файл успешно обновлен: {OUTPUT_FILE}")

if __name__ == "__main__":
    # Обновляем JSON-файл перед запуском бота
    update_works_config()

    # Запускаем бота
    bot = TelegramBot(API_TOKEN, PAYMENT_PROVIDER_TOKEN)
    bot.start()
