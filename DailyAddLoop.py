# -*- coding: UTF-8 -*-
"""
@Project ：scientificProject_wky
@File    ：DailyAddLoop.py
@IDE     ：PyCharm
@Author  ：爱写屎山的王可奕
@Date    ：2023/3/27 18:47
这里的代码意味着方便对文件的格式化提取
"""


class DailyAddLoop:
    def __init__(self):
        self.signal = True
        self.month = 3
        self.day = 20
        self.early = "004500"
        self.late = "124500"
        self.return_time = ""

    def processAdd(self):
        self.day += 1
        if self.day >= 30:
            self.day = 1
            self.month += 1
        if self.signal:
            self.return_time = self.early
            self.signal = False
        else:
            self.return_time = self.late
            self.signal = True
