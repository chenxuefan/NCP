# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/18 12:24 上午
@Describe 
"""
from abroad import AbroadEpidemic
from china import ChinaEpidemic
from chart import make_chart_echart
import time
import numpy as np
import pandas as pd
import schedule, time



def combineAbroadAndChina():
    dataOfChina = np.loadtxt('./tables/china.csv',
                             skiprows=1,
                             dtype='str',
                             delimiter=',',
                             usecols=(0, 1, 2, 3, 4),
                             unpack=True)
    dataOfAbroad = np.loadtxt('./tables/abroad.csv',
                              skiprows=1,
                              dtype='str',
                              delimiter=',',
                              usecols=(0, 1, 2, 3, 4),
                              unpack=True
                              )

    print(dataOfAbroad)
    print(dataOfChina)

    # 定义dataframe的三个变量
    data = []
    index = dataOfChina[0]
    columns = ['confirm', 'heal', 'dead', 'newAddConfirm']

    for i,day1 in enumerate(dataOfChina[0]):
        if i < 18:
            data.append([
                int(dataOfChina[1][i]),
                int(dataOfChina[2][i]),
                int(dataOfChina[3][i]),
                int(dataOfChina[4][i])
            ])
        for day2 in dataOfAbroad[0]:
            try:
                if day1 == day2:
                    data.append([
                        int(dataOfChina[1][i])+int(dataOfAbroad[1][i]),
                        int(dataOfChina[2][i])+int(dataOfAbroad[2][i]),
                        int(dataOfChina[3][i])+int(dataOfAbroad[3][i]),
                        int(dataOfChina[4][i])+int(dataOfAbroad[4][i]),
                    ])
                    # print(data)
            except:pass

    print(data)
    print(len(index),len(data),len(columns))
    df = pd.DataFrame(index=index,data=data,columns=columns)
    df.to_csv('./tables/{}.csv'.format('global'),encoding='gbk')
    print(df)

def mainWork():
    # 爬取海外疫情数据
    AbroadEpidemic().spider_Daily()
    # 爬取国内疫情数据
    ChinaEpidemic().spider_Daily()
    # 组合海外数据与国内数据
    combineAbroadAndChina()
    # 制作图表
    make_chart_echart(csvName='./tables/global.csv',chartName='global',chartPath='./',titleName='全球')

mainWork()
# schedule.every().day.at('00:01').do(mainWork)
# while True:
#         schedule.run_pending()
#         time.sleep(1)