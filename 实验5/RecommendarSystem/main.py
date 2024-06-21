import pandas as pd
import numpy as np

from utils import get_data, recommend, get_data_n,get_data_anime
from user_recommend import sse,calculate_score

train_data,user_id,anime_id=get_data('./data/train_set.csv')
test_data=get_data_n('./data/test_set.csv')
train_data = pd.DataFrame(train_data, columns=['user_id', 'anime_id', 'rating'])
utility_matrix = train_data.pivot_table(values='rating', index='user_id', columns='anime_id', fill_value=0)
utility_matrix = utility_matrix.replace(0, np.nan)
similarity_matrix=utility_matrix.T.corr('pearson')
#recommended_anime=recommend(465,similarity_matrix,utility_matrix,5,anime_id,10)
sse=sse(test_data,similarity_matrix,utility_matrix,5)
print(sse)
#print(recommended_anime)
#print(utility_matrix)
anime_data=get_data_anime('./data/anime.csv')