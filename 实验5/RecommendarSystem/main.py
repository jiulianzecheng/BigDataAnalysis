import pandas as pd
import numpy as np

from utils import get_data, get_data_n, get_data_anime
from user_recommend import sse, recommend_n_anime
from content_recommend import sse_content, content_recommend

# 获取训练集中的数据，所有的用户id,所有的动漫id
train_data, user_id, anime_id = get_data('./data/train_set.csv')
# 读取测试集中的数据
test_data = get_data_n('./data/test_set.csv')
# 获取效用矩阵
train_data = pd.DataFrame(train_data, columns=['user_id', 'anime_id', 'rating'])
utility_matrix = train_data.pivot_table(values='rating', index='user_id', columns='anime_id', fill_value=0)
utility_matrix = utility_matrix.replace(0, np.nan)
# 利用pearson相关系数计算相似度矩阵
similarity_matrix = utility_matrix.T.corr('pearson')
# recommended_anime=recommend(465,similarity_matrix,utility_matrix,5,anime_id,10)
# sse=sse(test_data,similarity_matrix,utility_matrix,10)
# print(sse)
# print(recommended_anime)
# print(utility_matrix)
# recommend_animes=recommend_n_anime(629,anime_id,similarity_matrix,utility_matrix,10,10)
# print(recommend_animes)

similarity_matrix = get_data_anime('./data/anime.csv')

sse = sse_content(test_data, similarity_matrix, utility_matrix,anime_id)
recommend_animes_content=content_recommend(629,similarity_matrix,utility_matrix,anime_id,20)
print(sse)
print(recommend_animes_content)
