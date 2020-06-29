'''
2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое,
требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

https://www.programmableweb.com/api/food
'''

import requests
import json
import config
from pprint import pprint

token = config.ftoken

# Search receipts
params = {'apiKey': token, 'query': 'burger', 'number': '3'}
data_w = requests.get('https://api.spoonacular.com/recipes/search', params=params)
data = data_w.json()

with open('fr.json', 'w') as f:
    json.dump(data, f)
