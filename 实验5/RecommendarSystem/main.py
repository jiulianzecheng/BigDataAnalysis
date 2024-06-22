import pandas as pd
import numpy as np

from utils import get_data, get_data_n, get_data_anime
from user_recommend import sse_user, recommend_n_anime
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

# 基于用户的协同过滤
sse=sse_user(test_data,similarity_matrix,utility_matrix,10)
recommend_animes=recommend_n_anime(629,anime_id,similarity_matrix,utility_matrix,10,20)
print("基于用户的协同过滤：")
print("sse："+str(sse))
print("推荐的动漫："+str(recommend_animes))

# 获取余弦相似度矩阵
similarity_matrix = get_data_anime('./data/anime.csv')
# 基于内容的协同过滤
sse = sse_content(test_data, similarity_matrix, utility_matrix,anime_id)
recommend_animes_content=content_recommend(629,similarity_matrix,utility_matrix,anime_id,20)
print("基于内容的协同过滤：")
print("sse："+str(sse))
print("推荐的动漫："+str(recommend_animes_content))

