from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd


def def_ls(yn):
    num = ''
    y = list(yn)
    while True:
        if y.count('\xa0') > 0:
            y.remove('\xa0')
        elif y.count(' ') > 0:
            y.remove(' ')
        elif y.count('') > 0:
            y.remove('')
        else:
            break
    #    print(y)
    for i in range(len(y)):
        num = num + y[i]
    num = int(num)
    return num


def def_salary(x):
    x = str(x)
    #    print(x)
    if x.isdigit():
        return x, None, None
    elif x.rfind('до') != -1:
        mx = def_ls(x[3:-4])
        mc = x[-4:]
        return None, mx, mc
    elif x.rfind('от') != -1:
        mn = def_ls(x[3:-4])
        mc = x[-4:]
        return mn, None, mc
    elif x.rfind('-') > 0:
        mn, z = x.split('-')
        mn = def_ls(mn)
        mx = def_ls(z[:-4])
        mc = z[-4:]
        return mn, mx, mc
    else:
        return None, None, None


def hhvacancy(key):
    main_link = 'https://www.hh.ru'
    search_link = '/search/vacancy'
    vacancy_data = []

    search = key
    n = 0
    lnum = 0

    while True:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'Accept': '*/*'}

        params = {'clusters': 'true', 'area': '1', 'enable_snipets': 'true', 'st': 'searchVacancy', 'text': search,
                  'fromSearch': 'true', 'from': 'suggest_post', 'page': n}

        response = requests.get(main_link + search_link, headers=header, params=params).text
        soup = bs(response, 'lxml')

        #with open('hhsoup.html', 'w') as f:
        #    f.write(str(soup))

        vacancy_list = soup.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
        #   pprint(vacancy_list)

        for v in vacancy_list:
            vacancy = {}
            vacancy['Вакансия'] = v.find('a', {'class': 'bloko-link HH-LinkModifier'}).getText()
            vacancy['link'] = main_link + v.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
            vacancy['salary_min'], vacancy['salary_max'], vacancy['salary_cur'] = def_salary(
                str(v.find('div', {'vacancy-serp-item__sidebar'}).getText()))
            vacancy['web-site'] = 'www.hh.ru'
            vacancy['keyword'] = search

            vacancy_data.append(vacancy)
            lnum += 1

        try:
            next_button = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}).getText()
            n += 1
        except:
            print(f'Всего занесенно {lnum} записей c hh.ru')
            break

    file = pd.DataFrame(vacancy_data)
    file.to_csv("hhvacancy.csv")
