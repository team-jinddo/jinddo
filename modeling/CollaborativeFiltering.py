import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeFiltering:
    def __init__(self, scoring_taste_user_based_path, score_by_bizid_path, visit_res_path):
        # 데이터 불러오기 및 초기화
        self.scoring_taste_user_based = pd.read_csv(scoring_taste_user_based_path, index_col=0).fillna(0)
        self.score_by_bizid = pd.read_csv(score_by_bizid_path)
        self.visit_res = pd.read_csv(visit_res_path, index_col=0)
    
    def cos_sim_calculator(self, user_vector):
        """
        입력된 유저의 맛 취향 벡터 기반으로 기존 유저와의 코사인 유사도 계산
        :param user_vector: 신규 유저의 맛 취향 벡터
        :return: 유사도 데이터프레임
        """
        cosine_sim = cosine_similarity(self.scoring_taste_user_based, np.array(user_vector).reshape(1, -1))
        similarity_df = pd.DataFrame(cosine_sim, index=self.scoring_taste_user_based.index, columns=['similarity_with_x'])
        return similarity_df.sort_values(by='similarity_with_x', ascending=False).reset_index()
    
    def get_visit_list(self, similarity_df):
        """
        가장 유사한 유저의 방문 목록 반환
        :param similarity_df: 유사도 데이터프레임
        :return: 방문한 bizId 리스트
        """
        most_similar_user_id = similarity_df.iloc[0]['author_id']
        visit_list = eval(self.visit_res[self.visit_res['author_id'] == most_similar_user_id]['biz_id'].values[0])
        return visit_list
    
    def recommended_bizid(self, visit_list, n):
        """
        상위 n개의 bizId 추출
        :param visit_list: 방문한 bizId 리스트
        :param n: 추출할 bizId 수
        :return: 상위 n개의 bizId 리스트
        """
        sorted_score_bizid = self.score_by_bizid[self.score_by_bizid['biz_id'].isin(visit_list)].sort_values(by='score', ascending=False)
        return sorted_score_bizid.iloc[:n, 0].to_list()


if __name__ == "__main__":
    recommender = CollaborativeFiltering(
        "C:/Users/SesacPython/Desktop/final_project/scoring_taste_user_based_fin.csv",
        "C:/Users/SesacPython/Desktop/final_project/score_by_bizid.csv",
        "C:/Users/SesacPython/Desktop/final_project/visit_res.csv"
    )

    # 유저의 취향 벡터 입력
    user_vector = input("Enter your taste vector: ")
    user_vector = eval(user_vector)  

    # 유사도 계산 및 추천
    similarity_df = recommender.cos_sim_calculator(user_vector)
    visit_list = recommender.get_visit_list(similarity_df)
    recommended_ids = recommender.recommended_bizid(visit_list, n=5)