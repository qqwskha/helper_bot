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

    # Проверяем существование директорий и файлов в existing_data
    disciplines_to_remove = []
    for discipline, practical_types in existing_data.items():
        discipline_path = os.path.join(BASE_PATH, discipline)
        if not os.path.exists(discipline_path):
            disciplines_to_remove.append(discipline)
            continue

        practical_types_to_remove = []
        for practical_type, variants in practical_types.items():
            practical_type_path = os.path.join(discipline_path, practical_type)
            if not os.path.exists(practical_type_path):
                practical_types_to_remove.append(practical_type)
                continue

            variants_to_remove = []
            for variant, data in variants.items():
                variant_path = os.path.join(practical_type_path, variant)
                if not os.path.exists(variant_path):
                    variants_to_remove.append(variant)
                    continue

                # Проверяем существование файлов внутри варианта
                files_exist = all(os.path.exists(file_path) for file_path in data.get("files", []))
                image_exists = data.get("image") is None or os.path.exists(data["image"])
                if not (files_exist and image_exists):
                    variants_to_remove.append(variant)

            # Удаляем варианты, которые больше не существуют
            for variant in variants_to_remove:
                del existing_data[discipline][practical_type][variant]

            # Удаляем практический тип, если он стал пустым
            if not existing_data[discipline][practical_type]:
                practical_types_to_remove.append(practical_type)

        # Удаляем практические типы, которые больше не существуют
        for practical_type in practical_types_to_remove:
            del existing_data[discipline][practical_type]

        # Удаляем дисциплину, если она стала пустой
        if not existing_data[discipline]:
            disciplines_to_remove.append(discipline)

    # Удаляем дисциплины, которые больше не существуют
    for discipline in disciplines_to_remove:
        del existing_data[discipline]

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
    BASE_PATH = "../files"  # Путь к корневой папке с файлами
    OUTPUT_FILE = "works_config.json"  # Путь к выходному JSON-файлу
    # Генерация JSON
    data = generate_json(BASE_PATH)
    # Сохранение JSON
    save_to_json(data, OUTPUT_FILE)
    print(f"JSON-файл успешно создан: {OUTPUT_FILE}")