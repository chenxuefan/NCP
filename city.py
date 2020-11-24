# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/25 3:06 上午
@Describe 
"""
import pandas as pd
import numpy as np
import requests


class CityEpidemic():
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
        try:
            if place == '中国':
                url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
                r = requests.get(url=url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})
                lis = eval(r.json()['data'])['chinaDayList']
                for date in lis:
                    self.dailyD.append("{}: confirm:{} heal:{} dead:{}".format(date['date'], date['confirm'], date['heal'],date['dead']))
            else:
                try:  # 城市
                    province = place
                    url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={}&'.format(province)
                    self.main_process(url, place)
                except:  # 省份
                    p = place.split('-')
                    province, city = p[0], p[1]
                    url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={}&city={}&'.format(province, city)
                    self.main_process(url, place)

        except:
            print("输入有误或网络错误，请重试\n")


