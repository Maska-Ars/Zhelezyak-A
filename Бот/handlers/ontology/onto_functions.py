from owlready2 import *
from os import remove
from handlers.ontology.NLTK_fucntions import delete_prepositions, reduction_to_roots, generate_combinations
from handlers.ontology.csv_functions import read_csv_all
from fuzzywuzzy import process


class Onto:
    # инициализация свойств и супер класса
    def __init__(self):

        onto_path.append("/path/to/owlready/onto/")
        self.onto = get_ontology("file://handlers/ontology/template.owl").load()
        cl_list = []  # переменная для показа классов, если в онтологии что-то есть уже
        for i in self.onto.classes():
            cl_list.append(str(i)[str(i).find('.') + 1:])

        if 'SuperClass' not in cl_list:

            with self.onto:
                class SuperClass(Thing):  # класс в котором лежат все классы
                    class useless_(Thing):
                        pass

                class Has_value(ObjectProperty):
                    rdf_domain = [self.onto.individuals()]
                    rdf_range = [self.onto.individuals()]
                    inverse_property = None

                class Value_of(ObjectProperty):
                    rdf_domain = [self.onto.individuals()]
                    rdf_range = [self.onto.individuals()]
                    inverse_property = Has_value

                Has_value.inverse_property = Value_of

                class One_of(ObjectProperty):
                    rdf_domain = [self.onto.individuals()]
                    rdf_range = [self.onto.individuals()]

                class Mis_a(ObjectProperty):
                    rdf_domain = [self.onto.individuals()]
                    rdf_range = [self.onto.individuals()]
                    inverse_property = One_of

                One_of.inverse_property = Mis_a

                class Has_stat(ObjectProperty):
                    rdf_domain = [self.onto.individuals()]
                    rdf_range = [self.onto.individuals()]
                    inverse_property = None

                class Stat_of(ObjectProperty):
                    rdf_domain = [self.onto.individuals()]
                    rdf_range = [self.onto.individuals()]
                    inverse_property = Has_stat

                Has_stat.inverse_property = Stat_of
        else:
            print('onto classes: ', cl_list)

        self.onto.load()

    # FUNTCTIONS TO CREATING

    # функция добавления экземпляра name в класс class_name, возвращает объект онтологии
    def add_entity(self, name, class_name):
        name = str(name)
        name = name.replace(' ', '_')
        new_class = types.new_class(class_name, (self.onto.SuperClass,))

        with self.onto:
            new_entity = new_class(name)

        return new_entity

    # функция загрузки строки из ксв - строка из csv в виде словаря(ent) в класс e_class
    def load_row_from_csv(self, ent: dict, e_class: str):
        # вычленения имени комплектующей из словаря

        keys = list(ent.keys())
        if '"' in ent['название']:
            ent['название'] = ent['название'].replace('"', 'duim')

        if '"' in ent['название']:
            ent['название'] = ent['название'].replace('%', 'proc')

        cur_unit = self.add_entity(ent['название'], e_class)

        keys = keys[1:]

        # добавления пар ключ-значение
        for k in keys:
            v = ent[k]
            if '"' in k:
                k = k.replace('"', 'duim')
            if "%" in k:
                k = k.replace('%', 'proc')
            if '"' in v:
                v = v.replace('"', 'duim')
            if "%" in v:
                v = v.replace('%', 'proc')
            # добавление объекта из текущей строчки ксв в класс его комплекутющей,
            # добавление ключа в класс stats в противном случае

            cur_k = self.add_entity(k, 'stats')

            # добавления значения из словаря, если оно есть
            if len(v) != 0:
                cur_v = self.add_entity(v, 'values')

                cur_unit.Has_stat.append(cur_k)
                cur_k.Stat_of.append(cur_unit)

                # добавление связи комплектующая имеет значение
                cur_unit.Has_value.append(cur_v)
                cur_v.Value_of.append(cur_unit)

            # добавление связи значение ключа одно из примеров значения для ключа
            if v != '':
                #
                # print(cur_v,' ',cur_k,type(cur_k),type(cur_v)) # debug print

                cur_k.Mis_a.append(cur_v)
                cur_v.One_of.append(cur_k)

    # добавление ВСЕХ ксв файлов в онтологию
    def add_all_from_dict(self, d):
        print('создание онтологии ')
        keys = list(d.keys())
        for tip in keys:
            tip_as_obj = self.add_entity('example_of_' + tip, tip)  # пример комплектующей
            for row in d[tip]:
                self.load_row_from_csv(row, tip)

            for k in d[tip][1].keys():  # добавление  всех характеристик для примера комплектующей
                if '"' in k:
                    k = k.replace('"', 'duim')
                if "%" in k:
                    k = k.replace('%', 'proc')
                k = k.replace(' ', '_')

                a = list(self.onto.search(iri='*' + k))
                if len(a) > 0:
                    t = None
                    print(a)
                    for item in a:
                        if k == str(item)[str(item).find('.') + 1:]:
                            t = a[0]

                            break
                    if t is not None:
                        tip_as_obj.Has_stat.append(t)
            print(f"{tip} закончен")

    # FUNCTIONS TO WORKING

    def save(self, file_name):

        if file_name in list(os.listdir()):  # проверка есть ли файл в директории, если да то перезаписываем его
            remove(file_name)
        self.onto.save(file=file_name, format='rdfxml')

    def read_onto(self, file_name):
        self.onto = get_ontology(f"file://{file_name}").load()

    # Функция принимает имя класса и возращает список элементов класса
    def look_class(self, class_name: str):
        return self.onto.search(is_a=self.onto.__getattr__(class_name))

    def print_all(self, individuals: bool):
        print('classes: ', list(self.onto.classes(), ), '\n')
        print('props: ', list(self.onto.properties()), '\n')
        if individuals is True:
            print('individuals:', list(self.onto.individuals()), '\n')

    def stats_of_object_in_dict(self, obj):
        d = {}
        stats = obj.Has_stat
        values = obj.Has_value
        for i in range(len(stats)):
            for j in range(len(values)):
                if stats[i] in values[j].One_of:
                    d.setdefault(str(stats[i]), str(values[j]))

        strd = f'{str(obj)} имеет следующие характеристики: \n'  # строка служащая выводом функции
        for key in d.keys():
            strd += f'{key[key.find(".") + 1::]} - {d[key][key.find(".") + 1::]}\n'

        return strd

    def search_object_by_name(self, s):  # поиск по имени
        s = delete_prepositions(s)
        s = reduction_to_roots(s)
        combo = generate_combinations(s)
        super = self.onto.SuperClass
        typ = None

        for word in combo:
            word = word.replace('_', '*')
            if len(word) > 4:
                types = list(self.onto.search(subclass_of=super, iri=f'*{word}*'))
                if len(types) > 0:
                    typ = types[0]
                    s = s.replace(word, '')
                    break

        ans = []
        count = 0
        while count < len(generate_combinations(s)):  # цикл для обхода комбинаций слов
            for word in reversed(generate_combinations(s)):
                ans_for_word_no_typ = list(self.onto.search(iri=f'*{word}*'))
                blacklist = [self.onto.values, self.onto.stats]
                for e in ans_for_word_no_typ:
                    if e.is_a[0] in blacklist:
                        ans_for_word_no_typ.remove(e)
                if len(ans_for_word_no_typ) < 50 and len(ans_for_word_no_typ) > 0:
                    item = process.extract(word, ans_for_word_no_typ)
                    if len(item) > 0:
                        item = item[0][0]
                        if item not in ans:
                            ans.append(item)
                            s = s.replace(word.replace('*', ' '), '')
                            break
            count += 1

        if len(ans) > 0:
            strd = ''
            for t in ans:
                strd += self.stats_of_object_in_dict(t)
            return strd
        else:
            return 'ничего не найдено'

    def search_object_by_description(self, s: str) -> str:
        s = delete_prepositions(s)
        s = reduction_to_roots(s)
        super = self.onto.SuperClass
        typ = None

        for word in generate_combinations(s):
            if len(word) > 4:
                types = list(self.onto.search(subclass_of=super, iri=f'*{word}*'))
                if len(types) > 0:
                    typ = types[0]
                    s = s.replace(word, '')
                    break

        if typ is None:
            return 'тип комплектующего не указан в сообщении'

        ch = []  # список характеристик из сообщения
        vl = []  # список значений из сообщения

        # список всех возможных характеристик для комплектующей
        all_stats = list(self.onto.search(Stat_of=self.onto.search(iri="*example_of*", is_a=typ)))

        for word in reversed(generate_combinations(s)):  # поиск самых похожих характеристик для комплектующей
            chs = []
            for e in all_stats:
                if word in str(e):
                    chs.append(e)
            cutted_chs = process.extract(s, chs)

            # поиск самых похожих значений для слова
            vls = list(self.onto.search(iri=f'*{word}*', is_a=self.onto.values))
            cutted_vls = process.extract(s, vls)

            if len(cutted_chs) <= 3 and len(cutted_chs) > 0:  # уточнение значения и удаление его из строки
                if cutted_chs[0][0] not in ch:
                    ch.append(cutted_chs[0][0])
                    s = s.replace(word, '')
                    continue
            # вставка значения в список vl и удаление слова из строки
            if (len(cutted_vls) > 0 and cutted_vls[0][0] not in vl):
                vl.append(cutted_vls[0][0])

                s = s.replace(word, '')
                continue

        # обработка пустого ввода
        if len(ch) == 0 and len(vl) == 0:
            return 'в сообщении не найдено характеристик и их значений'
        elif len(ch) == 0:
            return 'в сообщении не найдено характеристик '
        elif len(vl) == 0:
            return 'в сообщении не найдено значений для характеристик'

        res = []
        for stat in ch:  # поиск объединений для значений по характеристике и пересечений для характеристик

            set_for_stat = set()
            for value in vl:
                if value in stat.Mis_a:

                    a = set(list(self.onto.search(Has_stat=stat, Has_value=value, type=typ)))

                    set_for_stat = a.union(set_for_stat)

                    if len(set_for_stat) > 0:
                        res.append(set_for_stat)
                        print(set_for_stat, '\n')

        res1 = res[0]
        i = 0
        if len(res) > 0:
            for se in res:
                i += 1
                if len(se) > 0:
                    res1 = res1 & se
            strd = 'Найденные объекты: '
            for t in res1:
                strd += str(t) + ', '
            return strd
        else:
            return 'ничего не найдено'

    def find_and_stats(self, s):  # вывести самый похожий объект и его характеристки
        item = list(self.search_object_by_name(s))
        if type(item) is list:
            return self.stats_of_object_in_dict(item)
        else:
            return item

    def update_onto(self):
        filename = str(self.onto.name) + '.owl'
        if filename != 'template.owl':
            data_dict = read_csv_all()
            self.add_all_from_dict(data_dict)
            self.save(filename)
        else:
            print('ERROR U TRY UPDATE TEMPLATE FILE, WE CANT DO IT')