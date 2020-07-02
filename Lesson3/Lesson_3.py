'''
1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД (без датафрейма)
2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы. Поиск по двум полям (мин и макс зарплату)
3) Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта
'''

import hhsearch as hh
import superjobsearch as sj
from pymongo import MongoClient


def data_insert(data):
    n = 0
    for d in data:
        if vacancy.count({'vacancyId': d['vacancyId'], 'web-site': d['web-site']}) == 0:
            vacancy.insert_one(d)
            #print(d['vacancyId'])
            n += 1
    print(f'Вставлено новых {n} записей')

key = input('Введите поисковый запрос на hh.ru и superjob.ru: ')

hhvacancy = hh.hhvacancy(key)
sjvacancy = sj.superjobvacancy(key)

client = MongoClient('localhost', 27017)
db = client['vacancys_db']

vacancy = db.vacancys_db

#vacancy.delete_many({})

data_insert(hhvacancy)
data_insert(sjvacancy)
