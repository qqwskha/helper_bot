# src/titles_mapping.py
from src.config import PRACTICAL_WORKS

def generate_titles_mapping():
    titles_mapping = {}
    for discipline, practical_types in PRACTICAL_WORKS.items():
        # Добавляем дисциплины
        titles_mapping[discipline] = discipline.replace("_", " ").title()
        for practical_type, variants in practical_types.items():
            # Добавляем типы работ
            titles_mapping[practical_type] = practical_type.replace("_", " ").title()
            for variant in variants.keys():
                # Добавляем варианты
                titles_mapping[variant] = variant.replace("_", " ").title()
    return titles_mapping

TITLES_MAPPING = generate_titles_mapping()
TITLES_MAPPING.update({
    "ITPD": "Информационные технологии в профессиональной деятельности",
    "na4ert": "Начертательная геометрия",
    "kontrol_kart_Suhart": "Контрольные карты Шухарта",
    "opis_stat": "Описательная статистика",
    "prov_stat_gip": "Проверка статистических гипотез",
    "regress_analiz": "Регрессивный анализ данных",
    "veroyat_raspr": "Вероятностные распределения",
    "1v": "1 вариант",
    "2v": "2 вариант",
    "kart_chisl_nesoot_ed": "Карты числа несоответствий единицам продукции",
    "kart_doli_nesoot": "Карты доли несоотвествий",
})
REVERSED_TITLES_MAPPING = {value: key for key, value in TITLES_MAPPING.items()}