# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/11/18 12:24 上午
@Describe 
"""


from GUI import GUI
from PyQt5 import QtWidgets
import schedule,time,sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())


# schedule.every().day.at('00:01').do(mainWork)
# while True:
#         schedule.run_pending()
#         time.sleep(1)