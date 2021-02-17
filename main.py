# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/18 12:24 上午
@Describe 
"""
from abroad import AbroadEpidemic
from china import ChinaEpidemic
from global_ import GlobalEpidemic
from chart import make_chart_echart
import time
import numpy as np
import pandas as pd
import schedule, time


def mainWork():
    # 爬取海外疫情数据
    AbroadEpidemic().spider_Daily()
    # 爬取国内疫情数据
    ChinaEpidemic().spider_DXY()
    # 组合海外数据与国内数据
    GlobalEpidemic().combineAbroadAndChina()
    # 制作图表
    make_chart_echart(csvName='./tables/global.csv',chartName='global',titleName='全球')
    make_chart_echart(csvName='./tables/china.csv',chartName='china',titleName='中国')
    make_chart_echart(csvName='./tables/abroad.csv',chartName='abroad',titleName='海外')

mainWork()
schedule.every().day.at('09:01').do(mainWork)
while True:
         schedule.run_pending()
         time.sleep(1)