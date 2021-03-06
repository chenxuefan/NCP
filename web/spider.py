# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2021/1/3 11:51 下午
@Describe
"""
from multiprocessing import Pool
import xlrd,csv,requests,os,logging,time
import urllib.parse
import pandas as pd
import asyncio
import aiohttp

def get_all_country_name(): # 获取所有国家的名称
    ch_country = []
    en_country = []
    data = xlrd.open_workbook('./static/country.xls')
    sheet = data.sheets()[0]

    for c in sheet.col_values(1):
        if len(c)<15 and len(c)>1:
            ch_country.append(c)
    for c in sheet.col_values(2):
        if len(c)>1:
            en_country.append(c)

    ch_country,en_country =ch_country[1:],en_country[1:]
    with open('./static/country.csv','w+') as f:
        for i in range(244):
            csv.writer(f).writerow([ch_country[i],en_country[i]])

def get_now_country_data() -> list:  # 获取当前各个国家的数据
    """
    :returns : list of all country_confirm_num
    """
    countryDic = {}
    data = {}
    with open('./static/country.csv', 'r', encoding='utf-8') as f:
        for i in csv._reader(f):
            countryDic[i[0]] = i[1]

    # 获取国外各国疫情数据
    url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoforeignList'
    r = requests.post(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})
    for country in r.json()['data']['FAutoforeignList']:
        try:
            if '(the' in countryDic[country['name']]:
                i= countryDic[country['name']].index('(')
                key = countryDic[country['name']][:i].strip()
                data[key] = country['confirm']
            else:
                data[countryDic[country['name']]] = country['confirm']
        except:
            if country['name'] == '俄罗斯': data['Russia'] = country['confirm']
            elif country['name'] == '日本本土': data['Japan'] = country['confirm']
            # print(country)
    data = [[i, data[i]] for i in data]

    # 获取中国疫情数据
    r = requests.get(url='https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList',headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})
    china_confirm = r.json()['data']['chinaDayList'][-1]['confirm']
    data.append(['China',china_confirm])

    print(data)
    return data

def parser(ch,en): # 处理
    """
    :param ch: string Chinese name of country
    :param en: string English name of country
    :return:
    """
    try:
        country_parse = urllib.parse.quote(ch, encoding="utf-8")  # 编码加密
        url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country={}&'.format(country_parse)
        r = requests.post(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})
        # 保存到本地csv文件
        if r.json()['data'] != None:
            index = [date['date'] for date in r.json()['data']]
            columns = ['confirm', 'heal', 'dead', 'confirm_add']
            datalist = [[date['confirm'], date['heal'], date['dead'], date['confirm_add']] for date in r.json()['data']]
            df = pd.DataFrame(data=datalist, index=index, columns=columns)
            if not os.path.exists('./static/country/'): os.mkdir('./static/country/')
            df.to_csv('./static/country/' + en + '.csv', encoding='utf-8')
            print(f'{ch} - 已成功获取数据')
    except:
        print(f"{ch} - failed")

def Process_get_all_country_data(): # 多进程爬取数据
    '''一个城市调用一个接口'''
    countryDic = {}
    with open('./static/country.csv', 'r', encoding='utf-8') as f:
        for i in csv.reader(f):
            countryDic[i[0]] = i[1]

    p = Pool()
    for coutry in countryDic:
        p.apply_async(func=parser,args=(coutry,countryDic[coutry],))
    p.close()
    p.join()

def Async_get_all_country_data():
    '''使用 协程 进行数据的获取'''

    async def fetch(url):
        '''request'''
        async with aiohttp.ClientSession() as session:
            async with session.get(url,verify_ssl=False) as resp:
                return await resp.json()

    async def parse(ch,en,json):
        '''parser'''
        if json['data'] != None:
            index = [date['date'] for date in json['data']]
            columns = ['confirm', 'heal', 'dead', 'confirm_add']
            datalist = [[date['confirm'], date['heal'], date['dead'], date['confirm_add']] for date in json['data']]
            df = pd.DataFrame(data=datalist, index=index, columns=columns)
            if not os.path.exists('./static/country/'): os.mkdir('./static/country/')
            df.to_csv('./static/country/' + en + '.csv', encoding='utf-8')
            # print(f'{ch} - 已成功获取数据')
            return ch

    async def process(ch,en,url):
        return await parse(ch,en,await fetch(url))

    async def main():
        ''''''
        countryDic = {}
        with open('./static/country.csv', 'r', encoding='utf-8') as f:
            for i in csv.reader(f):
                countryDic[i[0]] = i[1]

        tasks = []
        for ch,en in countryDic.items():
            country_parse = urllib.parse.quote(ch, encoding="utf-8")  # 编码加密
            url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country={}&'.format(country_parse)
            task = asyncio.create_task(process(ch,en,url),name=ch)
            tasks.append(task)

        done,pendding = await asyncio.wait(tasks)
        country_count = len([task.result() for task in done if task.result() != None])
        print(f"共 {country_count} 个国家")

    asyncio.run(main())


if __name__ == '__main__':
    start = time.time()
    # Process_get_all_country_data()
    Async_get_all_country_data()
    end = time.time()
    print(f'共耗时：{end-start} s')