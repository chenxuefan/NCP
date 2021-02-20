# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/22 10:55 下午
@Describe
通过合并海外疫情和国内疫情得到全球疫情数据
"""
import numpy as np
import pandas as pd

class GlobalEpidemic():
    def __init__(self):
        self.dailyD = []
    def combine(self):
        list_of_China = np.loadtxt('./tables/china.csv',
                                 skiprows=1,
                                 dtype='str',
                                 delimiter=',',
                                 usecols=(0, 1, 2, 3),
                                 unpack=True)
        list_of_Abroad = np.loadtxt('./tables/abroad.csv',
                                  skiprows=1,
                                  dtype='str',
                                  delimiter=',',
                                  usecols=(0, 1, 2, 3),
                                  unpack=True)
        dict_of_China = dict()
        dict_of_Abroad = dict()
        for i in range(len(list_of_China[0])): dict_of_China[list_of_China[0][i]] = [list_of_China[1][i],list_of_China[2][i],list_of_China[3][i]]
        for i in range(len(list_of_Abroad[0])): dict_of_Abroad[list_of_Abroad[0][i]] = [list_of_Abroad[1][i],list_of_Abroad[2][i],list_of_Abroad[3][i]]

        dict_of_global = dict()
        for day in dict_of_China:
            ls = []
            for i in range(3):
                try: ls.append(int(dict_of_China[day][i])+int(dict_of_Abroad[day][i]))
                except: ls.append(int(dict_of_China[day][i])) # 1.28之前只有国内的数据
            dict_of_global[day] = ls

        for date in dict_of_global: self.dailyD.append([date]+dict_of_global[date])
        print(dict_of_global)

        # 定义dataframe的三个参数
        data = dict_of_global.values()
        index = dict_of_global.keys()
        columns = ['confirm', 'heal', 'dead']
        df = pd.DataFrame(index=index,columns=columns,data=data)
        df.to_csv('./tables/{}.csv'.format('global'), encoding='gbk')


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
                                  unpack=True)

        print(len(dataOfAbroad[1]),dataOfAbroad[1][-1])
        print(len(dataOfChina[1]),dataOfChina[1][-1])

        # 定义dataframe的三个参数
        data = []
        index = dataOfChina[0]
        columns = ['confirm', 'heal', 'dead']

        for i, day1 in enumerate(dataOfChina[0]):
            print(i,day1)
            if i < 15:
                data.append([
                    int(dataOfChina[1][i]),
                    int(dataOfChina[2][i]),
                    int(dataOfChina[3][i]),
                    # int(dataOfChina[4][i])
                ])
                # print(len(data),day1)
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
                        # int(dataOfChina[4][i]) + int(dataOfAbroad[4][i]),
                    ])

                    self.dailyD.append([
                        dataOfChina[0][i],
                        int(dataOfChina[1][i]) + int(dataOfAbroad[1][i - 15]),
                        int(dataOfChina[2][i]) + int(dataOfAbroad[2][i - 15]),
                        int(dataOfChina[3][i]) + int(dataOfAbroad[3][i - 15])
                    ])
                except Exception as e:
                    print(e)

        print(len(data),data[-1])
        print(len(index), len(data), len(columns))
        df = pd.DataFrame(index=index, data=data, columns=columns)
        df.to_csv('./tables/{}.csv'.format('global'), encoding='gbk')
        print(df)

# a = GlobalEpidemic()
# a.combine()
# print(a.dailyD)