# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2021/2/3 11:23 上午
@Describe 
"""
import requests

url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=timeline&isappinstalled=0'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}
r=requests.get(url=url,headers=headers)
r.encoding = 'utf-8'
print(r.text)