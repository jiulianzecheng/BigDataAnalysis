
import pandas as pd
import numpy as np
from collections import defaultdict


def calculate_score_content(user_id,similarity_matrix,utility_matrix,anime_id):
    """
    基于内容对动漫打分
    :param user_id: 用户id
    :param similarity_matrix: 余弦相似度矩阵
    :param utility_matrix: 效用矩阵
    :param anime_id: 动漫id
    :return:
    """
    # 取出user_id和anime_id对应的效用向量和相似度向量
    rating_vector=utility_matrix.loc[user_id]
    similarity_vector=similarity_matrix[anime_id]
    # 获取该用户已打分的动漫的id
    valid_rating_mask=~pd.isna(rating_vector)
    # 计算打分
    score = 0
    denominator = 0
    num = 0
    flag = 0
    for index,value in valid_rating_mask.items():
        if value:
            score += rating_vector[index]*similarity_vector[index]
            denominator += similarity_vector[index]
            if similarity_vector[index] != 0:
                num += 1
    score /= denominator
    # 判断有效的相似动漫的数量，便于对动漫进行推荐，相似动漫过少的动漫则不进行推荐
    if num >= 5:
        flag = 1
    return score, flag

def content_recommend(user_id,similarity_matrix,utility_matrix,animes_id,n):
    """
    基于内容对用户进行推荐
    :param user_id: 用户id
    :param similarity_matrix: 余弦相似度矩阵
    :param utility_matrix: 效用矩阵
    :param animes_id: 所有动漫id的集合
    :param n: 推荐动漫的数量
    :return:
    """
    result = defaultdict(float)
    # 遍历所有动漫计算得分
    for anime_id in animes_id:
        score,flag = calculate_score_content(user_id, similarity_matrix, utility_matrix, anime_id)
        # flag == 0表示该动漫的相似动漫过少，不予推荐
        if pd.isna(utility_matrix[anime_id][user_id]) and flag:
            result[anime_id] = score
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:n])
    return result


def sse_content(test_data, similarity_matrix, utility_matrix,animes_id):
    # 计算误差平方和
    result = 0
    for data in test_data:
        # 误差平方和
        score,flag= calculate_score_content(data[0], similarity_matrix, utility_matrix, data[1])
        result += (data[2] - score) ** 2
    return result