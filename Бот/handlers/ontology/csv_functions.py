from os import listdir
import csv


RUSSION_NAMES = {
    'bloki-pitaniya': 'блоки_питания',
    'materinskie-platy': 'материнские_платы',
    'operativnaya-pamyat': 'оперативная_память',
    'pci-kontrollery': 'pci_контроллеры',
    'processory': 'процессоры',
    'ssd-nakopiteli': 'ssd_накопители',
    'videokarty': 'видеокарты',
    'zhestkie-diski': 'жесткие_диски',
    'zvukovye-karty': 'звуковые_карты'
}


# Функция чтения всех производителей записанных в txt в папке производители
# Возвращает словарь списков строк
def read_all_company() -> dict:
    path = 'handlers/parser/производители'
    files = listdir(path)

    l = {}
    for file in files:
        l.setdefault(RUSSION_NAMES[file[:-4]], [])

        with open(f'{path}\{file}', 'r', encoding='utf-8') as f:
            for line in f:
                l[RUSSION_NAMES[file[:-4]]].append(line[:-1])

    return l


# Функция чтения всех словарей записанных в csv в папке комплектующие
# Возвращает словарь списков словарей, где ключ - название файла без расширения, значение список всех предметов из файла
def read_csv_all() -> dict:
    path = 'handlers/parser/комплектующие'
    files = listdir(path)

    companies = read_all_company()

    l = {}
    for file in files:
        l.setdefault(RUSSION_NAMES[file[:-4]], [])

        with open(f'{path}\{file}', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            for row in reader:
                d = {}
                keys = list(row.keys())

                name = row[''].lower()

                company = 'неизвестно'
                for comp in companies[RUSSION_NAMES[file[:-4]]]:
                    if len(comp) < len(name):
                        if name[0:len(comp)].lower() == comp.lower():
                            company = comp.lower()
                            break

                d.setdefault('название', name)

                d.setdefault('производитель', company)

                for j in range(1, len(keys)):
                    d.setdefault(keys[j].lower(), row[keys[j]].lower())

                l[RUSSION_NAMES[file[:-4]]].append(d)

    return l
