import pandas as pd


def sse(test_data,similarity_matrix,utility_matrix,k):
    result=0
    for data in test_data:
        result+=(data[2]-calculate_score(data[0],similarity_matrix,utility_matrix,k,data[1]))**2
    return result

def calculate_score(user_id,similarity_matrix,utility_matrix,k,anime_id):
    similarity_vector=similarity_matrix[user_id]
    k_neighbors=similarity_vector.nlargest(k).index
    rating_vector=utility_matrix[anime_id]
    score=(similarity_vector.loc[k_neighbors] * rating_vector.loc[k_neighbors]).sum()
    denominator = similarity_vector.loc[k_neighbors].sum()
    for i in k_neighbors:
        if pd.isna(rating_vector[i]):
            denominator -= similarity_vector[i]
    score/= denominator
    return score