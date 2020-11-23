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


class AbroadEpidemic:
    def __init__(self):
        self.base_url='https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,FAutoContinentStatis,FAutoGlobalDailyList,FAutoCountryConfirmAdd'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        self.response = requests.post(self.base_url, headers=self.headers)  #请求的数据
        self.FAutoGlobalStatis=dict()              #存储疫情统计数据的字典
        self.FAutoContinentStatis=dict()           #存储每日各个洲疫情数据的字典
        self.FAutoGlobalDailyList=dict()           #存储每日海外疫情数据的字典
        self.FAutoCountryConfirmAdd=dict()         #存储今日各国新增疫情数据的字典
        self.lastUpdateTime=''

        self.dailyD = []

    # 保存数据至csv文件
    def save_to_csv(self,index,columns,data,filename):
        df=pd.DataFrame(index=index,columns=columns,data=data)
        df.to_csv('./tables/{}.csv'.format(filename),encoding='gbk')

        # 生成图表
        # df.plot()
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        # plt.savefig('./charts/{}.png'.format(filename))
        # plt.show()
        df.describe()
        print(filename,df)

    # 海外每日的疫情数据
    def spider_Daily(self):
        DailyList=self.response.json()['data']['FAutoGlobalDailyList']
        for date in DailyList:
            self.FAutoGlobalDailyList[date['date']]=\
                [date['all']['confirm'],
                 date['all']['heal'],
                 date['all']['dead'],
                 ] #date['all']['newAddConfirm']
            self.dailyD.append([date['date'],date['all']['confirm'],date['all']['heal'],date['all']['dead']])
        # print(self.FAutoGlobalDailyList)
        self.save_to_csv(index=self.FAutoGlobalDailyList.keys(),
                         columns=['confirm','heal','dead'],
                         data=self.FAutoGlobalDailyList.values(),
                         filename='abroad')


    # 各个大洲的每日数据
    def spider_Continent(self):
        ContinentStatis=self.response.json()['data']['FAutoContinentStatis']
        # pprint(ContinentStatis)
        for date in ContinentStatis:
            try:
                self.FAutoContinentStatis[date['date']]=\
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
        print(self.FAutoContinentStatis)
        print(self.FAutoContinentStatis.keys())
        print([list(self.FAutoContinentStatis[i].keys())[2:] for i in self.FAutoContinentStatis.keys()])
        print([list(self.FAutoContinentStatis[i].values())[2:] for i in self.FAutoContinentStatis.keys()])
        self.save_to_csv(index=list(self.FAutoContinentStatis.keys()),
                         columns=['亚洲', '其他', '北美洲', '南美洲', '大洋洲', '欧洲', '非洲'],#[list(self.global_ContinentStatis_dict[i].keys())[2:] for i in self.global_ContinentStatis_dict.keys()],
                         data=[list(self.FAutoContinentStatis[i].values())[2:] for i in self.FAutoContinentStatis.keys()],
                         filename='各洲疫情数据')

    # 统计全局数据
    def spider_Statis(self):
        GlobalStatis=self.response.json()['data']['FAutoGlobalStatis']
        self.lastUpdateTime=GlobalStatis['lastUpdateTime']

        for key in list(GlobalStatis.keys()):
            self.FAutoGlobalStatis[key]=GlobalStatis[key]
        print(self.FAutoGlobalStatis.keys())
        self.save_to_csv(index=self.FAutoGlobalStatis.keys(),
                         columns=None,
                         data=self.FAutoGlobalStatis.values(),
                         filename='海外疫情数据综合统计')

    # 今日各国新增
    def spider_ConfirmAdd(self):
        CountryConfirmAdd=self.response.json()['data']['FAutoCountryConfirmAdd']

        for country in CountryConfirmAdd:
            self.FAutoCountryConfirmAdd[country]=CountryConfirmAdd[country]
        print(self.FAutoCountryConfirmAdd)

        self.save_to_csv(index=self.FAutoCountryConfirmAdd.keys(),
                         columns=['confirm'],
                         data=self.FAutoCountryConfirmAdd.values(),
                         filename='海外各国今日新增确诊')










