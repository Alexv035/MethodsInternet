# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pprint import pprint


class JobparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.vacancys_db

    def process_item(self, item, spider):
        salary = item['salary']
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary(salary)
        elif spider.name == 'sjru':
            item['salary_min'], item['salary_max'], item['currency'] = self.sj_process_salary(salary)
        salary_min = item['salary_min']
        salary_max = item['salary_max']
        salary_cur = item['currency']
        link = item['link']
        web_site = item['web_site']
        del item['salary']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        # pprint(item)
        return item

    def __del__(self):
        self.client.close()

    def def_ls(self, yn):
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

        for i in range(len(y)):
            num = num + y[i]
        num = int(num)
        return num

    def process_salary(self, salary):
        if (str(salary[0]).rfind('от') != -1) and (str(salary[2]).rfind('до') != -1):
            mx = self.def_ls(str(salary[3]))
            mn = self.def_ls(str(salary[1]))
            mc = salary[5]
            return mn, mx, mc
        elif (str(salary[0]).rfind('от') != -1) and (str(salary[4]).rfind('до') != -1):
            mn = self.def_ls(str(salary[1]))
            mc = salary[3]
            return mn, None, mc
        elif (str(salary[0]).rfind('до') != -1) and (str(salary[4]).rfind('до') != -1):
            mx = self.def_ls(str(salary[1]))
            mc = salary[3]
            return None, mx, mc
        else:
            return None, None, None

    def sj_process_salary(self, salary):
        if str(salary[2]).rfind('') != -1:
            mx = self.def_ls(salary[1])
            mn = self.def_ls(salary[0])
            mc = salary[3]
            return mn, mx, mc
        elif str(salary[0]).rfind('от') != -1:
            mn = self.def_ls(str(salary[2])[:-4])
            mc = str(salary[2])[-4:]
            return mn, None, mc
        elif str(salary[0]).rfind('до') != -1:
            mx = self.def_ls(str(salary[2])[:-4])
            mc = str(salary[2])[-4:]
            return None, mx, mc
        else:
            return None, None, None
