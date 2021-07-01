# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2021/1/3 6:51 下午
@Describe
"""
from flask import Flask,render_template
from chart import make_chart
from spider import get_now_country_data


if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello world!'

    @app.route('/now')
    def Now():
        make_chart(data=get_now_country_data())
        return render_template('map.html')

    @app.route('/process')
    def Process():
        return render_template('map.html')

    @app.route('/async')
    def Async():
        return render_template('map.html')


    app.run(port=3006)



