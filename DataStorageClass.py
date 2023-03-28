# -*- coding: UTF-8 -*-
"""
@Project ：scientificProject_wky
@File    ：DataStorageClass.py
@IDE     ：PyCharm
@Author  ：爱写屎山的王可奕
@Date    ：2023/3/27 18:47
"""
import pandas as pd


class DataStorageClass:
    def __init__(self):
        self.pd_data_tag_views = pd.DataFrame(columns=["Tags", "视频观看"])
        self.pd_data_weight = pd.DataFrame(columns=["视频投币", "视频收藏", "评论数", "视频点赞", "视频分享", "权重"])
        self.pd_data_kmeans_data = pd.DataFrame(columns=["Tags", "视频观看", "视频权重"])

    def kmeansDataDeduplication(self):
        self.pd_data_kmeans_data = self.pd_data_kmeans_data.groupby('Tags').agg(
            {'视频观看': 'mean', '视频权重': 'mean'}).reset_index()
        return self.pd_data_kmeans_data
