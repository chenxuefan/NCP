# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/22 10:55 下午
@Describe 
"""
import numpy as np
import pandas as pd

class GlobalEpidemic():
    def __init__(self):
        self.dailyD = []
    # 合并国内疫情数据和海外疫情数据
    def combineAbroadAndChina(self):
        dataOfChina = np.loadtxt('./tables/china.csv',
                                 skiprows=1,
                                 dtype='str',
                                 delimiter=',',
                                 usecols=(0, 1, 2, 3),
                                 unpack=True)
        dataOfAbroad = np.loadtxt('./tables/abroad.csv',
                                  skiprows=1,
                                  dtype='str',
                                  delimiter=',',
                                  usecols=(0, 1, 2, 3),
                                  unpack=True
                                  )

        print(dataOfAbroad)
        print(dataOfChina)

        # 定义dataframe的三个变量
        data = []
        index = dataOfChina[0]
        columns = ['confirm', 'heal', 'dead']

        for i, day1 in enumerate(dataOfChina[0]):
            if i < 15:
                data.append([
                    int(dataOfChina[1][i]),
                    int(dataOfChina[2][i]),
                    int(dataOfChina[3][i]),
                    # int(dataOfChina[4][i])
                ])
                self.dailyD.append([
                    dataOfChina[0][i],
                    dataOfChina[1][i],
                    dataOfChina[2][i],
                    dataOfChina[3][i]
                ])
            else:
                try:
                    data.append([
                        int(dataOfChina[1][i]) + int(dataOfAbroad[1][i - 15]),
                        int(dataOfChina[2][i]) + int(dataOfAbroad[2][i - 15]),
                        int(dataOfChina[3][i]) + int(dataOfAbroad[3][i - 15]),
                        # int(dataOfChina[4][i])+int(dataOfAbroad[4][i]),
                    ])
                    self.dailyD.append([
                        dataOfChina[0][i],
                        int(dataOfChina[1][i]) + int(dataOfAbroad[1][i - 15]),
                        int(dataOfChina[2][i]) + int(dataOfAbroad[2][i - 15]),
                        int(dataOfChina[3][i]) + int(dataOfAbroad[3][i - 15])
                    ])
                except Exception as e:
                    print(e)
        print(data)
        print(len(index), len(data), len(columns))
        df = pd.DataFrame(index=index, data=data, columns=columns)
        df.to_csv('./tables/{}.csv'.format('global'), encoding='gbk')
        print(df)