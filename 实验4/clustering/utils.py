import math

import numpy as np
from sklearn.preprocessing import StandardScaler


# def select_result(train_data):
#     cluster1=np.empty((60,11))
#     cluster2=np.empty((60,11))
#     cluster3=np.empty((60,11))
#     x=len(train_data)//180
#     for i in range(60):
#         # cluster1=np.append(cluster1,train_data[i*x],axis=0)
#         cluster1[i]=train_data[i*x]
#     for i in range(60,120):
#         # cluster2=np.append(cluster2,train_data[i*x],axis=0)
#         cluster2[i-60] = train_data[i * x]
#     for i in range(120,180):
#         # cluster3=np.append(cluster3,train_data[i*x],axis=0)
#         cluster3[i-120] = train_data[i * x]
#     # for i in range(180):
#     #     train_data=np.delete(train_data,i*x,axis=0)
#     return cluster1,cluster2,cluster3
def select_points(train_data):
    # cluster1=np.empty((60,11))
    # cluster2=np.empty((60,11))
    # cluster3=np.empty((60,11))
    x=len(train_data)//180
    result=np.empty((180,11))
    train_data = np.column_stack((train_data, np.zeros(len(train_data)).reshape(len(train_data), 1)))
    for i in range(60):
        # cluster1=np.append(cluster1,train_data[i*x],axis=0)
        # cluster1[i]=train_data[i]
        # cluster1[i][10]=1
        result[i]=train_data[300+i]
        result[i][10]=1
    for i in range(60,120):
        # cluster2=np.append(cluster2,train_data[i*x],axis=0)
        # cluster2[i-8500] = train_data[i]
        # cluster2[i-8500][10]=2
        result[i]=train_data[700+i]
        result[i][10]=2
    for i in range(120,180):
        # cluster3=np.append(cluster3,train_data[i*x],axis=0)
        # cluster3[i-17000] = train_data[i]
        # cluster3[i-17000][10]=3
        result[i]=train_data[1200+i]
        result[i][10]=3
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
    scaler=StandardScaler()
    data=scaler.fit_transform(data)
    # m,n=np.shape(data)
    # mean=np.mean(data,axis=0)
    # for i in range(m):
    #     for j in range(n):
    #         data[i][j]=(data[i][j]-np.min(data[:,j]))/(np.max(data[:,j])-np.min(data[:,j]))
    return data

def e_distance(x,y):
    sum=0
    for i in range(len(x)):
        sum+=(x[i]-y[i])**2
    result=math.sqrt(sum)
    return result

def kmeans(train_data,max_iter):
    cluster1=train_data[0:60,:-1]
    cluster2=train_data[60:120,:-1]
    cluster3=train_data[120:180,:-1]
    feature=train_data[:,:-1]
    centroid1 = np.mean(cluster1,axis=0)
    centroid2 = np.mean(cluster2,axis=0)
    centroid3 = np.mean(cluster3,axis=0)

    for j in range(max_iter):
        flag=0
        cluster1 = centroid1
        cluster2 = centroid2
        cluster3 = centroid3
        for i in range(len(feature)):
            distance1=e_distance(feature[i],centroid1)
            distance2=e_distance(feature[i],centroid2)
            distance3=e_distance(feature[i],centroid3)
            min_distance=min(distance1,distance2,distance3)
            if min_distance==distance1:
                cluster1=np.vstack((cluster1,feature[i]))
                # cluster1=np.array(cluster1,feature[i])
                train_data[i][10]=1
                # if train_data[i][10]!=1:
                #     flag=1
            elif min_distance==distance2:
                cluster2 = np.vstack((cluster2, feature[i]))
                # cluster2=np.append(cluster2,feature[i])
                train_data[i][10] = 2
                # if train_data[i][10] != 2:
                #     flag=1
            else:
                cluster3 = np.vstack((cluster3, feature[i]))
                # cluster3=np.append(cluster3,feature[i])
                train_data[i][10] = 3
                # if train_data[i][10] != 3:
                #     flag=1
        cluster1 = cluster1[1:]
        cluster2 = cluster2[1:]
        cluster3 = cluster3[1:]
        centroid1 = np.mean(cluster1, axis=0)
        centroid2 = np.mean(cluster2, axis=0)
        centroid3 = np.mean(cluster3, axis=0)
    sse = SSE(cluster1,cluster2,cluster3)
    return train_data,sse

def precise(train_data,result):
    num=0
    for i in range(len(train_data)):
        if train_data[i][10]==result[i][10]:
            num+=1
    return num/180
def SSE(cluster1,cluster2,cluster3):

    centroid1 = np.mean(cluster1, axis=0)
    centroid2 = np.mean(cluster2, axis=0)
    centroid3 = np.mean(cluster3, axis=0)
    result=0
    for i in range(len(cluster1)):
        result+=e_distance(cluster1[i],centroid1)**2
    for i in range(len(cluster2)):
        result+=e_distance(cluster2[i],centroid2)**2
    for i in range(len(cluster3)):
        result += e_distance(cluster3[i], centroid3)**2
    return result