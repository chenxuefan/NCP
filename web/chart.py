# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2021/1/3 3:27 下午
@Describe 
"""
import time
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ChartType,SymbolType,BMapType
from pyecharts.faker import Faker

def make_chart(data):
    """
    :param data: list of all country_confirm_num
    :return:
    """
    value = [i[1] for i in data]
    v = value.copy()
    v.remove(max(value))
    v.remove(min(value))
    max_ = sum(v)/len(v)
    c = (
        Map()
            .add("确诊人数",
                 data,
                 "world",
                 layout_size='100%',
                 min_scale_limit=1,
                 max_scale_limit=2,
                 # layout_size=0
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                title_opts={"text": '全球新冠疫情动态',"subtext":f"日期 {time.strftime('%Y-%m-%d')}"},  # 图表标题 ,  "{}".format("@author：Billie")
                # visualmap_opts=opts.VisualMapOpts(max_=max(value)),
                visualmap_opts=opts.VisualMapOpts(
                    max_=10000000,
                    is_piecewise=True,
                    pieces=[
                        {"min": 500000},
                        {"min": 200000, "max": 499999},
                        {"min": 100000, "max": 199999},
                        {"min": 50000, "max": 99999},
                        {"min": 10000, "max": 49999},
                        {"max": 9999},
                    ]
                )
            )
    )

    c.width = '1900px'
    c.height = '800px'
    c.render("./templates/map.html")