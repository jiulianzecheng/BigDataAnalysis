import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_data(file_path):
    data=pd.read_csv(file_path)
    data = data.to_numpy()
    user_id = np.unique(data[:, 0])
    anime_id = np.unique(data[:, 1])
    return data,user_id,anime_id
def get_data_n(file_path):
    data = pd.read_csv(file_path)
    data = data.to_numpy()
    return data
def get_data_anime(file_path):
    df = pd.read_csv(file_path, usecols=['Anime_id', 'Genres'])

    # 步骤3: 计算TF-IDF矩阵
    vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split(', '))
    tfidf_matrix = vectorizer.fit_transform(df['Genres'])
    # 计算余弦相似度矩阵
    similarity_matrix = cosine_similarity(tfidf_matrix,tfidf_matrix)
    cosine_sim_df = pd.DataFrame(similarity_matrix, index=df['Anime_id'], columns=df['Anime_id'])
    return cosine_sim_df


