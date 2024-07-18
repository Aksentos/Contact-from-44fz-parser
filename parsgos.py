import requests as req
import pandas as pd
from bs4 import BeautifulSoup as bs
from time import sleep


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/39.0.2171.95 Safari/537.36"
}
# сайт с фильтрами

# указываем список номеров закупок, откуда будем брать контакты
numbers = []


def get_data_to_exel(numbers: list):
    for number in numbers:
        sleep(1)
        URL = f"https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber={number}"
        page = req.get(URL, headers=HEADERS)
        soup = bs(page.text, "lxml")
        containers = soup.find_all("div", class_="container")
        url_data = containers[6]
        info = url_data.find_all("span", class_="section__info")

        # собираем нужные данные в переменные
        customer = info[1].text.replace("\n", "").strip()
        address = info[2].text.replace("\n", "").strip()
        responsible = info[4].text.replace("\n", "").strip()
        mail = info[5].text.replace("\n", "").strip()
        phone = info[6].text.replace("\n", "").strip()
        area = info[8].text.replace("\n", "").strip()

        # записываем все необходимое в таблицу Excel

        # создаем DataFrame из существующего файла, если он существует, иначе создаем новый
        try:
            df = pd.read_excel("contacts.xlsx", engine='openpyxl')
        except FileNotFoundError:
            df = pd.DataFrame()
        
        # добавляем новую строку с данными в DataFrame
        new_data = {"Customer": customer, "Address": address, "Responsible": responsible, "Mail": mail, "Phone": phone, "Area": area, "Number": number}
        df = df._append(new_data, ignore_index=True)

        # записываем DataFrame в файл Excel
        df.to_excel("contacts.xlsx", index=False)

    print("Данные были добавлены в contacts.xlsx")

get_data_to_exel(numbers)
