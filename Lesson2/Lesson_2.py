'''
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайта superjob.ru и hh.ru.
Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
    *Наименование вакансии
    *Предлагаемую зарплату (отдельно мин. и отдельно макс. и отдельно валюта)
    *Ссылку на саму вакансию
    *Сайт откуда собрана вакансия
По своему желанию можно добавить еще работодателя и расположение. Данная структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.
'''

import pandas as pd
import hhsearch as hh
import superjobsearch as sj

key = input('Введите поисковый запрос на hh.ru и superjob.ru.ru: ')

hh.hhvacancy(key)
sj.superjobvacancy(key)

DATASET_PATH = 'hhvacancy.csv'
hh_result = pd.read_csv(DATASET_PATH, index_col=0)

DATASET_PATH = 'superjobvacancy.csv'
superjob_result = pd.read_csv(DATASET_PATH, index_col=0)

vacancy = pd.concat([hh_result, superjob_result], ignore_index=True)

file = pd.DataFrame(vacancy)
file.to_csv("vacancy.csv")
