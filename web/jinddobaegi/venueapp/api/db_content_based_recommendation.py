import pymysql
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

load_dotenv()


class RestaurantRecommender:
    def __init__(self):
        """
        Initialize the class by connecting to the database and loading data.
        """
        self.connection = self.get_connection()
        self.df = self.load_data()

    def get_connection(self):
        """
        Establish connection to the database using environment variables.
        """
        return pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            charset=os.getenv('DB_CHARSET'),
            cursorclass=pymysql.cursors.DictCursor
        )

    def load_data(self):
        """
        Fetch restaurant data from the database and return it as a pandas DataFrame.
        """
        try:
            with self.connection.cursor() as cursor:
                # Fetch data from 'venueapp_venue' table
                sql = "SELECT biz_id, sweetness, spiciness, saltiness, sourness, cleanliness FROM venueapp_venue"
                cursor.execute(sql)
                result = cursor.fetchall()

                # Convert result to DataFrame
                df = pd.DataFrame(result)

                # Handle missing values
                df.fillna(0, inplace=True)

                return df

        except Exception as e:
            print(f"Error occurred: {e}")
            return pd.DataFrame()  # Return empty DataFrame on error

    def pearson_correlation(self, preferences, row):
        """
        Calculate the Pearson correlation between user preferences and restaurant's scores.
        """
        features = ['sweetness', 'spiciness', 'saltiness', 'sourness', 'cleanliness']
        user_scores = np.array([preferences[feature] for feature in features])
        restaurant_scores = np.array([row[feature] for feature in features])

        # Handle cases where standard deviation is zero
        if np.std(user_scores) == 0 or np.std(restaurant_scores) == 0:
            return 0
        return np.corrcoef(user_scores, restaurant_scores)[0, 1]

    def recommend(self, preferences, num_recommendations=5):
        """
        Recommend restaurants based on user preferences using Pearson correlation.
        """
        # Calculate the Pearson correlation between user preferences and each restaurant
        self.df['similarity'] = self.df.apply(lambda row: self.pearson_correlation(preferences, row), axis=1)

        # Sort by similarity score in descending order
        df_sorted = self.df.sort_values(by='similarity', ascending=False)

        # Get top N recommendations
        return df_sorted['biz_id'].head(num_recommendations)

    def close_connection(self):
        """
        Close the database connection when done.
        """
        self.connection.close()


# Example usage:

# # Initialize the recommender system
# recommender = RestaurantRecommender()
#
# # User preferences for restaurant features
# user_preferences = {
#     'sweetness': 2,
#     'spiciness': 3,
#     'saltiness': 5,
#     'sourness': 1,
#     'cleanliness': 4
# }
#
# # Get recommendations based on user preferences
# recommendations = recommender.recommend(user_preferences, num_recommendations=5)
#
# # Output the recommended restaurants
# print(f"식당별 맛 점수 기반 추천 식당: {recommendations.tolist()}")
#
# # Close the connection
# recommender.close_connection()