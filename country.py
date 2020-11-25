# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/25 3:06 上午
@Describe 
"""
import pandas as pd
import requests
import urllib.parse

class CountryEpidemic():
    def __init__(self):
        self.dailyD = []

    def main_process(self,url,place):
        r = requests.post(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})
        for date in r.json()['data']: self.dailyD.append([date['date'], date['confirm'], date['heal'], date['dead'],date['confirm_add']])
        # 保存到本地csv文件
        index = [date['date'] for date in r.json()['data']]
        columns = ['confirm', 'heal', 'dead', 'confirm_add']
        datalist = [[date['confirm'], date['heal'], date['dead'], date['confirm_add']] for date in r.json()['data']]
        df = pd.DataFrame(data=datalist, index=index, columns=columns)
        df.to_csv('./tables/' + place + '.csv', encoding='gbk')


    def spider_Daily(self,place):
            country_parse = urllib.parse.quote(place, encoding="utf-8")  # 编码加密
            url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country={}&'.format(country_parse)
            # url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?country={}&'.format(country_parse)
            self.main_process(url, place)
        # except Exception as err:print(err)


