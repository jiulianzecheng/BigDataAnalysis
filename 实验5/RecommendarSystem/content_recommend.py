
import pandas as pd
import numpy as np
from collections import defaultdict


def calculate_score_content(user_id,similarity_matrix,utility_matrix,anime_id,animes_id):
    rating_vector=utility_matrix.loc[user_id]
    # anime_id = np.where(animes_id == anime_id)[0]
    similarity_vector=similarity_matrix[anime_id]
    # similarity_vector = similarity_vector.reshape(-1, 1)
    valid_rating_mask=~pd.isna(rating_vector)
    # valid_similarity_vector = similarity_vector[valid_rating_mask]
    # valid_rating_vector = rating_vector[valid_rating_mask]
    # score = (valid_similarity_vector * valid_rating_vector).sum()
    # denominator = valid_similarity_vector.sum()
    # score=score/denominator
    score = 0
    denominator = 0
    # indices = np.where(valid_rating_mask)[0]
    num = 0
    flag = 0
    for index,value in valid_rating_mask.items():
        if value:
            score += rating_vector[index]*similarity_vector[index]
            denominator += similarity_vector[index]
            if similarity_vector[index] != 0:
                num += 1
    score /= denominator
    if num >= 10:
        flag = 1
    return score, flag

def content_recommend(user_id,similarity_matrix,utility_matrix,animes_id,n):
    result = defaultdict(float)
    for anime_id in animes_id:
        score,flag = calculate_score_content(user_id, similarity_matrix, utility_matrix, anime_id, animes_id)
        if pd.isna(utility_matrix[anime_id][user_id]) and flag:
            result[anime_id] = score
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:n])
    return result


def sse_content(test_data, similarity_matrix, utility_matrix,animes_id):
    result = 0
    for data in test_data:
        # 误差平方和
        result += (data[2] - calculate_score_content(data[0], similarity_matrix, utility_matrix, data[1],animes_id)) ** 2
    return result