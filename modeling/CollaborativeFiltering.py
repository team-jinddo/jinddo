import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ast

class CollaborativeFiltering:

    def __init__(self, scoring_taste_user_based_path, score_by_bizid_path, visit_res_path, review_data_fin_polarity_path, type_freq_by_user_path):
        # 데이터 불러오기 및 초기화
        self.scoring_taste_user_based = pd.read_csv(scoring_taste_user_based_path, index_col=0).fillna(0)
        self.score_by_bizid = pd.read_csv(score_by_bizid_path)
        self.visit_res = pd.read_csv(visit_res_path, index_col=0)
        self.review_data_fin_polarity = pd.read_csv(review_data_fin_polarity_path)
        self.type_freq_by_user = pd.read_csv(type_freq_by_user_path, index_col=0)

    def cos_sim_calculator(self, user_taste_vector):
        """유저의 맛 취향 벡터 기반 기존 유저와의 코사인 유사도 계산"""
        cosine_sim = cosine_similarity(self.scoring_taste_user_based, np.array(user_taste_vector).reshape(1, -1))
        taste_similarity_df = pd.DataFrame(cosine_sim, index=self.scoring_taste_user_based.index, columns=['similarity_with_x'])
        return taste_similarity_df.sort_values(by='similarity_with_x', ascending=False).reset_index()

    def calculate_pearson_sim_by_taste(self, user_taste_vector):
        """입력된 유저의 맛 취향 벡터 기반으로 기존 유저와의 피어슨 유사도 계산"""
        user_matrix = self.scoring_taste_user_based.to_numpy()
        user_taste_vector = np.array(user_taste_vector)

        # 평균 계산 및 중앙 배치
        user_matrix_mean = user_matrix.mean(axis=1).reshape(-1, 1)
        user_vector_mean = user_taste_vector.mean()
        user_matrix_centered = user_matrix - user_matrix_mean
        user_vector_centered = user_taste_vector - user_vector_mean

        # 분자 및 분모 계산
        numerator = np.dot(user_matrix_centered, user_vector_centered)
        denominator = np.linalg.norm(user_matrix_centered, axis=1) * np.linalg.norm(user_vector_centered)

        # Pearson 유사도 계산
        pearson_corr = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0)

        # 결과 DataFrame 생성
        taste_similarity_df = pd.DataFrame(pearson_corr, index=self.scoring_taste_user_based.index, columns=['similarity_with_x'])

        return taste_similarity_df.sort_values(by='similarity_with_x', ascending=False).reset_index()

    def calculate_pearson_sim_by_type(self, user_type_vector):
        """입력된 유저의 타입 취향 벡터 기반으로 기존 유저와의 피어슨 유사도 계산"""
        matrix = self.type_freq_by_user.to_numpy()
        single_row = np.array(user_type_vector)

        matrix_centered = matrix - matrix.mean(axis=1, keepdims=True)
        single_row_centered = single_row - np.mean(single_row)

        numerator = np.dot(matrix_centered, single_row_centered)
        matrix_norms = np.linalg.norm(matrix_centered, axis=1)
        single_row_norm = np.linalg.norm(single_row_centered)

        denominator = matrix_norms * single_row_norm
        denominator[denominator == 0] = 1

        pearson_similarity = numerator / denominator

        taste_similarity_df = pd.Series(pearson_similarity, index=self.type_freq_by_user.index)
        taste_similarity_df = taste_similarity_df.reset_index().rename(columns={'index': 'author_id', 0: 'similarity_with_x'}).sort_values(by='similarity_with_x', ascending=False)

        return taste_similarity_df

    def get_visit_list_by_type(self, taste_similarity_df):
        """(타입 취향 기준) 방문한 biz ID 중 상위 추천"""
        visit_list = []
        for author_id in taste_similarity_df['author_id']:
            biz_ids = self.review_data_fin_polarity[self.review_data_fin_polarity['author_id'] == author_id]['biz_id']
            visit_list.extend(biz_ids.tolist())
            if len(set(visit_list)) >= 5:
                return list(set(visit_list))[:5]  # 5개만 반환
        # return set(visit_list[:5])

    def get_visit_list_by_taste(self, taste_similarity_df):
        """(맛 취향 기준) 가장 유사한 유저의 방문 목록 반환"""
        similar_user_ids = taste_similarity_df['author_id']
        visit_list = []
        for author_id in similar_user_ids:
            # try:
            visit_list.extend(ast.literal_eval(self.visit_res[self.visit_res['author_id'] == author_id]['biz_id'].values[0]))
            # except (IndexError, ValueError):
            #     continue
            if len(set(visit_list)) >= 5:
                return list(set(visit_list))[:5]
        return list(set(visit_list))[:5]

    def recommended_bizid(self, visit_list):
        """(맛 취향 기준) 방문한 biz ID 중 상위 추천"""
        sorted_score_bizid = self.score_by_bizid[self.score_by_bizid['biz_id'].isin(visit_list)].sort_values(by='score', ascending=False)
        return sorted_score_bizid['biz_id'].tolist()


if __name__ == "__main__":
    recommender = CollaborativeFiltering(
    "C:/Users/SesacPython/Desktop/final_project/scoring_taste_user_based.csv",
    "C:/Users/SesacPython/Desktop/final_project/score_by_bizid.csv",
    "C:/Users/SesacPython/Desktop/final_project/visit_res.csv",
    "C:/Users/SesacPython/Desktop/final_project/review_data_fin_polarity.csv",
    "C:/Users/SesacPython/Desktop/final_project/type_freq_by_user.csv"
    )

    # 유저의 맛 취향 벡터 입력
    user_taste_vector = [1, 2, 3, 4, 5]

    # 유사도 계산 및 추천
    taste_similarity_df_by_taste = recommender.calculate_pearson_sim_by_taste(user_taste_vector)  # 피어슨 유사도
    visit_list_by_taste = recommender.get_visit_list_by_taste(taste_similarity_df_by_taste)
    recommended_ids_by_taste = recommender.recommended_bizid(visit_list_by_taste)

    # 유저 타입 취향 벡터 입력
    user_type_vector = [-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]

    taste_similarity_df_by_type = recommender.calculate_pearson_sim_by_type(user_type_vector)
    visit_list_by_type = recommender.get_visit_list_by_type(taste_similarity_df_by_type)
    recommended_ids_by_type = recommender.recommended_bizid(visit_list_by_type)
