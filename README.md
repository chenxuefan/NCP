# 新冠疫情（NCP）的监测与趋势分析

## 前言 🇨🇳

### 如何使用？

- Windows用户，直接下载项目下的`.exe`文件，点击即可使用

- 其他用户，运行项目下的`main.py`文件，需配置依赖库环境，方法有两个
  1. 使用命令`source ./venv/bin/activate`激活项目下的虚拟环境，即可运行
  2. 使用命令`pip install -r requirements.txt`安装依赖库

### 项目阐述

👨🏻‍💻 2020，注定是不平凡的一年，新冠疫情如晴天霹雳将沉浸在2020年春节气氛中的人们骤然推进人人自危的疫情防控中，新冠疫情的肆虐，使得我们每一个人都无法独善其身。

​	在国内疫情最严重的二月春节期间，我每天都在关注着最新的疫情动态，看着日趋增长的确诊人数，以及每日一千两千甚至是三千的新增确诊人数，我总是在想，到底什么时候才能挺过去啊？这一场艰难的抗疫，到底什么时候才能迎来转机？很快，国家和政府用最实际的行动，给了我们最肯定的答案。

​	面对这一场突如其来的危机，幸亏有强大的国家和政府，使我们大部分人平稳度过疫情的爆发期，在从一月初疫情爆发到二月底不到两个月的时间里，实施了最有效的措施，并在三月将新增确诊的数目减到了两位数。与此同时，面对海外疫情泛滥的波涛汹涌之势，面对海外民众的束手无策和听天由命之悲，生活在中国的人都暗暗庆幸自己不在海外。那一刻，真为自己身为国人而自豪。

​	数据是冷冰冰的，但是，借由数据，我们可以看到背后透露出来的国力雄厚、英雄气概，也只有亲身经历过这一场战役的我们，才深深懂得那一条逐渐归于直线的确诊曲线，来的有多么不容易。

![chart_plt](https://billie-s-album.oss-cn-beijing.aliyuncs.com/img/chart_plt.png)

本项目围绕疫情的几个关键特征（如确诊、治愈、死亡），绘制折线图，并在GUI图形页面进行交互与显示图表。

### 功能需求分析

### 技术需求分析

### API需求分析（来源：腾讯）

- 国内数据
  - 国内全局 - `https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare`
  - 国内全局 - `https://view.inews.qq.com/g2/getOnsInfo?name=disease_other`
  - 国内省份及城市 - `https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={}&city={}&`
- 海外数据
  - 海外全局 - `https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,FAutoContinentStatis,FAutoGlobalDailyList,FAutoCountryConfirmAdd`
  - 海外各国 - `https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country={}&`

### 技术栈

- PyQt5、numpy、pandas、requests、pyecharts、matplotlib

## 项目流程

🐛 数据爬取

📈 制作图表

📃 图形页面



 



