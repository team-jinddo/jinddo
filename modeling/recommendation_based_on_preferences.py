import pandas as pd
import numpy as np

class RestaurantRecommender:
    def __init__(self, file_path, features):
        self.file_path = file_path
        self.features = features
        self.df = pd.read_csv(file_path)
        self.df.fillna(0, inplace=True)  # Handle missing values
    
    def pearson_correlation(self, preferences, row):
        user_scores = np.array([preferences[feature] for feature in self.features])
        restaurant_scores = np.array([row[feature] for feature in self.features])
        # Return Pearson correlation, handle cases where standard deviation is zero
        if np.std(user_scores) == 0 or np.std(restaurant_scores) == 0:
            return 0
        return np.corrcoef(user_scores, restaurant_scores)[0, 1]
    
    def recommend(self, preferences, num_recommendations=5):
        # Calculate similarity for each restaurant
        self.df['similarity'] = self.df.apply(lambda row: self.pearson_correlation(preferences, row), axis=1)
        
        # Sort by similarity score in descending order and return top recommendations
        df_sorted = self.df.sort_values(by='similarity', ascending=False)
        
        return df_sorted['biz_id'].head(num_recommendations)

# Example usage:

# Define features
features = ['spicy_score', 'sweet_score', 'salty_score', 'sour_score', 'soft_score']

# Initialize the recommender system with the dataset path and features
recommender = RestaurantRecommender('./restaurant_taste_scores.csv', features)

# Input: User preferences
user_preferences = {
   'spicy_score': 3,
   'sweet_score': 2,
   'salty_score': 5,
   'sour_score': 1,
   'soft_score': 4
}

# Get recommendations
recommendations = recommender.recommend(user_preferences, num_recommendations=5)

# OUTPUT
print(f"식당별 맛 점수 기반 추천 식당: {recommendations.tolist()}")
