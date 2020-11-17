# -*- coding: utf-8 -*-
'''
@Author billie
@Date 2020/4/19 14:07
@Describe 

'''
import time

import requests,re,json
from pprint import pprint
import numpy as np
import pandas as pd
from chart import *
import matplotlib.pyplot as plt

'''
》》》api接口参数《《《
FAutoGlobalStatis,
FAutoContinentStatis,
FAutoGlobalDailyList, 每日全球数据
FAutoCountryConfirmAdd 当前疫情数据
'''


class GlobalEpidemic:
    def __init__(self):
        self.base_url='https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,FAutoContinentStatis,FAutoGlobalDailyList,FAutoCountryConfirmAdd'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        self.response = requests.post(self.base_url, headers=self.headers)#请求的数据
        self.global_Statis_dict=dict()#存储疫情统计数据的字典
        self.global_ContinentStatis_dict=dict()#存储每日各个洲疫情数据的字典
        self.global_DailyList_dict=dict()#存储每日全球疫情数据的字典
        self.global_CountryConfirmAdd_dict=dict()#存储今日各国新增疫情数据的字典
        self.lastUpdateTime=''

    # 全球每日的疫情数据
    def spider_Daily(self):
        DailyList=self.response.json()['data']['FAutoGlobalDailyList']
        for date in DailyList:
            self.global_DailyList_dict[date['date']]=\
                [date['all']['confirm'],
                 date['all']['heal'],
                 date['all']['dead'],
                 date['all']['newAddConfirm']]
        print(self.global_DailyList_dict)
        self.save_to_csv(index=self.global_DailyList_dict.keys(),
                         columns=['confirm','heal','dead','newAddConfirm'],
                         data=self.global_DailyList_dict.values(),
                         filename='全球每日疫情数据')

    # 各个大洲的每日数据
    def spider_Continent(self):
        ContinentStatis=self.response.json()['data']['FAutoContinentStatis']
        # pprint(ContinentStatis)
        for date in ContinentStatis:
            try:
                self.global_ContinentStatis_dict[date['date']]=\
                    {'nowConfirm':date['nowConfirm'],
                     'range':date['range'],
                     '亚洲':date['statis']['亚洲'],
                     '其他':date['statis']['其他'],
                     '北美洲':date['statis']['北美洲'],
                     '南美洲':date['statis']['南美洲'],
                     '大洋洲':date['statis']['大洋洲'],
                     '欧洲':date['statis']['欧洲'],
                     '非洲':date['statis']['非洲']}
            except:pass
        print(self.global_ContinentStatis_dict)
        print(self.global_ContinentStatis_dict.keys())
        print([list(self.global_ContinentStatis_dict[i].keys())[2:] for i in self.global_ContinentStatis_dict.keys()])
        print([list(self.global_ContinentStatis_dict[i].values())[2:] for i in self.global_ContinentStatis_dict.keys()])
        self.save_to_csv(index=list(self.global_ContinentStatis_dict.keys()),
                         columns=['亚洲', '其他', '北美洲', '南美洲', '大洋洲', '欧洲', '非洲'],#[list(self.global_ContinentStatis_dict[i].keys())[2:] for i in self.global_ContinentStatis_dict.keys()],
                         data=[list(self.global_ContinentStatis_dict[i].values())[2:] for i in self.global_ContinentStatis_dict.keys()],
                         filename='全球各洲疫情数据')

    # 统计全局数据
    def spider_Statis(self):
        GlobalStatis=self.response.json()['data']['FAutoGlobalStatis']
        self.lastUpdateTime=GlobalStatis['lastUpdateTime']

        for key in list(GlobalStatis.keys()):
            self.global_Statis_dict[key]=GlobalStatis[key]
        print(self.global_Statis_dict.keys())
        self.save_to_csv(index=self.global_Statis_dict.keys(),
                         columns=None,
                         data=self.global_Statis_dict.values(),
                         filename='全球疫情数据综合统计')

    # 今日各国新增
    def spider_ConfirmAdd(self):
        CountryConfirmAdd=self.response.json()['data']['FAutoCountryConfirmAdd']

        for country in CountryConfirmAdd:
            self.global_CountryConfirmAdd_dict[country]=CountryConfirmAdd[country]
        print(self.global_CountryConfirmAdd_dict)

        self.save_to_csv(index=self.global_CountryConfirmAdd_dict.keys(),
                         columns=['confirm'],
                         data=self.global_CountryConfirmAdd_dict.values(),
                         filename='全球各国今日新增确诊')

    def save_to_csv(self,index,columns,data,filename):
        df=pd.DataFrame(index=index,columns=columns,data=data)
        df.to_csv('./tables/{}.csv'.format(filename),encoding='gbk')
        # df.plot()
        # 生成图表
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.savefig('./charts/{}.png'.format(filename))
        plt.show()
        df.describe()
        print(df)

    def make_chart(self):
        print("正在生成图表...")
        make_chart_echart(csvName='tables/全球每日疫情数据.csv',chartPath='./',chartName='global',titleName='全球')
        # make_chart_plt(csvName='tables/全球每日疫情数据.csv',chartPath='./',chartName='全球')



billie=GlobalEpidemic()
while True:
    billie.spider_Daily()
    # billie.spider_Continent()
    # billie.spider_ConfirmAdd()
    billie.spider_Statis()
    billie.make_chart()
    time.sleep(10000)


