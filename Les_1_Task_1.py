import requests
import json

user = 'Alexv035'
login = requests.get('https://api.github.com/users/' + user + '/repos')

repos = []
data = login.json()

if len(data) != 0:
    print("Список репозиториев пользователя:")
    for data_i in data:
        repos.append(data_i['name'])
        print(f"{len(repos)}. {data_i['name']}")

    with open('gittext.json', 'w') as f:
        json.dump(repos, f)

else:
    print("У пользователя нет репозиториев.")
