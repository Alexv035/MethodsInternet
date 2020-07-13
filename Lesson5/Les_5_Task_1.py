'''
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных
(от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172
'''

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

import time
from datetime import date
from pprint import pprint

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.get('https://mail.ru')

login = driver.find_element_by_id('mailbox:login')
login.send_keys('study.ai_172@mail.ru')
login.send_keys(Keys.ENTER)
time.sleep(2)

login = driver.find_element_by_id('mailbox:password')
login.send_keys('NextPassword172')
login.send_keys(Keys.ENTER)

button = WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.XPATH,
                                    "//a[@class = 'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']"))
)
button.send_keys(Keys.ENTER)

emails_data = []
emails = {}
emails_num = 1

dtime = str(date.today())

emails['from'] = None
emails['date'] = None
emails['subject'] = None
emails['letter'] = None

button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[@class = 'letter-contact']")))

try:
    a = driver.find_element_by_class_name('letter-contact')
    emails['from'] = a.get_attribute('title')
except:
    print(f'error  from at the {emails_num}')

try:
    emails['date'] = driver.find_element_by_xpath("//div[@class='letter__date']").text
    if str(emails['date']).find('сегодня') == -1:
        x, y = str(emails['date']).split(',')
        emails['date'] = dtime + y
except:
    print(f'error date at the {emails_num}')

try:
    emails['subject'] = driver.find_element_by_xpath("//h2[@class='thread__subject thread__subject_pony-mode']").text
except:
    print(f'error subject at the {emails_num}')

try:
    ltext = driver.find_element_by_class_name('letter-body').text
    emails['letter'] = str(ltext).replace('\n', ' ')
except:
    print(f'error letter at the {emails_num}')

emails_num += 1
emails_data.append(emails)

while True:
    try:
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN)
        actions.perform()

        emails = {}
        emails['from'] = None
        emails['date'] = None
        emails['subject'] = None
        emails['letter'] = None

        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class = 'letter-contact']")))

        try:
            a = driver.find_element_by_class_name('letter-contact')
            emails['from'] = a.get_attribute('title')
        except:
            print(f'error from at the {emails_num}')

        try:
            emails['date'] = driver.find_element_by_xpath("//div[@class='letter__date']").text
            if str(emails['date']).find('сегодня') == -1:
                x, y = str(emails['date']).split(',')
                emails['date'] = dtime + y
        except:
            print(f'error date at the {emails_num}')

        try:
            emails['subject'] = driver.find_element_by_xpath(
                "//h2[@class='thread__subject thread__subject_pony-mode']").text
        except:
            print(f'error subject at the {emails_num}')

        try:
            ltext = driver.find_element_by_class_name('letter-body').text
            emails['letter'] = str(ltext).replace('\n', ' ')
        except:
            print(f'error letter at the {emails_num}')

        emails_num += 1
        emails_data.append(emails)
        print(emails)

    except:
        print(f'Всего {emails_num}')
        break

pprint(emails_data)
driver.quit()

client = MongoClient('localhost', 27017)
db = client['emails_db']
email_get = db.emails_db

email_get.delete_many({})
email_get.insert_many(emails_data)
