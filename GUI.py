# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/21 12:00 下午
@Describe


"""
from abroad import AbroadEpidemic
from china import ChinaEpidemic
from global_ import GlobalEpidemic
from city import CityEpidemic
from country import CountryEpidemic
from chart import make_chart_echart,make_chart_plt
import time

import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QPushButton
from PyQt5.QtGui import QIcon
import sys
import os

class GUI(QWidget):
    def __init__(self):
        super(GUI,self).__init__()
        self.initUI() # 使用initUI()方法创建一个GUI

    def initUI(self):

        # 窗体初始化
        self.setWindowTitle('NCP')
        self.setWindowIcon(QIcon('./charts/logo.png'))  # 设置窗体标题图标
        self.move(500,300)

        # 各个控件初始化
        self.label1 = QLabel("请选择：")
        self.combo = QComboBox()  # 下拉列表
        self.label2 = QLabel("或输入：")
        self.input = QLineEdit()  # 文本输入框
        self.btnSearch = QPushButton("查询")  # 查询按钮
        self.label3 = QLabel() # 占位标签
        self.chart = QLabel()  # 图表显示框
        self.text = QTextBrowser()  # 日志框

        self.combo.addItem("")
        self.combo.addItem("国内")
        self.combo.addItem("海外")
        self.combo.addItem("全球")
        self.combo.activated[str].connect(self.onActivated)  # 设置关联函数
        self.chart.setScaledContents(True)
        self.chart.setFixedSize(750,500)
        self.text.setFixedSize(500,500)
        self.btnSearch.clicked.connect(self.search)

        '''图像缩放:使用pixmap的scare方法，参数aspectRatioMode=Qt.KeepAspectRatio设置为等比例缩放，aspectRatioMode=Qt.IgnoreAspectRatio为不按比例缩放'''
        # scaredPixmap = pixmap.scaled(600, 400, aspectRatioMode=Qt.KeepAspectRatio)
        # 图像缩放：使用label的setScaledContents(True)方法，自适应label大小
        # chart.setPixmap(scaredPixmap)

        # 主体布局
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.label1, 0, 0, 1, 1)
        mainLayout.addWidget(self.combo, 0, 1, 1, 1)
        mainLayout.addWidget(self.label2, 0, 2, 1, 1)
        mainLayout.addWidget(self.input, 0, 3, 1, 1)
        mainLayout.addWidget(self.btnSearch, 0, 4, 1, 1)
        # mainLayout.addWidget(self.label3, 0, 5, 5, 5)
        mainLayout.addWidget(self.text, 1, 0, 5, 5)
        mainLayout.addWidget(self.chart, 1, 5, 5, 5)

        self.setLayout(mainLayout)
        # self.setWindowOpacity(0.9)  # 设置窗口透明度

    # 日志文本
    def Text(self,text,mode=0):
        if mode==0:
            self.text.append("[{}]{}".format(time.strftime('%H:%M:%S'),text))
        elif mode==1:
            self.text.append("{}".format(text))
        PyQt5.QtWidgets.QApplication.processEvents()
        PyQt5.QtWidgets.QApplication.processEvents()

    # 事件 - 获取下拉框的选择
    def onActivated(self, choice):
        self.choice = choice
        if self.choice == "国内":
            self.Text('正在获取疫情数据...')
            C = ChinaEpidemic()
            C.spider_DXY() # 爬取国内疫情数据
            for day in C.dailyD: self.Text("{}: confirm:{} heal:{} dead:{}".format(day[0],day[1],day[2],day[3]),1) # 输出数据到日志框
            self.Text('正在制作疫情趋势图...')
            make_chart_echart(csvName='./tables/china.csv', chartName='china', titleName='国内') # 制作图表
            self.chart.setPixmap(QPixmap("./charts/china.png").scaled(787,500)) # 显示图表
            self.Text('图表已存至本地(./charts/china.png)')

        elif self.choice == "海外":
            self.Text('正在获取疫情数据...')
            A = AbroadEpidemic()
            A.spider_Daily()  # 爬取海外疫情数据
            for day in A.dailyD: self.Text("{}: confirm:{} heal:{} dead:{}".format(day[0], day[1], day[2], day[3]),1) # 输出数据到日志框
            self.Text('正在制作疫情趋势图...')
            make_chart_echart(csvName='./tables/abroad.csv', chartName='abroad', titleName='海外') # 制作图表
            self.chart.setPixmap(QPixmap("./charts/abroad.png").scaled(787, 500)) # 显示图表
            self.Text('图表已存至本地(./charts/abroad.png)')

        elif self.choice == "全球":
            self.Text('正在获取疫情数据...')
            ChinaEpidemic().spider_DXY() # 获取国内数据
            AbroadEpidemic().spider_Daily() # 获取海外数据
            A = GlobalEpidemic()
            A.combineAbroadAndChina() # 组合海外数据与国内数据
            for day in A.dailyD: self.Text("{}: confirm:{} heal:{} dead:{}".format(day[0], day[1], day[2], day[3]),1) # 输出数据到日志框
            self.Text('正在制作疫情趋势图...')
            make_chart_echart(csvName='./tables/global.csv', chartName='global', titleName='全球') # 制作图表
            self.chart.setPixmap(QPixmap("./charts/global.png").scaled(787, 500)) # 显示图表
            self.Text('图表已存至本地(./charts/global.png)')


    # 查询 - 获取输入框内容进行查询
    def search(self):
        self.keyword = self.input.text()
        print(self.keyword)
        try:
            self.Text('正在获取疫情数据...')
            try: # 查询国家
                self.keyword = self.keyword.strip('-')
                C = CountryEpidemic()
                C.spider(self.keyword)
                dailyD = C.dailyD
                for day in dailyD: self.Text("{}: confirm:{} heal:{} dead:{} confirm_add:{}".format(day[0], day[1], day[2], day[3], day[4]),1)  # 输出数据到日志框
            except: # 查询国内省份或城市
                C = CityEpidemic()
                C.spider(self.keyword)
                dailyD = C.dailyD
                for day in dailyD: self.Text("{}: confirm:{} heal:{} dead:{} confirm_add:{}".format(day[0], day[1], day[2], day[3], day[4]),1)  # 输出数据到日志框


            self.Text('正在制作疫情趋势图...')
            make_chart_plt(csvName='{}{}{}'.format('./tables/', self.keyword, '.csv'), chartName=self.keyword)
            self.chart.setPixmap(QPixmap("./charts/{}.png".format(self.keyword)).scaled(666, 500))  # 显示图表
            self.Text('图表已存至本地(./charts/{}.png)'.format(self.keyword))

        except:
            self.Text('输入不合法，请重新输入')
            self.Text('>>>输入格式<<<  \n查询国家：国家名称（如美国）\n查询省份：省份名称 (如湖北) \n查询城市：对应省份名称-城市名称 (如湖北-武汉) ')

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())