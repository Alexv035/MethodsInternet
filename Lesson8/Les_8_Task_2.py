'''
4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
'''

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.insta
collection = db['instagram']

profiles = db.instagram

# Написать запрос к базе, который вернет список подписчиков только указанного пользователя
for profile in profiles.find({'id': '1818656135', 'followers': True},
                      {'full_name': 1, 'user_id': 1, '_id': 0}):
    print(profile)

# Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
for profile in profiles.find({'id': '1818656135', 'follow': True},
                      {'full_name': 1, 'user_id': 1, '_id': 0}):
    print(profile)