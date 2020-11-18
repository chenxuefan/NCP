# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/18 12:17 上午
@Describe
- 获取国内疫情数据
- api(丁香园)：https://file1.dxycdn.com/2020/1118/091/3894308898877218443-135.json

"""
import requests
from pprint import pprint
import numpy as np
import pandas as pd

class ChinaEpidemic:
    def __init__(self):
        self.base_url='https://file1.dxycdn.com/2020/1118/091/3894308898877218443-135.json'
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'file1.dxycdn.com',
            'Origin': 'https://ncov.dxy.cn',
            'Referer': 'https://ncov.dxy.cn/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }


    def spider_Daily(self):
        response = requests.get(
            url=self.base_url,
            headers=self.headers
        )
        r = response.json()['data']

        # 定义dataframe的三个变量
        data = []
        index = []
        columns = ['confirm','heal','dead','newAddConfirm']


        for day in r:
            index.append(str(day['dateId'])[4:6]+'.'+str(day['dateId'])[6:8])
            data.append([
                day['confirmedCount'],
                day['curedCount'],
                day['deadCount'],
                day['confirmedIncr']
            ])

        df = pd.DataFrame(index=index,data=data,columns=columns)
        # print(df)
        df.to_csv('./tables/{}.csv'.format('china'),encoding='gbk')

