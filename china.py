# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/18 12:17 上午
@Describe
- 获取国内疫情数据
- api(腾讯)：
    - https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare
    - {'nowSevere': 0, 'healRate': '0.0', 'noInfect': 0, 'importedCase': 0, 'deadRate': '2.4', 'date': '01.13', 'confirm': 41, 'suspect': 0, 'dead': 1, 'heal': 0, 'nowConfirm': 0}
    - https://view.inews.qq.com/g2/getOnsInfo?name=disease_other
- api(丁香园)：
    - https://file1.dxycdn.com/2020/1118/091/3894308898877218443-135.json
    - https://file1.dxycdn.com/2021/0203/371/5531818974268142643-135.json?t=26872025
    - 太难了

2021.02.03 更换api
"""
import time
import re
import requests
import pandas as pd


class ChinaEpidemic:
    def __init__(self):
        self.api_TC = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList'
        self.api_DXY = self.get_api()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        self.dailyD = []

    def get_api(self):
        url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=timeline&isappinstalled=0'
        r = requests.get(url=url)
        r.encoding = 'utf-8'
        api = re.search(
            r'"countryFullName":"China","statisticsData":"(.*?)"',
            r.text
        ).group(1)
        return api

    def save_to_csv(self,index,data,columns):
        self.df = pd.DataFrame(index=index, data=data, columns=columns)
        self.df.to_csv('./tables/{}.csv'.format('china'), encoding='gbk')

    def spider_TC(self):
        # 定义dataframe的三个变量
        data = []
        index = []
        columns = ['confirm', 'heal', 'dead']

        response = requests.get(
            url=self.api_TC,
            headers=self.headers
        )

        r = response.json()['data']['chinaDayList']
        for day in r:
            index.append(day['y']+'.'+str(day['date']))
            data.append([
                day['confirm'],
                day['heal'],
                day['dead']
            ])
            self.dailyD.append([day['date'],day['confirm'],day['heal'],day['dead']])
        self.save_to_csv(index=index,data=data,columns=columns)

    def spider_DXY(self):
        # 定义dataframe的三个变量
        data = []
        index = []
        columns = ['confirm', 'heal', 'dead']

        response = requests.get(
            url=self.api_DXY,
            headers=self.headers
        )

        r = response.json()['data']
        for day in r:
            dateId = str(day['dateId'])
            index.append(f"{dateId[0:4]}.{dateId[4:6]}.{dateId[6:8]}")
            data.append([
                day['confirmedCount'],
                day['curedCount'],
                day['deadCount']
            ])
            self.dailyD.append([f"{dateId[0:4]}.{dateId[4:6]}.{dateId[6:8]}", day['confirmedCount'], day['curedCount'], day['deadCount']])
        self.save_to_csv(index=index, data=data, columns=columns)



ChinaEpidemic().spider_DXY()
