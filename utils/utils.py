import os
import sys
import csv
from datetime import datetime
from html import unescape
from bs4 import BeautifulSoup


def print_template(message) -> str:
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"\r{current_date}: {message}"
    return message


def check_reports_folder_exist() -> str:
    try:
        root_folder = os.environ.get('PROJECT_ROOT')
        reports_folder = os.path.join(root_folder, "reports")

        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)
        return reports_folder
    except Exception as e:
        print(f"Could not find or create reports folder: {e}")


def write_offers_to_csv(offers):
    reports_folder = check_reports_folder_exist()

    print(print_template("Save to file..."))
    current_datetime = datetime.now()
    current_datetime_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # Генерация имени файла с указанием текущей даты
    csv_file_path = os.path.join(reports_folder, f"offers_{current_datetime_str}.csv")

    # Заголовки столбцов CSV-файла
    fieldnames = [
        "ID", "Available", "URL", "Price", "OldPrice", "CurrencyId", "CategoryId",
        "Picture", "Store", "Delivery", "Pickup", "Name", "Description", "SalesNotes",
        "ManufacturerWarranty", "Vendor", "Params"
    ]

    # Открытие CSV-файла для записи
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')

        # Запись заголовков столбцов
        writer.writeheader()

        # Запись данных объектов Offer в CSV-файл
        for offer in offers:
            description = unescape(offer.description)
            soup = BeautifulSoup(description, "html.parser")
            clean_description = soup.get_text().replace("\n", " ").replace(";", ",")
            writer.writerow({
                "ID": offer.id,
                "Available": offer.available,
                "URL": offer.url,
                "Price": offer.price,
                "OldPrice": offer.oldprice,
                "CurrencyId": offer.currencyId,
                "CategoryId": offer.categoryId,
                "Picture": offer.picture,
                "Store": offer.store,
                "Delivery": offer.delivery,
                "Pickup": offer.pickup,
                "Name": offer.name,
                "Description": clean_description,
                "SalesNotes": offer.sales_notes,
                "ManufacturerWarranty": offer.manufacturer_warranty,
                "Vendor": offer.vendor,
                "Params": ", ".join(offer.params)  # Преобразование списка параметров в строку
            })

    print(print_template(f"CSV file successfully created: {csv_file_path}"))


def update_progress(processed_lines, total_lines, current_line):
    progress = int((processed_lines / total_lines) * 100)
    sys.stdout.write(print_template(f"Progress: {progress}% ({processed_lines}/{total_lines}), current element: {current_line})"))
    sys.stdout.flush()
