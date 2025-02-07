# src/main.py
from src.bot import TelegramBot
from src.config import API_TOKEN, PAYMENT_PROVIDER_TOKEN
from src.file_scaner import update_works_config

if __name__ == "__main__":
    # Обновление JSON-файла перед запуском бота
    update_works_config()

    # Запуск бота
    bot = TelegramBot(API_TOKEN, PAYMENT_PROVIDER_TOKEN)
    bot.start()