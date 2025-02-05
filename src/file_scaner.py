# src/file_scaner.py
import json
import os

def generate_json(base_path):
    """
    Сканирует папки и генерирует JSON-структуру данных.
    :param base_path: Путь к корневой папке с файлами.
    :return: Словарь с данными для JSON.
    """
    practical_works = {}
    # Проходим по всем дисциплинам
    for discipline in os.listdir(base_path):
        discipline_path = os.path.join(base_path, discipline)
        if os.path.isdir(discipline_path):
            practical_works[discipline] = {}
            # Проходим по всем типам работ
            for practical_type in os.listdir(discipline_path):
                practical_type_path = os.path.join(discipline_path, practical_type)
                if os.path.isdir(practical_type_path):
                    practical_works[discipline][practical_type] = {}
                    # Проходим по всем вариантам
                    for variant in os.listdir(practical_type_path):
                        variant_path = os.path.join(practical_type_path, variant)
                        if os.path.isdir(variant_path):
                            # Собираем файлы внутри варианта
                            files = [os.path.join(variant_path, f) for f in os.listdir(variant_path) if os.path.isfile(os.path.join(variant_path, f))]
                            # Предполагаем, что preview.jpg существует
                            image_path = os.path.join(variant_path, "preview.jpg")
                            if not os.path.exists(image_path):
                                image_path = None  # Если preview.jpg отсутствует
                            # Определяем цену (можно хранить в отдельном файле или использовать фиксированное значение)
                            price = 500  # Пример фиксированной цены
                            practical_works[discipline][practical_type][variant] = {
                                "image": image_path,
                                "files": files,
                                "price": price,
                            }
    return practical_works

def save_to_json(data, output_file):
    """
    Сохраняет данные в JSON-файл.
    :param data: Словарь с данными.
    :param output_file: Путь к выходному JSON-файлу.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    BASE_PATH = "../files"  # Путь к корневой папке с файлами
    OUTPUT_FILE = "works_config.json"  # Путь к выходному JSON-файлу
    # Генерация JSON
    data = generate_json(BASE_PATH)
    # Сохранение JSON
    save_to_json(data, OUTPUT_FILE)
    print(f"JSON-файл успешно создан: {OUTPUT_FILE}")