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
    - 太难了

"""
import requests
import pandas as pd


class ChinaEpidemic:
    def __init__(self):
        self.base_url='https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        self.dailyD = []


    def spider_Daily(self):
        response = requests.get(
            url=self.base_url,
            headers=self.headers
        )

        r = response.json()['data']['chinaDayList']
        print(r)
        # 定义dataframe的三个变量
        data = []
        index = []
        columns = ['confirm','heal','dead']


        for day in r:
            index.append(str(day['date']))
            data.append([
                day['confirm'],
                day['heal'],
                day['dead']
            ])
            self.dailyD.append([day['date'],day['confirm'],day['heal'],day['dead']])

        self.df = pd.DataFrame(index=index,data=data,columns=columns)
        self.df.to_csv('./tables/{}.csv'.format('china'),encoding='gbk')
