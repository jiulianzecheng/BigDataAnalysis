import pandas as pd
from collections import defaultdict


def sse(test_data, similarity_matrix, utility_matrix, k):
    result = 0
    for data in test_data:
        # 误差平方和
        result += (data[2] - calculate_score(data[0], similarity_matrix, utility_matrix, k, data[1])) ** 2
    return result


def calculate_score(user_id, similarity_matrix, utility_matrix, k, anime_id):
    """
    计算某项某人对某个动漫的评分
    :param user_id:用户id
    :param similarity_matrix:相似度矩阵
    :param utility_matrix:效用矩阵
    :param k:选取的相似用户的个数
    :param anime_id:动漫id
    :return:计算出的得分
    """
    # 取出该用户对应的相似向量
    similarity_vector = similarity_matrix[user_id]
    # 取出所有用户对该动漫的评分
    rating_vector = utility_matrix[anime_id]

    # for i in range(len(similarity_vector)):
    #     if pd.isna(rating_vector[i]):
    #         similarity_vector[i] = np.nan
    # 选取有效的评分
    valid_ratings_mask = ~pd.isna(rating_vector)
    valid_similarity_vector = similarity_vector[valid_ratings_mask]
    valid_rating_vector = rating_vector[valid_ratings_mask]
    flag = 0
    if len(valid_similarity_vector) < k:
        flag = 1
    k_neighbors = valid_similarity_vector.nlargest(k)
    k_neighbors_index = valid_similarity_vector.nlargest(k).index
    score = (valid_similarity_vector.loc[k_neighbors_index] * valid_rating_vector.loc[k_neighbors_index]).sum()
    denominator = valid_similarity_vector.loc[k_neighbors_index].sum()
    score /= denominator
    return score, flag


def recommend_n_anime(user_id, animes_id, similarity_matrix, utility_matrix, k, n):
    """
    给用户推荐预测评分最高的n个动漫
    :param user_id: 用户id
    :param animes_id: 所有动漫的id
    :param similarity_matrix: 相似度矩阵
    :param utility_matrix: 效用矩阵
    :param k: 选取的相似用户的个数
    :param n:推荐动漫的数量
    :return:
    """
    result = defaultdict(float)
    for anime_id in animes_id:
        score,flag = calculate_score(user_id, similarity_matrix, utility_matrix, k, anime_id)
        if pd.isna(utility_matrix[user_id][anime_id]):
            if flag==0:
                result[anime_id] = score
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:n])
    return result
