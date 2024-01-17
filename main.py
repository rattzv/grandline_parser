import os
import sys
import requests
import xml.etree.ElementTree as ET

from utils.utils import print_template, write_offers_to_csv, update_progress
from model.offer import Offer
from model.category import Category, build_category_hierarchy, find_category_by_id, find_parent_categories


# Устанавливаем переменную окружения "PROJECT_ROOT" в путь до корневой папки проекта
os.environ['PROJECT_ROOT'] = os.path.dirname(os.path.abspath(__file__))


# URL файла YML
url = 'https://grandline.ru/grandline.yml'

try:
    # Загрузка содержимого файла YML
    print(print_template("Loading the contents of a YML ({}) file...".format(url)))
    response = requests.get(url)
    response.raise_for_status()
    print(print_template("Download completed!"))
    yml_content = response.content

    # Парсинг XML
    xml_root = ET.fromstring(yml_content)

    # Обработка данных YML
    offers = []
    for offer_element in xml_root.findall('.//offer'):
        offer = Offer.from_xml_element(offer_element)
        offers.append(offer)

    categories = []
    for category_element in xml_root.findall('.//category'):
        category = Category.from_xml_element(category_element)
        categories.append(category)

    # Построение иерархии категорий
    category_hierarchy = build_category_hierarchy(categories)

    processed_lines = 0
    total_lines = len(offers)

    # Вывод информации о предложениях
    for offer in offers:
        try:
            selected_category = find_category_by_id(offer.categoryId, category_hierarchy)
            if selected_category:
                hierarchy_category = find_parent_categories(category_hierarchy, selected_category)
                hierarchy_category.reverse()
                hierarchy_category.append(selected_category.name)
                offer.categoryId = ", ".join(hierarchy_category)
            else:
                offer.categoryId = None
            processed_lines += 1
            update_progress(processed_lines, total_lines,  offer.name)
        except Exception as e:
            print(f"Ошибка при обработке offer: {e}")

    sys.stdout.write('\n')

    write_offers_to_csv(offers)

except Exception as e:
    print(f"Ошибка при выполнении программы: {e}")
