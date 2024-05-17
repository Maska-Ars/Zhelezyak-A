import requests as rq  # Для парсинга страниц
import pandas as pd  # Для записи в виде таблицы в csv
from bs4 import BeautifulSoup as bs  # Для скрапинга страниц

from os import getcwd  # Для записи csv в отдельную папку

from threading import Thread  # Для потоков
from time import time, sleep  # Для потоков и определения времени работы


class Parser:

    def __init__(self):

        # Ссылка на основную страницу комплектующих
        self.link_original = 'https://n-katalog.ru/category/komplektuyushhie'
        # Черный список ненужных характеристик
        self.stats_black_list = [
            'Официальный сайт'
        ]
        # Черный список ненужных комплектующих
        self.components_black_list = [
            '/category/opticheskie-privody/list',
            '/category/prochie-komplektuyushhie/list',
            '/category/termopasty-i-termoprokladki/list',
            '/category/karmany-dlya-nakopitelej/list',
            '/category/korpusa/list',
            '/category/sistemy-oxlazhdeniya/list',
        ]

    # Функция извлечения всех ссылок на отдельные комплектующие
    def parse_links_to_components(self) -> list:
        response = rq.get(self.link_original, headers={'user-agent': 'bih'}).text
        soup = bs(response, 'html.parser')
        link_komponent_short = soup.find_all('a', style='font-size:16px;')

        for i in range(0, len(link_komponent_short)):
            link_komponent_short[i] = link_komponent_short[i]['href']

        return link_komponent_short

    # Функция парсинга всех деталей 1-го типа
    def parse_component(self, link_component: str) -> None:
        space = ' '
        print(f'start: {link_component[10:-5]}{space*(30-len(link_component[10:-5]))} | time = {time()} s')
        begin = time()

        sleep(0.000005)

        dataframe = pd.DataFrame()
        link_page = 'https://n-katalog.ru' + link_component

        response = rq.get(self.link_original, headers={'user-agent': 'bih'}).text
        soup = bs(response, 'html.parser')

        j = 0

        # Переход на следующий список
        while soup.find('div', class_="msg-search") is None:

            names_soup = soup.find_all('a', class_='model-short-title no-u')

            # Перебор всех ссылок на детали
            for namesoup in names_soup:

                name = namesoup.get_text().strip()

                data = {}

                linkname = "https://n-katalog.ru" + namesoup['href']

                response = rq.get(linkname, headers={'user-agent': 'bih'}).text
                soup = bs(response, 'html.parser')

                keys = soup.find_all('td', width='49%')
                values = soup.find_all('td', width='51%')

                for i in range(len(keys)):
                    if not keys[i].text.strip() in self.stats_black_list:
                        if values[i].text == ' ':
                            data[keys[i].text.strip()] = 'Есть'
                        else:
                            data[keys[i].text.strip()] = values[i].text.strip()

                # Сбор таблицы
                l = pd.DataFrame(data, index=[name])

                # Объединение полученной таблицы с конечной
                dataframe = pd.concat([l, dataframe])

            j += 1
            link = link_page + '/page-' + str(j)

            # Переход на следующую страницу
            response = rq.get(link, headers={'user-agent': 'bih'}).text
            soup = bs(response, 'html.parser')

        # Запись в csv
        file = getcwd() + '\\комплектующие\\' + link_component[10:-5] + '.csv'
        dataframe.to_csv(file, index=True, sep='|')

        print(f'end: {link_component[10:-5]}{space*(32-len(link_component[10:-5]))} | time = {time()} s')
        print(f'time_work = {(time()-begin) / 60} minutes')

        return None

    # Функция скрапинга производителей 1-го компонента
    def parse_company(self, link_component: str) -> None:

        link_page = 'https://n-katalog.ru' + link_component

        response = rq.get(link_page, headers={'user-agent': 'bih'}).text
        soup = bs(response, 'html.parser')

        file = open(getcwd() + '\\производители\\' + link_component[10:-5] + '.txt', 'w')
        for i in soup.find_all('label', class_='brand-best'):
            file.write(i.text + '\n')
        for i in soup.find_all('label', class_='model-not-best'):
            file.write(i.text + '\n')

        file.close()
        return None

    # Функция скрапинга всех производителей
    def parse_all_company(self):

        # Получение ссылок на страницы всех комплектующих
        link_komponent_short = self.parse_links_to_components()

        theards = []

        # Перебор ссылок на страницы к каждому типу комплектующей
        # Создание отдельных потоков для каждого вызова функции
        for link_component in link_komponent_short:
            if link_component not in self.components_black_list:
                theards.append(Thread(target=self.parse_company,
                                      args=(link_component,)))

        # Запуск всех потоков
        for theard in theards:
            theard.start()

    # Функция парсера для сайта n-katalog
    def parse_all_components(self) -> None:

        # Получение ссылок на страницы всех комплектующих
        link_component_short = self.parse_links_to_components()
        theards = []

        # Перебор ссылок на страницы к каждому типу комплектующей
        # Создание отдельных потоков для каждого вызова функции
        for link_component in link_component_short:
            if link_component not in self.components_black_list:
                theards.append(Thread(target=self.parse_component,
                                      args=(link_component,)))

        # Запуск всех потоков
        for theard in theards:
            theard.start()

        return None
