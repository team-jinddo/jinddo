import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RestaurantRecommender:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.load_data()
        self.features = ['spicy_score','sweet_score','salty_score','sour_score','soft_score']
    
    def load_data(self):
        return pd.read_csv(self.file_path)

    def handle_missing_values(self):
        self.df.fillna(0, inplace=True)

    def create_feature_matrix(self):
        return self.df[self.features]

    def compute_cosine_similarity(self):
        return cosine_similarity(self.create_feature_matrix())

    def recommend_based_on_preferences(self, preferences, num_recommendations=5):  
        preference_vector = np.array([preferences[feature] for feature in self.features]).reshape(1, -1)  # Input 맛 취향 점수에 대한 벡터 생성  
        sim_scores = cosine_similarity(preference_vector, self.create_feature_matrix())  # Input 맛 취향 점수와 식당별 맛 점수의 코사인 유사도 측정
        sim_scores = list(enumerate(sim_scores[0]))  # 코사인 유사도를 인덱스와 유사도 쌍으로 리스트 생성
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # 코사인 유사도를 내림차순 정렬
        biz_indices = [i[0] for i in sim_scores[:num_recommendations]]  # 상위 몇 위까지 가져올지에 대한 인덱스 추출
        return self.df.iloc[biz_indices]['biz_id']  # 추출한 인덱스 사용해서 biz_id 반환

    def run(self, user_preferences, num_recommendations=5):
        self.handle_missing_values()
        cosine_sim = self.compute_cosine_similarity()
        recommendation = self.recommend_based_on_preferences(user_preferences, num_recommendations)
        print(f"식당별 맛 점수 기반 추천 식당 목록: {recommendation.tolist()}")

if __name__ == "__main__":
    file_path = './restaurant_taste_scores.csv'
    user_preferences = {
       'spicy_score': 3,
       'sweet_score': 2,
       'salty_score': 5,
       'sour_score': 1,
       'soft_score': 4
    }
    recommender = RestaurantRecommender(file_path)
    recommender.run(user_preferences)