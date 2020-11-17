import threading
import time
import pandas as pd
import numpy as np
import requests
import json
import urllib.parse
from chart import *
from pprint import pprint

def main_process(url,place):
    r = requests.post(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})
    now = r.json()['data'][-1]
    print(now)
    print('confirm：{}\nheal：{}\ndead：{}\nconfirm_add：{}'.format(now['confirm'], now['heal'], now['dead'],now['confirm_add']))
    # 历史数据
    j = input('>>>是否阅读历史数据？(Y/N)')
    if j == 'Y' or j == 'y':
        for date in r.json()['data']:
            print(
            '{}: confirm:{} heal:{} dead:{} confirm_add:{}'
                .format(date['date'], date['confirm'], date['heal'],date['dead'], date['confirm_add']))
    else:
        pass
    # 制作图表
    try:
        j = input('>>>是否制作疫情趋势图？(Y/N)')
        if j == 'Y' or j == 'y':
            # 保存到本地csv文件
            index = [date['date'] for date in r.json()['data']]
            columns = ['confirm', 'heal', 'dead', 'confirm_add']
            datalist = [[date['confirm'], date['heal'], date['dead'], date['confirm_add']] for date in r.json()['data']]
            df = pd.DataFrame(data=datalist, index=index, columns=columns)
            df.to_csv('./tables/' + place + '.csv', encoding='gbk')
            # 制作图表
            make_chart_plt(csvName='{}{}{}'.format('tables/', place, '.csv'),
                           chartPath='charts/',
                           chartName=place)
            make_chart_echart(csvName='{}{}{}'.format('tables/', place, '.csv'),
                              chartPath='html/',
                              chartName=place,
                              titleName=place)
        else:
            pass
    except Exception as err:
        print(err)
def China_search():
    while True:
        try:
            print("\n>>>输入格式<<<  \n查询全局：中国 \n查询城市：对应省份名称-城市名称 (如湖北-武汉) \n查询省份：省份名称 (如湖北)")
            place = input(">>>请输入需要查询的地区:")
            if place == 'exit()': break
            p = place.split('-')
            if place == '中国':
                url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
                r=requests.get(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})
                lis=eval(r.json()['data'])['chinaDayList']
                for date in lis:

                    print(
                        '"confirm":72528,"suspect":6242,"dead":1870,"heal":12561,"nowConfirm":58097,"nowSevere":11741,"importedCase":0,"deadRate":"2.6","healRate":"17.3","date":"02.17","noInfect":0'
                            .format(date['date'], date['confirm'], date['heal'], date['dead']))
            try:
                province,city=p[0],p[1]
                url='https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={}&city={}&'.format(province,city)
                main_process(url,place)
                # except:print("抱歉，暂无此地区的数据。\n")
            except:
                province=p[0]
                url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={}&'.format(province)
                main_process(url, place)
        except:print("输入有误或网络错误，请重试\n")
# except Exception as err:print(err)
def Global_search():
    while True:
        country = input('>>>请输入需要查询的国家：')
        if country == 'exit()': break
        try:
            country_parse = urllib.parse.quote(country, encoding="utf-8")#编码加密
            url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country={}&'.format(country_parse)
            #url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?country={}&'.format(country_parse)
            main_process(url,country)
        except:print("暂无{}的数据，请重试\n".format(country))
        # except Exception as err:print(err)

if __name__ == '__main__':
    print('@author：人人都爱小雀斑')
    while True:
        try:
            judge=int(input('请选择查询的地区(0-国内/1-海外)：'))
            if judge==0:China_search()
            elif judge==1:Global_search()
        except:print('输入有误或网络错误，请重试\n')
