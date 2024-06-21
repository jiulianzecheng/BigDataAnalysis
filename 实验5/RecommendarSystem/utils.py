import pandas as pd
import numpy as np
from collections import defaultdict
def get_data(file_path):
    data=pd.read_csv(file_path)
    data = data.to_numpy()
    user_id = np.unique(data[:, 0])
    anime_id = np.unique(data[:, 1])
    return data,user_id,anime_id
def get_data_n(file_path):
    data=pd.read_csv(file_path)
    data = data.to_numpy()
    user_id = np.unique(data[:, 0])
    anime_id = np.unique(data[:, 1])
    return data
def get_data_anime(file_path):
    df = pd.read_csv(file_path)

    df = df[['Anime_id', 'Genres']]

    df['Genres'] = df['Genres'].str.split(', ')
    df = df.explode('Genres')
    df = pd.get_dummies(df, columns=['Genres'])

    feature_matrix = df.values
    return feature_matrix

def recommend(user_id,similarity_matrix,utility_matrix,k,anime_id,n):
    similarity_vector=similarity_matrix[user_id].fillna(np.NINF)
    sorted_indices = similarity_vector.argsort()[::-1]
    score=defaultdict(float)
    for id in anime_id:
        if pd.isna(utility_matrix.loc[user_id, id]):
            rating_vector=utility_matrix[id]
            k_neighbors=[]
            i=0
            for j in sorted_indices:
                if not pd.isna(rating_vector[j]):
                    k_neighbors.append(j)
                    i+=1
                if i>=k:
                    break
            sum_similarity=0
            for k in k_neighbors:
                score[id]+=similarity_vector[k]*rating_vector[k]
                sum_similarity+=similarity_vector[k]
            score[id]/=sum_similarity

    recommended_anime = sorted(score.items(), key=lambda x: x[1], reverse=True)[:n]
    return recommended_anime
