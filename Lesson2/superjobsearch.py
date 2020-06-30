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
    #        print(y)
    for i in range(len(y)):
        num = num + y[i]
    num = int(num)
    return num


def def_salary(x):
    x = str(x)
    #    print(x)
    if x.isdigit():
        return x, None, None
    elif x.rfind('до') != -1 and x.rfind('договорён') == -1:
        mx = def_ls(x[3:-4])
        mc = x[-4:]
        return None, mx, mc
    elif x.rfind('от') != -1:
        mn = def_ls(x[3:-4])
        mc = x[-4:]
        return mn, None, mc
    elif x.rfind('—') > 0:
        mn, z = x.split('—')
        mn = def_ls(mn)
        mx = def_ls(z[:-4])
        mc = z[-4:]
        return mn, mx, mc
    else:
        return None, None, None


def superjobvacancy(key):
    main_link = 'https://www.superjob.ru'
    search_link = '/vacancy/search/'
    vacancy_data = []

    search = key
    n = 1
    lnum = 0

    while True:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'Accept': '*/*'}

        params = {'keywords': search, 'page': n}

        response = requests.get(main_link + search_link, headers=header, params=params).text
        soup = bs(response, 'lxml')

        #with open('superjob_soup.html', 'w') as f:
        #    f.write(str(soup))

        vacancy_list = soup.find_all('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ _1JhPh _2gFpt _1znz6 _2nteL'})
        #    pprint(vacancy_list)

        for v in vacancy_list:
            vacancy = {}
            vacancy['Вакансия'] = v.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'}).getText()
            vacancy['link'] = main_link + v.find('a')['href']
            vacancy['salary_min'], vacancy['salary_max'], vacancy['salary_cur'] = def_salary(
                str(v.find('span', {'_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText()))
            vacancy['web-site'] = 'www.superjob.ru'
            vacancy['keyword'] = search
            vacancy_data.append(vacancy)
            lnum += 1

        try:
            next_button = soup.find('a',
                                    {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'}).getText()
            n += 1
        except:
            print(f'Всего занесенно {lnum} записей c superjob.ru')
            break

    file = pd.DataFrame(vacancy_data)
    file.to_csv("superjobvacancy.csv")
