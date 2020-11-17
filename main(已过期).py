# -*- coding: utf-8 -*-
'''
@Author billie
@Date 2020/3/21 8:34
@Describe 

'''
import requests,re,time
import selenium
from selenium.webdriver.chrome.options import Options
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from urllib.parse import quote

class Epidemic():
    def __init__(self):
        self.country_list=[]#储存所有国家的名称
        self.base_url='https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?country='
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        self.abroad_confirm = 0
        self.abroad_heal = 0
        self.abroad_dead = 0

    def global_now_data(self):
            url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
            import requests, pprint
            r = requests.post(url)
            pprint.pprint(r.json())
    def find_country_name(self):
        url='https://zhidao.baidu.com/question/335286555.html'
        r=requests.get(url,self.headers)
        r.encoding='gbk'
        root=BeautifulSoup(r.text,'lxml')
        ps=root.find_all('p')
        for p in ps[2:32]:
            p=re.findall('\w+',p.text)
            for i in p:
                if len(i)==1:p.remove(i)#如字节为1则剔除
            self.country_list+=p#合并到国家列表
        with open('country_list.txt','w')as f:#将国家的名称写入本地txt
            for i in self.country_list:
                f.write(i+'\n')
    def find_country_name2(self):
        url='https://news.qq.com/zt2020/page/feiyan.htm#/global?ct=Uzbekistan'
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = selenium.webdriver.Chrome(options=options)#
        driver.get(url)
        tbodys=driver.find_elements_by_xpath('//*[@id="foreignWraper"]/table/tbody')
        with open('country_list.txt', 'w')as f:
            for tbody in tbodys:
                f.write(tbody.find_element_by_xpath('./tr/th/span').text+'\n')
    def spider(self):
        self.country_list=open('./country_list.txt','r').readlines()#从本地txt获取国家的名称
        all_country_info=dict()
        for country in self.country_list:
            country=country.strip('\n')
            print(country)
            try:
                country_quote=quote(country)
                r=requests.get(self.base_url+country_quote,self.headers)
                dates=r.json()['data']#该国家所有日期的数据
                # print(dates)
                for i in dates:
                    try:#该日期的数据字典已存在，则补充
                        all_country_info[country+'confirm'].update({float(i['date']):i['confirm']})
                        all_country_info[country+'heal'].update({float(i['date']):i['heal']})
                        all_country_info[country+'dead'].update({float(i['date']):i['dead']})
                        # all_country_info[country+'confirm_add'].update({float(i['date']):i['confirm_add']})
                    except:#该日期的数据字典不存在，则新建字典
                        all_country_info[country + 'confirm']={i['date']: i['confirm']}
                        all_country_info[country + 'heal']={i['date']: i['heal']}
                        all_country_info[country + 'dead']={i['date']: i['dead']}
                    # all_country_info[date]={**all_country_info,**{country : , country + 'heal': i['heal'],country + 'dead': i['dead']}}
            # except: print('{} 未统计疫情'.format(country))
            except Exception as err:print(err)
            # except:pass
            # all_country[country]=coun

        # print(self.abroad_confirm,self.abroad_heal,self.abroad_dead)
        # print(all_country_info.keys())
        # print(all_country_info.values())
        df = pd.DataFrame(all_country_info)
        df.to_csv('main.csv',encoding='gbk')
        # print(df)

    def test(self):
        df=pd.read_csv('./main.csv',encoding='gbk')
        df=df.groupby('美国confirm').size()
        # print(df)
billie=Epidemic()
# billie.find_country_name2()
billie.spider()
# billie.test()