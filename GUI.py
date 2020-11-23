# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/21 12:00 下午
@Describe 
"""
from abroad import AbroadEpidemic
from china import ChinaEpidemic
from global_ import GlobalEpidemic
from chart import make_chart_echart
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

        # 各个控件初始化
        self.label = QLabel("请选择：")
        self.combo = QComboBox()  # 下拉列表
        self.btnSearch = QPushButton("查询")  # 查询按钮
        self.chart = QLabel()  # 图表显示框
        self.text = QTextBrowser()  # 日志框

        self.combo.addItem("")
        self.combo.addItem("国内")
        self.combo.addItem("海外")
        self.combo.addItem("全球")
        self.combo.activated[str].connect(self.onActivated)  # 设置关联函数
        self.chart.setScaledContents(True)
        self.chart.setFixedSize(750,500)
        self.text.setFixedSize(400,500)


        '''图像缩放:使用pixmap的scare方法，参数aspectRatioMode=Qt.KeepAspectRatio设置为等比例缩放，aspectRatioMode=Qt.IgnoreAspectRatio为不按比例缩放'''
        # scaredPixmap = pixmap.scaled(600, 400, aspectRatioMode=Qt.KeepAspectRatio)
        # 图像缩放：使用label的setScaledContents(True)方法，自适应label大小
        # chart.setPixmap(scaredPixmap)

        # 主体布局
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.label,0,0,1,1)
        mainLayout.addWidget(self.combo,0,1,1,1)
        mainLayout.addWidget(self.btnSearch,0,2,1,1)
        mainLayout.addWidget(self.text, 1, 0, 3, 5)
        mainLayout.addWidget(self.chart, 1, 5, 4, 7)

        self.setLayout(mainLayout)
        self.setWindowOpacity(0.9)  # 设置窗口透明度

    # 事件 - 获取下拉框的选择
    def onActivated(self, choice):

        self.choice = choice
        if self.choice == "国内":

            self.text.append("[{}]正在获取全球疫情数据...".format(time.strftime('%Y-%m-%d %H:%M:%S')))
            PyQt5.QtWidgets.QApplication.processEvents()
            C = ChinaEpidemic()
            C.spider_Daily()# 爬取国内疫情数据
            for day in C.dailyD:
                self.text.append("{}: confirm:{} heal:{} dead:{}".format(day[0],day[1],day[2],day[3]))# 输出数据到日志框
                PyQt5.QtWidgets.QApplication.processEvents()
            self.text.append("[{}]正在制作疫情趋势图...".format(time.strftime('%Y-%m-%d %H:%M:%S')))
            PyQt5.QtWidgets.QApplication.processEvents()
            PyQt5.QtWidgets.QApplication.processEvents()
            make_chart_echart(csvName='./tables/china.csv', chartName='china', titleName='国内')# 制作图表
            self.chart.setPixmap(QPixmap("./charts/china.png").scaled(750,500))# 显示图表

        elif self.choice == "海外":
            self.text.append("[{}]正在获取全球疫情数据...".format(time.strftime('%Y-%m-%d %H:%M:%S')))
            PyQt5.QtWidgets.QApplication.processEvents()
            A = AbroadEpidemic()
            A.spider_Daily()  # 爬取海外疫情数据
            for day in A.dailyD:
                self.text.append("{}: confirm:{} heal:{} dead:{}".format(day[0], day[1], day[2], day[3]))  # 输出数据到日志框
                PyQt5.QtWidgets.QApplication.processEvents()
            self.text.append("[{}]正在制作疫情趋势图...".format(time.strftime('%Y-%m-%d %H:%M:%S')))
            PyQt5.QtWidgets.QApplication.processEvents()
            PyQt5.QtWidgets.QApplication.processEvents()
            make_chart_echart(csvName='./tables/abroad.csv', chartName='abroad', titleName='海外')  # 制作图表
            self.chart.setPixmap(QPixmap("./charts/abroad.png").scaled(750, 500))  # 显示图表
        elif self.choice == "全球":
            self.text.append("[{}]正在获取全球疫情数据...".format(time.strftime('%Y-%m-%d %H:%M:%S')))
            ChinaEpidemic().spider_Daily() # 获取国内数据
            AbroadEpidemic().spider_Daily() # 获取海外数据
            A = GlobalEpidemic()
            A.combineAbroadAndChina()  # 组合海外数据与国内数据
            for day in A.dailyD:
                self.text.append("{}: confirm:{} heal:{} dead:{}".format(day[0], day[1], day[2], day[3]))  # 输出数据到日志框
                PyQt5.QtWidgets.QApplication.processEvents()
            self.text.append("[{}]正在制作疫情趋势图...".format(time.strftime('%Y-%m-%d %H:%M:%S')))
            PyQt5.QtWidgets.QApplication.processEvents()
            PyQt5.QtWidgets.QApplication.processEvents()
            make_chart_echart(csvName='./tables/global.csv', chartName='global', titleName='全球')  # 制作图表
            self.chart.setPixmap(QPixmap("./charts/global.png").scaled(750, 500))  # 显示图表


