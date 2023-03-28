# -*- coding: UTF-8 -*-
"""
@Project ：scientificProject_wky
@File    ：DataProcessMain.py
@IDE     ：PyCharm
@Author  ：爱写屎山的王可奕
@Date    ：2023/3/27 18:45
@Comment ：命名规范:
1.类名：首字母大写，驼峰命名法 例如：DataStorageClass
2.函数名：首字母小写，驼峰命名法 例如：kmeansDataProcess
3.变量名：首字母小写，下划线命名法 例如：pd_data_csv
"""
# import numpy as np
import pandas as pd
from DataStorageClass import DataStorageClass
from KmeansFunc import KmeansFunc
from DailyAddLoop import DailyAddLoop

if __name__ == "__main__":
    datastorage = DataStorageClass()
    loopfunc = DailyAddLoop()
    kmeansfunc = KmeansFunc()

    while True:
        # 这块循环负责数据的提取和存储
        # 数据读取
        loopfunc.processAdd()
        data_name = f"20230{loopfunc.month}{loopfunc.day}-{loopfunc.return_time}.csv"
        try:
            pd_data_csv = pd.read_csv(f'./data/datalist/{data_name}', header=0, encoding='utf-8',
                                      engine='python', dtype={'Tags': list})
        except FileNotFoundError:
            print("Find All!")
            break
        pd_data_csv = pd_data_csv.drop_duplicates()  # 去重
        # 完成数据读取,进行数据提取
        # 1.提取出所有的视频Tag对其进行统计,将其统计到储存类的实例属性中
        # 使用遍历将其中的TAG以及其视频播放量和其他权重，TAG为点，其他权重为横轴，纵轴为视频播放量，预期进行K-means聚类，得到三种分类的
        # TAG质量，将其用列表的方式给DataStorageClass类的实例属性，利用遍历CSV将其权重计算出，并单独存储为一个dataframe，以aid为唯一索引
        # 权重: 硬币x0.4+收藏x0.3+评论x0.4+播放x0.25+点赞x0.4+分享x0.6
        # 计算权重
        weight = [0.4, 0.3, 0.4, 0.4, 0.6]
        pd_data_weight_temp = pd_data_csv[
            ["视频投币", "视频收藏", "评论数", "视频点赞", "视频分享"]]  # 选择相关权重变量
        pd_data_weight = pd_data_weight_temp.mul(weight, axis=1)  # 乘以权重
        pd_data_weight["权重"] = pd_data_weight.sum(axis=1)  # 求和
        # 至此，权重计算完毕
        pd_data_tag_views = pd_data_csv[["Tags", "视频观看"]]  # 将Tags和视频观看提取出来
        # 至此，将k-means算法需要的全部数据提取完毕
        datastorage.pd_data_tag_views = pd.concat([datastorage.pd_data_tag_views, pd_data_tag_views])
        datastorage.pd_data_weight = pd.concat([datastorage.pd_data_weight, pd_data_weight])
        # 开始为K-means做数据规整
        temp_pd_data_kmeans_data = kmeansfunc.kmeansDataProcess(datastorage)
        datastorage.pd_data_kmeans_data = pd.concat([datastorage.pd_data_kmeans_data, temp_pd_data_kmeans_data])  #
        # 将其全部存储到储存类的实例属性中,此时整体需要第二次去重
    # 第二次去重
    datastorage.pd_data_kmeans_data = datastorage.kmeansDataDeduplication()
    # print(datastorage.pd_data_kmeans_data)
    # 至此，数据处理完毕，开始进行K-means聚类
    kmeansfunc.kmeansProcess(datastorage.pd_data_kmeans_data, 3)

