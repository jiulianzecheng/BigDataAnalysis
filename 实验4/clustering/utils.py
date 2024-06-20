import math

import numpy as np
from sklearn.preprocessing import StandardScaler


def select_points(train_data):
    """
    数据选择
    :param train_data: 整个训练数据集
    :return:
    """
    x = len(train_data) // 180
    result = np.empty((180, 11))
    # 在数据集最后添加一列表示所属的类
    train_data = np.column_stack((train_data, np.zeros(len(train_data)).reshape(len(train_data), 1)))
    for i in range(60):
        result[i] = train_data[300 + i]
        result[i][10] = 1
    for i in range(60, 120):
        result[i] = train_data[700 + i]
        result[i][10] = 2
    for i in range(120, 180):
        result[i] = train_data[1200 + i]
        result[i][10] = 3
    # for i in range(180):
    #     train_data=np.delete(train_data,i*x,axis=0)
    return result


def scaler(data):
    '''
    数据标准化函数
    x=(x-u)/r,u为平均值，r为方差
    :param data: 标准化前的数据
    :return: 标准化后的数据
    '''
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    return data


def e_distance(x, y):
    """
    计算欧式距离
    :param x:
    :param y:
    :return:
    """
    sum = 0
    for i in range(len(x)):
        sum += (x[i] - y[i]) ** 2
    result = math.sqrt(sum)
    return result


def kmeans(train_data, max_iter):
    # 去除数据中的聚类特征
    cluster1 = train_data[0:60, :-1]
    cluster2 = train_data[60:120, :-1]
    cluster3 = train_data[120:180, :-1]
    feature = train_data[:, :-1]
    # 计算每个类的质心
    centroid1 = np.mean(cluster1, axis=0)
    centroid2 = np.mean(cluster2, axis=0)
    centroid3 = np.mean(cluster3, axis=0)

    for j in range(max_iter):
        # 用三个聚类质心来初始化聚类
        cluster1 = centroid1
        cluster2 = centroid2
        cluster3 = centroid3
        for i in range(len(feature)):
            # 计算欧式距离
            distance1 = e_distance(feature[i], centroid1)
            distance2 = e_distance(feature[i], centroid2)
            distance3 = e_distance(feature[i], centroid3)
            # 将点划分到距离最近的聚类
            min_distance = min(distance1, distance2, distance3)
            # 更新对应的聚类
            if min_distance == distance1:
                cluster1 = np.vstack((cluster1, feature[i]))
                train_data[i][10] = 1
            elif min_distance == distance2:
                cluster2 = np.vstack((cluster2, feature[i]))
                train_data[i][10] = 2
            else:
                cluster3 = np.vstack((cluster3, feature[i]))
                train_data[i][10] = 3
        # 计算更新后聚类的质心
        cluster1 = cluster1[1:]
        cluster2 = cluster2[1:]
        cluster3 = cluster3[1:]
        centroid1 = np.mean(cluster1, axis=0)
        centroid2 = np.mean(cluster2, axis=0)
        centroid3 = np.mean(cluster3, axis=0)
    # 计算sse值
    sse = SSE(cluster1, cluster2, cluster3)
    return train_data, sse


def precise(train_data, result):
    """
    计算准确率
    :param train_data:
    :param result:
    :return:
    """
    num = 0
    for i in range(len(train_data)):
        if train_data[i][10] == result[i][10]:
            num += 1
    return num / 180


def SSE(cluster1, cluster2, cluster3):
    """
    计算sse值
    :param cluster1:
    :param cluster2:
    :param cluster3:
    :return:
    """
    centroid1 = np.mean(cluster1, axis=0)
    centroid2 = np.mean(cluster2, axis=0)
    centroid3 = np.mean(cluster3, axis=0)
    result = 0
    for i in range(len(cluster1)):
        result += e_distance(cluster1[i], centroid1) ** 2
    for i in range(len(cluster2)):
        result += e_distance(cluster2[i], centroid2) ** 2
    for i in range(len(cluster3)):
        result += e_distance(cluster3[i], centroid3) ** 2
    return result
