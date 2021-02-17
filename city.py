# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/25 3:06 上午
@Describe 
"""
import pandas as pd
import requests

class CityEpidemic():
    def __init__(self):
        self.dailyD = []

    def main_process(self,url,place):
        print(url)
        r = requests.post(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})
        try:
            for date in r.json()['data']:
                self.dailyD.append([f"{date['year']}.{date['date']}", date['confirm'], date['heal'], date['dead'],date['confirm_add']])
                index = [f"{date['year']}.{date['date']}" for date in r.json()['data']]
        except:
            for date in r.json()['data']:
                self.dailyD.append([f"{date['y']}.{date['date']}", date['confirm'], date['heal'], date['dead'],date['confirm_add']])
                index = [f"{date['y']}.{date['date']}" for date in r.json()['data']]

        # 保存到本地csv文件
        columns = ['confirm', 'heal', 'dead', 'confirm_add']
        datalist = [[date['confirm'], date['heal'], date['dead'], date['confirm_add']] for date in r.json()['data']]
        df = pd.DataFrame(data=datalist, index=index, columns=columns)
        df.to_csv('./tables/' + place + '.csv', encoding='gbk')


    def spider(self,place):
        try:  # 省份
            province = place
            url = f'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={province}&'
            self.main_process(url, place)
        except:  # 城市
            province, city = place.split('-')
            url = f'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={province}&city={city}&'
            self.main_process(url, place)

# CityEpidemic().spider('广东-深圳')
