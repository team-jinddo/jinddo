import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load data
def load_data(file_path):
    return pd.read_csv(file_path)

# Handle missing values
def handle_missing_values(df):
    df.fillna(0, inplace=True)
    return df

# Create a feature matrix
def create_feature_matrix(df):
    features = ['spicy_score','sweet_score','salty_score','sour_score','soft_score']
    return df[features]

# Compute cosine similarity
def compute_cosine_similarity(feature_matrix):
    return cosine_similarity(feature_matrix)

# Recommend based on preferences
def recommend_based_on_preferences(preferences, feature_matrix, cosine_sim, num_recommendations=5):
    # Input 맛 취향 점수에 대한 벡터 생성
    preference_vector = np.array([preferences[feature] for feature in feature_matrix.columns]).reshape(1, -1)

    # Input 맛 취향 점수와 식당별 맛 점수의 코사인 유사도 측정
    sim_scores = cosine_similarity(preference_vector, feature_matrix)

    # 코사인 유사도를 인덱스와 유사도 쌍으로 리스트 생성
    sim_scores = list(enumerate(sim_scores[0]))

    # 코사인 유사도를 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 상위 몇 위까지 가져올지에 대한 인덱스 추출
    biz_indices = [i[0] for i in sim_scores[:num_recommendations]]

    # 추출한 인덱스 사용해서 biz_id 반환
    return biz_indices

# Get recommended biz_ids
def get_recommended_biz_ids(preferences, feature_matrix, cosine_sim, df, num_recommendations=5):
    biz_indices = recommend_based_on_preferences(preferences, feature_matrix, cosine_sim, num_recommendations)
    return df.iloc[biz_indices]['biz_id']

# Main function
def main():
    file_path = './restaurant_taste_scores.csv'
    df = load_data(file_path)
    df = handle_missing_values(df)
    feature_matrix = create_feature_matrix(df)
    cosine_sim = compute_cosine_similarity(feature_matrix)

    user_preferences = {
       'spicy_score': 3,
       'sweet_score': 2,
       'salty_score': 1,
       'sour_score': 1,
       'soft_score': 4
    }

    recommended_biz_ids = get_recommended_biz_ids(user_preferences, feature_matrix, cosine_sim)
    print(f"식당별 맛 점수 기반 추천 식당 목록: {recommended_biz_ids.tolist()}")

if __name__ == "__main__":
    main()