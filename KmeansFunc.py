# -*- coding: UTF-8 -*-
"""
@Project : scientificProject_wky 
@File    : KmeansFunc.py
@IDE     : PyCharm 
@Author  : 爱写屎山的王可奕
@Date    : 2023/3/27 19:46 
@Comment : 这个类用来实现K-means算法和可视化
"""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans


class KmeansFunc:
    def __init__(self):
        self.pd_data_tag_views_exploded = pd.DataFrame(columns=["Tags", "视频观看"])
        self.pd_data_weight = pd.DataFrame(columns=["视频投币", "视频收藏", "评论数", "视频点赞", "视频分享", "权重"])
        self.pd_data_kmeans_data = pd.DataFrame(columns=["Tags", "视频观看", "视频权重"])

    def kmeansDataProcess(self, datastorage):
        """
        将传入函数统一转化为需要的格式，即拆开列表，去重，合并
        :param datastorage: 一个DataStorageClass类的实例
        :return: 返回一个dataframe，它是k-means聚类需要的算法的输入
        """
        self.pd_data_tag_views_exploded = datastorage.pd_data_tag_views
        self.pd_data_weight = datastorage.pd_data_weight
        connect_dataframe = pd.concat([self.pd_data_tag_views_exploded, self.pd_data_weight],
                                      axis=1)  # 将两个dataframe进行连接
        # print(connect_dataframe)
        connect_dataframe['Tags'] = connect_dataframe['Tags'].apply(self.str_to_list)
        narray = connect_dataframe.to_numpy()  # 将dataframe转换为numpy数组
        # print(narray[:, 0].shape)
        narray_tags_list = narray[:, 0]  # Tags list
        narray_views = narray[:, 1]  # 视频观看
        narry_weight = narray[:, 7]  # 权重
        # 提取出三个numpy
        dataframe_reconnect = pd.DataFrame(
            {"Tags": narray_tags_list, "视频观看": narray_views, "视频权重": narry_weight})
        dataframe_reconnect_exploded = dataframe_reconnect.explode('Tags')
        # 至此，列表的tags被拆解完毕
        # DONE: 将拆解的列表去重，每一个文件去重后concat到DataStorageClass里存储方便后续处理
        dataframe_reconnect_exploded_unique = dataframe_reconnect_exploded.groupby('Tags').agg(
            {'视频观看': 'mean', '视频权重': 'mean'}).reset_index()
        # 上面的函数负责去重
        return dataframe_reconnect_exploded_unique  # 返回一个dataframe,它是k-means聚类需要的算法的输入

    @staticmethod
    def str_to_list(str_value):
        # 去除字符串中的空格
        str_value = str_value.replace(' ', '')
        # 解析字符串为列表
        list_value = str_value[1:-1].split(',')
        return list_value

    def kmeansProcess(self, pd_data_kmeans_data, k=3):
        """
        这个函数用来实现k-means算法
        :param pd_data_kmeans_data: 一个dataframe，它是k-means聚类需要的算法的输入
        :param k: 聚类的个数 default = 3
        :return: 返回一个dataframe，它是k-means聚类需要的算法的输出
        """
        # 为了实现聚心的每次的不同，使用的是k-means++算法，种子为当前日期的整数形式
        import datetime
        random_state_time = int(datetime.datetime.now().strftime("%H%M%S"))
        # 获取相关的整数化的当前日期
        df_kmeans = pd_data_kmeans_data
        feature = df_kmeans.iloc[:, 1:3].values  # 视频观看和视频权重为特征值
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=random_state_time)  # 实例化
        kmeans_result = kmeans.fit_predict(feature)  # 训练,返回的是每个样本所属的簇,即聚类结果
        df_kmeans['聚类结果'] = kmeans_result  # 将聚类结果添加到dataframe中
        # 可视化聚类结果
        plt.figure(figsize=(1280/72, 720/72), dpi=72)
        plt.scatter(feature[kmeans_result == 0, 0], feature[kmeans_result == 0, 1], s=15, c='red', label='Cluster 1')
        plt.scatter(feature[kmeans_result == 1, 0], feature[kmeans_result == 1, 1], s=15, c='blue', label='Cluster 2')
        plt.scatter(feature[kmeans_result == 2, 0], feature[kmeans_result == 2, 1], s=15, c='green', label='Cluster 3')
        # 显示质心
        plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=150, c='yellow', label='Centroids')
        # 设置标题和坐标轴标签
        plt.title('tags的热度权重的Kmeans聚类分析', fontproperties='SimHei', fontsize=20)
        plt.xlabel('视频观看', fontproperties='SimHei', fontsize=14)
        plt.ylabel('视频权重', fontproperties='SimHei', fontsize=14)
        plt.ticklabel_format(style='plain', axis='both')
        plt.legend()
        # 保存图片
        plt.savefig('./data/DataVisualization/聚类结果.png')
        # 将df_kmeans中tags聚类的名字改了，改成低级、中级、高级
        df_kmeans['聚类结果'] = df_kmeans['聚类结果'].replace({0: '低级标签', 1: '中级标签', 2: '高级标签'})
        # 保存csv文件
        df_kmeans.to_csv('./data/DataVisualization/聚类结果.csv', index=False)
