from flask import Flask,render_template
from multiprocessing import Pool
from chart import make_chart
import xlrd,csv,requests,urllib,os,logging
import pandas as pd


app = Flask(__name__)

@app.route('/')
def hello_world():
    make_chart(data=get_now_country_data())
    return render_template('map.html')
    #
def get_all_country(): # 获取所有国家的名称
    ch_country = []
    en_country = []
    data = xlrd.open_workbook('./static/country.xls')
    sheet = data.sheets()[0]
    for c in sheet.col_values(1):
        if len(c)<15 and len(c)>1: ch_country.append(c)
    for c in sheet.col_values(2):
        if len(c)>1: en_country.append(c)
    ch_country,en_country =ch_country[1:],en_country[1:]
    with open('./static/country.csv','w+') as f:
        for i in range(244): csv.writer(f).writerow([ch_country[i],en_country[i]])

def parser(ch,en): # 处理
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
        print(ch)

def get_all_country_data(): # 多进程爬取数据
    countryDic = {}
    with open('./static/country.csv', 'r', encoding='utf-8')as f:
        for i in csv.reader(f): countryDic[i[0]] = i[1]

    p = Pool()
    for coutry in countryDic:
        p.apply_async(func=parser,args=(coutry,countryDic[coutry],))
    p.close()
    p.join()

def get_now_country_data() -> list:  # 获取当前各个国家的数据
    countryDic = {}
    data = {}
    with open('./static/country.csv', 'r', encoding='utf-8')as f:
        for i in csv.reader(f): countryDic[i[0]] = i[1]

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

    r = requests.get(url='https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList',headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})
    china_confirm = r.json()['data']['chinaDayList'][-1]['confirm']
    data.append(['China',china_confirm])

    print(data)
    return data

if __name__ == '__main__':
    app.run(port=3006)
    # get_all_country()
    # get_country_data()



