# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/25 3:20 上午
@Describe 
"""
# 导入，Qapplication，单行文本框，窗口
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget
# 导入文本校验器：整数校验器,浮点数校验器,正则校验器
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator
# 导入Qt正则模块
from PyQt5.QtCore import QRegExp
import sys


class lineEditDemo(QWidget):
    def __init__(self, parent=None):
        super(lineEditDemo, self).__init__(parent)
        self.setWindowTitle('QLineEdit例子')
        self.resize(300, 300)

        int_validato = QIntValidator(50, 100, self)  # 实例化整型验证器，并设置范围为50-100
        int_le = QLineEdit(self)  # 整型文本框
        int_le.setValidator(int_validato)  # 设置验证
        int_le.move(50, 10)

        # 实例化浮点型验证器，并设置范围为-100到100，并精确2位小数
        float_validato = QDoubleValidator(-100, 100, 2, self)
        float_le = QLineEdit(self)  # 浮点文本框
        float_le.setValidator(float_validato)  # 设置验证
        float_le.move(50, 50)

        re = QRegExp('[a-zA-Z0-9]+$')  # 正则:只允许出现的大小写字母和数字
        re_validato = QRegExpValidator(re, self)  # 实例化正则验证器
        re_le = QLineEdit(self)  # 正则文本框
        re_le.setValidator(re_validato)  # 设置验证
        re_le.move(50, 90)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = lineEditDemo()
    win.show()
    sys.exit(app.exec_())