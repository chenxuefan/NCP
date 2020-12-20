# 新冠疫情（NCP）的监测与趋势分析

## 1. 前言 🇨🇳

### 1.1 如何使用？

1. 下载整个项目至本地，使用命令`source ./venv/bin/activate`激活项目下的虚拟环境，即可运行
2. 在项目文件下使用命令`pip install -r requirements.txt`安装依赖库
3. 配置[chromedriver](https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare) 
4. 运行项目下的`main.py`文件

### 1.2 项目阐述

👨🏻‍💻 2020，注定是不平凡的一年，新冠疫情如晴天霹雳将沉浸在2020年春节气氛中的人们骤然推进人人自危的疫情防控中，新冠疫情的肆虐，使得我们每一个人都无法独善其身。

​	面对这一场突如其来的危机，幸亏有强大的国家和政府，使我们大部分人平稳度过疫情的爆发期，在从一月初疫情爆发到二月底不到两个月的时间里，实施了最有效的措施，并在三月将新增确诊的数目减到了两位数。

​	数据是冷冰冰的，但是，借由数据，我们可以看到背后透露出来的国力雄厚、英雄气概，也只有亲身经历过这一场战役的我们，才深深懂得那一条逐渐归于直线的确诊曲线，来的有多么不容易。

![chart_plt](https://billie-s-album.oss-cn-beijing.aliyuncs.com/img/chart_plt.png)

本项目围绕疫情的几个关键特征（如确诊、治愈、死亡），绘制折线图，并在GUI图形页面进行交互与显示图表。

### 1.3 技术栈

- python - PyQt5、numpy、pandas、requests、pyecharts、matplotlib

## 2. 需求分析

### 2.1 功能需求分析

![ncp1](https://billie-s-album.oss-cn-beijing.aliyuncs.com/img/ncp1.png)/*功能图示*/

![ncp2](https://billie-s-album.oss-cn-beijing.aliyuncs.com/img/ncp2.png)/*图形界面组件设计*/

![image-20201125213231534](https://billie-s-album.oss-cn-beijing.aliyuncs.com/img/image-20201125213231534.png)/*图形界面示意图*/

### 2.2 技术需求分析

🐛 **数据爬取** - requests（一个requests吃遍天），由于是使用API的方式获取数据，因此只需要添加简单的请求头就可以轻松获取到数据。

🔍 **数据分析** - numpy、pandas，请求返回的数据为json格式，采用`pd.DataFrame()`将其处理并保存至csv文件。

📈 **制作图表** - echarts、matplotlib，提供两种不同风格的图表，并生成网页图表（echarts）。

📃 **图形页面** - PyQt5，极简风格，没有修饰。

### 2.3 API需求分析（来源：腾讯）

下面是本项目用到的API：

- 国内数据
  - 国内全局 - `https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare`
  - 国内全局 - `https://view.inews.qq.com/g2/getOnsInfo?name=disease_other`
  - 国内省份及城市 - `https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={}&city={}&`
- 海外数据
  - 海外全局 - `https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,FAutoContinentStatis,FAutoGlobalDailyList,FAutoCountryConfirmAdd`
  - 海外各国 - `https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country={}&`

## 3. 开发流程

🐛 **数据爬取** 

🔍 **数据分析** 

📈 **制作图表** 

📃 **图形页面** 

## 4. 后记

在线图表（每日更新）

- china - [https://download.billie52707.cn/NCP/china.html](https://download.billie52707.cn/NCP/china.html)
- abroad - [https://download.billie52707.cn/NCP/abroad.html](https://download.billie52707.cn/NCP/abroad.html)
- global - [https://download.billie52707.cn/NCP/global.html](https://download.billie52707.cn/NCP/global.html)

项目详解 - [新冠疫情（NCP）的监测与趋势分析](https://billie52707.cn/posts/2020/11/ncp-readme/)



