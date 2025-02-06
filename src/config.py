# src/config.py
from dotenv import load_dotenv
import os
import json
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("config_errors.log"),  # Логи записываются в файл
        logging.StreamHandler(),  # Логи выводятся в консоль
    ],
)

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значений переменных
API_TOKEN = os.getenv("API_TOKEN")
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
FEEDBACK_CHANNEL_ID = int(os.getenv("FEEDBACK_CHANNEL_ID"))

# Путь к файлу works_config.json
current_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к директории src
works_config_path = os.path.join(current_dir, "works_config.json")  # Полный путь к файлу

# Структура данных по умолчанию
DEFAULT_PRACTICAL_WORKS = {
    "komp_grafika": {
        "pr_rab": {
            "pr1": {
                "image": "../files/komp_grafika/pr_rab/pr1/preview.jpg",
                "files": [
                    "../files/komp_grafika/pr_rab/pr1/Построение видов.cdw",
                    "../files/komp_grafika/pr_rab/pr1/preview.jpg",
                ],
                "price": 500,
            }
        }
    }
}

def validate_data(data):
    """
    Валидация структуры данных.
    """
    if not isinstance(data, dict):
        raise ValueError("Данные должны быть словарем.")
    for discipline, practical_types in data.items():
        if not isinstance(practical_types, dict):
            raise ValueError(f"Дисциплина '{discipline}' должна содержать словарь типов работ.")
        for practical_type, variants in practical_types.items():
            if not isinstance(variants, dict):
                raise ValueError(f"Тип работы '{practical_type}' должен содержать словарь вариантов.")
            for variant, details in variants.items():
                if not isinstance(details, dict) or "image" not in details or "files" not in details or "price" not in details:
                    raise ValueError(f"Вариант '{variant}' должен содержать ключи 'image', 'files' и 'price'.")

def create_backup(file_path):
    """
    Создание резервной копии файла.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    try:
        os.rename(file_path, backup_path)
        logging.info(f"Создана резервная копия файла: {backup_path}")
    except Exception as e:
        logging.error(f"Ошибка при создании резервной копии: {e}")

try:
    # Проверяем, существует ли файл works_config.json
    if not os.path.exists(works_config_path):
        logging.warning(f"Файл {works_config_path} не найден. Создаем новый файл с данными по умолчанию.")
        with open(works_config_path, "w", encoding="utf-8") as file:
            json.dump(DEFAULT_PRACTICAL_WORKS, file, ensure_ascii=False, indent=4)
        PRACTICAL_WORKS = DEFAULT_PRACTICAL_WORKS
    else:
        # Загружаем данные из файла
        with open(works_config_path, "r", encoding="utf-8") as file:
            PRACTICAL_WORKS = json.load(file)
            validate_data(PRACTICAL_WORKS)  # Валидация данных
except json.JSONDecodeError as e:
    logging.error(f"Ошибка декодирования JSON в файле {works_config_path}: {e}")
    raise ValueError(f"Ошибка декодирования JSON в файле {works_config_path}: {e}")
except FileNotFoundError as e:
    logging.error(f"Ошибка загрузки конфигурации: {e}")
    raise FileNotFoundError(f"Ошибка загрузки конфигурации: {e}")
except Exception as e:
    logging.error(f"Произошла ошибка при загрузке файла {works_config_path}: {e}")
    raise RuntimeError(f"Произошла ошибка при загрузке файла {works_config_path}: {e}")

def add_new_discipline(discipline_name, practical_types):
    """
    Добавление новой дисциплины в файл works_config.json.
    """
    global PRACTICAL_WORKS
    if discipline_name in PRACTICAL_WORKS:
        logging.warning(f"Дисциплина '{discipline_name}' уже существует.")
        return
    PRACTICAL_WORKS[discipline_name] = practical_types
    try:
        create_backup(works_config_path)  # Создаем резервную копию
        with open(works_config_path, "w", encoding="utf-8") as file:
            json.dump(PRACTICAL_WORKS, file, ensure_ascii=False, indent=4)
        logging.info(f"Добавлена новая дисциплина: {discipline_name}")
    except Exception as e:
        logging.error(f"Ошибка при добавлении новой дисциплины: {e}")
        raise RuntimeError(f"Ошибка при добавлении новой дисциплины: {e}")