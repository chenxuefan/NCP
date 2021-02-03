'''
@author: 人人都爱小雀斑
@time: 2020/2/26 17:57
@desc: pyecharts制作折线图等
'''

import numpy as np
import matplotlib.pyplot as plt
from pyecharts.charts import *
from pyecharts import options as opts
# from example.commons import Faker #pip install pyecharts==1.0
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

def make_chart_echart(csvName,chartName,titleName=''):  # pyechart
    print('正在制作echarts图表...')
    (time, confirm, heal, dead) = np.loadtxt(csvName,
                                                    # encoding="",
                                                    skiprows=1,
                                                    dtype='str',
                                                    delimiter=',',
                                                    usecols=(0, 1, 2, 3),
                                                    unpack=True)
    print(list(time))
    # 折线图表
    chart_Line = (
        Line()  # Bar()#init_opts=opts.InitOpts(theme=ThemeType.LIGHT)
            # x轴
            # .add_xaxis([i[-5:].lstrip('0') for i in list(time)]) # [::-1]列表反转
            .add_xaxis(list(time)) # [::-1]列表反转
            # y轴
            .add_yaxis("confirm",
                       list(confirm),
                       linestyle_opts=opts.LineStyleOpts(width=2),  # 线条样式
                       is_smooth=True,  # 平滑曲线
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.1),  # 区域渲染
                       label_opts=opts.LabelOpts(is_show=True)  # 显示具体数据True
            )
            .add_yaxis("heal", list(heal), label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("dead", list(dead), label_opts=opts.LabelOpts(is_show=False))
            # .add_yaxis("newAddConfirm", list(add), label_opts=opts.LabelOpts(is_show=False))  # True

            # 全局配置项
            .set_global_opts(
                # 表格标题
                title_opts={"text": titleName+"疫情趋势图"},  # 图表标题 , "subtext": "{}".format("@author：Billie")
                # xlabel写法1
                # xaxis_opts={"name":"日期"},
                # xlabel写法2
                xaxis_opts=opts.AxisOpts(
                    name="日期",
                    axistick_opts=opts.AxisTickOpts(is_align_with_label=True), boundary_gap=False,  # 图像贴近y轴
                ),
                # yaxis_opts={"name":"人数",}
                # ylabel
                yaxis_opts=opts.AxisOpts(
                    name="人数",
                    # type_="log",is_scale=True,#10,100,1000
                    splitline_opts=opts.SplitLineOpts(is_show=True) # 水平分割线
                )
            )

            # 系列配置项(需放置最后)
            # .set_series_opts(
            #     symbol_size=[34, 30],
            # areastyle_opts=opts.AreaStyleOpts(opacity=0.5),#渲染
            # label_opts=opts.LabelOpts(is_show=False),#显示数据
            # )
    )

    # 设置图表长度
    chart_Line.width = '100'

    # 保存为html
    # chart_Line.render(chartPath + chartName + ".html")

    # 保存为png
    make_snapshot(snapshot,chart_Line.render("./html/"+chartName+".html"), "./charts/"+chartName+".png")

    print('已制作echarts图表！')

def make_chart_plt(csvName,chartName):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # windows 正常显示中文标签
    plt.rcParams["font.family"] = 'Arial Unicode MS'  # macos 正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # 变量此时的数据类型:<class 'numpy.ndarray'>
    (date,confirm_add)=np.loadtxt(csvName,skiprows=1,dtype=str,delimiter=',',usecols=(0,4),unpack=True)
    # 清洗数据
    for i in range(len(confirm_add)):
        if confirm_add[i] == '':confirm_add[i] = 0
        else:pass
    date=[str(i).lstrip('0') for i in date]#处理时间，去掉月份第一位的0
    confirm_add=[float(i) for i in confirm_add]#类型转换成浮点数
    (confirm, heal, dead) = np.loadtxt(csvName,
                                        skiprows=1,
                                        dtype=float,
                                        delimiter=',',
                                        usecols=(1, 2, 3),
                                        unpack=True)
    plt.figure(figsize=(6,4),dpi=200)
    plt.plot(date,confirm, linewidth=1, label="confirm")
    plt.plot(date,heal, linewidth=1, label="heal")
    plt.plot(date,dead, linewidth=1, label="dead")
    plt.plot(date,confirm_add, linewidth=1, label="confirm_add")
    plt.grid()
    # x轴标注
    # plt.xticks(range(0,len(date),10))#以10天为间隔显示
    months = {'1.01':'Jan','2.01':'Feb', '3.01':'Mar', '4.01':'Apr', '5.01':'May', '6.01':'June', '7.01':'July', '8.01':'Aug', '9.01':'Sept', '10.01':'Oct','11.01':'Nov','12.01':'Dec'}
    x,val = [],[]
    for day in date:
        key = day[-5:].lstrip('0')
        if key in months:
            x.append(day)
            val.append(months[key])
    print(x)
    print(val)
    plt.xticks(x,val)
    #----------很牛逼的一段算法----------
    if   int(confirm[-1])<10000: ticks=range(0,int(confirm[-1]),1000) #标注点的y坐标，以每 k为间隔
    elif int(confirm[-1])<50000: ticks=range(0,int(confirm[-1]),5000) #以每 k为间隔
    elif int(confirm[-1])<100000: ticks=range(0,int(confirm[-1]),20000) #以每20k为间隔
    elif int(confirm[-1])<200000: ticks = range(0, int(confirm[-1]), 50000)  #以每50k为间隔
    elif int(confirm[-1])<1000000: ticks = range(0, int(confirm[-1]), 200000)  #以每200k为间隔
    elif int(confirm[-1])<10000000: ticks = range(0, int(confirm[-1]), 1000000)  #以每1000k为间隔
    else: ticks = range(0, int(confirm[-1]), 2000000)  #以每1000k为间隔
    labels=[str(int(i/1000))+'k' for i in ticks] #标注，以..k显示
    labels[0]=0 #插入第一项为0
    #---------------------------------
    # y轴标注
    plt.yticks(ticks,labels)
    plt.annotate(text=int(confirm[-1]),xy=(date[-1], confirm[-1]),xytext=(-20, 2), textcoords='offset points') # 标注最后一天的数据
    # plt.text(date[-1], confirm[-1], int(confirm[-1]), ha='center', va='bottom', fontsize=10, alpha=1, color='mediumvioletred')#标注最后一项的数据
    # plt.xlabel("日期",fontsize="7")
    # plt.ylabel("人数",fontsize="7")
    plt.suptitle(chartName+"疫情趋势图",y=1)#图表大标题,y为标题位置的偏移距离
    plt.title("@author:billie(数据来自腾讯)",loc='right', fontsize=8)#子图表标题
    plt.legend()  # 设置图例的前题是y指定了label
    plt.savefig("./charts/{}.png".format(chartName),dpi=1000,bbox_inches = 'tight')
    print('已制作plt图表!')


