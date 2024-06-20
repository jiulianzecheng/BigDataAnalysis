import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from utils import select_points, scaler, kmeans,precise

data=pd.read_csv('./anime.csv',usecols=['Popularity','Score-10','Score-9','Score-8','Score-7','Score-6','Score-5','Score-4','Score-3','Score-2'])
# data['Popularity'] = data['Popularity'].astype(int)
data = data.apply(pd.to_numeric, errors='coerce')
data = data.dropna()
data=data.to_numpy()
train_data=data[np.argsort(-data[:,0])]

train_data_n=select_points(train_data)
train_data=scaler(train_data_n)

result,sse=kmeans(train_data,1000)
# cluster1_n,cluster2_n,cluster3_n=select_result(result)
precise_r=precise(train_data_n,result)
print(precise_r)
print(sse)

x = result[:,9]
y = result[:,1]

plt.figure()

labels=set(result[:,10])
# 使用不同的颜色对每个聚类进行绘制
for i in labels:
    plt.scatter(x[result[:,10] == i], y[result[:,10] == i], label=f'Cluster {i}')

# 添加图例
plt.legend()

# 添加x轴和y轴的标签
plt.xlabel('Score 10')
plt.ylabel('Score 2')

# 显示图形
plt.show()